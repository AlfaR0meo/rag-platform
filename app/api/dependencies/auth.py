from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.dependencies import get_db
from app.models.user import User

# OAuth2PasswordBearer - это класс, предоставляемый FastAPI для обработки аутентификации с помощью OAuth2 и JWT токенов. Он позволяет легко извлекать токен из заголовка Authorization в формате Bearer и использовать его для получения текущего пользователя. В данном случае, мы указываем URL для получения токена (tokenUrl="auth/login"), что означает, что пользователи должны отправлять свои учетные данные на этот URL, чтобы получить JWT токен для последующей аутентификации при доступе к защищенным маршрутам API. Это упрощает процесс аутентификации и обеспечивает безопасность, гарантируя, что только авторизованные пользователи могут получить доступ к определенным ресурсам.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Функция для получения текущего пользователя из JWT токена, который передается в заголовке Authorization в формате Bearer. Эта функция декодирует токен, извлекает из него идентификатор пользователя (user_id) и затем выполняет запрос к базе данных для получения информации о пользователе. Если токен недействителен или пользователь не найден, функция выбрасывает исключение HTTP 401 Unauthorized, что обеспечивает безопасность доступа к защищенным маршрутам API.
def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    # Объект исключение для невалидных токенов
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    # Проверяем наличие секретного ключа
    if not settings.JWT_SECRET_KEY:
        raise credentials_exception
    
    # Декодируем токен и извлекаем user_id    
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception
    # Если токен не может быть декодирован, выбрасываем исключение
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    # Если пользователь не найден, выбрасываем исключение
    if user is None:
        raise credentials_exception

    # Если пользователь найден, возвращаем его объект
    return user
