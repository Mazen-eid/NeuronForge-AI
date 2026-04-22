from __future__ import annotations

from neuronforge.db import DB


def test_run_lifecycle(tmp_path):
    db = DB(tmp_path / "t.sqlite3")
    run_id = db.start_run("ch1", topic="hello")
    assert run_id > 0
    db.finish_run(run_id, "uploaded", video_url="https://youtu.be/x", meta={"k": "v"})
    runs = db.recent_runs()
    assert len(runs) == 1
    assert runs[0]["status"] == "uploaded"
    assert runs[0]["video_url"] == "https://youtu.be/x"


def test_used_topics_dedup(tmp_path):
    db = DB(tmp_path / "t.sqlite3")
    assert not db.is_topic_used("ch", "t")
    db.mark_topic_used("ch", "t")
    assert db.is_topic_used("ch", "t")
    # Idempotent
    db.mark_topic_used("ch", "t")
    assert db.is_topic_used("ch", "t")
