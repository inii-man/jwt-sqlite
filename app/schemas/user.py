from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional

def validate_password_byte_length(cls, v):
    if len(v.encode('utf-8')) > 72:
        raise ValueError("Password must not exceed 72 bytes")
    return v

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    full_name: Optional[str] = None
    role: str = Field(default="user", pattern="^(admin|user|viewer)$")

    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        return validate_password_byte_length(cls, v)

class UserLogin(BaseModel):
    username: str
    password: str = Field(min_length=8, max_length=72)

    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        return validate_password_byte_length(cls, v)

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int
    username: str
    role: str