from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.professional_auth import (
    PROFESSIONAL_TOKEN_EXPIRE_SECONDS,
    create_professional_token,
    verify_password,
    hash_password,
)
from app.core.rate_limit import professional_login_limiter
from app.db.session import get_db
from app.models.professional import Professional
from app.schemas.professional_auth import (
    ProfessionalLoginRequest,
    ProfessionalLoginResponse,
    ProfessionalMeResponse,
    ProfessionalRegisterRequest,
    ProfessionalRegisterResponse,
)
from app.core.professional_auth import require_professional
from app.models.category import Category
from app.models.location import Location
from app.models.professional_category import ProfessionalCategory
from app.models.professional_location import ProfessionalLocation


router = APIRouter(
    prefix="/api/professional/auth",
    tags=["professional-auth"],
)


@router.post(
    "/register",
    response_model=ProfessionalRegisterResponse,
)
def professional_register(
    data: ProfessionalRegisterRequest,
    db: Session = Depends(get_db),
):
    first_name = data.first_name.strip()
    last_name = data.last_name.strip()
    phone = data.phone.strip()

    if not first_name or not last_name or not phone:
        raise HTTPException(
            status_code=400,
            detail="Nombre, apellido y teléfono son obligatorios.",
        )

    existing_professional = db.scalar(
        select(Professional).where(
            Professional.phone == phone
        )
    )

    if existing_professional is not None:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un profesional registrado con ese teléfono.",
        )

    category = db.get(
        Category,
        data.category_id,
    )

    if category is None or not category.is_active:
        raise HTTPException(
            status_code=400,
            detail="El oficio seleccionado no es válido.",
        )

    location = db.get(
        Location,
        data.location_id,
    )

    if location is None or not location.is_active:
        raise HTTPException(
            status_code=400,
            detail="La localidad seleccionada no es válida.",
        )

    professional = Professional(
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        password_hash=hash_password(data.password),
        account_enabled=False,
        is_active=False,
        identity_verified=False,
    )

    db.add(professional)
    db.flush()

    professional_category = ProfessionalCategory(
        professional_id=professional.id,
        category_id=category.id,
    )

    professional_location = ProfessionalLocation(
        professional_id=professional.id,
        location_id=location.id,
    )

    db.add(professional_category)
    db.add(professional_location)

    db.commit()

    return {
        "message": (
            "Solicitud recibida. "
            "Tu perfil será revisado antes de ser activado."
        )
    }


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