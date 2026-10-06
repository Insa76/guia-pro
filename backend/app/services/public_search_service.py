from sqlalchemy.orm import Session

from app.services.search_service import search_professionals


def public_search_professionals(
    db: Session,
    category_slug: str | None = None,
    location_name: str | None = None,
    query: str | None = None,
) -> list[dict]:

    results = search_professionals(
        db=db,
        category_slug=category_slug,
        location_name=location_name,
        query=query,
    )

    public_results = []

    for result in results:
        public_results.append(
            {
                "id": result["id"],
                "first_name": result["first_name"],
                "last_name": result["last_name"],
                "description": result["description"],
                "years_experience": result["years_experience"],
                "identity_verified": result["identity_verified"],
                "average_rating": result["average_rating"],
                "total_reviews": result["total_reviews"],
                "total_jobs": result["total_jobs"],
                "rated_jobs": result["rated_jobs"],
                "category_name": result["category_name"],
                "category_slug": result["category_slug"],
                "location_name": result["location_name"],
                "locality": result["locality"],
                "province": result["province"],
            }
        )

    return public_results