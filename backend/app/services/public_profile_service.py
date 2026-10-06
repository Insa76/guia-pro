from sqlalchemy.orm import Session

from app.models.professional import Professional
from app.services.reputation_service import (
    get_professional_reputation,
)


def get_public_professional_profile(
    db: Session,
    professional_id: int,
) -> dict | None:

    professional = db.get(
        Professional,
        professional_id,
    )

    if professional is None:
        return None

    if not professional.is_active:
        return None

    reputation = get_professional_reputation(
        db,
        professional_id,
    )

    categories = [
        {
            "id": item.category.id,
            "name": item.category.name,
            "slug": item.category.slug,
        }
        for item in professional.categories
        if item.category.is_active
    ]

    locations = [
        {
            "id": item.location.id,
            "name": item.location.name,
            "locality": item.location.locality,
            "province": item.location.province,
        }
        for item in professional.locations
        if item.location.is_active
    ]

    reviews = [
        {
            "id": review.id,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at.isoformat(),
        }
        for review in sorted(
            professional.reviews,
            key=lambda item: item.id,
            reverse=True,
        )
    ]

    return {
        "id": professional.id,
        "first_name": professional.first_name,
        "last_name": professional.last_name,
        "description": professional.description,
        "years_experience": professional.years_experience,
        "whatsapp": professional.whatsapp,
        "instagram": professional.instagram,
        "identity_verified": professional.identity_verified,
        "average_rating": reputation["average_rating"],
        "total_reviews": reputation["total_reviews"],
        "total_jobs": reputation["total_jobs"],
        "rated_jobs": reputation["rated_jobs"],
        "categories": categories,
        "locations": locations,
        "reviews": reviews,
    }