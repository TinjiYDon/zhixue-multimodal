from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "zhixue-backend"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    database_url: str = "postgresql+asyncpg://zhixue:zhixue_dev@localhost:5435/zhixue"

    s3_endpoint: str = "http://localhost:9000"
    s3_access_key: str = "minio"
    s3_secret_key: str = "minio_dev_secret"
    s3_bucket: str = "zhixue-media"

    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # Auth / WeChat mini-program (Z0 ship gate)
    auth_required: bool = True
    auth_dev_login: bool = True  # local/CI；生产应 false 并配置微信密钥
    wechat_app_id: str = ""
    wechat_app_secret: str = ""
    session_ttl_seconds: int = 7 * 24 * 3600

    # Upload limits (B6)
    upload_max_bytes: int = 200 * 1024 * 1024  # 200 MiB
    upload_allowed_content_types: str = (
        "video/mp4,audio/mpeg,audio/wav,audio/x-wav,image/png,image/jpeg,application/pdf"
    )


settings = Settings()


def allowed_upload_content_types() -> set[str]:
    return {
        p.strip().lower()
        for p in settings.upload_allowed_content_types.split(",")
        if p.strip()
    }
