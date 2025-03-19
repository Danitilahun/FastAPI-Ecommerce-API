from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.auth import UserResponse
from app.services.user import UserService

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return UserService.list_users(db)