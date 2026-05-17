# Константы, используемые в приложении

# Максимально допустимый размер файла для загрузки
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

# Разрешенные расширения для загрузки документов
ALLOWED_EXTENSIONS = {
    ".txt",
    ".md",
    ".pdf",
}

# Разрешенные MIME-типы для загрузки документов
ALLOWED_MIME_TYPES = {
    "text/plain",
    "text/markdown",
    "application/pdf",
}
