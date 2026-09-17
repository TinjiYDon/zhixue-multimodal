# 方向同步（组员必读）· 2026-09-13

> Owner：`TinjiYDon` · 已合入：PR [#17](https://github.com/TinjiYDon/zhixue-multimodal/pull/17) → `main`  
> 请 `git pull origin main` 后阅读；小程序同学优先对齐合规 Gate。

## 人读摘要

| 项 | 内容 |
|----|------|
| 定位 | 课堂多模态 Agent；**不接入 ICU** |
| 本阶段主线 | 微信小程序 **上架合规 Z0** → 健全性 Z1 → 再提审 |
| 飞轮 | 学习反馈默认 **关闭**（见 [`DATA_FLYWHEEL.md`](DATA_FLYWHEEL.md)） |
| 本周请做 | Review `main`；B 联调鉴权；C 按 [VIDEO_OPTIMIZATION.md](VIDEO_OPTIMIZATION.md) 推进实测验收；运维推进 HTTPS（B2） |

## 角色提示

| 角色 | 请关注 |
|------|--------|
| B 小程序 | 设置页、token、隐私/协议页、探活 `/health`；勿删 health |
| A Web | 与 Bearer 鉴权联调；勿假定匿名可写 |
| D 后端 | `AUTH_*` 生产配置；保持 `/health` |
| C 多媒体 | 上传 MIME/大小限制；**视频实测 P0/P1** 见 [VIDEO_OPTIMIZATION.md](VIDEO_OPTIMIZATION.md) |
| 负责人 | B2 域名 / 类目资质 / 法务正文 |

分工总表仍以 [`TEAM_ASSIGNMENT.md`](TEAM_ASSIGNMENT.md) 为准。

## 已合入改动（请 Review）

- Bearer 会话鉴权 · 保护 upload / ask / 写接口  
- 上传 MIME + 大小限制  
- 小程序：timeout/token、设置页、隐私/协议页、`VITE_API_BASE`  
- [`WECHAT_COMPLIANCE.md`](WECHAT_COMPLIANCE.md) · [`DEPLOY_HTTPS.md`](DEPLOY_HTTPS.md) · [`ACCEPTANCE_MINIAPP.md`](ACCEPTANCE_MINIAPP.md)

## 合规进度（摘要）

| 方面 | 状态 |
|------|------|
| B1 鉴权 | 工程已落地（生产密钥/开关待配） |
| B2 HTTPS 合法域名 | **未完成（运维 Blocker）** |
| B3 隐私/协议页 | 工程已铺页；法务正文待替换 |
| B4 账号注销 | 工程已落地 |
| B5 密钥不进仓 | 持续遵守 |
| B6 上传限制 | 工程已落地 |
| 提审材料勾选表 §1–6 | 多数未勾完（资质、出境说明、正式协议等） |

详情见 [`WECHAT_COMPLIANCE.md`](WECHAT_COMPLIANCE.md)。**清单未全绿 → 禁止提审。**

## 验收命令

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest tests/test_auth.py -q
```

## Draft / 已关闭 PR（知情）

| PR | 状态 | 内容 | 建议 |
|----|------|------|------|
| [#14](https://github.com/TinjiYDon/zhixue-multimodal/pull/14) Draft | 开 | 删 web/miniapp 调试 log、空 scss、未用类型 | 低风险，可择机合 |
| [#16](https://github.com/TinjiYDon/zhixue-multimodal/pull/16) Draft | 开 | 删 `scripts/` 已发布 issue/邮件草稿 | 纯文档/脚本减法，可择机合 |
| [#15](https://github.com/TinjiYDon/zhixue-multimodal/pull/15) | **已关闭** | 夜间清理：删根 `/health`、动 `deps.py` | **不要合**；与鉴权/探活冲突 |

## Agent 上下文

```text
SSOT: docs/TEAM_ASSIGNMENT.md · docs/TEAM_DIRECTION.md · docs/WECHAT_COMPLIANCE.md
禁区: 勿删 /health；勿提交 AppSecret；飞轮默认关
Issue: #6 #7 仍为功能向（timeline/RAG），合规优先于新功能扩面
```
