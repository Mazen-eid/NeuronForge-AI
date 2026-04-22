"""FastAPI backend used by the `frontend/` dashboard."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import __version__
from .config import find_channel, load_channels
from .db import DB
from .llm import get_llm
from .orchestrator import run_channel
from .settings import get_settings

log = logging.getLogger(__name__)


app = FastAPI(title="NeuronForge AI", version=__version__)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, Any]:
    return {"ok": True, "version": __version__}


@app.get("/channels")
def list_channels() -> dict[str, Any]:
    s = get_settings()
    channels = [
        {
            "id": c.id,
            "language": c.language,
            "niche": c.niche,
            "platform": c.platform,
            "cron": c.cron,
        }
        for c in load_channels(s.channels_dir)
    ]
    return {"channels": channels}


@app.get("/runs")
def recent_runs(limit: int = 20) -> dict[str, Any]:
    s = get_settings()
    db = DB(s.db_path)
    return {"runs": db.recent_runs(limit=limit)}


class RunRequest(BaseModel):
    dry_run: bool = True


@app.post("/channels/{channel_id}/run")
async def trigger_run(
    channel_id: str, payload: RunRequest, background_tasks: BackgroundTasks
) -> dict[str, Any]:
    s = get_settings()
    ch = find_channel(s.channels_dir, channel_id)
    if ch is None:
        raise HTTPException(404, f"Channel {channel_id} not found")
    # Fire and forget - the frontend polls /runs for status.
    background_tasks.add_task(_run_bg, ch, payload.dry_run)
    return {"queued": True, "channel_id": channel_id, "dry_run": payload.dry_run}


async def _run_bg(ch, dry_run: bool) -> None:
    try:
        await run_channel(ch, dry_run=dry_run)
    except Exception:  # noqa: BLE001
        log.exception("Background run failed")


class AssistantRequest(BaseModel):
    prompt: str
    language: str = "en"


@app.post("/assistant/ideas")
async def assistant_ideas(req: AssistantRequest) -> dict[str, Any]:
    llm = get_llm()
    system = (
        "You are a concise content-strategy assistant. "
        "When the user asks for video ideas, respond with a numbered list only. "
        f"Respond in language code: {req.language}."
    )
    text = await llm.complete(system=system, user=req.prompt, temperature=0.9, max_tokens=700)
    ideas = _split_numbered(text)
    return {"ideas": ideas, "raw": text}


def _split_numbered(text: str) -> list[str]:
    out: list[str] = []
    for line in text.splitlines():
        s = line.strip().lstrip("-*").lstrip()
        if not s:
            continue
        # Drop a leading "1.", "2)", etc.
        i = 0
        while i < len(s) and s[i].isdigit():
            i += 1
        if i > 0 and i < len(s) and s[i] in ".)":
            s = s[i + 1 :].strip()
        out.append(s)
    return out


def run() -> None:
    import uvicorn

    s = get_settings()
    uvicorn.run("neuronforge.api:app", host=s.api_host, port=s.api_port, reload=False)


if __name__ == "__main__":  # pragma: no cover
    asyncio.run(run())  # type: ignore[func-returns-value]
