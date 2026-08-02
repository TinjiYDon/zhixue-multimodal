import logging
import os
import subprocess

logger = logging.getLogger(__name__)


def extract_audio(input_path: str, output_path: str, sample_rate: int = 16000) -> str:
    """Extract audio stream from media file using ffmpeg."""
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
        str(output_path),
    ]

    logger.info("extract_audio: %s -> %s (%s Hz)", input_path, output_path, sample_rate)

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
