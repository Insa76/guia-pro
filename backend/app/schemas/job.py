from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobCreate(BaseModel):
    professional_id: int | None = None
    title: str = Field(min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=2000)
    status: str = Field(default="completed", min_length=2, max_length=30)
    completed_at: datetime | None = None


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    professional_id: int
    title: str
    description: str | None
    status: str
    completed_at: datetime | None