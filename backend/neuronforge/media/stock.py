from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path

import httpx

from ..settings import get_settings

log = logging.getLogger(__name__)


@dataclass
class StockMedia:
    path: Path
    source: str  # "pexels" | "pixabay" | "solid"


async def fetch_background_images(
    query: str, count: int, out_dir: Path, resolution: tuple[int, int]
) -> list[StockMedia]:
    """Try Pexels, then Pixabay, then a solid-color fallback. Never raises."""
    out_dir.mkdir(parents=True, exist_ok=True)
    s = get_settings()

    if s.pexels_api_key:
        try:
            return await _fetch_pexels(query, count, out_dir, s.pexels_api_key)
        except Exception as e:  # noqa: BLE001
            log.warning("Pexels fetch failed: %s", e)

    if s.pixabay_api_key:
        try:
            return await _fetch_pixabay(query, count, out_dir, s.pixabay_api_key)
        except Exception as e:  # noqa: BLE001
            log.warning("Pixabay fetch failed: %s", e)

    return _solid_fallback(count, out_dir, resolution)


async def _fetch_pexels(
    query: str, count: int, out_dir: Path, api_key: str
) -> list[StockMedia]:
    url = "https://api.pexels.com/v1/search"
    params = {"query": query, "per_page": count, "orientation": "portrait"}
    headers = {"Authorization": api_key}
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(url, params=params, headers=headers)
        resp.raise_for_status()
        photos = resp.json().get("photos", [])
        out = []
        for i, p in enumerate(photos[:count]):
            img_url = p["src"]["large2x"]
            dest = out_dir / f"pexels_{i:03d}.jpg"
            img = await client.get(img_url)
            img.raise_for_status()
            dest.write_bytes(img.content)
            out.append(StockMedia(path=dest, source="pexels"))
    return out


async def _fetch_pixabay(
    query: str, count: int, out_dir: Path, api_key: str
) -> list[StockMedia]:
    url = "https://pixabay.com/api/"
    params = {
        "key": api_key,
        "q": query,
        "image_type": "photo",
        "orientation": "vertical",
        "per_page": max(3, count),
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        hits = resp.json().get("hits", [])
        out = []
        for i, h in enumerate(hits[:count]):
            img_url = h.get("largeImageURL") or h.get("webformatURL")
            if not img_url:
                continue
            dest = out_dir / f"pixabay_{i:03d}.jpg"
            img = await client.get(img_url)
            img.raise_for_status()
            dest.write_bytes(img.content)
            out.append(StockMedia(path=dest, source="pixabay"))
    return out


def _solid_fallback(
    count: int, out_dir: Path, resolution: tuple[int, int]
) -> list[StockMedia]:
    """Generate solid-color JPG backgrounds via FFmpeg's lavfi color source."""
    palette = ["#1e3a8a", "#7c3aed", "#0f766e", "#b91c1c", "#c2410c", "#166534"]
    out = []
    for i in range(count):
        color = palette[i % len(palette)]
        dest = out_dir / f"solid_{i:03d}.jpg"
        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "lavfi",
                    "-i",
                    f"color=c={color}:s={resolution[0]}x{resolution[1]}",
                    "-frames:v",
                    "1",
                    str(dest),
                ],
                check=True,
                capture_output=True,
            )
            out.append(StockMedia(path=dest, source="solid"))
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            log.warning("FFmpeg solid-fallback failed: %s", e)
    return out
