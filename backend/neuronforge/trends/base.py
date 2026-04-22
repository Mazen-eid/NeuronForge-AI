from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Trend:
    title: str
    source: str
    score: float = 0.0
    url: str | None = None


class TrendSource(ABC):
    @abstractmethod
    async def fetch(self) -> list[Trend]:
        ...
