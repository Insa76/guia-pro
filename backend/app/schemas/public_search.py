from pydantic import BaseModel


class PublicProfessionalSearchResult(BaseModel):
    id: int
    first_name: str
    last_name: str
    description: str | None
    years_experience: int | None
    identity_verified: bool

    average_rating: float
    total_reviews: int
    total_jobs: int
    rated_jobs: int

    category_name: str
    category_slug: str

    location_name: str
    locality: str
    province: str