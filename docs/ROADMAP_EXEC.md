# 执行路线图 ROADMAP_EXEC（人机双可读）

> 更新：2026-08-02 · PR #1 仍 OPEN + CHANGES_REQUESTED · **本轮不合** · Wave3/miniapp 已合 · 无 ML 划分

## 人读摘要

| Wave | 含义 | 状态 |
|------|------|------|
| ICU Wave1/2 | 见 decision/scheduling 仓 | 独立 |
| **Wave3（本仓）** | job→timeline fixture 钩子 | ✅ 骨架 |
| **MILE-3** | 小程序列表/问答骨架 | ✅ PR #11 |
| MILE-1 | D PG + C 转写 + Owner 真数据 | ⏳ 等队友（阻塞于 PR #1 返工） |

**本仓无监督训练集划分（N/A）。** 质量靠 schema + course_id 隔离。

## Agent 上下文

```text
Wave3：POST /api/v1/courses/{id}/timeline/from-fixture
miniapp：miniapp/（UniApp）· tip 含 3e5f03c
验收：pytest tests/ -q
真数据：C transcript + D PG；替换 fixture
禁止：答辩假装 placeholder 为真实转写；RAG 跨 course_id
文档：docs/DEMO_E2E.md
PR #1：继续不合直至 schema/依赖/样例/测试满足 request-changes
```

## 并行队友

- [ ] C：PR #1 按 schema 返工（#4）· **Owner 不 merge**
- [ ] D：Course/Job PG（#5）
- [ ] A：接 timeline/ask（#7 · `#P0-6d`）
- [x] B：小程序骨架（#8 / PR #11）· 接真 API 待 MILE-1
