from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.location import Location
    from app.models.professional import Professional


class ProfessionalLocation(Base):
    __tablename__ = "professional_locations"

    professional_id: Mapped[int] = mapped_column(
        ForeignKey("professionals.id", ondelete="CASCADE"),
        primary_key=True,
    )

    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id", ondelete="CASCADE"),
        primary_key=True,
    )

    professional: Mapped["Professional"] = relationship(
        "Professional",
        back_populates="locations",
    )

    location: Mapped["Location"] = relationship(
        "Location",
        back_populates="professionals",
    )