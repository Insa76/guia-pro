from pydantic import BaseModel, Field


class PublicProfessionalRegistration(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)

    phone: str = Field(min_length=6, max_length=30)
    whatsapp: str | None = Field(default=None, max_length=30)

    description: str | None = Field(default=None, max_length=2000)

    years_experience: int | None = Field(
        default=None,
        ge=0,
        le=80,
    )

    instagram: str | None = Field(
        default=None,
        max_length=150,
    )

    category_id: int
    location_id: int


class PublicProfessionalRegistrationResponse(BaseModel):
    id: int
    first_name: str
    last_name: str

    message: str