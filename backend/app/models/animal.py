from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class AnimalCreate(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    medical_history: Optional[str] = None

# Novo modelo para atualização, permitindo campos opcionais
class AnimalUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    medical_history: Optional[str] = None

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