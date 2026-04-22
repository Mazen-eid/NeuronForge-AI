"""Runtime settings loaded from environment variables (or .env file)."""
from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven settings.

    All API keys are optional. The pipeline gracefully degrades when a key is
    missing (it will use the `mock` provider, which returns deterministic stub
    content suitable for dry runs).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM provider selection: "groq" | "openai" | "ollama" | "mock"
    llm_provider: str = Field(default="mock")
    groq_api_key: str | None = None
    groq_model: str = "llama-3.3-70b-versatile"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"

    # Stock-media providers (both offer generous free tiers)
    pexels_api_key: str | None = None
    pixabay_api_key: str | None = None

    # YouTube OAuth client secret & token paths (see README for setup)
    youtube_client_secret_file: Path = Path("secrets/youtube_client_secret.json")
    youtube_token_dir: Path = Path("secrets/youtube_tokens")

    # Local paths
    data_dir: Path = Path("data")
    channels_dir: Path = Path("channels")
    db_path: Path = Path("data/neuronforge.sqlite3")

    # API
    api_host: str = "0.0.0.0"  # noqa: S104 - dev convenience
    api_port: int = 8000
    cors_origins: list[str] = ["*"]


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
        _settings.data_dir.mkdir(parents=True, exist_ok=True)
    return _settings


def reset_settings_for_tests() -> None:
    global _settings
    _settings = None
