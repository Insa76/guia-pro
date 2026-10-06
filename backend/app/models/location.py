from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.professional_location import ProfessionalLocation


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True,
    )

    locality: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        default="Resistencia",
    )

    province: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        default="Chaco",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    professionals: Mapped[list["ProfessionalLocation"]] = relationship(
        "ProfessionalLocation",
        back_populates="location",
        cascade="all, delete-orphan",
    )