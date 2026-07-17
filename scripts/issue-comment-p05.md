## 进度更新（负责人 · main）

### 已完成（骨架）
- [x] `schemas/transcript.py` — 转写/OCR JSON 契约（C 须对齐）
- [x] `services/alignment.py` — `align_segments_to_pages()` 工具函数 + 占位 API
- [x] `services/agent.py` + `POST /api/v1/courses/{id}/ask` — RAG 占位

### 待完成（依赖 C/D）
- [ ] pgvector 索引 + LLM 正式 RAG
- [ ] 从 DB/MinIO 加载转写+OCR 后跑全链路对齐
- [ ] `#P0-5c` 全链路 demo 文档

### 阻塞
- C #4 转写 JSON · D #5 Worker 写库
