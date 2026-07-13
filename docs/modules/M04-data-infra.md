# M04 · 基础设施（全员 · 已交付）

> **状态：已交付** — 无需专人维护。每人本地开发前执行一次即可。

## 用法

```powershell
# 仓库根目录
docker compose up -d
```

| 服务 | 端口（默认） | 用途 |
|------|--------------|------|
| PostgreSQL | 5435 | 课程、Job、RAG 数据（D / 负责人） |
| Redis | 6379 | 任务队列（D Worker） |
| MinIO | 9000 / 9001 | 媒体文件（负责人 upload） |

连接串见 `backend/.env.example`。

## 历史分工说明

- 原 **队友 D** 完成 compose 编排（#P0-1 ✅）
- 后续 D 主责转为 **M6 业务 API**（见 [M05-backend-jobs-api.md](M05-backend-jobs-api.md)）
- 若端口冲突，改环境变量 `ZHIXUE_PG_PORT` 等，**提 PR 需 @负责人**

## 验收（新人自检）

- [ ] `docker compose ps` 三个服务 healthy / running
- [ ] `curl http://localhost:8000/api/v1/health`（后端启动后）

Worker 与 Job API 见 M05，不在本文维护。
