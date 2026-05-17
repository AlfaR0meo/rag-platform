from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.rag import RAGRequest
from app.services.rag_service import RAGService


router = APIRouter(prefix="/rag", tags=["RAG"])


# Эндпоинт для обработки вопроса и генерации ответа
@router.post("/")
async def ask_question(
    request: RAGRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await RAGService.ask_question(
        db=db,
        query=request.query,
        current_user=current_user,
    )
