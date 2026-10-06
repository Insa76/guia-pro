from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.professional import Professional
from app.models.verification import Verification
from app.schemas.verification import VerificationCreate


def create_verification(
    db: Session,
    data: VerificationCreate,
) -> Verification:
    professional = db.get(Professional, data.professional_id)

    if professional is None:
        raise ValueError("Professional not found")

    existing_verification = db.execute(
        select(Verification).where(
            Verification.professional_id == data.professional_id
        )
    ).scalar_one_or_none()

    if existing_verification is not None:
        raise ValueError("This professional already has a verification request")

    verification = Verification(
        professional_id=data.professional_id,
        status="pending",
        method=data.method,
        notes=data.notes,
    )

    db.add(verification)
    db.commit()
    db.refresh(verification)

    return verification


def get_verification(
    db: Session,
    verification_id: int,
) -> Verification | None:
    return db.get(Verification, verification_id)


def get_verification_by_professional(
    db: Session,
    professional_id: int,
) -> Verification | None:
    professional = db.get(Professional, professional_id)

    if professional is None:
        raise ValueError("Professional not found")

    result = db.execute(
        select(Verification).where(
            Verification.professional_id == professional_id
        )
    )

    return result.scalar_one_or_none()