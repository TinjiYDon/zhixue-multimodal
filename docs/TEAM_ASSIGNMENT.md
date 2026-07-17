# 五人分工总表（全员必读）

> **新人从这里开始** → 找到自己的角色 → 读对应模块文档 → 在 [`BACKLOG.md`](BACKLOG.md) 领任务 → 按 [`CONTRIBUTING.md`](../CONTRIBUTING.md) 提 PR

| 文档 | 用途 |
|------|------|
| 本文 | 谁做什么、不做什么、第一步 |
| [COLLABORATION.md](COLLABORATION.md) | 联调顺序、契约、周会、排错 |
| [BACKLOG.md](BACKLOG.md) | 可勾选任务（#P0-x） |
| [OWNER_VS_TEAM.md](OWNER_VS_TEAM.md) | 各角色交付清单与答辩标准 |

---

## 一、架构与数据流

```
                    ┌─────────────────────────────────────┐
                    │  负责人：upload / alignment / RAG   │
                    │  OpenAPI 审批 · router 合并         │
                    └──────────────┬──────────────────────┘
                                   │
     web (A) ──────┐               │ REST /docs
     miniapp (B) ──┼──► FastAPI ◄──┤
                    │               │
                    │    ┌──────────┴──────────┐
                    │    │  D：courses / jobs  │
                    │    │  PG 持久化 · Worker  │
                    │    └──────────┬──────────┘
                    │               │ 调用
                    └──► C：FFmpeg · WhisperX · OCR
```

**基础设施（全员自理，无专岗）：** 根目录 `docker compose up -d` → PG / Redis / MinIO

---

## 二、成员 × 模块 × 目录

> **Collaborators 列表顺序 = 角色顺序**：小程序 → 前端 → 多媒体 → 后端接口

| 成员 | GitHub | 角色 | 模块 |
|------|--------|------|------|
| **负责人** | `TinjiYDon` | 集成 + upload + RAG | M5 |
| **oceancat91** | `oceancat91` | **小程序** B | M2 · `#P0-7` |
| **RynnYuan** | `RynnYuan` | **前端** A | M1 · `#P0-6` |
| **whq6830-arch** | `whq6830-arch` | **多媒体** C | M3 · `#P0-3` |
| **yucc280** | `yucc280` | **后端接口** D | M6 · `#P0-4` |

| 角色 | 目录/文件 | 不要改 |
|------|-----------|--------|
| 负责人 | `upload.py` `agent.py` `alignment.py` | — |
| B · oceancat91 | `miniapp/` | 后端 |
| A · RynnYuan | `web/` | 后端 |
| C · whq6830-arch | `backend/app/services/multimedia/` | agent/alignment |
| D · yucc280 | `jobs.py` `job_service.py` `course_service.py` `workers/` | upload/RAG |
| 全员 | `docker compose up -d` | 非必要不改 compose |

| 模块 | 说明 | 文档 |
|------|------|------|
| M1 | Vue 时间轴 / PPT / 问答 UI | [M01-frontend-vue.md](modules/M01-frontend-vue.md) |
| M2 | UniApp 列表 / 问答 | [M02-miniapp.md](modules/M02-miniapp.md) |
| M3 | 音视频转写 + OCR | [M03-multimedia.md](modules/M03-multimedia.md) |
| M4 | Docker 依赖（**已交付**） | [M04-data-infra.md](modules/M04-data-infra.md) |
| M5 | 上传 + 对齐 + RAG | [TODO_OWNER.md](TODO_OWNER.md) |
| M6 | Job API + Worker + Course PG | [M05-backend-jobs-api.md](modules/M05-backend-jobs-api.md) |
| M7 | OpenAPI 契约 | [adr/001-api-contract-first.md](adr/001-api-contract-first.md) |

---

## 三、各成员：第一步做什么

### 负责人

1. `docker compose up -d`
2. ~~实现 `#P0-2` upload API~~ ✅ 已完成（presign + complete）
3. 与 D 对齐：`upload/complete` → `POST /jobs` 联调
4. 审批 D/C 的 API schema PR；等 C/D 交付后完成 pgvector RAG

→ 待办：[TODO_OWNER.md](TODO_OWNER.md)

### 队友 A（Web）

1. `cd web && npm install && npm run dev`
2. 读 [M01](modules/M01-frontend-vue.md) · [web/TEAM_OWNER.md](../web/TEAM_OWNER.md)
3. 领 `#P0-6`：课程列表页（调 `GET /api/v1/courses`）
4. API 以 `http://localhost:8000/docs` 为准，变更等负责人通知

### 队友 B（小程序）

1. 读 [M02](modules/M02-miniapp.md) · [miniapp/TEAM_OWNER.md](../miniapp/TEAM_OWNER.md)
2. UniApp 官方脚手架初始化 `miniapp/`
3. 领 `#P0-7`：课程列表 + 简单问答入口
4. 配置域名白名单对接后端

### 队友 C（多媒体 / WhisperX）

1. 本机安装 **FFmpeg**
2. 读 [M03](modules/M03-multimedia.md) · `multimedia/OWNER.md`
3. 领 `#P0-3` → `#P0-3b`：sample.mp4 → 带时间戳 JSON
4. 输出对齐 `backend/app/schemas/transcript.py`（负责人已定义），再交给 D Worker 写库

**边界：** 你写算法函数，不写 REST 路由；Whisper/WhisperX 在本模块实现。

### 队友 D（后端 API + Job）

1. `docker compose up -d`（与全员相同，**不再维护 compose**）
2. 读 [M05-backend-jobs-api.md](modules/M05-backend-jobs-api.md) · `workers/OWNER.md`
3. 领 `#P0-2b` Course PostgreSQL → `#P0-4` Job API → `#P0-4b` Worker
4. Worker 内调用 C 的 `transcribe_media()`，**不自己实现 Whisper**

**边界：** 你是 **FastAPI 接口 + 任务状态**；upload / RAG / alignment 在负责人。

---

## 四、API 谁定义、谁实现

| API / 契约 | 定义（审批） | 实现 |
|------------|--------------|------|
| `/upload` | 负责人 | 负责人 |
| `/courses` CRUD | 负责人 + D | D（PG）；负责人 review |
| `/jobs` | 负责人 + D | D |
| `/ask` `/timeline` | 负责人 | 负责人 |
| 转写 JSON schema | 负责人确认 | C 产出，D Worker 入库 |
| Job 状态枚举 | D 提议 | D |

**变更流程：** GitHub Issue → 负责人更新 `/docs` 说明 → @ 相关成员 → 再写代码

---

## 五、联调顺序（整队）

```
1. 全员     docker compose up -d
2. D        Course PG + GET/POST courses、jobs API
3. 负责人   upload API（创建 media + 触发 job）
4. C        sample 转写 JSON 跑通
5. D        Worker 调 C，job pending → done
6. 负责人   alignment + RAG + /ask
7. A / B    前端 / 小程序对接
```

里程碑：[BACKLOG.md](BACKLOG.md) `#MILE-1`～`#MILE-4`

---

## 六、答辩最低标准（每人一条）

| 成员 | 最低交付 |
|------|----------|
| 负责人 | 上传 → 转写入库 → 对齐/问答 可 demo |
| A | Web 时间轴 + 调 `/ask` |
| B | 小程序课程列表 |
| C | 给定 mp4 → 带时间戳转写 JSON |
| D | POST/GET `/jobs` + Course 落 PG + Worker 可跑 |

---

## 七、常见问题

| 问题 | 答案 |
|------|------|
| D 还要管 Docker 吗？ | **不用**。compose 已写好，全员自己 `up -d`。 |
| Whisper 谁做？ | **C** 实现；D 的 Worker **调用** C。 |
| course_service 谁做？ | **D**（PG）；负责人不再写内存版扩展。 |
| 能改 agent.py 吗？ | **不能**（C/D/A/B 均禁止，开 issue）。 |
| push 被拒？ | 找负责人加 GitHub Collaborator **Write**，或 Fork + PR。 |

负责人详细待办：[TODO_OWNER.md](TODO_OWNER.md)
