from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "zhixue-backend"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    database_url: str = "postgresql+asyncpg://zhixue:zhixue_dev@localhost:5435/zhixue"
    redis_url: str = "redis://localhost:6379/0"

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

    # Upload limits (B6) — 13min@720p≈189MiB 曾顶满 200MiB；默认放宽到 512MiB
    upload_max_bytes: int = 512 * 1024 * 1024
    upload_allowed_content_types: str = (
        "video/mp4,audio/mpeg,audio/wav,audio/x-wav,image/png,image/jpeg,application/pdf"
    )

    # MinIO / S3 timeouts（大文件下载与小请求分离，V-P0-4）
    s3_connect_timeout_seconds: float = 5.0
    s3_read_timeout_seconds: float = 120.0

    # ASR reproducibility (V-P0-1) — 评测/回归建议 ASR_REPRODUCIBLE=true 或 ASR_CPU_THREADS=1
    asr_reproducible: bool = False
    asr_cpu_threads: int = 0  # 0=库默认；>0 固定线程数；reproducible 时强制为 1

    # Job 失败时是否仍灌 fixture 时间轴（演示用）。生产/实测应 false（V-P0-3）
    timeline_fixture_on_job_fail: bool = False

    # V-P1 audio / ASR accuracy
    asr_audio_preprocess: bool = True  # highpass + loudnorm
    asr_highpass_hz: int = 80
    asr_loudnorm: bool = True
    asr_initial_prompt: str = (
        "数据库 关系模型 Ted Codd 指针 耦合度 增删改查 浏览器 模块 面向对象"
    )
    asr_model_short: str = "small"
    asr_model_long: str = "base"
    asr_long_threshold_sec: float = 480.0  # ≥8min 用 long 档
    asr_compression_ratio_warn: float = 2.35  # Whisper 默认重复阈附近
    asr_no_speech_prob_warn: float = 0.9


settings = Settings()


def allowed_upload_content_types() -> set[str]:
    return {
        p.strip().lower()
        for p in settings.upload_allowed_content_types.split(",")
        if p.strip()
    }
