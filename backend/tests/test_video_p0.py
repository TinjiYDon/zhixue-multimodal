"""V-P0 timeline data_source + failed empty cues + ASR thread config."""

from __future__ import annotations

import asyncio

from app.core import config
from app.services import timeline_store
from app.services.multimedia import transcription


def test_fixture_timeline_sets_data_source(client):
    timeline_store.clear_for_tests()
    course = client.post("/api/v1/courses", json={"title": "src"}).json()
    cid = course["id"]
    body = client.post(f"/api/v1/courses/{cid}/timeline/from-fixture").json()
    assert body["status"] == "ok"
    assert body["data_source"] == "fixture"
    assert body["message"] and "fixture" in body["message"].lower()


def test_placeholder_timeline_data_source(client):
    timeline_store.clear_for_tests()
    body = client.get("/api/v1/courses/no-such-yet/timeline").json()
    assert body["status"] == "placeholder"
    assert body["data_source"] == "placeholder"


def test_asr_ingest_marks_data_source_asr():
    timeline_store.clear_for_tests()
    result = {
        "backend": "whisperx",
        "segments": [
            {"start": 0.0, "end": 1.0, "text": "hello"},
            {"start": 1.0, "end": 2.0, "text": "world"},
        ],
    }
    tl = asyncio.run(
        timeline_store.ingest_job_result_to_timeline(
            "c-asr", result, use_fixture_on_fail=False
        )
    )
    assert tl.data_source == "asr"
    assert tl.status == "ok"
    assert len(tl.cues) == 2
    assert "ASR" in (tl.message or "")


def test_failed_job_empty_timeline():
    timeline_store.clear_for_tests()
    tl = asyncio.run(
        timeline_store.ingest_job_result_to_timeline(
            "c-fail",
            None,
            use_fixture_on_fail=False,
            job_failed=True,
            error_msg="未检出可识别语音",
        )
    )
    assert tl.status == "failed"
    assert tl.data_source == "failed"
    assert tl.cues == []
    assert tl.duration_sec == 0
    assert "failed" in (tl.message or "").lower()


def test_resolve_asr_threads_reproducible(monkeypatch):
    monkeypatch.setattr(config.settings, "asr_reproducible", True)
    monkeypatch.setattr(config.settings, "asr_cpu_threads", 8)
    assert transcription.resolve_asr_cpu_threads() == 1

    monkeypatch.setattr(config.settings, "asr_reproducible", False)
    monkeypatch.setattr(config.settings, "asr_cpu_threads", 2)
    assert transcription.resolve_asr_cpu_threads() == 2

    monkeypatch.setattr(config.settings, "asr_cpu_threads", 0)
    assert transcription.resolve_asr_cpu_threads() is None
