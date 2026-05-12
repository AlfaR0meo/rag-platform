from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings


# Настройка хеширования паролей
pwd_context = CryptContext(
    # Указываем алгоритмы хеширования, которые будут использоваться для паролей
    schemes=["bcrypt"],
    deprecated="auto",
)

# Хеширование пароля с помощью выбранного алгоритма
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Проверка соответствия введенного пароля и хешированного пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Создание JWT токена с указанием субъекта и времени истечения срока действия
def create_access_token(
    subject: str | Any,
    expires_delta: timedelta | None = None,
) -> str:
    # Вычисляем время истечения срока действия токена, добавляя expires_delta к текущему времени. Если expires_delta не предоставлено, используем значение по умолчанию из настроек приложения.
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Создаем словарь to_encode, который будет содержать данные для кодирования в JWT токен. В данном случае, мы добавляем время истечения срока действия токена (exp) и идентификатор субъекта (sub), который обычно представляет собой уникальный идентификатор пользователя или его email.
    to_encode = {
        "exp": expire,
        "sub": str(subject),
    }

    # Кодируем данные в JWT токен с использованием секретного ключа и алгоритма, указанных в настройках приложения. Функция jwt.encode принимает словарь данных для кодирования, секретный ключ и алгоритм, и возвращает сгенерированный JWT токен в виде строки.
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
