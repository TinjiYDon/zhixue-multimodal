## Request changes · PR #1 多媒体（whq6830-arch）

@whq6830-arch 感谢已有 ffmpeg/WhisperX/OCR 实质代码。按负责人契约，**暂不合并**，请按下列项返工后 `@TinjiYDon`。

### 必须修改

1. **Schema**：复用 `backend/app/schemas/transcript.py`；OCR 对齐官方 `OcrPageResult`（不要自定义 `raw_text/blocks` 作为对外契约）
2. **依赖**：写入 `backend/requirements.txt`；删除仓库根目录误放的 `requirements.txt`
3. **清理**：删除可疑文件 `multimedia/4.6.1`；sample 媒体改到 `tests/fixtures/` 或文档外链（勿堆在 services 目录）
4. **测试**：至少 1 个 pytest（可 mock ffmpeg/whisper）；PR 描述补「如何验证」+ `Closes #4`
5. **签名**：与 Worker 契约对齐 `transcribe_media(job_id, media_key)`（见 M03 / M05）

### 验收

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest tests/ -q
```

关联：Issue #4 · BACKLOG `#P0-3`
