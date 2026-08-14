# 验收报告 · zhixue-multimodal

> 日期：2026-08-14  
> 环境：Windows · Docker Desktop · PG `5435` / Redis / MinIO  
> 后端：`127.0.0.1:8000` · 前端：`127.0.0.1:5173`  
> 截图：[acceptance-screens/](acceptance-screens/)

## Agent 上下文

```text
repo: zhixue-multimodal
acceptance_date: 2026-08-14
result: conditional_pass
pytest: 14 passed
auth: none (no login/logout)
smoke: health -> courses -> timeline -> from-fixture -> ask -> home
screenshots: docs/acceptance-screens/01-home.png, 02-course.png
```

## 总评

| 项 | 结果 |
|----|------|
| 总体 | **有条件通过**（核心链路可用；无登录；UI 小瑕疵） |
| 依赖 / 迁移 | 通过（`docker compose up -d`；启动 `create_all`） |
| 后端 / 前端启动 | 通过 |
| 视觉验收 | 通过（见备注） |
| 冒烟 | 通过（见替代链路） |
| pytest | **14 passed** |

## 环境与启动

| 步骤 | 动作 | 结果 |
|------|------|------|
| Docker | `docker compose up -d` | PG / Redis / MinIO Up |
| 环境变量 | `DATABASE_URL=postgresql+asyncpg://zhixue:zhixue_dev@localhost:5435/zhixue` | 与 `.env` 一致 |
| Schema | 启动时 `init_db` / `create_all` | courses / jobs 就绪 |
| 后端 | `uvicorn app.main:app --port 8000` | startup complete |
| 前端 | `npm run dev -- --port 5173` | Vite ready；`/api` 代理 8000 |
| 测试 | `pytest tests/ -q` | 14 passed |

## 冒烟链路

本项目 **无登录 / 退出**。冒烟定义为：

**首页健康检查 → 课程列表 → 进入课程 → timeline / fixture → ask → 回首页**

| 检查项 | 结果 | 备注 |
|--------|------|------|
| `GET /api/v1/health` | 通过 | `status=ok` |
| `GET /api/v1/courses` | 通过 | 含 `pg-smoke` |
| `GET .../timeline` | 通过 | placeholder 或 fixture |
| `POST .../timeline/from-fixture` | 通过 | `status=ok` |
| `POST .../ask` | 通过 | 占位 RAG + sources |
| Vite 代理 health | 通过 | |
| 登录 / 退出 | 不适用 | 无 auth |

## 视觉验收

| 截图 | 内容 |
|------|------|
| [01-home.png](acceptance-screens/01-home.png) | 健康检查 ok + 课程卡片 |
| [02-course.png](acceptance-screens/02-course.png) | 详情：字幕 / 时间轴 / PPT / 问答；`timeline=ok` |

| 项 | 通过/失败 | 说明 |
|----|-----------|------|
| 首页与课程数据 | 通过 | 真 API |
| 课程详情双栏 | 通过 | 视频区为模拟占位 |
| 时间轴中文 | 通过 | fixture |
| 首页「课程列表」标题重复 | **失败（轻微）** | UI 瑕疵 |
| 真实视频流 / 正式 RAG | 失败（预期） | 占位 |

## 日志摘要

- 后端无 Traceback / 5xx；上述 API 均为 200。
- 前端 Vite 启动无 error。

## 遗留

1. Issues #6 / #7 仍 open。  
2. PR #13 未审。  
3. 答辩勿声称账号登录链路。  
4. 建议修首页重复标题。

## 结论

**有条件通过。** 正式答辩前：修标题重复、对齐 #6/#7 验收标准、补一次 UI 内「提问」口播截图。
