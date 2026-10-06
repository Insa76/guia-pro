import hashlib

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.professional import Professional
from app.models.review import Review


def get_public_review_context(
    db: Session,
    token: str,
):
    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    stmt = (
        select(Job, Professional)
        .join(
            Professional,
            Professional.id == Job.professional_id,
        )
        .where(
            Job.review_token_hash == token_hash
        )
    )

    result = db.execute(stmt).first()

    if result is None:
        raise ValueError("Token de valoración inválido.")

    job, professional = result

    existing_review = db.execute(
        select(Review.id).where(
            Review.job_id == job.id
        )
    ).scalar_one_or_none()

    return {
        "job_id": job.id,
        "professional_id": professional.id,
        "first_name": professional.first_name,
        "last_name": professional.last_name,
        "title": job.title,
        "already_reviewed": existing_review is not None,
    }