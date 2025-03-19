from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool
    created_at: str
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
