from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.job import Job
    from app.models.professional_category import ProfessionalCategory
    from app.models.professional_location import ProfessionalLocation
    from app.models.review import Review
    from app.models.verification import Verification


class Professional(Base):
    __tablename__ = "professionals"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
    )

    password_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    account_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    activation_token_hash: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        unique=True,
        index=True,
    )

    activation_token_created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    activation_token_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    whatsapp: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    years_experience: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    instagram: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    identity_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="professional",
        cascade="all, delete-orphan",
    )

    jobs: Mapped[list["Job"]] = relationship(
        "Job",
        back_populates="professional",
        cascade="all, delete-orphan",
    )

    verification: Mapped["Verification | None"] = relationship(
        "Verification",
        back_populates="professional",
        uselist=False,
        cascade="all, delete-orphan",
    )

    categories: Mapped[list["ProfessionalCategory"]] = relationship(
        "ProfessionalCategory",
        back_populates="professional",
        cascade="all, delete-orphan",
    )

    locations: Mapped[list["ProfessionalLocation"]] = relationship(
        "ProfessionalLocation",
        back_populates="professional",
        cascade="all, delete-orphan",
    )