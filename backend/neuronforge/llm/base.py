from __future__ import annotations

from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Minimal chat-style interface. Returns plain text."""

    @abstractmethod
    async def complete(
        self,
        system: str,
        user: str,
        *,
        temperature: float = 0.7,
        max_tokens: int = 1200,
    ) -> str:
        ...
