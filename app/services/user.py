from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.models import User
from app.schemas.auth import UserCreate, UserResponse
from app.services.auth import AuthService

class UserService:
    @staticmethod
    def create_user(user: UserCreate, db: Session) -> UserResponse:
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = AuthService.get_password_hash(user.password)
        db_user = User(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return UserResponse(email=db_user.email, is_active=db_user.is_active)

    @staticmethod
    def list_users(db: Session) -> list[UserResponse]:
        users = db.query(User).all()
        return [UserResponse(email=user.email, is_active=user.is_active) for user in users]
