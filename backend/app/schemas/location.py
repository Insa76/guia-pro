from pydantic import BaseModel, ConfigDict, Field


class LocationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    locality: str = Field(
        default="Resistencia",
        min_length=2,
        max_length=120,
    )
    province: str = Field(
        default="Chaco",
        min_length=2,
        max_length=120,
    )


class LocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    locality: str
    province: str
    is_active: bool