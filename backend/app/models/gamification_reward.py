from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class GamificationRewardBase(BaseModel):
    nome: str = Field(..., example="Desconto de 10% em banho")
    pontos_necessarios: int = Field(..., example=500)
    tipo: Optional[str] = Field(None, example="desconto")
    descricao: Optional[str] = Field(None, example="Desconto de 10% em serviço de banho e tosa na clínica")

class GamificationRewardCreate(GamificationRewardBase):
    pass

class GamificationRewardUpdate(BaseModel):
    nome: Optional[str] = Field(None, example="Desconto de 15% em banho")
    pontos_necessarios: Optional[int] = Field(None, example=600)
    tipo: Optional[str] = Field(None, example="desconto")
    descricao: Optional[str] = Field(None, example="Desconto de 15% em serviço de banho e tosa na clínica")

class GamificationRewardResponse(GamificationRewardBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 