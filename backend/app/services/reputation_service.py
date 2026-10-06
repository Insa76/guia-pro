from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.professional import Professional
from app.models.review import Review


def get_professional_reputation(
    db: Session,
    professional_id: int,
) -> dict:
    professional = db.get(Professional, professional_id)

    if professional is None:
        raise ValueError("Professional not found")

    total_jobs = db.scalar(
        select(func.count(Job.id)).where(
            Job.professional_id == professional_id
        )
    ) or 0

    total_reviews = db.scalar(
        select(func.count(Review.id)).where(
            Review.professional_id == professional_id
        )
    ) or 0

    average_rating = db.scalar(
        select(func.avg(Review.rating)).where(
            Review.professional_id == professional_id
        )
    )

    rated_jobs = db.scalar(
        select(func.count(Review.job_id))
        .join(Job, Review.job_id == Job.id)
        .where(
            Review.professional_id == professional_id,
            Review.job_id.is_not(None),
        )
    ) or 0

    return {
        "average_rating": round(float(average_rating), 2)
        if average_rating is not None
        else 0.0,
        "total_reviews": int(total_reviews),
        "total_jobs": int(total_jobs),
        "rated_jobs": int(rated_jobs),
    }