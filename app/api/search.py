from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.search import SearchRequest
from app.services.search_service import SearchService


router = APIRouter(prefix="/search",tags=["Search"])


@router.post("/")
def semantic_search(
    request: SearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SearchService.semantic_search(
        db=db,
        query=request.query,
        current_user=current_user,
        limit=request.limit,
    )
