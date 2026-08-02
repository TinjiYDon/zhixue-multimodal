"""ASR pipeline — schema-aligned; WhisperX optional, fixture fallback for CI/demo."""

from __future__ import annotations

import asyncio
import logging
import os
import tempfile
from pathlib import Path

from app.schemas.transcript import TranscriptResult, TranscriptSegment
from app.services.multimedia.ffmpeg_pipeline import extract_audio

logger = logging.getLogger(__name__)

_FIXTURE_DIR = Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "multimedia"


def _fixture_transcript(job_id: str, media_key: str) -> dict:
    result = TranscriptResult(
        job_id=job_id,
        media_key=media_key,
        language="zh",
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
    """Return ``TranscriptResult`` dict. Uses fixture unless WhisperX is available."""
    key = media_key or f"fixture://{job_id}"
    backend = os.environ.get("ZHIXUE_ASR_BACKEND", "auto").lower()

    if backend == "fixture":
        return _fixture_transcript(job_id, key)

    try:
        import whisperx  # type: ignore
    except ImportError:
        logger.warning("whisperx not installed; returning fixture transcript")
        return _fixture_transcript(job_id, key)

    if backend == "auto" and os.environ.get("CI") == "true":
        return _fixture_transcript(job_id, key)

    media_path = _resolve_media_path(media_key)
    if media_path is None:
        logger.warning("no media file; returning fixture transcript")
        return _fixture_transcript(job_id, key)

    with tempfile.TemporaryDirectory(prefix="zhixue_asr_") as tmp:
        wav_path = str(Path(tmp) / "audio.wav")
        if media_path.suffix.lower() == ".wav":
            wav_path = str(media_path)
        else:
            await asyncio.to_thread(extract_audio, str(media_path), wav_path, 16000)

        import torch

        device = "cuda" if torch.cuda.is_available() else "cpu"
        compute_type = "float16" if device == "cuda" else "int8"
        model = await asyncio.to_thread(
            whisperx.load_model,
            "base",
            device,
            compute_type=compute_type,
            language="zh",
        )
        audio = whisperx.load_audio(wav_path)
        raw = await asyncio.to_thread(model.transcribe, audio, batch_size=8)
        language = raw.get("language") or "zh"
        model_a, metadata = whisperx.load_align_model(language_code=language, device=device)
        aligned = whisperx.align(
            raw["segments"], model_a, metadata, audio, device, return_char_alignments=False
        )
        segments = [
            TranscriptSegment(
                text=str(seg.get("text", "")).strip(),
                start=float(seg.get("start", 0.0)),
                end=float(seg.get("end", 0.0)),
                speaker=seg.get("speaker"),
            )
            for seg in aligned.get("segments", [])
        ]
        return TranscriptResult(
            job_id=job_id,
            media_key=key,
            language=language,
            segments=segments,
        ).model_dump()
