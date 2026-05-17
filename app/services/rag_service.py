from sqlalchemy.orm import Session

from app.models.user import User

from app.services.llm_service import LLMService
from app.services.search_service import SearchService

from app.core.decorators import log_execution

# Сервис для реализации RAG
class RAGService:

    # Основной метод для обработки вопроса и генерации ответа
    @staticmethod
    @log_execution("rag_request")
    async def ask_question(
        db: Session, 
        query: str, 
        current_user: User,
    ):
        search_results = (
            SearchService.semantic_search(
                db=db,
                query=query,
                current_user=current_user,
                limit=5,
            )
        )

        if not search_results:
            return {
                "answer":
                    "No relevant documents found.",
                "sources": [],
            }

        context = "\n\n".join(
            result["content"]
            for result in search_results
        )

        answer = (
            await LLMService.generate_answer(
                query=query,
                context=context,
            )
        )

        return {
            "answer": answer,
            "sources": search_results,
        }
