from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.search import ProfessionalSearchResult
from app.services.search_service import search_professionals


router = APIRouter(
    prefix="/api/search",
    tags=["search"],
)


@router.get(
    "/professionals",
    response_model=list[ProfessionalSearchResult],
)
def search(
    category: str | None = None,
    location: str | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
):
    return search_professionals(
        db=db,
        category_slug=category,
        location_name=location,
        query=q,
    )