from __future__ import annotations

import httpx

from .base import LLMClient

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


class GroqClient(LLMClient):
    """Groq OpenAI-compatible chat completions. Generous free tier."""

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile") -> None:
        self.api_key = api_key
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
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(GROQ_URL, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        return data["choices"][0]["message"]["content"]
