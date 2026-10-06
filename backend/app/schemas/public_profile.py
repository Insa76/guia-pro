from pydantic import BaseModel


class PublicProfileCategory(BaseModel):
    id: int
    name: str
    slug: str


class PublicProfileLocation(BaseModel):
    id: int
    name: str
    locality: str
    province: str


class PublicProfileReview(BaseModel):
    id: int
    rating: int
    comment: str | None
    created_at: str


class PublicProfessionalProfile(BaseModel):
    id: int
    first_name: str
    last_name: str
    description: str | None
    years_experience: int | None

    whatsapp: str | None
    instagram: str | None

    identity_verified: bool

    average_rating: float
    total_reviews: int
    total_jobs: int
    rated_jobs: int

    categories: list[PublicProfileCategory]
    locations: list[PublicProfileLocation]
    reviews: list[PublicProfileReview]