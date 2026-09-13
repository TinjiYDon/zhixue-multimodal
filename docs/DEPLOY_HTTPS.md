# 微信小程序 HTTPS / 合法域名部署清单 · zhixue-multimodal

> 更新：2026-09-13 · 对应 [WECHAT_COMPLIANCE.md](WECHAT_COMPLIANCE.md) **B2**  
> 本文件只解决**工程侧配置步骤**；ICP / 证书 / 备案仍由运维负责人完成。

## 目标状态

| 项 | 开发态 | 提审/生产态 |
|----|--------|-------------|
| API 基址 | `http://localhost:8000` 或内网 IP | `https://<正式域名>` |
| `VITE_API_BASE` | 可空（走默认） | 构建时注入正式 HTTPS |
| `urlCheck`（`manifest.json` / `project.config.json`） | `false` | **`true`** |
| 微信后台「request 合法域名」 | 可不配（勾选不校验） | 仅正式域名，无端口、无路径 |

## 微信后台需登记的域名能力

在「开发 → 开发管理 → 开发设置 → 服务器域名」配置同一 HTTPS 主机：

| 类型 | 用途 |
|------|------|
| request 合法域名 | `uni.request` / 上传 / ask / auth |
| uploadFile 合法域名 | 课件上传（若走微信上传通道） |
| downloadFile 合法域名 | 若小程序下载课件 |

**不要**把路径写进域名（错误：`https://api.example.com/api`；正确：`https://api.example.com`）。

## 后端路径白名单（调试/网关放行参考）

小程序会访问（均在 `VITE_API_BASE` 之下）：

- `GET /health`（探活；**勿删除**，与 nightly #15 冲突原因）
- `POST /api/v1/auth/login` · `POST /api/v1/auth/logout` · `GET|DELETE /api/v1/auth/me`
- `POST /api/v1/upload` · ask / courses / jobs 写接口（需 Bearer）

TLS 终止可在 Nginx / Caddy / 云负载均衡；上游可仍为内网 HTTP。

## 构建与验收命令

```powershell
# 1) 设置正式基址后构建小程序
cd d:\project\zhixue-multimodal\miniapp
$env:VITE_API_BASE = "https://your-api.example.com"
npm run build:mp-weixin

# 2) 将 urlCheck 改为 true 后再用微信开发者工具上传（提审前）
# 编辑 miniapp/src/manifest.json 与 miniapp/project.config.json

# 3) 探活
curl.exe -fsS https://your-api.example.com/health
```

## 关闭 B2 的验收标准

- [ ] 正式域 HTTPS 证书有效（无自签）
- [ ] 微信后台合法域名已填且与 `VITE_API_BASE` 主机一致
- [ ] `urlCheck: true` 下首页能登录 / 探活成功
- [ ] 本机不再依赖「不校验合法域名」勾选

未全勾前：**禁止**在 [ACCEPTANCE_MINIAPP.md](ACCEPTANCE_MINIAPP.md) 标记可提审。
