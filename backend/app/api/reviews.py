from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.admin_auth import require_admin
from app.core.rate_limit import public_review_limiter
from app.db.session import get_db
from app.schemas.review import ReviewCreate, ReviewResponse
from app.services.review_service import (
    create_review,
    get_review,
    get_reviews_by_professional,
)
from app.schemas.public_review import (
    PublicReviewCreate,
    PublicReviewResponse,
    PublicReviewContext,
)
from app.services.review_token_service import (
    create_public_review,
)

from app.services.public_review_service import get_public_review_context


router = APIRouter(
    prefix="/api/reviews",
    tags=["reviews"],
)


@router.post(
    "",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_review_endpoint(
    data: ReviewCreate,
    db: Session = Depends(get_db),
    admin_authenticated: bool = Depends(require_admin),
):
    try:
        return create_review(db, data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/professional/{professional_id}",
    response_model=list[ReviewResponse],
)
def list_professional_reviews(
    professional_id: int,
    db: Session = Depends(get_db),
    admin_authenticated: bool = Depends(require_admin),
):
    try:
        return get_reviews_by_professional(db, professional_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{review_id}",
    response_model=ReviewResponse,
)
def get_review_endpoint(
    review_id: int,
    db: Session = Depends(get_db),
    admin_authenticated: bool = Depends(require_admin),
):
    review = get_review(db, review_id)

    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    return review


@router.post(
    "/public/{token}",
    response_model=PublicReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_public_review_endpoint(
    request: Request,
    token: str,
    data: PublicReviewCreate,
    db: Session = Depends(get_db),
):
    client_ip = (
        request.client.host
        if request.client
        else "unknown"
    )

    if not public_review_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail=(
                "Demasiados intentos de valoración. "
                "Intentá nuevamente más tarde."
            ),
        )

    try:
        review = create_public_review(
            db,
            token,
            data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    public_review_limiter.reset(client_ip)

    return PublicReviewResponse(
        id=review.id,
        job_id=review.job_id,
        professional_id=review.professional_id,
        rating=review.rating,
        comment=review.comment,
    )


@router.get(
    "/public/{token}",
    response_model=PublicReviewContext,
)
def get_public_review_context_endpoint(
    token: str,
    db: Session = Depends(get_db),
):
    try:
        return get_public_review_context(
            db,
            token,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )