from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.professional_auth import require_professional
from app.db.session import get_db
from app.schemas.job import JobCreate, JobResponse
from app.schemas.review_token import (
    ReviewTokenJobResponse,
    ReviewTokenResponse,
)
from app.services.job_service import (
    create_job,
    get_job,
    get_jobs_by_professional,
)
from app.services.review_token_service import (
    generate_review_token,
    get_job_by_review_token,
)

router = APIRouter(
    prefix="/api/jobs",
    tags=["jobs"],
)


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job_endpoint(
    data: JobCreate,
    db: Session = Depends(get_db),
    professional_id: int = Depends(require_professional),
):
    """
    Crea un trabajo para el profesional autenticado.

    El professional_id enviado por el frontend no se utiliza
    para determinar el dueño del trabajo.

    El dueño se obtiene exclusivamente del token de autenticación.
    """

    data.professional_id = professional_id

    try:
        return create_job(db, data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/professional/{professional_id}",
    response_model=list[JobResponse],
)
def list_professional_jobs(
    professional_id: int,
    db: Session = Depends(get_db),
    authenticated_professional_id: int = Depends(require_professional),
):
    """
    Lista los trabajos del profesional autenticado.

    El ID de la URL debe coincidir con el profesional
    identificado por el token.
    """

    if professional_id != authenticated_professional_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No podés acceder a los trabajos de otro profesional.",
        )

    try:
        return get_jobs_by_professional(
            db,
            authenticated_professional_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
def get_job_endpoint(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = get_job(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return job


@router.post(
    "/{job_id}/review-token",
    response_model=ReviewTokenResponse,
)
def generate_review_token_endpoint(
    job_id: int,
    db: Session = Depends(get_db),
    professional_id: int = Depends(require_professional),
):
    """
    Genera un enlace de valoración únicamente para un trabajo
    perteneciente al profesional autenticado.
    """

    job = get_job(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    if job.professional_id != professional_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No podés generar una valoración para un trabajo de otro profesional.",
        )

    try:
        token = generate_review_token(
            db,
            job_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return ReviewTokenResponse(
        job_id=job_id,
        review_token=token,
        review_url=f"/review/{token}",
    )


@router.get(
    "/review-token/{token}",
    response_model=ReviewTokenJobResponse,
)
def get_job_by_review_token_endpoint(
    token: str,
    db: Session = Depends(get_db),
):
    """
    Endpoint público.

    El cliente utiliza el token recibido por el profesional
    para consultar los datos mínimos necesarios para valorar
    un trabajo.
    """

    job = get_job_by_review_token(
        db,
        token,
    )

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Review link not found or invalid",
        )

    professional = job.professional

    return ReviewTokenJobResponse(
        job_id=job.id,
        professional_id=professional.id,
        professional_name=(
            f"{professional.first_name} "
            f"{professional.last_name}"
        ),
        job_title=job.title,
        job_description=job.description,
        completed_at=(
            job.completed_at.isoformat()
            if job.completed_at
            else None
        ),
        already_reviewed=job.review is not None,
    )