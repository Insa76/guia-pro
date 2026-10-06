from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.location import Location
from app.models.professional import Professional
from app.models.professional_category import ProfessionalCategory
from app.models.professional_location import ProfessionalLocation
from app.schemas.public_registration import (
    PublicProfessionalRegistration,
)
from app.models.verification import Verification


def register_professional(
    db: Session,
    data: PublicProfessionalRegistration,
):
    # ---------------------------------------------------------
    # VALIDAR CATEGORÍA
    # ---------------------------------------------------------

    category = db.get(Category, data.category_id)

    if category is None or not category.is_active:
        raise ValueError("La categoría seleccionada no existe.")


    # ---------------------------------------------------------
    # VALIDAR LOCALIDAD
    # ---------------------------------------------------------

    location = db.get(Location, data.location_id)

    if location is None or not location.is_active:
        raise ValueError("La localidad seleccionada no existe.")


    # ---------------------------------------------------------
    # VALIDAR TELÉFONO
    # ---------------------------------------------------------

    existing_professional = db.execute(
        select(Professional).where(
            Professional.phone == data.phone
        )
    ).scalar_one_or_none()

    if existing_professional is not None:
        raise ValueError(
            "Ya existe un profesional registrado con ese teléfono."
        )


    # ---------------------------------------------------------
    # CREAR PROFESIONAL
    # ---------------------------------------------------------

    professional = Professional(
        first_name=data.first_name.strip(),
        last_name=data.last_name.strip(),
        phone=data.phone.strip(),
        whatsapp=(
            data.whatsapp.strip()
            if data.whatsapp
            else None
        ),
        description=(
            data.description.strip()
            if data.description
            else None
        ),
        years_experience=data.years_experience,
        instagram=(
            data.instagram.strip()
            if data.instagram
            else None
        ),

        # IMPORTANTE:
        # Un registro nuevo NO queda publicado ni verificado.
        is_active=False,
        identity_verified=False,
    )

    db.add(professional)

    try:
        db.flush()

        # -----------------------------------------------------
        # ASOCIAR CATEGORÍA
        # -----------------------------------------------------

        professional_category = ProfessionalCategory(
            professional_id=professional.id,
            category_id=category.id,
        )

        db.add(professional_category)


        # -----------------------------------------------------
        # ASOCIAR LOCALIDAD
        # -----------------------------------------------------

        professional_location = ProfessionalLocation(
            professional_id=professional.id,
            location_id=location.id,
        )

        db.add(professional_location)

        verification = Verification(
            professional_id=professional.id,
            status="pending",
            method="public_registration",
            notes="Registro realizado desde Guia Pro.",
            )
        
        db.add(verification)

        db.commit()
        db.refresh(professional)

    except Exception:
        db.rollback()
        raise


    return professional