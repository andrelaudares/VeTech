from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime, date

class ActivityPlanBase(BaseModel):
    animal_id: UUID
    clinic_id: UUID
    atividade_id: UUID
    data_inicio: date
    data_fim: Optional[date] = None
    orientacoes: Optional[str] = Field(None, example="Aumentar gradualmente a intensidade")
    status: str = Field(..., example="ativo")
    frequencia_semanal: Optional[int] = Field(None, example=3)
    duracao_minutos: Optional[int] = Field(None, example=20)
    intensidade: Optional[str] = Field(None, example="leve")

class ActivityPlanCreate(ActivityPlanBase):
    pass

class ActivityPlanUpdate(BaseModel):
    atividade_id: Optional[UUID] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    orientacoes: Optional[str] = Field(None, example="Manter intensidade")
    status: Optional[str] = Field(None, example="inativo")
    frequencia_semanal: Optional[int] = Field(None, example=4)
    duracao_minutos: Optional[int] = Field(None, example=25)
    intensidade: Optional[str] = Field(None, example="moderada")

class ActivityPlanResponse(ActivityPlanBase):
    id: UUID
    nome_atividade: Optional[str] = Field(None, example="Caminhada") # Campo adicional populado no endpoint
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 