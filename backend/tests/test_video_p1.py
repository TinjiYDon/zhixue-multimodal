"""V-P1 ASR preprocess / model choice / quality flags."""

from __future__ import annotations

from app.core import config
from app.services.multimedia import ffmpeg_pipeline, transcription


def test_choose_asr_model_short_vs_long(monkeypatch):
    monkeypatch.setattr(config.settings, "asr_model_short", "small")
    monkeypatch.setattr(config.settings, "asr_model_long", "base")
    monkeypatch.setattr(config.settings, "asr_long_threshold_sec", 480.0)
    assert transcription.choose_asr_model(37.0) == "small"
    assert transcription.choose_asr_model(479.9) == "small"
    assert transcription.choose_asr_model(480.0) == "base"
    assert transcription.choose_asr_model(780.0) == "base"


def test_collect_quality_flags_thresholds(monkeypatch):
    monkeypatch.setattr(config.settings, "asr_compression_ratio_warn", 2.35)
    monkeypatch.setattr(config.settings, "asr_no_speech_prob_warn", 0.9)
    raw = [
        {"text": "ok", "compression_ratio": 1.2, "no_speech_prob": 0.1},
        {"text": "repeat…", "compression_ratio": 3.0, "no_speech_prob": 0.2},
        {"text": "silence?", "compression_ratio": 1.0, "no_speech_prob": 0.95},
        {"text": "both", "compression_ratio": 2.5, "no_speech_prob": 0.99},
    ]
    flags, by_idx = transcription.collect_quality_flags(raw)
    assert len(flags) == 3
    assert by_idx[1] == ["high_compression_ratio"]
    assert by_idx[2] == ["high_no_speech_prob"]
    assert set(by_idx[3]) == {"high_compression_ratio", "high_no_speech_prob"}
    assert 0 not in by_idx


def test_ffmpeg_af_filters_default(monkeypatch):
    monkeypatch.setattr(config.settings, "asr_audio_preprocess", True)
    monkeypatch.setattr(config.settings, "asr_highpass_hz", 80)
    monkeypatch.setattr(config.settings, "asr_loudnorm", True)
    af = ffmpeg_pipeline._build_af_filters()
    assert af is not None
    assert "highpass=f=80" in af
    assert "loudnorm=" in af


def test_ffmpeg_af_filters_disabled(monkeypatch):
    monkeypatch.setattr(config.settings, "asr_audio_preprocess", False)
    assert ffmpeg_pipeline._build_af_filters() is None
    assert ffmpeg_pipeline._build_af_filters(preprocess=False) is None


def test_transcript_result_carries_quality_fields():
    from app.schemas.transcript import TranscriptResult, TranscriptSegment

    result = TranscriptResult(
        job_id="j1",
        media_key="k",
        backend="whisperx",
        asr_model="small",
        duration_sec=37.0,
        quality_flags=[{"index": 0, "issues": ["high_compression_ratio"]}],
        segments=[
            TranscriptSegment(
                text="x",
                start=0.0,
                end=1.0,
                quality_issues=["high_compression_ratio"],
            )
        ],
    )
    dumped = result.model_dump()
    assert dumped["asr_model"] == "small"
    assert dumped["quality_flags"][0]["issues"] == ["high_compression_ratio"]
    assert dumped["segments"][0]["quality_issues"] == ["high_compression_ratio"]
