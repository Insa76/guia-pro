
from datetime import datetime

from pydantic import BaseModel


class AdminVerificationListItem(BaseModel):
    verification_id: int
    professional_id: int

    first_name: str
    last_name: str
    phone: str
    whatsapp: str | None
    description: str | None
    years_experience: int | None
    instagram: str | None

    status: str
    method: str | None
    notes: str | None
    verified_at: datetime | None

