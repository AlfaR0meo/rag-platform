from sentence_transformers import SentenceTransformer

# Сервис для генерации эмбеддингов. Он отвечает за преобразование текстовых данных в векторные представления (эмбеддинги), которые используются для эффективного поиска и сравнения информации в системах RAG. Эмбеддинги позволяют сохранять семантическую информацию о тексте и обеспечивают более точные результаты при генерации ответов на основе извлеченной информации. Идея: похожие тексты -> похожие vectors. Это основа семантического поиска
class EmbeddingService:
    # Инициализация модели для генерации эмбеддингов. Размер embedding vector для модели "paraphrase-multilingual-MiniLM-L12-v2" составляет 384. Это означает, что каждый текст будет представлен в виде вектора из 384 чисел, которые отражают его семантическое содержание
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    @staticmethod
    def generate_embedding(text: str) -> list[float]:
        # Генерация эмбеддинга для данного текста с помощью модели SentenceTransformer
        embedding = EmbeddingService.model.encode(text)
        # Преобразование эмбеддинга в список чисел для удобства хранения и передачи
        return embedding.tolist()
