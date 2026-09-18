# 微信小程序上架合规包 · zhixue-multimodal

> 更新：2026-09-13 · Wave **Z0**  
> **Gate**：本清单未全绿 → **禁止提审**。  
> 飞轮采集默认关闭；提审通过后再开可选反馈（见 [DATA_FLYWHEEL.md](DATA_FLYWHEEL.md)）。

## 上架顺序

1. Z0 合规清单全绿  
2. Z1 健全性验收（[ACCEPTANCE_MINIAPP.md](ACCEPTANCE_MINIAPP.md)）  
3. 微信公众平台提审  
4. （可选）打开学习反馈飞轮开关  

---

## Blocker 清单（工程必须处理）

| ID | 项 | 现状（2026-09-13） | 上架前动作 | 状态 |
|----|-----|-------------------|------------|------|
| **B1** | 后端 API **鉴权** | ✅ `POST /auth/login` · Bearer · 保护 upload/ask/写课程/建 job | 生产设 `AUTH_REQUIRED=true`、`AUTH_DEV_LOGIN=false` + 微信密钥 | **工程已落地**（生产配置待填） |
| **B2** | HTTPS **合法域名** | miniapp 支持 `VITE_API_BASE` / 本地 storage 覆盖；步骤见 [DEPLOY_HTTPS.md](DEPLOY_HTTPS.md) | 配置正式 HTTPS 域名；关 `urlCheck:false` | **BLOCKER**（运维） |
| **B3** | 隐私政策 / 用户协议 **可打开** | `pages/legal/*` + 设置页入口 | 法务替换正式文案 | 工程已铺页面 |
| **B4** | 账号注销入口 | ✅ `DELETE /auth/me` + 小程序设置页 | 联调验证 | **工程已落地** |
| **B5** | 密钥不进仓 | `.env` / `.env.example` | 勿提交微信 AppSecret | 持续 |
| **B6** | 上传限制 | ✅ content_type 白名单 + `size_bytes` / `upload_max_bytes` | 按产品调限额 | **工程已落地** |

---

## 合规检查表（提审材料）

### 1. 隐私与协议

- [ ] 隐私政策全文（收集目的、范围、存储、第三方 SDK、用户权利）
- [ ] 用户服务协议
- [ ] 小程序内「设置/关于」可打开上述页面（`pages/legal/privacy`、`pages/legal/terms`）
- [ ] 首次使用敏感能力前弹窗说明（若申请录音/相册）

### 2. 权限最小化

- [ ] `manifest.json` → `mp-weixin.permission` / `requiredPrivateInfos` **仅**声明实际使用项
- [ ] 当前骨架：`requiredPrivateInfos: []`、`permission: {}` —— 若后续录音/选文件，同步提审说明
- [ ] 拒绝权限后仍有可用降级路径（只读课程列表等）

### 3. 登录与身份

- [ ] 微信登录方案文档（code2session、session 有效期）
- [ ] 账号注销 / 删除个人学习数据
- [ ] 未登录态行为边界写清

### 4. 内容与未成年人

- [ ] 类目选「教育」及所需资质材料（负责人准备证照；工程只留清单）
- [ ] 课堂辅助场景说明；无医疗诊断/代考/作弊宣传
- [ ] 若有 UGC：审核或举报入口

### 5. 数据与第三方

- [ ] 教育数据存储地域与保留周期说明
- [ ] 日志脱敏（学号/手机号等）
- [ ] WhisperX / LLM / 对象存储：是否出境、数据处理协议
- [ ] 飞轮反馈：**默认关**；开启需同意开关

### 6. 安全

- [ ] 全站 HTTPS
- [ ] 无明文密钥
- [ ] 接口鉴权（B1）
- [ ] 上传大小/MIME 限制（B6）

---

## 类目与资质（负责人）

| 材料 | Owner | 备注 |
|------|-------|------|
| 主体营业执照 / 学校证明 | 负责人 | 按微信教育类目要求 |
| ICP / 域名 | 负责人 | 与合法域名一致 |
| 软著或其他（若要求） | 负责人 | 按审校反馈补 |

---

## 相关

- [ACCEPTANCE_MINIAPP.md](ACCEPTANCE_MINIAPP.md) · [DATA_FLYWHEEL.md](DATA_FLYWHEEL.md) · [miniapp/README.md](../miniapp/README.md)
