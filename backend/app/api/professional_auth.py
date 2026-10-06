from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.professional_auth import (
    PROFESSIONAL_TOKEN_EXPIRE_SECONDS,
    create_professional_token,
    verify_password,
)
from app.core.rate_limit import professional_login_limiter
from app.db.session import get_db
from app.models.professional import Professional
from app.schemas.professional_auth import (
    ProfessionalLoginRequest,
    ProfessionalLoginResponse,
    ProfessionalMeResponse,
)
from app.core.professional_auth import require_professional


router = APIRouter(
    prefix="/api/professional/auth",
    tags=["professional-auth"],
)


@router.post(
    "/login",
    response_model=ProfessionalLoginResponse,
)
def professional_login(
    request: Request,
    data: ProfessionalLoginRequest,
    db: Session = Depends(get_db),
):
    client_ip = (
        request.client.host
        if request.client
        else "unknown"
    )

    if not professional_login_limiter.is_allowed(
        client_ip
    ):
        raise HTTPException(
            status_code=429,
            detail=(
                "Demasiados intentos de inicio de sesión. "
                "Intentá nuevamente más tarde."
            ),
        )

    phone = data.phone.strip()

    if not phone:
        raise HTTPException(
            status_code=400,
            detail="El teléfono es obligatorio.",
        )

    professional = db.scalar(
        select(Professional).where(
            Professional.phone == phone
        )
    )

    if professional is None:
        raise HTTPException(
            status_code=401,
            detail="Teléfono o contraseña incorrectos.",
        )

    if not professional.is_active:
        raise HTTPException(
            status_code=403,
            detail="La cuenta del profesional no está activa.",
        )

    if not professional.account_enabled:
        raise HTTPException(
            status_code=403,
            detail=(
                "La cuenta todavía no está habilitada "
                "para acceder al panel."
            ),
        )

    if not professional.password_hash:
        raise HTTPException(
            status_code=403,
            detail=(
                "La cuenta todavía no tiene una contraseña "
                "configurada."
            ),
        )

    if not verify_password(
        data.password,
        professional.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Teléfono o contraseña incorrectos.",
        )

    professional_login_limiter.reset(client_ip)

    token = create_professional_token(
        professional.id
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": PROFESSIONAL_TOKEN_EXPIRE_SECONDS,
    }


@router.get(
    "/me",
    response_model=ProfessionalMeResponse,
)
def professional_me(
    professional_id: int = Depends(
        require_professional
    ),
    db: Session = Depends(get_db),
):
    professional = db.get(
        Professional,
        professional_id,
    )

    if professional is None:
        raise HTTPException(
            status_code=404,
            detail="Professional not found",
        )

    return {
        "professional_id": professional.id,
        "first_name": professional.first_name,
        "last_name": professional.last_name,
    }