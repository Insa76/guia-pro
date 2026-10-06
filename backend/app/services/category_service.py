from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate


def create_category(
    db: Session,
    data: CategoryCreate,
) -> Category:
    category = Category(
        name=data.name,
        slug=data.slug,
        description=data.description,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_categories(
    db: Session,
) -> list[Category]:
    statement = (
        select(Category)
        .where(Category.is_active.is_(True))
        .order_by(Category.name.asc())
    )

    return list(db.scalars(statement).all())


def get_category(
    db: Session,
    category_id: int,
) -> Category | None:
    return db.get(Category, category_id)