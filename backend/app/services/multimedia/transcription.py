"""ASR pipeline — 队友 C 实现 (WhisperX + worker).

TODO:
- 从 MinIO 拉取媒体
- FFmpeg 抽音频
- WhisperX 转写 + 时间戳
- 写入 PostgreSQL / 对象存储
"""


async def transcribe_media(job_id: str) -> dict:
    raise NotImplementedError("队友 C · multimedia/transcription.py")
