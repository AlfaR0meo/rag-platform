import shutil
from uuid import uuid4
from pathlib import Path
import os
from app.core.constants import ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES, MAX_FILE_SIZE

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.document import Document
from app.models.document_chunk import DocumentChunk

from app.services.document_processing_service import DocumentProcessingService
from app.services.qdrant_service import QdrantService

from app.core.decorators import log_execution

# Папка для хранения загруженных файлов
UPLOAD_DIR = Path("uploads")
# Создаем папку, если ее нет
UPLOAD_DIR.mkdir(exist_ok=True)

# Сервис для работы с документами
class DocumentService:
    
    # Загрузка и сохранение документа
    @staticmethod
    @log_execution("document_upload")
    def save_document(
        db: Session, 
        file: UploadFile, 
        current_user: User
    ) -> Document:
        extension = Path(str(file.filename)).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="File extension not allowed",
            )

        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=400,
                detail="File MIME type not allowed",
            )

        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File too large (max 5 MB)",
            )

        unique_filename = f"{current_user.id}_{uuid4()}{extension}"

        file_path = UPLOAD_DIR / unique_filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        document = Document(
            filename=file.filename,
            stored_filename=unique_filename,
            filepath=str(file_path),
            owner_id=current_user.id,
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        DocumentProcessingService.process_document(
            db=db,
            document=document
        )

        return document

    # Получение документов текущего пользователя
    @staticmethod
    def get_user_documents(db: Session, current_user: User):
        return db.query(Document).filter(
            Document.owner_id == current_user.id
        ).all()

    # Удаление документа и его чанков, а также связанных данных в Qdrant
    @staticmethod
    @log_execution("document_delete")
    def delete_document(
        db: Session,
        document_id: int,
        current_user: User,
    ):
        document = db.query(Document).filter(
            Document.id == document_id,
            Document.owner_id == current_user.id,
        ).first()

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found",
            )

        QdrantService.delete_document_chunks(
            document_id=document.id
        )

        db.query(DocumentChunk).filter(
            DocumentChunk.document_id == document.id
        ).delete()

        if os.path.exists(document.filepath):
            os.remove(document.filepath)

        db.delete(document)

        db.commit()

        return {
            "message":
                "Document deleted successfully"
        }
