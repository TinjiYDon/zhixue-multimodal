from pydantic import BaseModel, Field


class UploadPresignRequest(BaseModel):
    course_id: str = Field(..., min_length=1)
    filename: str = Field(..., min_length=1, max_length=255)
    content_type: str = Field(default="application/octet-stream", max_length=128)


class UploadPresignResponse(BaseModel):
    media_key: str
    upload_url: str
    bucket: str
    expires_in: int = 3600
    content_type: str = "application/octet-stream"


class UploadCompleteRequest(BaseModel):
    course_id: str = Field(..., min_length=1)
    media_key: str = Field(..., min_length=1)


class UploadCompleteResponse(BaseModel):
    course_id: str
    media_key: str
    job_id: str | None = None
    message: str | None = None
