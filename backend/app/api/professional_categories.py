from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.admin_auth import require_admin

from app.db.session import get_db
from app.schemas.professional_category import (
    ProfessionalCategoryCreate,
    ProfessionalCategoryResponse,
)
from app.services.professional_category_service import (
    create_professional_category,
    get_professional_categories,
)


router = APIRouter(
    prefix="/api/professional-categories",
    tags=["professional-categories"],
)


@router.post(
    "",
    response_model=ProfessionalCategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: ProfessionalCategoryCreate,
    db: Session = Depends(get_db),
    admin_authenticated: bool = Depends(require_admin)
):
    try:
        return create_professional_category(db, data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/professional/{professional_id}",
    response_model=list[ProfessionalCategoryResponse],
)
def list_for_professional(
    professional_id: int,
    db: Session = Depends(get_db),
    admin_authenticated: bool = Depends(require_admin),
):
    return get_professional_categories(
        db,
        professional_id,
    )