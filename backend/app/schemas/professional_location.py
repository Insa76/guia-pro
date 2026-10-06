from pydantic import BaseModel


class ProfessionalLocationCreate(BaseModel):
    professional_id: int
    location_id: int


class ProfessionalLocationResponse(BaseModel):
    professional_id: int
    location_id: int