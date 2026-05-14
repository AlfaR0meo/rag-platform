from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.chunking_service import ChunkingService
from app.services.text_extraction_service import TextExtractionService
from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService

# Сервис для обработки документов. Он отвечает за извлечение текста из загруженных документов, разбиение текста на чанки и сохранение этих чанков в базе данных. Этот сервис является ключевым компонентом системы RAG, так как обеспечивает подготовку данных для эффективного поиска и генерации ответов на основе извлеченной информации.
class DocumentProcessingService:

    # Основной метод для обработки документа
    @staticmethod
    def process_document(db: Session, document: Document) -> None:
        text = TextExtractionService.extract_text(document.filepath)
        chunks = ChunkingService.chunk_text(text=text)

        for index, chunk in enumerate(chunks):
            db_chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                content=chunk,
            )

            db.add(db_chunk)
            db.commit()
            db.refresh(db_chunk)

            embedding = EmbeddingService.generate_embedding(chunk)

            QdrantService.index_chunk(
                chunk_id=db_chunk.id,
                embedding=embedding,
                content=chunk,
                document_id=document.id,
            )
