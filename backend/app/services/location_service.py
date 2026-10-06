from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.location import Location
from app.schemas.location import LocationCreate


def create_location(
    db: Session,
    data: LocationCreate,
) -> Location:
    location = Location(
        name=data.name,
        locality=data.locality,
        province=data.province,
    )

    db.add(location)
    db.commit()
    db.refresh(location)

    return location


def get_locations(
    db: Session,
) -> list[Location]:
    statement = (
        select(Location)
        .where(Location.is_active.is_(True))
        .order_by(Location.name.asc())
    )

    return list(db.scalars(statement).all())


def get_location(
    db: Session,
    location_id: int,
) -> Location | None:
    return db.get(Location, location_id)