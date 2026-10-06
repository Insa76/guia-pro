from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os

from app.db.session import get_db
from app.schemas.verification import VerificationResponse
from app.services.verification_admin_service import (
    update_verification_status,
)
from app.schemas.admin_verification import AdminVerificationListItem
from app.services.verification_admin_list_service import (
    list_pending_verifications,
)
from app.core.admin_auth import require_admin
from app.schemas.professional_activation_admin import (
    ProfessionalActivationAdminResponse,
)
from app.services.professional_activation_admin_service import (
    generate_professional_activation,
)



class VerificationStatusUpdate(BaseModel):
    status: str


router = APIRouter(
    prefix="/api/admin/verifications",
    tags=["admin-verifications"],
    dependencies=[Depends(require_admin)],
)

@router.get(
    "/pending",
    response_model=list[AdminVerificationListItem],
)
def list_pending_verifications_endpoint(
    db: Session = Depends(get_db),
):
    return list_pending_verifications(db)


@router.patch(
    "/{verification_id}",
    response_model=VerificationResponse,
)
def update_verification_endpoint(
    verification_id: int,
    data: VerificationStatusUpdate,
    db: Session = Depends(get_db),
):
    try:
        return update_verification_status(
            db,
            verification_id,
            data.status,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

@router.post(
    "/{verification_id}/activation",
    response_model=ProfessionalActivationAdminResponse,
)
def generate_activation_endpoint(
    verification_id: int,
    db: Session = Depends(get_db),
):
    activation_base_url = os.getenv(
        "PROFESSIONAL_ACTIVATION_URL",
        "http://localhost:5500/professional-activation.html",
    )

    try:
        return generate_professional_activation(
            db,
            verification_id,
            activation_base_url,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc    