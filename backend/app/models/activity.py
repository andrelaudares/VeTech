from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class ActivityBase(BaseModel):
    nome: str = Field(..., example="Caminhada")
    tipo: str = Field(..., example="cardiovascular")
    calorias_estimadas_por_minuto: Optional[int] = Field(None, example=5)

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    nome: Optional[str] = Field(None, example="Caminhada Leve")
    tipo: Optional[str] = Field(None, example="cardiovascular")
    calorias_estimadas_por_minuto: Optional[int] = Field(None, example=4)

class ActivityResponse(ActivityBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 