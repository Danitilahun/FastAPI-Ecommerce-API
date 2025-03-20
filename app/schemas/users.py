from pydantic import BaseModel , EmailStr
from typing import List, Optional
from datetime import datetime
from app.schemas.orders import OrderBase


class BaseConfig:
    from_attributes = True


class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    password: str
    role: str
    is_active: bool
    created_at: datetime
    orders: List[OrderBase]

    class Config(BaseConfig):
        pass


class UserCreate(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str

    class Config(BaseConfig):
        pass


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None 

    class Config:
        from_attributes = True



class UserOut(BaseModel):
    message: str
    data: UserBase

    class Config(BaseConfig):
        pass


class UsersOut(BaseModel):
    message: str
    data: List[UserBase]

    class Config(BaseConfig):
        pass


class UserOutDelete(BaseModel):
    message: str
    data: UserBase

    class Config(BaseConfig):
        pass
