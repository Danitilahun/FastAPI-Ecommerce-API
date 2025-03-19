from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import List
from app.schemas.orders import OrderBase


# Base
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


class Signup(BaseModel):
    full_name: str
    username: str
    email: EmailStr  
    password: constr(min_length=8)

    class Config(BaseConfig):
        pass


class UserOut(BaseModel):
    message: str
    data: UserBase

    class Config(BaseConfig):
        pass


# Token
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    expires_in: int
