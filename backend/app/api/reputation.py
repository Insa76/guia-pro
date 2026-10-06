from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.admin_auth import require_admin

from app.db.session import get_db
from app.schemas.reputation import ProfessionalReputationResponse
from app.services.reputation_service import get_professional_reputation


router = APIRouter(
    prefix="/api/reputation",
    tags=["reputation"],
)


@router.get(
    "/professional/{professional_id}",
    response_model=ProfessionalReputationResponse,
)
def get_professional_reputation_endpoint(
    professional_id: int,
    db: Session = Depends(get_db),
    admin_authenticated: bool = Depends(require_admin),
):
    try:
        return get_professional_reputation(
            db,
            professional_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc