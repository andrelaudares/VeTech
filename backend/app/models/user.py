from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import bcrypt

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)  # Mantemos para validação, mas não será armazenado
    phone: str = Field(..., min_length=10, max_length=15)

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str
    created_at: Optional[datetime] = None

def hash_password(password: str) -> str:
    """Gera o hash da senha usando bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta"""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    ) 