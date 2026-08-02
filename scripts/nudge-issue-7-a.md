## 跟进 · A（RynnYuan）· PR #9 合并后 API 对接

@RynnYuan PR #9（课程页 UI）已按计划合并，辛苦！

### 下一刀（人读）

| 项 | 内容 |
|----|------|
| 已完成 | P0-6 UI：列表 / timeline mock / PPT / 问答面板 |
| 待做 | 接真实 API；修正 ask 路径 |
| 契约 | `GET /api/v1/courses` · `GET /api/v1/courses/{id}/timeline`（负责人本轮占位）· `POST /api/v1/courses/{id}/ask` |

### Agent 上下文

```text
扩展 web/src/api/client.ts
不要使用 POST /api/v1/ask（错误路径）
CourseView 使用路由 :id
mock 可保留为 fallback
关联 Issue #7
```

有问题开子评论即可。
