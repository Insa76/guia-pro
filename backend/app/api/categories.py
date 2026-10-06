from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.admin_auth import require_admin

from app.db.session import get_db
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
)
from app.services.category_service import (
    create_category,
    get_categories,
    get_category,
)


router = APIRouter(
    prefix="/api/categories",
    tags=["categories"],
)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    admin_authenticated: bool = Depends(require_admin),
):
    return create_category(db, data)


@router.get(
    "",
    response_model=list[CategoryResponse],
)
def list_all(
    db: Session = Depends(get_db),
):
    return get_categories(db)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_one(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = get_category(db, category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return category