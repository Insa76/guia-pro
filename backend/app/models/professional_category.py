from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.professional import Professional


class ProfessionalCategory(Base):
    __tablename__ = "professional_categories"

    professional_id: Mapped[int] = mapped_column(
        ForeignKey("professionals.id", ondelete="CASCADE"),
        primary_key=True,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        primary_key=True,
    )

    professional: Mapped["Professional"] = relationship(
        "Professional",
        back_populates="categories",
    )

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="professionals",
    )