from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.location import Location
from app.models.professional import Professional
from app.models.professional_location import ProfessionalLocation
from app.schemas.professional_location import ProfessionalLocationCreate


def create_professional_location(
    db: Session,
    data: ProfessionalLocationCreate,
) -> ProfessionalLocation:
    professional = db.get(
        Professional,
        data.professional_id,
    )

    if professional is None:
        raise ValueError("Professional not found")

    location = db.get(
        Location,
        data.location_id,
    )

    if location is None:
        raise ValueError("Location not found")

    existing = db.scalar(
        select(ProfessionalLocation).where(
            ProfessionalLocation.professional_id
            == data.professional_id,
            ProfessionalLocation.location_id
            == data.location_id,
        )
    )

    if existing is not None:
        raise ValueError(
            "Professional already has this location"
        )

    professional_location = ProfessionalLocation(
        professional_id=data.professional_id,
        location_id=data.location_id,
    )

    db.add(professional_location)
    db.commit()
    db.refresh(professional_location)

    return professional_location


def get_professional_locations(
    db: Session,
    professional_id: int,
) -> list[ProfessionalLocation]:
    statement = (
        select(ProfessionalLocation)
        .where(
            ProfessionalLocation.professional_id
            == professional_id
        )
        .order_by(
            ProfessionalLocation.location_id.asc()
        )
    )

    return list(db.scalars(statement).all())