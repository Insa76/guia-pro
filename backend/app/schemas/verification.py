from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class VerificationCreate(BaseModel):
    professional_id: int
    method: str = Field(min_length=2, max_length=50)
    notes: str | None = Field(default=None, max_length=2000)


class VerificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    professional_id: int
    status: str
    method: str | None
    notes: str | None
    verified_at: datetime | None