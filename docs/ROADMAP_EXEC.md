# 执行路线图 ROADMAP_EXEC（人机双可读）

> 更新：2026-07-25 · 无 ML train/val/test · Wave3 fixture timeline 并行

## 人读摘要

| Wave | 含义 | 状态 |
|------|------|------|
| ICU Wave1/2 | 见 decision/scheduling 仓 | 独立 |
| **Wave3（本仓）** | job→timeline fixture 钩子 | ✅ 骨架 |
| MILE-1 | D PG + C 转写 + Owner 真数据 | ⏳ 等队友 |

**本仓无监督训练集划分（N/A）。** 质量靠 schema + course_id 隔离。

## Agent 上下文

```text
Wave3：POST /api/v1/courses/{id}/timeline/from-fixture
存储：app/services/timeline_store.py（内存）
Worker failed/done 后会尝试 ingest fixture → timeline + RAG context
验收：pytest tests/test_timeline_fixture.py tests/ -q
真数据：C transcript.py + D PG；替换 fixture
禁止：答辩假装 placeholder 为真实转写；RAG 跨 course_id
文档：docs/DEMO_E2E.md
```

## 并行队友

- [ ] C：PR #1 按 schema 返工（#4）
- [ ] D：Course/Job PG（#5）
- [ ] A：接 timeline/ask（#7）
- [ ] B：小程序（#8）
