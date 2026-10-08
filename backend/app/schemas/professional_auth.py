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


class ProfessionalRegisterRequest(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=1, max_length=30)
    password: str = Field(min_length=6, max_length=200)
    category_id: int
    location_id: int


class ProfessionalRegisterResponse(BaseModel):
    message: str