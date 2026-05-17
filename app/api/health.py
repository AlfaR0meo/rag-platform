from fastapi import APIRouter


router = APIRouter(prefix="/health", tags=["Health"])

# Эндпоинт для проверки состояния сервиса
@router.get("/")
def health_check():
    return {
        "status": "ok"
    }
