"""FFmpeg helpers — extract 16 kHz mono WAV for ASR (optional loudnorm/highpass)."""

from __future__ import annotations

import logging
import os
import subprocess

from app.core.config import settings

logger = logging.getLogger(__name__)


def _build_af_filters(*, preprocess: bool | None = None) -> str | None:
    """V-P1-1: highpass + EBU R128 loudnorm to reduce clipping / level skew."""
    use = settings.asr_audio_preprocess if preprocess is None else preprocess
    if not use:
        return None
    parts: list[str] = []
    hz = int(settings.asr_highpass_hz or 0)
    if hz > 0:
        parts.append(f"highpass=f={hz}")
    if settings.asr_loudnorm:
        # Target -16 LUFS, true peak -1.5 dBTP — avoids 0 dBFS tops
        parts.append("loudnorm=I=-16:TP=-1.5:LRA=11")
    return ",".join(parts) if parts else None


def extract_audio(
    input_path: str,
    output_path: str,
    sample_rate: int = 16000,
    *,
    preprocess: bool | None = None,
) -> str:
    """Extract mono PCM WAV at ``sample_rate`` using system ``ffmpeg``."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"input media not found: {input_path}")

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        str(sample_rate),
        "-ac",
        "1",
    ]
    af = _build_af_filters(preprocess=preprocess)
    if af:
        cmd.extend(["-af", af])
    cmd.append(str(output_path))

    logger.info(
        "extract_audio: %s -> %s (%s Hz, af=%s)",
        input_path,
        output_path,
        sample_rate,
        af or "none",
    )
    try:
        subprocess.run(  # nosemgrep: python.lang.security.audit.dangerous-subprocess-use-audit
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        err = exc.stderr.decode("utf-8", errors="ignore") if exc.stderr else str(exc)
        raise RuntimeError(f"ffmpeg failed: {err}") from exc

    return os.path.abspath(output_path)
