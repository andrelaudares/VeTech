from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class GamificationGoalBase(BaseModel):
    clinic_id: Optional[UUID] = Field(None, description="ID da clínica associada (opcional na criação, obtido do token)")
    descricao: str = Field(..., example="Realizar caminhadas 5x por semana")
    tipo: str = Field(..., example="atividade", description="Tipo de meta (ex: atividade, alimentacao, peso, consulta)")
    quantidade: int = Field(..., example=5)
    unidade: str = Field(..., example="caminhadas")
    periodo: Optional[str] = Field(None, example="semanal", description="Período da meta (ex: diario, semanal, mensal)")
    pontos_recompensa: int = Field(..., example=100)
    status: Optional[str] = Field("ativa", example="ativa", description="Status da meta (ativa, inativa)")

class GamificationGoalCreate(GamificationGoalBase):
    clinic_id: UUID # Obrigatório no body da requisição POST conforme documentação

class GamificationGoalUpdate(BaseModel):
    descricao: Optional[str] = Field(None, example="Realizar caminhadas 4x por semana")
    tipo: Optional[str] = Field(None, example="atividade")
    quantidade: Optional[int] = Field(None, example=4)
    unidade: Optional[str] = Field(None, example="caminhadas")
    periodo: Optional[str] = Field(None, example="semanal")
    pontos_recompensa: Optional[int] = Field(None, example=80)
    status: Optional[str] = Field(None, example="ativa")

class GamificationGoalResponse(GamificationGoalBase):
    id: UUID
    # clinic_id é herdado de GamificationGoalBase
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 