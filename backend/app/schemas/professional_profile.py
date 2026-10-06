from pydantic import BaseModel


class ProfessionalProfileCategory(BaseModel):
    id: int
    name: str
    slug: str


class ProfessionalProfileLocation(BaseModel):
    id: int
    name: str
    locality: str
    province: str


class ProfessionalProfileReputation(BaseModel):
    average_rating: float
    total_reviews: int
    total_jobs: int
    rated_jobs: int


class ProfessionalProfileResponse(BaseModel):
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

    reputation: ProfessionalProfileReputation

    categories: list[ProfessionalProfileCategory]
    locations: list[ProfessionalProfileLocation]