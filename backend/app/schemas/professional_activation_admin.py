from pydantic import BaseModel


class ProfessionalActivationAdminResponse(BaseModel):
    professional_id: int
    first_name: str
    last_name: str
    activation_token: str
    activation_url: str
    expires_at: str