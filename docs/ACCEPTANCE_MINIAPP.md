# 小程序健全性验收 · zhixue-multimodal

> 更新：2026-09-13 · Wave **Z1**  
> **前置**： [WECHAT_COMPLIANCE.md](WECHAT_COMPLIANCE.md) Blocker B1–B4 关闭后才可标记本页「可提审」。

## 环境

```powershell
cd d:\project\zhixue-multimodal\miniapp
npm install
npm run dev:mp-weixin
# 用微信开发者工具打开 dist/dev/mp-weixin（路径以构建输出为准）
```

后端：`docker compose up -d` 后启动 FastAPI；开发期可勾选「不校验合法域名」。

---

## 验收清单

| # | 场景 | 期望 | 结果 |
|---|------|------|------|
| 1 | 冷启动进入课程列表 | 无白屏；有加载态 | |
| 2 | 后端可用 | 健康状态「正常」；课程列表可渲染或空态文案 | |
| 3 | 后端不可用 / 弱网 | 错误态 +「重试」；不崩溃 | |
| 4 | 进入课程详情 | 参数带 id；问答区有超时/失败提示（接真 API 后） | |
| 5 | 隐私政策入口 | 列表页底栏可进 `pages/legal/privacy` | |
| 6 | 用户协议入口 | 列表页底栏可进 `pages/legal/terms` | |
| 7 | 权限拒绝（若申请录音/相册） | 有说明；核心浏览仍可用 | |
| 8 | 登出 / 注销 | 设置页可退出；注销调 `DELETE /auth/me` | |
| 9 | ASR/转写失败降级 | 友好提示或 fixture 说明，不裸堆栈 | |
| 10 | 上传超限/类型错误 | 明确错误码与文案（400 detail） | |
| 11 | 未登录提问 | ask 返回 401；登录后可问 | |
| 12 | 请求超时 | 15s 超时提示「请求超时…」 | |

## 观测（健全性）

- [ ] 关键 API 错误码统一（4xx/5xx → 可读 `detail`）
- [ ] 请求超时（建议 ≤15s）有提示
- [ ] 可选：合规同意后的埋点（默认关，见 DATA_FLYWHEEL）

## 可提审判定

- [ ] WECHAT_COMPLIANCE Blocker 全绿  
- [ ] 本表 1–7、9–10 通过  
- [ ] 8 在鉴权方案合并后通过  
- [ ] `BASE_URL` 已切 HTTPS 正式域  

Owner 签字：________  日期：________
