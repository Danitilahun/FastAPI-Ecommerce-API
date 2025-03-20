from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.users import UserCreate, UserUpdate
from app.utils.responses import ResponseHandler
from app.core.security import get_password_hash


class UserService:
    @staticmethod
    def get_all_users(db: Session, page: int, limit: int, search: str = "", role: str = "user"):
        users = db.query(User).order_by(User.id.asc()).filter(
            User.username.contains(search), User.role == role).limit(limit).offset((page - 1) * limit).all()
        return {"message": f"Page {page} with {limit} users", "data": users}

    @staticmethod
    def get_user(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            ResponseHandler.not_found_error("User", user_id)
        return ResponseHandler.get_single_success(user.username, user_id, user)

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        db_user = User(id=None, **user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return ResponseHandler.create_success(db_user.username, db_user.id, db_user)

    @staticmethod
    def update_user(db: Session, user_id: int, updated_user: UserUpdate):
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            ResponseHandler.not_found_error("User", user_id)

        if updated_user.email and updated_user.email != db_user.email:
            existing_user = db.query(User).filter(User.email == updated_user.email).first()
            if existing_user:
                raise ResponseHandler.conflict_error("Email is already in use")

        if updated_user.username and updated_user.username != db_user.username:
            existing_user = db.query(User).filter(User.username == updated_user.username).first()
            if existing_user:
                raise ResponseHandler.conflict_error("Username is already in use")

        if updated_user.full_name:
            db_user.full_name = updated_user.full_name
        if updated_user.email:
            db_user.email = updated_user.email
        if updated_user.username:
            db_user.username = updated_user.username
        if updated_user.password:
            db_user.password = get_password_hash(updated_user.password)

        db.commit()
        db.refresh(db_user)

        return ResponseHandler.update_success(db_user.username, db_user.id, db_user)

    @staticmethod
    def delete_user(db: Session, user_id: int):
        # Query the user by ID
        db_user = db.query(User).filter(User.id == user_id).first()

        # If the user doesn't exist, raise a not found error
        if not db_user:
            ResponseHandler.not_found_error("User", user_id)

        # Delete the user from the database
        db.delete(db_user)
        
        # Commit the deletion
        db.commit()

        # Return a success response with the user's information
        return ResponseHandler.delete_success(db_user.username, db_user.id, db_user)

