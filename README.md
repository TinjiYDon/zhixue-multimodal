# 智学多模态 Agent · 工程骨架

申报书对应技术栈：**FastAPI（后端）** + **Vue（Web）** + **UniApp（小程序）**；异步任务与对象存储通过 Docker 编排拉起。

## 目录结构

```
code/
├── backend/          # FastAPI：API、领域服务、异步任务入口（占位）
├── web/              # Vue 3 + Vite：师生 Web 端
├── miniapp/          # 小程序：见 README，建议用官方脚手架初始化
├── docker-compose.yml
└── README.md
```

## 本地启动

### 1. 依赖服务（可选）

```bash
cd code
docker compose up -d
```

### 2. 后端

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate   # Windows
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

OpenAPI：`http://localhost:8000/docs`

若 `pip install` **超时**，可临时换镜像（示例）：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`。若遇 **ResolutionImpossible**，请先升级 pip：`python -m pip install -U pip`，仍失败请将完整报错贴出。

### 3. Web

```bash
cd web
npm install
npm run dev
```

默认代理 `/api` → `http://localhost:8000`（见 `web/vite.config.ts`）。

### 4. 小程序

见 `miniapp/README.md`。

## 后续接入点（与申报书模块对应）

| 模块 | 建议落位 |
|------|----------|
| ASR（WhisperX 等） | `backend/app/services/transcription.py` + worker |
| 多模态对齐 | `backend/app/services/alignment.py` |
| Agent / LLM | `backend/app/services/agent.py` |
| 权限师生双端 | `backend/app/api/deps.py` + JWT/OAuth2 扩展 |
