"""Channel configuration loaded from YAML files under `channels/`."""
from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field


class TrendSource(BaseModel):
    kind: Literal["google_trends", "reddit", "youtube_rss"]
    # google_trends: geo code (e.g. "US", "EG"); reddit: subreddit; youtube_rss: channel_id
    query: str


class ChannelConfig(BaseModel):
    id: str = Field(..., description="Unique channel ID used for logs and URLs")
    language: Literal["en", "ar", "fr", "es"] = "en"
    niche: str = "general"
    platform: Literal["youtube_shorts", "youtube_long", "tiktok"] = "youtube_shorts"

    # Voice for edge-tts (see `edge-tts --list-voices`). Sensible defaults per language.
    tts_voice: str | None = None

    # Video parameters
    target_duration_seconds: int = 45
    resolution: tuple[int, int] = (1080, 1920)  # portrait for shorts
    fps: int = 30

    # Script & prompt tuning
    tone: str = "informative and engaging"
    system_prompt_extra: str = ""

    # Trend discovery inputs
    trend_sources: list[TrendSource] = Field(default_factory=list)

    # YouTube upload params (ignored in dry-run mode)
    youtube_category_id: str = "22"  # "People & Blogs"
    youtube_privacy: Literal["public", "unlisted", "private"] = "private"

    # How often to run for this channel (cron expression, interpreted by scheduler)
    cron: str = "0 */6 * * *"  # every 6 hours

    @property
    def default_tts_voice(self) -> str:
        if self.tts_voice:
            return self.tts_voice
        return {
            "en": "en-US-JennyNeural",
            "ar": "ar-EG-ShakirNeural",
            "fr": "fr-FR-DeniseNeural",
            "es": "es-ES-ElviraNeural",
        }[self.language]


def load_channel(path: Path) -> ChannelConfig:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return ChannelConfig(**data)


def load_channels(channels_dir: Path) -> list[ChannelConfig]:
    if not channels_dir.exists():
        return []
    channels = []
    for p in sorted(channels_dir.glob("*.yaml")) + sorted(channels_dir.glob("*.yml")):
        channels.append(load_channel(p))
    return channels


def find_channel(channels_dir: Path, channel_id: str) -> ChannelConfig | None:
    for c in load_channels(channels_dir):
        if c.id == channel_id:
            return c
    return None
