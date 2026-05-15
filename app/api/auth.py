from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.auth import UserRegister, TokenResponse
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    try:
        user = AuthService.register_user(
            db=db,
            email=user_data.email,
            password=user_data.password,
        )

        return {
            "id": user.id,
            "email": user.email,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        token = AuthService.authenticate_user(
            db=db,
            email=form_data.username,
            password=form_data.password,
        )

        return {
            "access_token": token
        }
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )
    