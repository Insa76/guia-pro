from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.admin_auth import require_admin

from app.db.session import get_db
from app.schemas.professional_location import (
    ProfessionalLocationCreate,
    ProfessionalLocationResponse,
)
from app.services.professional_location_service import (
    create_professional_location,
    get_professional_locations,
)


router = APIRouter(
    prefix="/api/professional-locations",
    tags=["professional-locations"],
)


@router.post(
    "",
    response_model=ProfessionalLocationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: ProfessionalLocationCreate,
    db: Session = Depends(get_db),
    admin_authenticated: bool = Depends(require_admin),
):
    try:
        return create_professional_location(db, data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/professional/{professional_id}",
    response_model=list[ProfessionalLocationResponse],
)
def list_for_professional(
    professional_id: int,
    db: Session = Depends(get_db),
    admin_authenticated: bool = Depends(require_admin),
):
    return get_professional_locations(
        db,
        professional_id,
    )