## 合入说明 · D `course-job-zyc` → main

@yucc280 已整理合入 Job API + Course CRUD + Worker 骨架（分支无正式 PR 时由负责人代开）。

### 人读摘要

| 项 | 内容 |
|----|------|
| Owner | D · yucc280 |
| 已合 | POST/GET `/jobs` · Course GET/PATCH/DELETE · Worker |
| 加固 | 保留 timeline · upload→job · pytest |
| 仍待 | **PostgreSQL** 持久化 + 正式队列 |

### Agent 上下文

```text
路径：backend/app/api/v1/endpoints/jobs.py · services/job_service.py · workers/tasks.py
验收：cd backend && .venv\Scripts\python.exe -m pytest tests/ -q
注意：C 未实现时 job.status 可能为 failed（预期）
下一刀：#P0-2b / #P0-4c 落 PG
```
