from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.professional import Professional
from app.models.professional_category import ProfessionalCategory
from app.schemas.professional_category import ProfessionalCategoryCreate


def create_professional_category(
    db: Session,
    data: ProfessionalCategoryCreate,
) -> ProfessionalCategory:

    professional = db.get(
        Professional,
        data.professional_id,
    )

    if professional is None:
        raise ValueError("Professional not found")

    category = db.get(
        Category,
        data.category_id,
    )

    if category is None:
        raise ValueError("Category not found")

    existing = db.scalar(
        select(ProfessionalCategory).where(
            ProfessionalCategory.professional_id
            == data.professional_id,
            ProfessionalCategory.category_id
            == data.category_id,
        )
    )

    if existing is not None:
        raise ValueError("Professional already has this category")

    professional_category = ProfessionalCategory(
        professional_id=data.professional_id,
        category_id=data.category_id,
    )

    db.add(professional_category)
    db.commit()
    db.refresh(professional_category)

    return professional_category


def get_professional_categories(
    db: Session,
    professional_id: int,
) -> list[ProfessionalCategory]:

    statement = (
        select(ProfessionalCategory)
        .where(
            ProfessionalCategory.professional_id
            == professional_id
        )
        .order_by(ProfessionalCategory.category_id.asc())
    )

    return list(db.scalars(statement).all())