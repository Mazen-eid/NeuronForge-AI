from __future__ import annotations

import logging

import httpx

from .base import Trend, TrendSource

log = logging.getLogger(__name__)


class RedditSource(TrendSource):
    """Fetches hot posts from a subreddit via Reddit's public JSON endpoint."""

    def __init__(self, subreddit: str, limit: int = 20) -> None:
        self.subreddit = subreddit.lstrip("r/")
        self.limit = limit

    async def fetch(self) -> list[Trend]:
        url = f"https://www.reddit.com/r/{self.subreddit}/hot.json?limit={self.limit}"
        try:
            async with httpx.AsyncClient(
                timeout=15.0, headers={"User-Agent": "NeuronForge/0.1"}
            ) as client:
                resp = await client.get(url)
                resp.raise_for_status()
                data = resp.json()
        except Exception as e:  # noqa: BLE001
            log.warning("Reddit fetch failed for r/%s: %s", self.subreddit, e)
            return []
        out = []
        for child in data.get("data", {}).get("children", []):
            p = child.get("data", {})
            if p.get("stickied"):
                continue
            title = p.get("title")
            if not title:
                continue
            out.append(
                Trend(
                    title=title,
                    source=f"reddit/r/{self.subreddit}",
                    score=float(p.get("score", 0)),
                    url="https://www.reddit.com" + p.get("permalink", ""),
                )
            )
        return out
