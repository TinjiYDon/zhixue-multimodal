# 智学多模态 - UniApp 小程序

学生端轻量入口：课程列表、课程问答。

## 技术栈

- **UniApp** (Vue 3 + Vite + TypeScript)
- **微信小程序** (mp-weixin)

## 快速开始

```bash
# 安装依赖
npm install

# 开发模式（微信小程序）
npm run dev:mp-weixin

# 构建
npm run build:mp-weixin
```

开发时，在微信开发者工具中导入 `dist/dev/mp-weixin` 目录。

## 项目结构

```
miniapp/
├── src/
│   ├── api/            # API 服务层
│   │   └── index.ts    # 后端接口封装
│   ├── pages/
│   │   ├── index/      # 课程列表页
│   │   └── course/     # 课程详情 + 问答页
│   ├── App.vue         # 应用入口
│   ├── main.ts         # 主入口
│   ├── manifest.json   # 应用配置
│   ├── pages.json      # 页面路由配置
│   └── uni.scss        # 全局样式变量
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## 后端接口对接

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 健康检查 | GET | `/health` | 检查后端状态 |
| 课程列表 | GET | `/api/v1/courses` | 获取所有课程 |
| 课程详情 | GET | `/api/v1/courses/{id}` | 获取单个课程 |
| 课程问答 | POST | `/api/v1/courses/{id}/ask` | RAG 问答 |

## 域名配置

开发时在微信开发者工具「详情 → 本地设置」中勾选「不校验合法域名」。

正式发布前需在小程序管理后台配置以下 request 合法域名：
https://your-api-domain.com

## 验收标准

- [x] UniApp 项目初始化完成
- [x] 微信开发者工具可预览
- [x] 对接 GET /api/v1/courses 课程列表
- [x] 对接课程问答 POST /api/v1/courses/{id}/ask
- [x] 能调通 health + courses
