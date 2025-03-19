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
        db_user = User(email=user.email, username=user.username,  password=hashed_password, full_name= user.full_name , is_active = True)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return UserResponse(
             id=db_user.id,
             username=db_user.username,
             email=db_user.email,
             full_name=db_user.full_name,
             is_active=db_user.is_active,
             created_at=str(db_user.created_at),
             role=str(db_user.role),
        )

    @staticmethod
    def list_users(db: Session) -> list[UserResponse]:
        users = db.query(User).all()
        return [UserResponse(email=user.email, is_active=user.is_active) for user in users]
