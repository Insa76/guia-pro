from pydantic import BaseModel


class ReviewTokenResponse(BaseModel):
    job_id: int
    review_token: str
    review_url: str


class ReviewTokenJobResponse(BaseModel):
    job_id: int
    professional_id: int
    professional_name: str
    job_title: str
    job_description: str | None
    completed_at: str | None
    already_reviewed: bool