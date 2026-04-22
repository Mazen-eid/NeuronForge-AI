from __future__ import annotations

import os
from pathlib import Path

import pytest

os.environ.setdefault("LLM_PROVIDER", "mock")


@pytest.fixture()
def tmp_data_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    monkeypatch.setenv("DB_PATH", str(tmp_path / "test.sqlite3"))
    monkeypatch.setenv("CHANNELS_DIR", str(tmp_path / "channels"))
    Path(tmp_path / "channels").mkdir(exist_ok=True)
    # Reset cached settings so env vars are picked up
    from neuronforge.settings import reset_settings_for_tests

    reset_settings_for_tests()
    yield tmp_path
    reset_settings_for_tests()
