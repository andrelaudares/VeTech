from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
import bcrypt

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str
    password: str = Field(..., min_length=6)  # Mantemos para validação, mas não será armazenado
    phone: str = Field(..., min_length=10, max_length=15)
    subscription_tier: Literal["basic", "premium", "enterprise"] = "basic"

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    created_at: Optional[datetime] = None

class ClinicProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=15)

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