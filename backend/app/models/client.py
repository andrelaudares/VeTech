"""
Modelos para autenticação e dados de clientes (tutores)
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

class ClientLoginData(BaseModel):
    """Dados de login para clientes"""
    email: EmailStr
    password: str

class ClientAuthResponse(BaseModel):
    """Resposta de autenticação para clientes"""
    access_token: str
    token_type: str = "bearer"
    user_type: str = "client"
    client: Dict[str, Any]

class ClientProfileUpdate(BaseModel):
    """Dados para atualização do perfil do cliente"""
    tutor_name: Optional[str] = None
    phone: Optional[str] = None

class AnimalUpdate(BaseModel):
    """Dados para atualização do animal pelo cliente"""
    name: Optional[str] = None
    weight: Optional[float] = None
    medical_history: Optional[str] = None

class DualLoginData(BaseModel):
    """Dados de login que funciona para clínicas e clientes"""
    email: EmailStr
    password: str
    user_type: Optional[str] = None  # 'clinic' ou 'client', opcional para auto-detecção

class UserTypeResponse(BaseModel):
    """Resposta da verificação de tipo de usuário"""
    user_type: str  # 'clinic' ou 'client'
    user_id: str
    email: str
    name: str
    redirect_url: str