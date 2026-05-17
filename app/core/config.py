from pydantic_settings import BaseSettings, SettingsConfigDict

# Конфигурация приложения, которая загружает настройки из переменных окружения и .env файла. Она включает в себя параметры для подключения к базе данных, настройки JWT, параметры для Qdrant и OpenRouter
class Settings(BaseSettings):
    APP_NAME: str = "RAG Platform API"
    APP_VERSION: str = "1.0.0"

    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    QDRANT_HOST: str
    QDRANT_PORT: int

    OPENROUTER_API_KEY: str
    OPENROUTER_MODEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

# Создаем экземпляр настроек, который будет использоваться во всем приложении для доступа к конфигурационным параметрам. Благодаря использованию Pydantic, все параметры будут автоматически загружены из переменных окружения или .env файла при инициализации экземпляра Settings. Если какие-то параметры не будут найдены, то будет выброшено исключение, что поможет избежать проблем с отсутствующими настройками в процессе выполнения приложения.
settings = Settings() # type: ignore
