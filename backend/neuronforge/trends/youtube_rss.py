from __future__ import annotations

import asyncio
import logging

from .base import Trend, TrendSource

log = logging.getLogger(__name__)


class YouTubeRSSSource(TrendSource):
    """Fetches the latest videos from a YouTube channel's public RSS feed (no API key needed)."""

    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id

    async def fetch(self) -> list[Trend]:
        return await asyncio.to_thread(self._fetch_sync)

    def _fetch_sync(self) -> list[Trend]:
        try:
            import feedparser
        except ImportError:
            log.warning("feedparser not installed; skipping YouTube RSS")
            return []
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={self.channel_id}"
        try:
            parsed = feedparser.parse(url)
        except Exception as e:  # noqa: BLE001
            log.warning("YouTube RSS fetch failed: %s", e)
            return []
        out = []
        for entry in parsed.entries[:25]:
            out.append(
                Trend(
                    title=entry.get("title", ""),
                    source=f"youtube/{self.channel_id}",
                    url=entry.get("link"),
                )
            )
        return out
