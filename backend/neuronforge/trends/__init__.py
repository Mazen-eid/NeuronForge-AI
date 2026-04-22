"""Trend discovery from free sources."""
from __future__ import annotations

from ..config import ChannelConfig
from .base import Trend, TrendSource
from .google_trends import GoogleTrendsSource
from .reddit import RedditSource
from .youtube_rss import YouTubeRSSSource


def build_sources(channel: ChannelConfig) -> list[TrendSource]:
    out: list[TrendSource] = []
    for spec in channel.trend_sources:
        if spec.kind == "google_trends":
            out.append(GoogleTrendsSource(geo=spec.query))
        elif spec.kind == "reddit":
            out.append(RedditSource(subreddit=spec.query))
        elif spec.kind == "youtube_rss":
            out.append(YouTubeRSSSource(channel_id=spec.query))
    return out


async def discover_trends(channel: ChannelConfig) -> list[Trend]:
    """Gather trends from every configured source. Failures on one source are
    logged and skipped so the pipeline never hard-fails on trend discovery."""
    import logging

    log = logging.getLogger(__name__)
    all_trends: list[Trend] = []
    for src in build_sources(channel):
        try:
            all_trends.extend(await src.fetch())
        except Exception as e:  # noqa: BLE001 - best-effort, log and continue
            log.warning("Trend source %s failed: %s", type(src).__name__, e)
    return all_trends


__all__ = [
    "Trend",
    "TrendSource",
    "GoogleTrendsSource",
    "RedditSource",
    "YouTubeRSSSource",
    "build_sources",
    "discover_trends",
]
