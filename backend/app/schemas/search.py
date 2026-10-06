from pydantic import BaseModel


class ProfessionalSearchResult(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str
    whatsapp: str | None
    description: str | None
    years_experience: int | None
    instagram: str | None
    is_active: bool
    identity_verified: bool

    category_id: int
    category_name: str
    category_slug: str

    location_id: int
    location_name: str
    locality: str
    province: str

    average_rating: float
    total_reviews: int
    total_jobs: int
    rated_jobs: int