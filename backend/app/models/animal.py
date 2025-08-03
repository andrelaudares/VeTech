from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime, date

class AnimalCreate(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    medical_history: Optional[str] = None
    date_birth: Optional[date] = None
    tutor_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

# Novo modelo para atualização, permitindo campos opcionais
class AnimalUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    medical_history: Optional[str] = None
    date_birth: Optional[date] = None
    tutor_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    
    class Config:
        from_attributes = True  # Pydantic v2 - substitui orm_mode

class AnimalResponse(BaseModel):
    id: UUID4
    clinic_id: UUID4
    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    medical_history: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    date_birth: Optional[date] = None
    tutor_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    tutor_user_id: Optional[UUID4] = None  # Novo campo para vincular com auth.users
    client_active: Optional[bool] = None
    client_activated_at: Optional[datetime] = None
    client_last_login: Optional[datetime] = None
    gamification_level: Optional[int] = None
    total_points: Optional[int] = None
    gamification_points: Optional[int] = None

# Modelo para ativação de cliente
class ClientActivationRequest(BaseModel):
    tutor_name: str
    email: str
    phone: Optional[str] = None
    password: Optional[str] = None  # Campo opcional para senha
    generate_password: bool = True  # Indica se deve gerar senha automaticamente
    temporary_password: bool = False  # Indica se é senha temporária

class ClientActivationResponse(BaseModel):
    success: bool
    message: str
    user_id: Optional[UUID4] = None  # ID do usuário criado em auth.users
    login_url: Optional[str] = None
    temporary_password: Optional[str] = None  # Senha temporária gerada

# Modelo para alternar status do cliente
class ClientStatusToggleRequest(BaseModel):
    active: bool

class ClientStatusToggleResponse(BaseModel):
    success: bool
    message: str
    client_active: bool

# Modelo para informações do cliente
class ClientInfoResponse(BaseModel):
    tutor_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    tutor_user_id: Optional[UUID4] = None
    client_active: bool
    client_activated_at: Optional[datetime] = None
    client_last_login: Optional[datetime] = None