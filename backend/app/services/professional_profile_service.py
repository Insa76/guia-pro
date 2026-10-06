from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.location import Location
from app.models.professional import Professional
from app.models.professional_category import ProfessionalCategory
from app.models.professional_location import ProfessionalLocation
from app.schemas.professional_profile_update import ProfessionalProfileUpdate
from app.services.professional_service import get_professional_profile


def update_professional_profile(
    db: Session,
    professional_id: int,
    data: ProfessionalProfileUpdate,
):
    professional = db.get(Professional, professional_id)

    if professional is None:
        raise ValueError("Professional not found")

    # ============================================================
    # DATOS DEL PERFIL
    # ============================================================

    if data.description is not None:
        professional.description = data.description.strip() or None

    if data.years_experience is not None:
        professional.years_experience = data.years_experience

    if data.whatsapp is not None:
        professional.whatsapp = data.whatsapp.strip() or None

    if data.instagram is not None:
        professional.instagram = data.instagram.strip() or None

    # ============================================================
    # CATEGORÍAS
    # ============================================================

    if data.category_ids is not None:
        category_ids = list(dict.fromkeys(data.category_ids))

        if category_ids:
            categories = db.scalars(
                select(Category).where(
                    Category.id.in_(category_ids),
                    Category.is_active.is_(True),
                )
            ).all()

            found_category_ids = {category.id for category in categories}

            missing_category_ids = [
                category_id
                for category_id in category_ids
                if category_id not in found_category_ids
            ]

            if missing_category_ids:
                raise ValueError(
                    f"Category not found or inactive: {missing_category_ids}"
                )

        db.execute(
            delete(ProfessionalCategory).where(
                ProfessionalCategory.professional_id == professional_id
            )
        )

        for category_id in category_ids:
            db.add(
                ProfessionalCategory(
                    professional_id=professional_id,
                    category_id=category_id,
                )
            )

    # ============================================================
    # ZONAS
    # ============================================================

    if data.location_ids is not None:
        location_ids = list(dict.fromkeys(data.location_ids))

        if location_ids:
            locations = db.scalars(
                select(Location).where(
                    Location.id.in_(location_ids),
                    Location.is_active.is_(True),
                )
            ).all()

            found_location_ids = {location.id for location in locations}

            missing_location_ids = [
                location_id
                for location_id in location_ids
                if location_id not in found_location_ids
            ]

            if missing_location_ids:
                raise ValueError(
                    f"Location not found or inactive: {missing_location_ids}"
                )

        db.execute(
            delete(ProfessionalLocation).where(
                ProfessionalLocation.professional_id == professional_id
            )
        )

        for location_id in location_ids:
            db.add(
                ProfessionalLocation(
                    professional_id=professional_id,
                    location_id=location_id,
                )
            )

    db.commit()

    return get_professional_profile(
        db,
        professional_id,
    )