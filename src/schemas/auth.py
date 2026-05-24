from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, examples=["John Doe"])
    email: EmailStr = Field(..., examples=["john.doe@example.com"])
    password: str = Field(..., min_length=6, max_length=32, examples=["securepassword"])

class UserLogin(BaseModel):
    email: EmailStr= Field(..., examples=["john.doe@example.com"])
    password: str = Field(..., examples=["securepassword"])

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: UUID
    name:str

