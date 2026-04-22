from __future__ import annotations


def _fmt_ts(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def srt_from_captions(captions: list[str], total_duration: float) -> str:
    """Spread `captions` evenly across `total_duration` to produce a valid .srt file."""
    if not captions:
        return ""
    per = max(0.5, total_duration / len(captions))
    parts = []
    for i, text in enumerate(captions):
        start = i * per
        end = min((i + 1) * per, total_duration)
        parts.append(f"{i + 1}\n{_fmt_ts(start)} --> {_fmt_ts(end)}\n{text}\n")
    return "\n".join(parts)
