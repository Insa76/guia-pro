from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.admin_auth import require_admin

from app.db.session import get_db
from app.schemas.verification import (
    VerificationCreate,
    VerificationResponse,
)
from app.services.verification_service import (
    create_verification,
    get_verification,
    get_verification_by_professional,
)


router = APIRouter(
    prefix="/api/verifications",
    tags=["verifications"],
    dependencies=[Depends(require_admin)],
)


@router.post(
    "",
    response_model=VerificationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_verification_endpoint(
    data: VerificationCreate,
    db: Session = Depends(get_db),
    admin_authenticated: bool = Depends(require_admin),
):
    try:
        return create_verification(db, data)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get(
    "/professional/{professional_id}",
    response_model=VerificationResponse,
)
def get_professional_verification_endpoint(
    professional_id: int,
    db: Session = Depends(get_db),
):
    try:
        verification = get_verification_by_professional(
            db,
            professional_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    if verification is None:
        raise HTTPException(
            status_code=404,
            detail="Verification not found",
        )

    return verification


@router.get(
    "/{verification_id}",
    response_model=VerificationResponse,
)
def get_verification_endpoint(
    verification_id: int,
    db: Session = Depends(get_db),
):
    verification = get_verification(
        db,
        verification_id,
    )

    if verification is None:
        raise HTTPException(
            status_code=404,
            detail="Verification not found",
        )

    return verification