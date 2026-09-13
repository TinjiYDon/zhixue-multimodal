from pydantic import BaseModel, Field


class UploadPresignRequest(BaseModel):
    course_id: str = Field(..., min_length=1)
    filename: str = Field(..., min_length=1, max_length=255)
    content_type: str = Field(default="video/mp4", max_length=128)
    size_bytes: int | None = Field(
        default=None,
        ge=1,
        description="可选：客户端声明文件大小，用于服务端限额校验",
    )


class UploadPresignResponse(BaseModel):
    media_key: str
    upload_url: str
    bucket: str
    expires_in: int = 3600
    content_type: str = "video/mp4"
    max_bytes: int | None = None


class UploadCompleteRequest(BaseModel):
    course_id: str = Field(..., min_length=1)
    media_key: str = Field(..., min_length=1)


class UploadCompleteResponse(BaseModel):
    course_id: str
    media_key: str
    job_id: str | None = None
    message: str | None = None
