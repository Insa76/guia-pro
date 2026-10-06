from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.professional_activation import (
    ProfessionalActivationRequest,
    ProfessionalActivationResponse,
    ProfessionalActivationSuccessResponse,
)
from app.services.professional_activation_service import (
    activate_professional_account,
    validate_activation_token,
)


router = APIRouter(
    prefix="/api/professional/activation",
    tags=["professional-activation"],
)


@router.get(
    "/validate",
    response_model=ProfessionalActivationResponse,
)
def validate_activation(
    token: str,
    db: Session = Depends(get_db),
):
    professional = validate_activation_token(db, token)

    if professional is None:
        raise HTTPException(
            status_code=400,
            detail="El enlace de activación no es válido o ya venció.",
        )

    return {
        "valid": True,
        "professional_id": professional.id,
        "first_name": professional.first_name,
        "last_name": professional.last_name,
        "expires_at": professional.activation_token_expires_at.isoformat(),
    }


@router.post(
    "/activate",
    response_model=ProfessionalActivationSuccessResponse,
)
def activate_account(
    data: ProfessionalActivationRequest,
    db: Session = Depends(get_db),
):
    try:
        professional = activate_professional_account(
            db,
            data.token,
            data.password,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return {
        "message": "Cuenta activada correctamente.",
        "professional_id": professional.id,
    }