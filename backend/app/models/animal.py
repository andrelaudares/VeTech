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

class AnimalResponse(BaseModel):
    id: UUID4
    clinics_id: UUID4
    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    medical_history: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None 