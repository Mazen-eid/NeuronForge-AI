"""Compose a narrated short-form video from:
- one audio file (narration)
- N still images (slideshow backgrounds)
- optional burned-in captions (SRT-driven)

This is intentionally simple so it runs on any machine with FFmpeg. It is NOT a
replacement for DaVinci Resolve; it's enough to produce watchable Shorts.
"""
from __future__ import annotations

import asyncio
import logging
import subprocess
import wave
from pathlib import Path

from .captions import srt_from_captions

log = logging.getLogger(__name__)


def _probe_audio_duration(audio_path: Path) -> float:
    """Return duration in seconds. Uses ffprobe if present, else a heuristic for WAV."""
    try:
        out = subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(audio_path),
            ]
        )
        return float(out.strip())
    except (FileNotFoundError, subprocess.CalledProcessError, ValueError):
        if audio_path.suffix.lower() == ".wav":
            with wave.open(str(audio_path), "rb") as w:
                return w.getnframes() / float(w.getframerate())
        return 30.0


async def assemble_video(
    audio_path: Path,
    image_paths: list[Path],
    captions: list[str],
    out_path: Path,
    *,
    resolution: tuple[int, int] = (1080, 1920),
    fps: int = 30,
) -> Path:
    return await asyncio.to_thread(
        _assemble_sync,
        audio_path,
        image_paths,
        captions,
        out_path,
        resolution,
        fps,
    )


def _assemble_sync(
    audio_path: Path,
    image_paths: list[Path],
    captions: list[str],
    out_path: Path,
    resolution: tuple[int, int],
    fps: int,
) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if not image_paths:
        raise ValueError("At least one background image is required")

    duration = _probe_audio_duration(audio_path)
    per_image = max(1.5, duration / len(image_paths))
    width, height = resolution

    # Write a concat demuxer file describing the slideshow.
    concat_file = out_path.with_suffix(".concat.txt")
    with concat_file.open("w", encoding="utf-8") as f:
        for img in image_paths:
            f.write(f"file '{img.resolve()}'\n")
            f.write(f"duration {per_image:.3f}\n")
        # FFmpeg concat demuxer quirk: repeat the last file with no duration.
        f.write(f"file '{image_paths[-1].resolve()}'\n")

    video_filter = (
        f"scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height},format=yuv420p"
    )

    # Burn captions in if any, using an .srt generated from the caption list.
    srt_path: Path | None = None
    if captions:
        srt_path = out_path.with_suffix(".srt")
        srt_path.write_text(srt_from_captions(captions, duration), encoding="utf-8")
        video_filter += (
            f",subtitles='{srt_path.resolve()}':force_style="
            "'FontName=Arial,FontSize=18,PrimaryColour=&H00FFFFFF,"
            "OutlineColour=&H00000000,Outline=2,Shadow=0,Alignment=2,MarginV=120'"
        )

    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-i",
        str(audio_path),
        "-vf",
        video_filter,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "23",
        "-r",
        str(fps),
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-shortest",
        "-movflags",
        "+faststart",
        str(out_path),
    ]
    log.info("Running FFmpeg: %s", " ".join(cmd))
    subprocess.run(cmd, check=True, capture_output=True)
    concat_file.unlink(missing_ok=True)
    if srt_path is not None:
        srt_path.unlink(missing_ok=True)
    return out_path
