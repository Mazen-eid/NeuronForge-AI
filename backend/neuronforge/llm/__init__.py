"""Pluggable LLM clients. Default to a deterministic mock so dry runs work without any keys."""
from __future__ import annotations

import logging

from ..settings import get_settings
from .base import LLMClient
from .groq_client import GroqClient
from .mock_client import MockClient
from .ollama_client import OllamaClient
from .openai_client import OpenAIClient

log = logging.getLogger(__name__)


def get_llm() -> LLMClient:
    s = get_settings()
    provider = s.llm_provider.lower()
    if provider == "groq" and s.groq_api_key:
        return GroqClient(api_key=s.groq_api_key, model=s.groq_model)
    if provider == "openai" and s.openai_api_key:
        return OpenAIClient(api_key=s.openai_api_key, model=s.openai_model)
    if provider == "ollama":
        return OllamaClient(base_url=s.ollama_base_url, model=s.ollama_model)
    if provider != "mock":
        log.warning(
            "LLM provider %r requested but no credentials available; falling back to mock.",
            provider,
        )
    return MockClient()


__all__ = [
    "LLMClient",
    "MockClient",
    "GroqClient",
    "OpenAIClient",
    "OllamaClient",
    "get_llm",
]
