# 成员 D · 业务 API + 任务域

- **职责**：Job/Course REST API、PostgreSQL 持久化、Redis Worker（**后端接口向**）
- **入口**：`backend/app/api/v1/endpoints/jobs.py` · `services/job_service.py` · `course_service.py` · `workers/tasks.py`
- **文档**：`docs/modules/M05-backend-jobs-api.md`
- **不再主责**：`docker-compose.yml`（#P0-1 已交付，compose 保留在仓库）

## 与负责人边界

| D | 负责人 |
|---|--------|
| `/jobs` CRUD、Course PG | `/upload` 预签名、alignment、RAG |
| Worker 调 C 的转写 | OpenAPI 字段最终审批 |
| 提 PR 注册 router | merge + 联调编排 |
