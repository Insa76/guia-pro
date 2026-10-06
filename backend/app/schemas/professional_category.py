from pydantic import BaseModel


class ProfessionalCategoryCreate(BaseModel):
    professional_id: int
    category_id: int


class ProfessionalCategoryResponse(BaseModel):
    professional_id: int
    category_id: int