"""Multimedia outputs must match official transcript/OCR schemas (no GPU)."""

from __future__ import annotations

import asyncio
import os

from app.schemas.transcript import OcrResult, TranscriptResult


def test_transcribe_fixture_schema():
    os.environ["ZHIXUE_ASR_BACKEND"] = "fixture"
    from app.services.multimedia.transcription import transcribe_media

    raw = asyncio.run(transcribe_media("job-1", "fixture://demo"))
    parsed = TranscriptResult.model_validate(raw)
    assert parsed.job_id == "job-1"
    assert parsed.segments
    assert parsed.segments[0].end >= parsed.segments[0].start


def test_ocr_fixture_schema():
    os.environ["ZHIXUE_OCR_BACKEND"] = "fixture"
    from app.services.multimedia.ocr import run_ocr

    raw = asyncio.run(run_ocr("asset-1"))
    parsed = OcrResult.model_validate(raw)
    assert parsed.asset_id == "asset-1"
    assert parsed.pages[0].page == 1
    assert parsed.pages[0].blocks[0].text
    assert "raw_text" not in raw


def test_ffmpeg_cmd_is_list(monkeypatch, tmp_path):
    from app.services.multimedia import ffmpeg_pipeline

    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)

        class R:
            returncode = 0

        return R()

    monkeypatch.setattr(ffmpeg_pipeline.subprocess, "run", fake_run)
    inp = tmp_path / "in.mp4"
    inp.write_bytes(b"x")
    out = tmp_path / "out.wav"
    ffmpeg_pipeline.extract_audio(str(inp), str(out), 16000)
    assert calls and calls[0][0] == "ffmpeg"
    assert "-ar" in calls[0]
