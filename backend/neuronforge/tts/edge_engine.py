"""Free TTS via Microsoft Edge's online neural voices (edge-tts library).

No API key required. Supports Arabic, English, French, Spanish (and 70+ other voices).
"""
from __future__ import annotations

import asyncio
import logging
import subprocess
import wave
from pathlib import Path

log = logging.getLogger(__name__)


async def synthesize(text: str, voice: str, out_path: Path) -> Path:
    """Synthesize `text` to `out_path` (.mp3). Falls back to silent WAV if edge-tts fails."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import edge_tts

        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(out_path))
        return out_path
    except Exception as e:  # noqa: BLE001
        log.warning("edge-tts failed (%s); generating silent fallback.", e)
        return await asyncio.to_thread(_silent_wav_fallback, out_path, len(text))


def _silent_wav_fallback(out_path: Path, text_len: int) -> Path:
    """Write a silent WAV of roughly the expected duration (~150 wpm)."""
    duration_s = max(3.0, text_len / 15.0)
    wav_path = out_path.with_suffix(".wav")
    sample_rate = 24000
    n_frames = int(duration_s * sample_rate)
    with wave.open(str(wav_path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(b"\x00\x00" * n_frames)
    # Convert to mp3 if ffmpeg is available, else return the wav.
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(wav_path), str(out_path)],
            check=True,
            capture_output=True,
        )
        wav_path.unlink(missing_ok=True)
        return out_path
    except (FileNotFoundError, subprocess.CalledProcessError):
        return wav_path
