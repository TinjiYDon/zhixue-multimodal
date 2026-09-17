"""ASR pipeline — schema-aligned; WhisperX optional, fixture fallback for CI/demo."""

from __future__ import annotations

import asyncio
import logging
import os
import tempfile
import wave
from pathlib import Path
from typing import Any

from app.core.config import settings
from app.schemas.transcript import TranscriptResult, TranscriptSegment
from app.services.multimedia.ffmpeg_pipeline import extract_audio

logger = logging.getLogger(__name__)

_FIXTURE_DIR = Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "multimedia"


def patch_faster_whisper_compatibility():
    """动态兼容新版 faster-whisper 以及 pyannote 的参数冲突问题"""
    # 1. 修复 faster-whisper 参数缺失
    try:
        from faster_whisper.transcribe import TranscriptionOptions
        import inspect

        sig = inspect.signature(TranscriptionOptions.__init__)
        if "multilingual" in sig.parameters and "hotwords" in sig.parameters:
            orig_init = TranscriptionOptions.__init__

            def new_init(self, *args, **kwargs):
                if "multilingual" not in kwargs and len(args) < 32:
                    kwargs["multilingual"] = False
                if "hotwords" not in kwargs and len(args) < 33:
                    kwargs["hotwords"] = None
                orig_init(self, *args, **kwargs)

            TranscriptionOptions.__init__ = new_init
            logger.info("已成功注入 faster-whisper 新版参数兼容补丁。")
    except Exception as e:
        logger.warning("注入 faster-whisper 补丁微小异常: %s", e)

    # 2. 修复 Pyannote Token 参数不兼容问题
    def make_clean_init(orig_init_fn):
        def clean_init(self, *args, **kwargs):
            kwargs.pop("use_auth_token", None)
            kwargs.pop("token", None)
            return orig_init_fn(self, *args, **kwargs)

        return clean_init

    try:
        from pyannote.runtime.base import Inference

        Inference.__init__ = make_clean_init(Inference.__init__)
    except Exception:
        pass

    try:
        from pyannote.audio.core.inference import Inference

        Inference.__init__ = make_clean_init(Inference.__init__)
    except Exception:
        pass


def resolve_asr_cpu_threads() -> int | None:
    """Return fixed thread count for CT2/Whisper, or None for library default.

    V-P0-1: int8 multi-thread reduction order is nondeterministic; set 1 for eval.
    """
    if settings.asr_reproducible:
        return 1
    if settings.asr_cpu_threads and settings.asr_cpu_threads > 0:
        return int(settings.asr_cpu_threads)
    return None


def choose_asr_model(duration_sec: float) -> str:
    """V-P1-4: short → small (准), long → base (稳/快)."""
    if duration_sec >= float(settings.asr_long_threshold_sec):
        return settings.asr_model_long or "base"
    return settings.asr_model_short or "small"


def wav_duration_sec(path: str) -> float:
    with wave.open(path, "rb") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate() or 1
        return float(frames) / float(rate)


def collect_quality_flags(raw_segments: list[dict[str, Any]]) -> tuple[list[dict], dict[int, list[str]]]:
    """V-P1-3: flag near-hallucination metrics from Whisper-style segments."""
    flags: list[dict] = []
    by_index: dict[int, list[str]] = {}
    cr_warn = float(settings.asr_compression_ratio_warn)
    nsp_warn = float(settings.asr_no_speech_prob_warn)
    for i, seg in enumerate(raw_segments):
        issues: list[str] = []
        cr = seg.get("compression_ratio")
        nsp = seg.get("no_speech_prob")
        try:
            if cr is not None and float(cr) >= cr_warn:
                issues.append("high_compression_ratio")
        except (TypeError, ValueError):
            pass
        try:
            if nsp is not None and float(nsp) >= nsp_warn:
                issues.append("high_no_speech_prob")
        except (TypeError, ValueError):
            pass
        if issues:
            by_index[i] = issues
            flags.append(
                {
                    "index": i,
                    "issues": issues,
                    "compression_ratio": cr,
                    "no_speech_prob": nsp,
                    "text": str(seg.get("text", ""))[:80],
                }
            )
    return flags, by_index


def _apply_thread_env(threads: int) -> None:
    value = str(threads)
    for key in (
        "OMP_NUM_THREADS",
        "MKL_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "CT2_NUM_THREADS",
    ):
        os.environ[key] = value


def _fixture_transcript(job_id: str, media_key: str) -> dict:
    """CI / 环境不满足时的 Mock 降级数据"""
    result = TranscriptResult(
        job_id=job_id,
        media_key=media_key,
        language="zh",
        backend="fixture",
        asr_model="fixture",
        duration_sec=3.0,
        segments=[
            TranscriptSegment(text="智学多媒体转写样例。", start=0.0, end=1.5, speaker=None),
            TranscriptSegment(text="Schema 契约验收通过。", start=1.5, end=3.0, speaker=None),
        ],
    )
    return result.model_dump()


def _resolve_media_path(media_key: str | None) -> Path | None:
    env_path = os.environ.get("ZHIXUE_MEDIA_PATH")
    if env_path and Path(env_path).exists():
        return Path(env_path)
    if media_key:
        candidate = Path(media_key)
        if candidate.exists():
            return candidate
    sample = _FIXTURE_DIR / "sample.wav"
    if sample.exists():
        return sample
    return None


async def transcribe_media(job_id: str, media_key: str | None = None) -> dict:
    """Return TranscriptResult dict. Uses fixture unless WhisperX is available."""
    key = media_key or f"fixture://{job_id}"
    backend = os.environ.get("ZHIXUE_ASR_BACKEND", "auto").lower()

    if backend == "fixture":
        return _fixture_transcript(job_id, key)

    try:
        import whisperx  # type: ignore
        import torch
    except ImportError:
        logger.warning("whisperx not installed; returning fixture transcript")
        return _fixture_transcript(job_id, key)

    if backend == "auto" and os.environ.get("CI") == "true":
        return _fixture_transcript(job_id, key)

    media_path = _resolve_media_path(media_key)
    if media_path is None:
        logger.warning("no media file; returning fixture transcript")
        return _fixture_transcript(job_id, key)

    patch_faster_whisper_compatibility()

    threads = resolve_asr_cpu_threads()
    if threads is not None:
        _apply_thread_env(threads)
        logger.info("ASR cpu_threads fixed to %s (reproducible=%s)", threads, settings.asr_reproducible)

    with tempfile.TemporaryDirectory(prefix="zhixue_asr_") as tmp:
        wav_path = str(Path(tmp) / "audio.wav")
        # Always normalize via ffmpeg when preprocess on (even if source is wav)
        await asyncio.to_thread(extract_audio, str(media_path), wav_path, 16000)

        duration = wav_duration_sec(wav_path)
        model_name = choose_asr_model(duration)
        logger.info("ASR model=%s duration=%.1fs", model_name, duration)

        device = "cuda" if torch.cuda.is_available() else "cpu"
        compute_type = "float16" if device == "cuda" else "int8"
        load_kwargs: dict[str, Any] = {
            "device": device,
            "compute_type": compute_type,
            "language": "zh",
        }
        if threads is not None:
            load_kwargs["threads"] = threads
        prompt = (settings.asr_initial_prompt or "").strip()
        if prompt:
            load_kwargs["asr_options"] = {"initial_prompt": prompt}

        try:
            model = await asyncio.to_thread(whisperx.load_model, model_name, **load_kwargs)
        except TypeError:
            load_kwargs.pop("threads", None)
            load_kwargs.pop("asr_options", None)
            model = await asyncio.to_thread(whisperx.load_model, model_name, **load_kwargs)

        audio = whisperx.load_audio(wav_path)
        transcribe_kwargs: dict[str, Any] = {"batch_size": 8}
        if prompt:
            transcribe_kwargs["initial_prompt"] = prompt
        try:
            raw = await asyncio.to_thread(model.transcribe, audio, **transcribe_kwargs)
        except TypeError:
            raw = await asyncio.to_thread(model.transcribe, audio, batch_size=8)

        language = raw.get("language") or "zh"
        raw_segments = list(raw.get("segments") or [])
        quality_flags, issues_by_idx = collect_quality_flags(raw_segments)

        model_a, metadata = whisperx.load_align_model(language_code=language, device=device)
        aligned = whisperx.align(
            raw_segments, model_a, metadata, audio, device, return_char_alignments=False
        )
        aligned_segs = list(aligned.get("segments") or [])
        segments: list[TranscriptSegment] = []
        for i, seg in enumerate(aligned_segs):
            segments.append(
                TranscriptSegment(
                    text=str(seg.get("text", "")).strip(),
                    start=float(seg.get("start", 0.0)),
                    end=float(seg.get("end", 0.0)),
                    speaker=seg.get("speaker"),
                    quality_issues=list(issues_by_idx.get(i, [])),
                )
            )
        return TranscriptResult(
            job_id=job_id,
            media_key=key,
            language=language,
            backend="whisperx",
            asr_model=model_name,
            duration_sec=duration,
            quality_flags=quality_flags,
            segments=segments,
        ).model_dump()
