from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.documents import router as documents_router

from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(documents_router)

@app.get("/")
def root():
    return {
        "message": f"{settings.APP_NAME} 🚀"
    }
