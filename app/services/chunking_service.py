# Сервис для разбиения текста на чанки. Чанки – это небольшие фрагменты текста, которые используются для эффективного хранения и обработки информации в системах RAG. Они позволяют сохранять контекст и обеспечивают более точные результаты при генерации ответов на основе извлеченной информации.
class ChunkingService:

    # Разбиение текста на чанки с заданным размером и перекрытием. Чанки очень важны для RAG, так как позволяют эффективно обрабатывать большие тексты и сохранять контекст при генерации ответов. Основные проблемы: если чанк слишком маленький, то теряется контекст; если слишком большой, то плохой retrieval.
    @staticmethod
    def chunk_text(
        text: str, 
        chunk_size: int = 500, 
        overlap: int = 100
    ) -> list[str]:
        
        chunks = []

        text_length = len(text)
        start = 0

        while start < text_length:

            end = start + chunk_size

            if end >= text_length:
                chunks.append(
                    text[start:].strip()
                )
                break

            adjusted_end = end

            while (
                adjusted_end < text_length
                and text[adjusted_end]
                not in [".", "!", "?", "\n"]
            ):
                adjusted_end += 1

            chunk = text[
                start:adjusted_end + 1
            ].strip()

            chunks.append(chunk)

            start = adjusted_end + 1 - overlap

            if start < 0:
                start = 0

        return chunks
