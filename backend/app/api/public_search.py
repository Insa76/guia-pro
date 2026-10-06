from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.public_search import (
    PublicProfessionalSearchResult,
)
from app.services.public_search_service import (
    public_search_professionals,
)


router = APIRouter(
    prefix="/api/public/search",
    tags=["public-search"],
)


@router.get(
    "/professionals",
    response_model=list[PublicProfessionalSearchResult],
)
def public_search_professionals_endpoint(
    category: str | None = None,
    location: str | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
):
    return public_search_professionals(
        db=db,
        category_slug=category,
        location_name=location,
        query=q,
    )