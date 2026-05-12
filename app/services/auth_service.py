from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User


class AuthService:

    @staticmethod
    def register_user(db: Session, email: str, password: str) -> User:
        existing_user = db.query(User).filter(
            User.email == email
        ).first()

        if existing_user:
            raise ValueError("User already exists")

        user = User(
            email=email,
            hashed_password=hash_password(password),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> str:
        user = db.query(User).filter(
            User.email == email
        ).first()

        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        return create_access_token(subject=user.id)
