"""`neuronforge` CLI — run the pipeline locally, schedule it, or serve the API."""
from __future__ import annotations

import asyncio
import json
import logging

import typer
from rich.console import Console
from rich.table import Table

from .config import find_channel, load_channels
from .orchestrator import run_channel
from .settings import get_settings

console = Console()
app = typer.Typer(help="NeuronForge AI automation CLI", no_args_is_help=True)


def _setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


@app.command()
def channels(verbose: bool = typer.Option(False, "--verbose", "-v")) -> None:
    """List configured channels."""
    _setup_logging(verbose)
    s = get_settings()
    table = Table("ID", "Lang", "Niche", "Platform", "Cron")
    for c in load_channels(s.channels_dir):
        table.add_row(c.id, c.language, c.niche, c.platform, c.cron)
    console.print(table)


@app.command("run")
def run_cmd(
    channel_id: str = typer.Argument(..., help="Channel ID (see `neuronforge channels`)"),
    dry_run: bool = typer.Option(True, "--dry-run/--upload", help="Skip the upload step"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Run the full pipeline once for a single channel."""
    _setup_logging(verbose)
    s = get_settings()
    ch = find_channel(s.channels_dir, channel_id)
    if ch is None:
        console.print(f"[red]Channel {channel_id!r} not found[/red]")
        raise typer.Exit(code=1)
    result = asyncio.run(run_channel(ch, dry_run=dry_run))
    console.print_json(json.dumps({
        "run_id": result.run_id,
        "channel_id": result.channel_id,
        "status": result.status,
        "topic": result.topic,
        "video_path": result.video_path,
        "video_url": result.video_url,
        "error": result.error,
    }, ensure_ascii=False))


@app.command()
def schedule(verbose: bool = typer.Option(False, "--verbose", "-v")) -> None:
    """Run the scheduler until Ctrl+C (cron-driven per-channel runs)."""
    from .scheduler import serve_forever

    _setup_logging(verbose)
    asyncio.run(serve_forever())


@app.command()
def api(verbose: bool = typer.Option(False, "--verbose", "-v")) -> None:
    """Serve the FastAPI dashboard backend."""
    from .api import run as run_api

    _setup_logging(verbose)
    run_api()


@app.command("youtube-auth")
def youtube_auth(channel_id: str) -> None:
    """Complete the one-time YouTube OAuth flow for a channel."""
    from .uploader.youtube import run_auth_flow

    path = run_auth_flow(channel_id)
    console.print(f"[green]Saved refresh token to {path}[/green]")


if __name__ == "__main__":  # pragma: no cover
    app()
