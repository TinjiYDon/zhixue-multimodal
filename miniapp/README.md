# 小程序（UniApp）

与申报书一致，建议使用 **UniApp** 单独工程对接同一后端 `FastAPI`。

## 推荐初始化方式

在 `miniapp` 目录外或使用 HBuilderX：

```bash
# 官方 Vue3 + Vite 版模板（需已安装 Node）
npx degit dcloudio/uni-preset-vue#vite-ts zhixue-miniapp
```

将生成工程中的接口 **baseURL** 配置为后端地址（正式环境域名；本地调试可在开发者工具里勾选合法域名或使用局域网 IP）。

## 与本仓库后端的约定

- REST 前缀：`/api/v1`
- 认证：后续统一采用 Bearer Token（由后端 `deps.py` 扩展）
- 大文件上传：建议走 **预签名 URL**（MinIO/S3），小程序直传对象存储后回调后端写入元数据

## 目录说明

当前仅放置说明文档；真正的 UniApp 工程可用脚手架生成后放入 `miniapp/` 或与 `web/` 并列。
