from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_data_dir, monkeypatch):
    channels_dir = tmp_data_dir / "channels"
    repo_channels = Path(__file__).resolve().parents[1] / "channels"
    for p in repo_channels.glob("*.yaml"):
        (channels_dir / p.name).write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
    from neuronforge.api import app

    return TestClient(app)


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert "version" in body


def test_channels_endpoint(client):
    r = client.get("/channels")
    assert r.status_code == 200
    ids = {c["id"] for c in r.json()["channels"]}
    assert "example-en-tech" in ids


def test_runs_endpoint(client):
    r = client.get("/runs?limit=5")
    assert r.status_code == 200
    assert "runs" in r.json()


def test_run_unknown_channel(client):
    r = client.post("/channels/does-not-exist/run", json={"dry_run": True})
    assert r.status_code == 404


def test_assistant_ideas(client):
    r = client.post("/assistant/ideas", json={"prompt": "Give me 3 YouTube Shorts ideas", "language": "en"})
    assert r.status_code == 200
    body = r.json()
    assert "raw" in body
    assert "ideas" in body
