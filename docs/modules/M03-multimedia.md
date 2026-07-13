# M03 · 多媒体处理（队友 C）

## 目录

`backend/app/services/multimedia/`

| 文件 | 职责 |
|------|------|
| `ffmpeg_pipeline.py` | 抽音频、重采样 |
| `transcription.py` | WhisperX ASR |
| `ocr.py` | PPT/板书 OCR |

## 依赖

- FFmpeg 系统安装
- MinIO 对象路径由负责人 upload API 提供（`POST /api/v1/upload/presign`）

## 输出契约

实现结果须符合 `backend/app/schemas/transcript.py`：

- `TranscriptResult` / `TranscriptSegment` — ASR
- `OcrResult` / `OcrPageResult` — OCR

## 验收

- 单测或脚本：给定 sample.mp4 → 返回带时间戳 JSON
