from typing import Literal

from pydantic import BaseModel, Field

TimelineDataSource = Literal["asr", "fixture", "placeholder", "failed"]


class TimelineCue(BaseModel):
    """One subtitle/segment cue on the course timeline."""

    t_start: float = Field(..., ge=0, description="seconds")
    t_end: float = Field(..., ge=0, description="seconds")
    text: str = ""


class TimelineSlide(BaseModel):
    """PPT/slide anchor aligned to time."""

    page: int = Field(..., ge=1)
    t_start: float = Field(..., ge=0)
    title: str = ""
    image_url: str | None = None


class TimelineResponse(BaseModel):
    course_id: str
    status: str = Field(
        ...,
        description="ok | placeholder | failed — failed means job 未产出可用字幕",
    )
    duration_sec: float = 0
    cues: list[TimelineCue] = Field(default_factory=list)
    slides: list[TimelineSlide] = Field(default_factory=list)
    message: str | None = None
    data_source: TimelineDataSource | None = Field(
        default=None,
        description="asr=真实转写 · fixture=演示夹具 · placeholder=无 job · failed=任务失败空轴",
    )
