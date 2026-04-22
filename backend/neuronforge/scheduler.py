"""APScheduler-based cron runner that dispatches to the orchestrator."""
from __future__ import annotations

import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from .config import load_channels
from .orchestrator import run_channel
from .settings import get_settings

log = logging.getLogger(__name__)


async def _run_and_log(channel_id: str) -> None:
    from .config import find_channel

    s = get_settings()
    ch = find_channel(s.channels_dir, channel_id)
    if ch is None:
        log.error("Scheduled channel %r not found", channel_id)
        return
    await run_channel(ch, dry_run=False)


def build_scheduler() -> AsyncIOScheduler:
    s = get_settings()
    scheduler = AsyncIOScheduler(timezone="UTC")
    for channel in load_channels(s.channels_dir):
        scheduler.add_job(
            _run_and_log,
            CronTrigger.from_crontab(channel.cron),
            args=[channel.id],
            id=f"channel-{channel.id}",
            replace_existing=True,
        )
        log.info("Scheduled channel %s with cron %s", channel.id, channel.cron)
    return scheduler


async def serve_forever() -> None:
    scheduler = build_scheduler()
    scheduler.start()
    log.info("Scheduler started. Press Ctrl+C to exit.")
    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        scheduler.shutdown()
