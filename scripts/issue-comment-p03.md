## 转写 schema 已发布

负责人已在 main 定义输出契约，请按此实现 #P0-3 / #P0-3b / #P0-3c：

- 文件：`backend/app/schemas/transcript.py`
- ASR：`TranscriptResult` + `TranscriptSegment`（`text`, `start`, `end`, `speaker?`）
- OCR：`OcrResult` + `OcrPageResult` + `OcrBlock`

PR #1 未合并（仅注释无实现），请重做后 `Closes #4`。

文档：`docs/modules/M03-multimedia.md`
