"""End-to-end pipeline: trend -> script -> tts -> media -> video -> (upload)."""
from __future__ import annotations

import json
import logging
import random
from dataclasses import asdict, dataclass
from datetime import UTC, datetime

from .config import ChannelConfig
from .db import DB
from .llm import get_llm
from .media import fetch_background_images
from .script import ScriptPlan, generate_script
from .settings import get_settings
from .trends import discover_trends
from .tts import synthesize

log = logging.getLogger(__name__)


@dataclass
class RunResult:
    run_id: int
    channel_id: str
    status: str
    topic: str | None = None
    script: dict | None = None
    video_path: str | None = None
    video_url: str | None = None
    error: str | None = None


def _pick_topic(trends: list, channel_id: str, db: DB) -> str | None:
    random.shuffle(trends)
    trends.sort(key=lambda t: getattr(t, "score", 0.0), reverse=True)
    for t in trends:
        if not db.is_topic_used(channel_id, t.title):
            return t.title
    return trends[0].title if trends else None


async def run_channel(channel: ChannelConfig, *, dry_run: bool = False) -> RunResult:
    s = get_settings()
    db = DB(s.db_path)
    run_id = db.start_run(channel.id)
    result = RunResult(run_id=run_id, channel_id=channel.id, status="running")
    work_dir = s.data_dir / "runs" / f"{channel.id}_{run_id}"
    work_dir.mkdir(parents=True, exist_ok=True)

    try:
        log.info("[%s] Discovering trends…", channel.id)
        trends = await discover_trends(channel)
        if not trends:
            log.info("[%s] No trends found; using channel niche as fallback topic.", channel.id)
            topic = f"Latest in {channel.niche}"
        else:
            topic = _pick_topic(trends, channel.id, db) or trends[0].title
        result.topic = topic
        log.info("[%s] Topic: %s", channel.id, topic)

        log.info("[%s] Generating script…", channel.id)
        llm = get_llm()
        plan: ScriptPlan = await generate_script(llm, channel, topic)
        result.script = plan.to_dict()
        (work_dir / "script.json").write_text(
            json.dumps(plan.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )

        log.info("[%s] Synthesizing narration…", channel.id)
        audio_path = work_dir / "narration.mp3"
        await synthesize(plan.full_narration, channel.default_tts_voice, audio_path)

        log.info("[%s] Fetching background images…", channel.id)
        images = await fetch_background_images(
            query=channel.niche,
            count=max(4, len(plan.captions) // 2 or 4),
            out_dir=work_dir / "images",
            resolution=channel.resolution,
        )
        if not images:
            raise RuntimeError("Could not produce any background images (no ffmpeg?).")

        log.info("[%s] Assembling video…", channel.id)
        from .video import assemble_video

        video_path = work_dir / "video.mp4"
        await assemble_video(
            audio_path=audio_path,
            image_paths=[img.path for img in images],
            captions=plan.captions,
            out_path=video_path,
            resolution=channel.resolution,
            fps=channel.fps,
        )
        result.video_path = str(video_path)

        if dry_run:
            result.status = "dry_run_ok"
            db.finish_run(
                run_id,
                "dry_run_ok",
                video_path=str(video_path),
                meta={"script": plan.to_dict(), "topic": topic},
            )
            db.mark_topic_used(channel.id, topic)
            log.info("[%s] Dry run complete: %s", channel.id, video_path)
            return result

        log.info("[%s] Uploading to YouTube…", channel.id)
        from .uploader import YouTubeUploader

        uploader = YouTubeUploader(channel.id)
        upload_info = await uploader.upload(
            video_path,
            title=plan.title,
            description=f"{plan.description}\n\n" + " ".join(plan.hashtags),
            tags=[h.lstrip("#") for h in plan.hashtags],
            category_id=channel.youtube_category_id,
            privacy=channel.youtube_privacy,
        )
        result.video_url = upload_info.get("url")
        result.status = "uploaded"
        db.finish_run(
            run_id,
            "uploaded",
            video_path=str(video_path),
            video_url=result.video_url,
            meta={
                "script": plan.to_dict(),
                "topic": topic,
                "upload": {k: v for k, v in upload_info.items() if k != "raw"},
                "finished_at": datetime.now(UTC).isoformat(),
            },
        )
        db.mark_topic_used(channel.id, topic)
        log.info("[%s] Uploaded: %s", channel.id, result.video_url)
        return result

    except Exception as e:
        log.exception("[%s] Pipeline failed", channel.id)
        result.status = "error"
        result.error = f"{type(e).__name__}: {e}"
        db.finish_run(run_id, "error", error=result.error, meta=asdict(result))
        return result
