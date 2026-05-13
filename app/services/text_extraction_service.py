from pathlib import Path
from pypdf import PdfReader

# Сервис для извлечения текста из документов
class TextExtractionService:

    # Извлечение текста из файла
    @staticmethod
    def extract_text(file_path: str) -> str:
        # Получаем расширение файла
        extension = Path(file_path).suffix.lower()

        if extension in {".txt", ".md"}:
            return TextExtractionService._extract_txt(file_path)

        if extension == ".pdf":
            return TextExtractionService._extract_pdf(file_path)

        raise ValueError("Unsupported file type")

    # Извлечение текста из текстового файла
    @staticmethod
    def _extract_txt(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    # Извлечение текста из PDF файла
    @staticmethod
    def _extract_pdf(file_path: str) -> str:
        # Используем pypdf для извлечения текста из PDF
        reader = PdfReader(file_path)
        # Инициализируем пустую строку для хранения извлеченного текста
        text = ""

        # Проходим по каждой странице PDF и извлекаем текст
        for page in reader.pages:
            # Извлекаем текст с текущей страницы
            extracted = page.extract_text()

            # Если текст был извлечен, добавляем его к общей строке
            if extracted:
                text += extracted + "\n"

        # Возвращаем весь извлеченный текст
        return text
