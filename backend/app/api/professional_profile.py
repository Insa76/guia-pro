from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.professional_auth import require_professional
from app.db.session import get_db
from app.schemas.professional_profile_update import ProfessionalProfileUpdate
from app.services.professional_profile_service import (
    update_professional_profile,
)


router = APIRouter(
    prefix="/api/professional/profile",
    tags=["professional-profile"],
)


@router.patch(
    "",
    status_code=status.HTTP_200_OK,
)
def update_my_profile(
    data: ProfessionalProfileUpdate,
    db: Session = Depends(get_db),
    professional_id: int = Depends(require_professional),
):
    try:
        return update_professional_profile(
            db,
            professional_id,
            data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )