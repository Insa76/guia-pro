from pydantic import BaseModel, Field


class ProfessionalActivationResponse(BaseModel):
    valid: bool
    professional_id: int
    first_name: str
    last_name: str
    expires_at: str


class ProfessionalActivationRequest(BaseModel):
    token: str = Field(min_length=20, max_length=500)
    password: str = Field(min_length=8, max_length=200)


class ProfessionalActivationSuccessResponse(BaseModel):
    message: str
    professional_id: int