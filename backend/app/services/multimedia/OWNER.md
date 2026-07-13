# 成员 C · 多媒体（WhisperX / OCR）

- **职责**：FFmpeg 抽音频、**WhisperX 转写**、PPT/板书 OCR
- **入口**：本目录 `ffmpeg_pipeline.py` `transcription.py` `ocr.py`
- **文档**：`docs/modules/M03-multimedia.md` · BACKLOG `#P0-3`
- **输出契约**：转写/OCR JSON → 对齐 `backend/app/schemas/transcript.py`（负责人已定义）

## 你不做

- REST API（`/jobs` 等）→ 队友 D
- upload / alignment / RAG → 负责人
- Docker 维护 → 全员自理 `docker compose up -d`

## 第一步

1. 安装 FFmpeg
2. 实现 `#P0-3b`：本地 sample.mp4 → 带 `{text, start, end}` 的 JSON
3. 提供可调用函数签名，供 D Worker 使用，例如 `async def transcribe_media(job_id: str) -> dict`
