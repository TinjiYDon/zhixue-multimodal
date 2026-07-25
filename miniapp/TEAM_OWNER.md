# 队友负责 · UniApp 小程序

> 负责人：**队友 B** · 参考 `docs/modules/M02-miniapp.md`

## 当前状态

✅ UniApp (Vue 3 + TypeScript + Vite) 项目已初始化完成

### 已完成功能

- **P0-7**: UniApp 初始化 + 域名白名单配置
- **P0-7b**: 课程列表页 + 简单问答页

### 页面

| 页面 | 路径 | 对接接口 |
|------|------|----------|
| 课程列表 | `pages/index/index` | `GET /api/v1/courses` |
| 课程问答 | `pages/course/index` | `POST /api/v1/courses/{id}/ask` |

### 开发说明

```bash
npm install
npm run dev:mp-weixin
```

在微信开发者工具中导入 `dist/dev/mp-weixin` 目录即可预览。
