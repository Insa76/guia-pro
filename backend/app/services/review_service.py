from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.review import Review
from app.models.professional import Professional
from app.schemas.review import ReviewCreate


def create_review(db: Session, data: ReviewCreate) -> Review:
    professional = db.get(Professional, data.professional_id)

    if professional is None:
        raise ValueError("Professional not found")

    job = db.get(Job, data.job_id)

    if job is None:
        raise ValueError("Job not found")

    if job.professional_id != data.professional_id:
        raise ValueError(
            "Job does not belong to the specified professional"
        )

    if job.status != "completed":
        raise ValueError(
            "Only completed jobs can receive a review"
        )

    existing_review = db.execute(
        select(Review).where(Review.job_id == data.job_id)
    ).scalar_one_or_none()

    if existing_review is not None:
        raise ValueError(
            "This job already has a review"
        )

    review = Review(
        professional_id=data.professional_id,
        job_id=data.job_id,
        rating=data.rating,
        comment=data.comment,
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review


def get_review(
    db: Session,
    review_id: int,
) -> Review | None:
    return db.get(Review, review_id)


def get_reviews_by_professional(
    db: Session,
    professional_id: int,
) -> list[Review]:
    professional = db.get(Professional, professional_id)

    if professional is None:
        raise ValueError("Professional not found")

    result = db.execute(
        select(Review)
        .where(Review.professional_id == professional_id)
        .order_by(Review.id.desc())
    )

    return list(result.scalars().all())