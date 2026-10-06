from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.admin_auth import require_admin
from app.db.session import get_db

from app.schemas.professional import (
    ProfessionalCreate,
    ProfessionalResponse,
)

from app.schemas.professional_profile import (
    ProfessionalProfileResponse, 
)

from app.services.professional_service import (
    create_professional,
    get_professional,
    get_professional_profile,
    get_professionals,
    get_all_professionals,
)

from app.models.professional import Professional
from app.core.admin_auth import require_admin
from app.schemas.professional_profile_update import ProfessionalProfileUpdate
from app.services.professional_profile_service import (
    update_professional_profile,
)


router = APIRouter(
    prefix="/api/professionals",
    tags=["professionals"],
)


@router.post(
    "",
    response_model=ProfessionalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: ProfessionalCreate,
    db: Session = Depends(get_db),
    admin_authenticated: bool = Depends(require_admin),
):
    return create_professional(db, data)


@router.get(
    "",
    response_model=list[ProfessionalResponse],
)
def list_all(
    db: Session = Depends(get_db),
):
    return get_professionals(db)

@router.get("/admin/list", response_model=list[ProfessionalResponse])
def admin_list_all(
    db: Session = Depends(get_db),
    admin_authenticated: bool = Depends(require_admin),
):
    return get_all_professionals(db)

@router.patch(
    "/admin/{professional_id}",
    response_model=ProfessionalResponse,
)
def admin_update_professional(
    professional_id: int,
    data: ProfessionalProfileUpdate,
    db: Session = Depends(get_db),
    admin_authenticated: bool = Depends(require_admin),
):
    professional = get_professional(
        db,
        professional_id,
    )

    if professional is None:
        raise HTTPException(
            status_code=404,
            detail="Professional not found",
        )

    try:
        return update_professional_profile(
            db,
            professional_id,
            data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get(
    "/{professional_id}/profile",
    response_model=ProfessionalProfileResponse,
)
def get_profile(
    professional_id: int,
    db: Session = Depends(get_db),
):
    profile = get_professional_profile(
        db,
        professional_id,
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professional not found",
        )

    if not profile["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professional not found",
        )

    return profile



@router.patch(
    "/{professional_id}/status",
    response_model=ProfessionalResponse,
)
def update_status(
    professional_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
     admin_authenticated: bool = Depends(require_admin),
):
    professional = get_professional(
        db,
        professional_id,
    )

    if professional is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professional not found",
        )

    professional.is_active = is_active

    db.commit()
    db.refresh(professional)

    return professional