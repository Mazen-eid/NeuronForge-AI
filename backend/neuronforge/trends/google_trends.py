from __future__ import annotations

import asyncio
import logging

from .base import Trend, TrendSource

log = logging.getLogger(__name__)


class GoogleTrendsSource(TrendSource):
    """Uses `pytrends` to fetch trending searches for a given geo (e.g. "US", "egypt")."""

    def __init__(self, geo: str = "united_states") -> None:
        self.geo = geo

    async def fetch(self) -> list[Trend]:
        return await asyncio.to_thread(self._fetch_sync)

    def _fetch_sync(self) -> list[Trend]:
        try:
            from pytrends.request import TrendReq
        except ImportError:
            log.warning("pytrends not installed; skipping Google Trends")
            return []
        try:
            pytrends = TrendReq(hl="en-US", tz=0)
            df = pytrends.trending_searches(pn=self.geo)
        except Exception as e:  # noqa: BLE001
            log.warning("Google Trends fetch failed: %s", e)
            return []
        out = []
        for i, row in enumerate(df.itertuples(index=False)):
            title = str(row[0])
            out.append(Trend(title=title, source="google_trends", score=100.0 - i))
        return out
