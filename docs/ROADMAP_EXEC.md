# 执行路线图 ROADMAP_EXEC

> 更新：2026-08-02 · **MILE-1 Course/Job PG ✅** · S2（decision）暂缓

## 人读摘要

| Wave | 含义 | 状态 |
|------|------|------|
| Wave3 / MILE-3 | fixture timeline + miniapp | ✅ |
| P0-3 多媒体 | schema + ASR/OCR | ✅ PR #12 |
| **MILE-1** | Course/Job **PostgreSQL** | ✅ Owner 代合 |
| MILE-2 | Web 接真 timeline/ask | ⏳ A |

## Agent 上下文

```text
PG：docker compose up -d postgres · 端口 5435
DATABASE_URL=postgresql+asyncpg://zhixue:zhixue_dev@localhost:5435/zhixue
启动时 create_all；脚本：scripts/init_schema.sql
验收：cd backend && pytest tests/ -q（SQLite 内存）
真库冒烟：同上 DATABASE_URL 指向 5435
```
