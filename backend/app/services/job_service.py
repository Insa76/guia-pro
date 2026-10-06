from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.professional import Professional
from app.schemas.job import JobCreate


def create_job(db: Session, data: JobCreate) -> Job:
    professional = db.get(Professional, data.professional_id)

    if professional is None:
        raise ValueError("Professional not found")

    job = Job(
        professional_id=data.professional_id,
        title=data.title,
        description=data.description,
        status=data.status,
        completed_at=data.completed_at,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_jobs_by_professional(
    db: Session,
    professional_id: int,
) -> list[Job]:
    professional = db.get(Professional, professional_id)

    if professional is None:
        raise ValueError("Professional not found")

    result = db.execute(
        select(Job)
        .where(Job.professional_id == professional_id)
        .order_by(Job.id.desc())
    )

    return list(result.scalars().all())


def get_job(
    db: Session,
    job_id: int,
) -> Job | None:
    return db.get(Job, job_id)