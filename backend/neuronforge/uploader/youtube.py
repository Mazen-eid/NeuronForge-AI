"""YouTube upload via the official Data API v3 with OAuth 2.0 installed-app flow.

Setup (one-time, zero cost):
  1. Go to https://console.cloud.google.com/ and create a project.
  2. Enable "YouTube Data API v3".
  3. Configure OAuth consent screen (External, Testing is fine).
  4. Create OAuth client ID of type "Desktop app".
  5. Download the JSON, save it to `backend/secrets/youtube_client_secret.json`.
  6. Run `python -m neuronforge youtube-auth <channel_id>` to complete the browser
     OAuth flow once per channel. A refresh token is cached at
     `backend/secrets/youtube_tokens/<channel_id>.json`.
"""
from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path

from ..settings import get_settings

log = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def _token_path(channel_id: str) -> Path:
    d = get_settings().youtube_token_dir
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{channel_id}.json"


def _client_secret_path() -> Path:
    return get_settings().youtube_client_secret_file


def has_credentials(channel_id: str) -> bool:
    return _token_path(channel_id).exists() and _client_secret_path().exists()


def run_auth_flow(channel_id: str) -> Path:
    """Open a browser to complete OAuth and persist the refresh token.

    Call this once per channel before running uploads. Safe to re-run.
    """
    from google_auth_oauthlib.flow import InstalledAppFlow

    if not _client_secret_path().exists():
        raise FileNotFoundError(
            f"Missing OAuth client secret file at {_client_secret_path()}. "
            "Follow the setup steps in the module docstring."
        )
    flow = InstalledAppFlow.from_client_secrets_file(
        str(_client_secret_path()), scopes=SCOPES
    )
    creds = flow.run_local_server(port=0)
    _token_path(channel_id).write_text(creds.to_json(), encoding="utf-8")
    return _token_path(channel_id)


def _load_credentials(channel_id: str):
    from google.oauth2.credentials import Credentials

    path = _token_path(channel_id)
    if not path.exists():
        raise FileNotFoundError(
            f"No token for channel {channel_id!r}. Run `neuronforge youtube-auth {channel_id}` first."
        )
    data = json.loads(path.read_text(encoding="utf-8"))
    return Credentials.from_authorized_user_info(data, SCOPES)


class YouTubeUploader:
    """Resumable upload of one video + metadata to YouTube."""

    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id

    async def upload(
        self,
        video_path: Path,
        *,
        title: str,
        description: str,
        tags: list[str],
        category_id: str = "22",
        privacy: str = "private",
    ) -> dict:
        return await asyncio.to_thread(
            self._upload_sync,
            video_path,
            title,
            description,
            tags,
            category_id,
            privacy,
        )

    def _upload_sync(
        self,
        video_path: Path,
        title: str,
        description: str,
        tags: list[str],
        category_id: str,
        privacy: str,
    ) -> dict:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        creds = _load_credentials(self.channel_id)
        youtube = build("youtube", "v3", credentials=creds, cache_discovery=False)
        body = {
            "snippet": {
                "title": title[:95],
                "description": description,
                "tags": tags[:30],
                "categoryId": category_id,
            },
            "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False},
        }
        media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True, mimetype="video/mp4")
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                log.info("Upload progress: %d%%", int(status.progress() * 100))
        video_id = response.get("id")
        return {
            "video_id": video_id,
            "url": f"https://youtu.be/{video_id}" if video_id else None,
            "raw": response,
        }
