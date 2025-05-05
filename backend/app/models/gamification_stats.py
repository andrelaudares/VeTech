from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class GoalProgress(BaseModel):
    meta_id: UUID
    descricao: str = Field(..., example="Realizar caminhadas 4x por semana")
    progresso_atual: Optional[int] = Field(None, example=3)
    meta_total: Optional[int] = Field(None, example=4)
    percentual: Optional[float] = Field(None, example=75.0)
    status: str = Field(..., example="em_andamento")

class PointsHistory(BaseModel):
    data: datetime = Field(..., example="2023-11-12T10:30:00Z")
    pontos: int = Field(..., example=100)

class GamificationStatsResponse(BaseModel):
    pontos_totais: int = Field(..., example=750, description="Total de pontos acumulados pelo animal")
    pontos_periodo: int = Field(..., example=250, description="Pontos ganhos no período solicitado")
    pontos_disponiveis: int = Field(..., example=500, description="Pontos disponíveis para resgate (Total - Usados)")
    recompensas_resgatadas: int = Field(..., example=1, description="Número de recompensas já resgatadas")
    metas_concluidas: int = Field(..., example=5, description="Número de metas concluídas no período")
    metas_em_andamento: int = Field(..., example=2, description="Número de metas atualmente em andamento")
    progresso_metas: List[GoalProgress] = Field([], description="Lista com o progresso em cada meta ativa")
    historico_pontos: List[PointsHistory] = Field([], description="Histórico de pontos ganhos no período") 