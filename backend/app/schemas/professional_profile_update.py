from pydantic import BaseModel, Field


class ProfessionalProfileUpdate(BaseModel):
    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    years_experience: int | None = Field(
        default=None,
        ge=0,
        le=80,
    )

    whatsapp: str | None = Field(
        default=None,
        max_length=50,
    )

    instagram: str | None = Field(
        default=None,
        max_length=150,
    )

    category_ids: list[int] | None = None

    location_ids: list[int] | None = None