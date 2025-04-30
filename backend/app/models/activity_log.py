from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime, date

class ActivityLogBase(BaseModel):
    plano_id: UUID
    animal_id: UUID
    data: date
    realizado: bool = Field(..., example=True)
    duracao_realizada_minutos: Optional[int] = Field(None, example=22)
    observacao_tutor: Optional[str] = Field(None, example="Animal apresentou boa disposição")

class ActivityLogCreate(ActivityLogBase):
    pass

class ActivityLogUpdate(BaseModel):
    data: Optional[date] = None
    realizado: Optional[bool] = Field(None, example=False)
    duracao_realizada_minutos: Optional[int] = Field(None, example=25)
    observacao_tutor: Optional[str] = Field(None, example="Cansou no final")

class ActivityLogResponse(ActivityLogBase):
    id: UUID
    nome_atividade: Optional[str] = Field(None, example="Caminhada") # Campo adicional populado no endpoint
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 