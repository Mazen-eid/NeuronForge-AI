from __future__ import annotations

import httpx

from .base import LLMClient


class OllamaClient(LLMClient):
    """Local Ollama server (https://ollama.com). Fully free if you have a decent GPU/CPU."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.1") -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def complete(
        self,
        system: str,
        user: str,
        *,
        temperature: float = 0.7,
        max_tokens: int = 1200,
    ) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(f"{self.base_url}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
        return data.get("message", {}).get("content", "")
