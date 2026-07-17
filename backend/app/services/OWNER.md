# 负责人 · 后端集成（M5）

- **职责**：upload、alignment、RAG/Agent、OpenAPI 审批、router 合并
- **入口**：`agent.py` `alignment.py` · `api/v1/endpoints/upload.py` · `api/v1/endpoints/ask.py`
- **不负责**：`course_service` PG、`jobs` API、Worker、Whisper（队友 D / C）

## 队友边界

| 模块 | 负责人 | D | C |
|------|--------|---|---|
| upload / ask | ✅ | | |
| courses/jobs API | 审批 | ✅ 实现 | |
| 转写算法 | | 调 C | ✅ 实现 |

→ [docs/TODO_OWNER.md](../../../docs/TODO_OWNER.md)
