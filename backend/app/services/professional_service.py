from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.professional import Professional
from app.schemas.professional import ProfessionalCreate
from app.services.reputation_service import get_professional_reputation
from app.models.verification import Verification


def create_professional(
    db: Session,
    data: ProfessionalCreate,
) -> Professional:
    professional = Professional(
        first_name=data.first_name,
        last_name=data.last_name,
        phone=data.phone,
        whatsapp=data.whatsapp,
        description=data.description,
        years_experience=data.years_experience,
        instagram=data.instagram,
    )

    db.add(professional)
    db.flush()

    verification = Verification(
        professional_id=professional.id,
        status="pending",
        method="manual",
    )

    db.add(verification)

    db.commit()
    db.refresh(professional)

    return professional


def get_professionals(
    db: Session,
) -> list[Professional]:
    statement = (
        select(Professional)
        .where(Professional.is_active.is_(True))
        .order_by(Professional.id.desc())
    )
    

    return list(db.scalars(statement).all())

def get_all_professionals(
    db: Session,
) -> list[Professional]:
    statement = (
        select(Professional)
        .order_by(Professional.id.desc())
    )

    return list(db.scalars(statement).all())


def get_professional(
    db: Session,
    professional_id: int,
) -> Professional | None:
    return db.get(Professional, professional_id)

def get_professional_profile(
    db: Session,
    professional_id: int,
) -> dict | None:

    professional = db.get(
        Professional,
        professional_id,
    )

    if professional is None:
        return None

    categories = [
        {
            "id": relation.category.id,
            "name": relation.category.name,
            "slug": relation.category.slug,
        }
        for relation in professional.categories
        if relation.category.is_active
    ]

    locations = [
        {
            "id": relation.location.id,
            "name": relation.location.name,
            "locality": relation.location.locality,
            "province": relation.location.province,
        }
        for relation in professional.locations
        if relation.location.is_active
    ]

    reputation = get_professional_reputation(
        db,
        professional_id,
    )

    return {
        "id": professional.id,
        "first_name": professional.first_name,
        "last_name": professional.last_name,
        "phone": professional.phone,
        "whatsapp": professional.whatsapp,
        "description": professional.description,
        "years_experience": professional.years_experience,
        "instagram": professional.instagram,
        "is_active": professional.is_active,
        "identity_verified": professional.identity_verified,
        "reputation": reputation,
        "categories": categories,
        "locations": locations,
    }