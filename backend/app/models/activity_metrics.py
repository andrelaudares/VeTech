from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import date

class WeeklyProgress(BaseModel):
    semana: date = Field(..., description="Data de início da semana (segunda-feira)")
    minutos: int = Field(..., description="Total de minutos de atividade na semana")
    atividades: int = Field(..., description="Número de atividades realizadas na semana")

class ActivityMetricsResponse(BaseModel):
    total_atividades: int = Field(..., description="Total de atividades realizadas no período")
    total_minutos: int = Field(..., description="Total de minutos de atividade no período")
    media_minutos_por_atividade: Optional[float] = Field(None, description="Média de minutos por atividade")
    calorias_estimadas: Optional[float] = Field(None, description="Total de calorias estimadas gastas no período")
    completude_plano: Optional[float] = Field(None, description="Percentual de dias com atividade realizada vs. dias esperados no período")
    atividades_por_tipo: Dict[str, int] = Field(..., description="Contagem de atividades realizadas por tipo/nome")
    progresso_semanal: List[WeeklyProgress] = Field(..., description="Progresso de atividades por semana")

    class Config:
        orm_mode = True # Embora não seja diretamente do ORM, pode ser útil 