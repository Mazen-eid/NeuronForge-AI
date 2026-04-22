from __future__ import annotations

from pathlib import Path

from neuronforge.config import load_channel, load_channels

REPO_CHANNELS = Path(__file__).resolve().parents[1] / "channels"


def test_load_example_channels():
    channels = load_channels(REPO_CHANNELS)
    ids = {c.id for c in channels}
    assert "example-en-tech" in ids
    assert "example-ar-tech" in ids
    assert "example-en-history" in ids


def test_default_tts_voice():
    ch = load_channel(REPO_CHANNELS / "example-en-tech.yaml")
    assert ch.default_tts_voice.startswith("en-")
    ar = load_channel(REPO_CHANNELS / "example-ar-tech.yaml")
    assert ar.default_tts_voice.startswith("ar-")
