from pydantic import BaseModel


class ProfessionalReputationResponse(BaseModel):
    average_rating: float
    total_reviews: int
    total_jobs: int
    rated_jobs: int