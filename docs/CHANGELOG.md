# Changelog · zhixue-multimodal

> 更新：2026-08-14  
> 人读：本仓 PR / Release。  
> AI：仅本仓；upload 默认样例 `video/mp4`；无登录体系。

## Agent 上下文

```text
repo: zhixue-multimodal
release: zhixue-mile2
open_issues: #6 #7
open_pr: #13 multimedia_new
upload_default: video/mp4 (no MIME whitelist in API)
auth: none
```

## [Unreleased]

- **鉴权骨架（Z0）**：`/api/v1/auth/login|logout|me` · Bearer 保护 upload/ask/写接口；`DELETE /auth/me` 注销。
- **上传限制（B6）**：content_type 白名单 + `size_bytes` / `UPLOAD_MAX_BYTES`。
- 小程序：统一超时/错误、token、设置页（登录/注销/飞轮开关）、`VITE_API_BASE`。
- 微信上架合规文档更新 Blocker 状态；健全性见 `ACCEPTANCE_MINIAPP.md`。
- Open PR [#13](https://github.com/TinjiYDon/zhixue-multimodal/pull/13)（`multimedia_new`）。
- Open Issues [#6](https://github.com/TinjiYDon/zhixue-multimodal/issues/6)、[#7](https://github.com/TinjiYDon/zhixue-multimodal/issues/7)。

## 2026-07 / 08

- **Merged** [#12](https://github.com/TinjiYDon/zhixue-multimodal/pull/12)：ASR/OCR schema + fixture。
- **Merged** [#11](https://github.com/TinjiYDon/zhixue-multimodal/pull/11)：UniApp miniapp P0。
- **Merged** [#9](https://github.com/TinjiYDon/zhixue-multimodal/pull/9)：Web 课程页 timeline/PPT/QA。
- main：Course/Job PostgreSQL（MILE-1）；Web 接 timeline/ask（MILE-2 骨架）。
- Release：[zhixue-mile2](https://github.com/TinjiYDon/zhixue-multimodal/releases/tag/zhixue-mile2)。

## 相关

| 文档 | 用途 |
|------|------|
| [PROGRESS.md](PROGRESS.md) | 里程碑 |
| [ROADMAP.md](ROADMAP.md) | 下一版本 |
| [ACCEPTANCE_ZHIXUE.md](ACCEPTANCE_ZHIXUE.md) | 人工验收 |
| [ROADMAP_EXEC.md](ROADMAP_EXEC.md) | MILE 执行记录 |
