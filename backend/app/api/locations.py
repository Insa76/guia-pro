from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.admin_auth import require_admin

from app.db.session import get_db
from app.schemas.location import (
    LocationCreate,
    LocationResponse,
)
from app.services.location_service import (
    create_location,
    get_location,
    get_locations,
)


router = APIRouter(
    prefix="/api/locations",
    tags=["locations"],
)


@router.post(
    "",
    response_model=LocationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: LocationCreate,
    db: Session = Depends(get_db),
    admin_authenticated: bool = Depends(require_admin),
):
    return create_location(db, data)


@router.get(
    "",
    response_model=list[LocationResponse],
)
def list_all(
    db: Session = Depends(get_db),
):
    return get_locations(db)


@router.get(
    "/{location_id}",
    response_model=LocationResponse,
)
def get_one(
    location_id: int,
    db: Session = Depends(get_db),
):
    location = get_location(db, location_id)

    if location is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )

    return location