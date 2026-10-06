from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.professional import Professional
from app.models.verification import Verification


def update_verification_status(
    db: Session,
    verification_id: int,
    status: str,
) -> Verification:

    if status not in {"verified", "rejected"}:
        raise ValueError(
            "Verification status must be 'verified' or 'rejected'"
        )

    verification = db.get(Verification, verification_id)

    if verification is None:
        raise ValueError("Verification not found")

    professional = db.get(
        Professional,
        verification.professional_id,
    )

    if professional is None:
        raise ValueError("Professional not found")

    verification.status = status

    if status == "verified":
        verification.verified_at = datetime.now(timezone.utc)
        professional.identity_verified = True
        professional.is_active = True

    else:
        verification.verified_at = None
        professional.identity_verified = False
        professional.is_active = False

    db.commit()
    db.refresh(verification)

    return verification