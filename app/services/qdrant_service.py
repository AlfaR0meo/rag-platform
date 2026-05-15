from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
    FieldCondition,
    Filter,
    MatchValue,
)
from app.core.config import settings

# Сервис для взаимодействия с Qdrant, который будет использоваться для создания коллекции и индексирования векторов
class QdrantService:
    # Название коллекции для хранения векторов, связанных с документами
    COLLECTION_NAME = "document_chunks"

    # Инициализация клиента Qdrant с использованием настроек из конфигурации приложения
    client = QdrantClient(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT,
    )

    # Метод для создания коллекции в Qdrant, если она еще не существует
    @classmethod
    def create_collection(cls):
        # Получаем список существующих коллекций в Qdrant
        collections = cls.client.get_collections()

        # Проверяем, существует ли уже коллекция с заданным именем
        collection_exists = any(
            collection.name == cls.COLLECTION_NAME
            for collection in collections.collections
        )

        # Если коллекция уже существует, то ничего не делаем
        if collection_exists:
            return

        # Если коллекция не существует, то создаем ее с определенной конфигурацией векторов (размером 384 и косинусным расстоянием)
        cls.client.create_collection(
            collection_name=cls.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

    # Метод для индексирования чанков документов в Qdrant. Он принимает идентификатор чанка, его эмбеддинг, текстовое содержание и идентификатор документа, к которому он относится. Затем он сохраняет эту информацию в виде точки в коллекции Qdrant, что позволяет эффективно выполнять поиск по семантическому сходству в будущем
    @classmethod
    def index_chunk(
        cls,
        chunk_id: int,
        embedding: list[float],
        content: str,
        document_id: int,
    ):
        cls.client.upsert(
            collection_name=cls.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=chunk_id,
                    vector=embedding,
                    payload={
                        "content": content,
                        "document_id": document_id,
                    },
                )
            ],
        )

    # Метод для выполнения поиска в Qdrant по эмбеддингу запроса. Он принимает эмбеддинг запроса, список идентификаторов документов, которые нужно учитывать при поиске, и количество результатов, которые нужно вернуть. Метод выполняет поиск в коллекции Qdrant, используя косинусное расстояние для оценки сходства между эмбеддингами, и возвращает наиболее релевантные результаты
    @classmethod
    def search(
        cls,
        query_embedding: list[float],
        document_ids: list[int],
        limit: int = 5,
    ):
        # Выполняем поиск в коллекции Qdrant, используя эмбеддинг запроса и фильтруя результаты по идентификаторам документов. Результаты сортируются по релевантности, и возвращается указанное количество наиболее релевантных результатов
        results = cls.client.search(
            collection_name=cls.COLLECTION_NAME,
            query_vector=query_embedding,
            limit=limit,
            # Фильтр для ограничения поиска только теми точками, которые принадлежат указанным документам. Это позволяет сузить результаты поиска и повысить релевантность возвращаемых данныхs
            query_filter=Filter(
                should=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    )
                    for document_id in document_ids
                ]
            )
        )

        return results
