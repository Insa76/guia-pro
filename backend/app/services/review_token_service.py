import hashlib
import secrets
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.review import Review
from app.schemas.public_review import PublicReviewCreate


def generate_review_token(
    db: Session,
    job_id: int,
) -> str:

    job = db.get(Job, job_id)

    if job is None:
        raise ValueError("Job not found")

    if job.status != "completed":
        raise ValueError(
            "Only completed jobs can generate a review link"
        )

    if job.review is not None:
        raise ValueError(
            "This job already has a review"
        )

    token = secrets.token_urlsafe(32)

    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    job.review_token_hash = token_hash
    job.review_token_created_at = datetime.now(
        timezone.utc
    )

    db.commit()
    db.refresh(job)

    return token


def get_job_by_review_token(
    db: Session,
    token: str,
) -> Job | None:

    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    job = db.execute(
        select(Job).where(
            Job.review_token_hash == token_hash
        )
    ).scalar_one_or_none()

    return job


def create_public_review(
    db: Session,
    token: str,
    data: PublicReviewCreate,
) -> Review:

    job = get_job_by_review_token(
        db,
        token,
    )

    if job is None:
        raise ValueError(
            "Review link not found or invalid"
        )

    if job.status != "completed":
        raise ValueError(
            "Only completed jobs can be reviewed"
        )

    if job.review is not None:
        raise ValueError(
            "This job already has a review"
        )

    review = Review(
        professional_id=job.professional_id,
        job_id=job.id,
        rating=data.rating,
        comment=data.comment,
    )

    db.add(review)

    # El token es de un solo uso.
    job.review_token_hash = None
    job.review_token_created_at = None

    db.commit()
    db.refresh(review)

    return review