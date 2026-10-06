from pydantic import BaseModel, ConfigDict, Field


class ProfessionalCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=6, max_length=30)
    whatsapp: str | None = Field(default=None, max_length=30)
    description: str | None = Field(default=None, max_length=2000)
    years_experience: int | None = Field(default=None, ge=0, le=100)
    instagram: str | None = Field(default=None, max_length=150)


class ProfessionalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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