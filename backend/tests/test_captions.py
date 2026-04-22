from __future__ import annotations

from neuronforge.video.captions import srt_from_captions


def test_srt_format():
    srt = srt_from_captions(["hello", "world"], total_duration=4.0)
    assert "1\n00:00:00,000 --> 00:00:02,000\nhello" in srt
    assert "2\n00:00:02,000 --> 00:00:04,000\nworld" in srt


def test_srt_empty():
    assert srt_from_captions([], 10.0) == ""
