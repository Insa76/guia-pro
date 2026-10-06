from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.public_profile import (
    PublicProfessionalProfile,
)
from app.services.public_profile_service import (
    get_public_professional_profile,
)


router = APIRouter(
    prefix="/api/public/professionals",
    tags=["public-professionals"],
)


@router.get(
    "/{professional_id}/profile",
    response_model=PublicProfessionalProfile,
)
def get_public_professional_profile_endpoint(
    professional_id: int,
    db: Session = Depends(get_db),
):
    profile = get_public_professional_profile(
        db,
        professional_id,
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Professional not found",
        )

    return profile