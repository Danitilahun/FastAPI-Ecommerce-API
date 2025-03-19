from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    email: str
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str
