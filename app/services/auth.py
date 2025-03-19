from fastapi import HTTPException, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.models import User
from app.db.database import get_db
from app.core.security import verify_password, get_user_token, get_token_payload
from app.core.security import get_password_hash
from app.utils.responses import ResponseHandler
from app.schemas.auth import Signup


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    @staticmethod
    async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
        user = db.query(User).filter(User.username == user_credentials.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

        if not verify_password(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

        return await get_user_token(id=user.id)

    @staticmethod
    async def signup(db: Session, user: Signup):
        existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username or email already exists."
            )
        
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        
        db_user = User(id=None, **user.model_dump())
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return ResponseHandler.create_success(db_user.username, db_user.id, db_user)
    
    @staticmethod
    async def create_admin(db: Session, user: Signup):
        existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username or email already exists."
            )
        
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        
        db_user = User(id=None, **user.model_dump())
        db_user.role = "admin"
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return ResponseHandler.create_success(db_user.username, db_user.id, db_user)


    @staticmethod
    async def get_refresh_token(token: str, db: Session):
        try:
            print("token", token)
            payload = get_token_payload(token)
            user_id = payload.get("id")
            print(f"Payload: {payload}, User ID: {user_id}")
            
            if not user_id:
                raise ResponseHandler.invalid_token("refresh")
                
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                raise ResponseHandler.invalid_token("refresh")
                
            return await get_user_token(user.id)
        except Exception as e:
            print(f"Error: {str(e)}")
            raise ResponseHandler.invalid_token("refresh")


