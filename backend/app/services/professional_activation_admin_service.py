from app.services.professional_activation_service import create_activation_token
from sqlalchemy.orm import Session


def generate_professional_activation(
    db: Session,
    verification_id: int,
    activation_base_url: str,
):
    professional, token, expires_at = create_activation_token(
        db,
        verification_id,
    )

    activation_url = (
        f"{activation_base_url}?token={token}"
    )

    return {
        "professional_id": professional.id,
        "first_name": professional.first_name,
        "last_name": professional.last_name,
        "activation_token": token,
        "activation_url": activation_url,
        "expires_at": expires_at.isoformat(),
    }