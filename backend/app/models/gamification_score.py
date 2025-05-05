from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class GamificationScoreBase(BaseModel):
    animal_id: UUID = Field(..., description="ID do animal que recebeu os pontos")
    meta_id: Optional[UUID] = Field(None, description="ID da meta relacionada (se aplicável)")
    atividade_realizada_id: Optional[UUID] = Field(None, description="ID da atividade realizada relacionada (se aplicável)")
    pontos_obtidos: int = Field(..., example=100)
    data: datetime = Field(..., example="2023-11-12T10:30:00Z")
    descricao: Optional[str] = Field(None, example="Meta semanal de caminhadas alcançada")

class GamificationScoreCreate(GamificationScoreBase):
    pass

# Não há PUT/PATCH definido para pontuações na documentação da Sprint 6
# class GamificationScoreUpdate(BaseModel):
#    pass

class GamificationScoreResponse(GamificationScoreBase):
    id: UUID
    meta_descricao: Optional[str] = Field(None, example="Realizar caminhadas 4x por semana", description="Descrição da meta (populada no endpoint)")
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True 