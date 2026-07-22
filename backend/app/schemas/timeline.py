from pydantic import BaseModel, Field


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
        description="ok | placeholder — placeholder until jobs/multimedia write real cues",
    )
    duration_sec: float = 0
    cues: list[TimelineCue] = Field(default_factory=list)
    slides: list[TimelineSlide] = Field(default_factory=list)
    message: str | None = None
