from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.user import User

from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService

from app.core.decorators import log_execution

# Сервис для выполнения семантического поиска по документам пользователя
class SearchService:

    # Метод для выполнения семантического поиска по документам конкретного пользователя с помощью Qdrant
    @staticmethod
    @log_execution("semantic_search")
    def semantic_search(
        db: Session,
        query: str,
        current_user: User,
        limit: int = 5,
    ):

        query_embedding = EmbeddingService.generate_embedding(query)

        documents = db.query(Document).filter(
            Document.owner_id == current_user.id
        ).all()

        document_ids = [
            document.id
            for document in documents
        ]

        if not document_ids:
            return []

        # Выполняем поиск в Qdrant по embedding запроса и ID документов пользователя
        results = QdrantService.search(
            query_embedding=query_embedding,
            document_ids=document_ids,
            limit=limit,
        )

        formatted_results = []

        for result in results:
            formatted_results.append(
                {
                    "content": result.payload["content"], # type: ignore
                    "document_id": result.payload["document_id"], # type: ignore
                    "score": result.score,
                }
            )

        return formatted_results
