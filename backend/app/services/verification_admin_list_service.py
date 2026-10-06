
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.professional import Professional
from app.models.verification import Verification


def list_pending_verifications(db: Session):
    statement = (
        select(Verification, Professional)
        .join(
            Professional,
            Professional.id == Verification.professional_id,
        )
        .where(
            Verification.status == "pending"
        )
        .order_by(Verification.id.asc())
    )

    results = db.execute(statement).all()

    return [
        {
            "verification_id": verification.id,
            "professional_id": professional.id,
            "first_name": professional.first_name,
            "last_name": professional.last_name,
            "phone": professional.phone,
            "whatsapp": professional.whatsapp,
            "description": professional.description,
            "years_experience": professional.years_experience,
            "instagram": professional.instagram,
            "status": verification.status,
            "method": verification.method,
            "notes": verification.notes,
            "verified_at": verification.verified_at,
        }
        for verification, professional in results
    ]
