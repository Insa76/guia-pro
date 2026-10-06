from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.rate_limit import public_registration_limiter
from app.db.session import get_db
from app.schemas.public_registration import (
    PublicProfessionalRegistration,
    PublicProfessionalRegistrationResponse,
)
from app.services.public_registration_service import (
    register_professional,
)


router = APIRouter(
    prefix="/api/public",
    tags=["public-registration"],
)


@router.post(
    "/professionals/register",
    response_model=PublicProfessionalRegistrationResponse,
)
def register_professional_endpoint(
    request: Request,
    data: PublicProfessionalRegistration,
    db: Session = Depends(get_db),
):
    client_ip = (
        request.client.host
        if request.client
        else "unknown"
    )

    if not public_registration_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail=(
                "Demasiados intentos de registro. "
                "Intentá nuevamente más tarde."
            ),
        )

    try:
        professional = register_professional(
            db=db,
            data=data,
        )

        public_registration_limiter.reset(client_ip)

        return PublicProfessionalRegistrationResponse(
            id=professional.id,
            first_name=professional.first_name,
            last_name=professional.last_name,
            message=(
                "Registro recibido. "
                "Tu perfil quedará pendiente de revisión."
            ),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )