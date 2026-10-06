
from pydantic import BaseModel, Field


class PublicReviewCreate(BaseModel):
    rating: int = Field(
        ge=1,
        le=5,
    )

    comment: str | None = Field(
        default=None,
        max_length=2000,
    )


class PublicReviewResponse(BaseModel):
    id: int
    job_id: int
    professional_id: int
    rating: int
    comment: str | None


class PublicReviewContext(BaseModel):
    job_id: int
    professional_id: int
    first_name: str
    last_name: str
    title: str
    already_reviewed: bool
