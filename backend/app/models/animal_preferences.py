from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class PetPreferencesCreate(BaseModel):
    """Modelo para criação de preferências alimentares"""
    gosta_de: Optional[str] = None
    nao_gosta_de: Optional[str] = None

class PetPreferencesUpdate(BaseModel):
    """Modelo para atualização de preferências alimentares"""
    gosta_de: Optional[str] = None
    nao_gosta_de: Optional[str] = None

class PetPreferencesResponse(BaseModel):
    """Modelo para resposta de preferências alimentares"""
    id: UUID4
    animal_id: UUID4
    gosta_de: Optional[str] = None
    nao_gosta_de: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None 