from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.job import Job
from app.models.location import Location
from app.models.professional import Professional
from app.models.professional_category import ProfessionalCategory
from app.models.professional_location import ProfessionalLocation
from app.models.review import Review


def search_professionals(
    db: Session,
    category_slug: str | None = None,
    location_name: str | None = None,
    query: str | None = None,
) -> list[dict]:

    total_jobs_subquery = (
        select(
            func.count(Job.id)
        )
        .where(
            Job.professional_id == Professional.id
        )
        .correlate(Professional)
        .scalar_subquery()
    )

    total_reviews_subquery = (
        select(
            func.count(Review.id)
        )
        .where(
            Review.professional_id == Professional.id
        )
        .correlate(Professional)
        .scalar_subquery()
    )

    average_rating_subquery = (
        select(
            func.avg(Review.rating)
        )
        .where(
            Review.professional_id == Professional.id
        )
        .correlate(Professional)
        .scalar_subquery()
    )

    rated_jobs_subquery = (
        select(
            func.count(Review.job_id)
        )
        .where(
            Review.professional_id == Professional.id,
            Review.job_id.is_not(None),
        )
        .correlate(Professional)
        .scalar_subquery()
    )

    statement = (
        select(
            Professional.id,
            Professional.first_name,
            Professional.last_name,
            Professional.phone,
            Professional.whatsapp,
            Professional.description,
            Professional.years_experience,
            Professional.instagram,
            Professional.is_active,
            Professional.identity_verified,

            func.coalesce(
                average_rating_subquery,
                0,
            ).label("average_rating"),

            total_reviews_subquery.label(
                "total_reviews"
            ),

            total_jobs_subquery.label(
                "total_jobs"
            ),

            rated_jobs_subquery.label(
                "rated_jobs"
            ),

            Category.id.label("category_id"),
            Category.name.label("category_name"),
            Category.slug.label("category_slug"),

            Location.id.label("location_id"),
            Location.name.label("location_name"),
            Location.locality,
            Location.province,
        )
        .join(
            ProfessionalCategory,
            ProfessionalCategory.professional_id
            == Professional.id,
        )
        .join(
            Category,
            Category.id
            == ProfessionalCategory.category_id,
        )
        .join(
            ProfessionalLocation,
            ProfessionalLocation.professional_id
            == Professional.id,
        )
        .join(
            Location,
            Location.id
            == ProfessionalLocation.location_id,
        )
        .where(
            Professional.is_active.is_(True),
            Category.is_active.is_(True),
            Location.is_active.is_(True),
        )
    )

    if category_slug:
        statement = statement.where(
            Category.slug == category_slug.strip().lower()
        )

    if location_name:
        statement = statement.where(
            Location.name.ilike(
                location_name.strip()
            )
        )

    if query:
        search_text = f"%{query.strip()}%"

        statement = statement.where(
            (
                Professional.first_name.ilike(search_text)
                | Professional.last_name.ilike(search_text)
                | Professional.description.ilike(search_text)
            )
        )

    statement = statement.order_by(
        Professional.first_name.asc(),
        Professional.last_name.asc(),
    )

    rows = db.execute(
        statement
    ).mappings().all()

    return [
        {
            **dict(row),
            "average_rating": round(
                float(row["average_rating"] or 0),
                2,
            ),
            "total_reviews": int(
                row["total_reviews"] or 0
            ),
            "total_jobs": int(
                row["total_jobs"] or 0
            ),
            "rated_jobs": int(
                row["rated_jobs"] or 0
            ),
        }
        for row in rows
    ]