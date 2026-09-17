"""MinIO / S3 presigned upload helpers."""

from __future__ import annotations

import uuid
from datetime import timedelta
from functools import lru_cache
from urllib.parse import urlparse

import urllib3
from minio import Minio
from minio.error import S3Error

from app.core.config import settings


@lru_cache
def get_minio_client() -> Minio:
    parsed = urlparse(settings.s3_endpoint)
    endpoint = parsed.netloc or parsed.path
    secure = parsed.scheme == "https"
    # 读超时放宽，避免大对象瞬时卡顿导致整次失败（V-P0-4）
    timeout = urllib3.Timeout(
        connect=float(settings.s3_connect_timeout_seconds),
        read=float(settings.s3_read_timeout_seconds),
    )
    http_client = urllib3.PoolManager(timeout=timeout, retries=urllib3.Retry(total=2))
    return Minio(
        endpoint,
        access_key=settings.s3_access_key,
        secret_key=settings.s3_secret_key,
        secure=secure,
        http_client=http_client,
    )


def ensure_media_bucket() -> None:
    client = get_minio_client()
    if not client.bucket_exists(settings.s3_bucket):
        client.make_bucket(settings.s3_bucket)


def build_media_key(course_id: str, filename: str) -> str:
    suffix = filename.rsplit(".", 1)[-1].lower() if "." in filename else "bin"
    return f"courses/{course_id}/{uuid.uuid4().hex}.{suffix}"


def presign_put_object(
    media_key: str,
    expires_seconds: int = 3600,
    content_type: str = "application/octet-stream",
) -> str:
    ensure_media_bucket()
    client = get_minio_client()
    # Client must send the same Content-Type on PUT as echoed in presign response.
    return client.presigned_put_object(
        settings.s3_bucket,
        media_key,
        expires=timedelta(seconds=expires_seconds),
    )


def object_exists(media_key: str) -> bool:
    client = get_minio_client()
    try:
        client.stat_object(settings.s3_bucket, media_key)
        return True
    except S3Error:
        return False
    except Exception:
        return False
