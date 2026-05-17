from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user
from app.models.user import User


router = APIRouter(prefix="/users", tags=["Users"])


# Эндпоинт для получения информации о текущем пользователе
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
    }
