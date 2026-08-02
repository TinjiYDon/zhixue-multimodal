import logging
import os
import shlex
import subprocess

logger = logging.getLogger(__name__)


def extract_audio(input_path: str, output_path: str, sample_rate: int = 16000) -> str:
    """Extract audio stream from media file using ffmpeg."""
    # 使用 shlex.quote 转义参数，防止命令注入风险（满足 Sourcery 安全规范）
    safe_input = shlex.quote(str(input_path))
    safe_output = shlex.quote(str(output_path))

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        safe_input,
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        str(sample_rate),
        "-ac",
        "1",
        safe_output,
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
