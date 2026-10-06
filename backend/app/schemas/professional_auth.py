from pydantic import BaseModel, Field


class ProfessionalLoginRequest(BaseModel):
    phone: str = Field(min_length=1, max_length=30)
    password: str = Field(min_length=1, max_length=200)


class ProfessionalLoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class ProfessionalMeResponse(BaseModel):
    professional_id: int