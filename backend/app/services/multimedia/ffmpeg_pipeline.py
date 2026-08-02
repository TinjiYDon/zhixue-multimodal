"""FFmpeg helpers — extract 16 kHz mono WAV for ASR."""

from __future__ import annotations

import logging
import os
import subprocess

logger = logging.getLogger(__name__)


def extract_audio(input_path: str, output_path: str, sample_rate: int = 16000) -> str:
    """Extract mono PCM WAV at ``sample_rate`` using system ``ffmpeg``."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"input media not found: {input_path}")

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        str(sample_rate),
        "-ac",
        "1",
        output_path,
    ]
    logger.info("extract_audio: %s -> %s (%s Hz)", input_path, output_path, sample_rate)
    try:
        subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        err = exc.stderr.decode("utf-8", errors="ignore") if exc.stderr else str(exc)
        raise RuntimeError(f"ffmpeg failed: {err}") from exc

    return os.path.abspath(output_path)
