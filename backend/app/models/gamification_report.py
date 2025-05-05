from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from uuid import UUID
from datetime import date

class ReportAnimalInfo(BaseModel):
    id: UUID
    nome: Optional[str] = Field(None, example="Rex")
    tutor: Optional[str] = Field(None, example="João Silva")

class ReportPeriod(BaseModel):
    inicio: date = Field(..., example="2023-09-01")
    fim: date = Field(..., example="2023-11-30")

class ReportSummary(BaseModel):
    pontos_acumulados: int = Field(..., example=1250)
    recompensas_resgatadas: int = Field(..., example=2)
    metas_concluidas: int = Field(..., example=15)

class ReportCategoryProgress(BaseModel):
    total_metas: int = Field(..., example=6)
    concluidas: int = Field(..., example=5)
    percentual: Optional[float] = Field(None, example=83.3)

class ReportProgressByCategory(BaseModel):
    atividade: Optional[ReportCategoryProgress] = None
    alimentacao: Optional[ReportCategoryProgress] = None
    consulta: Optional[ReportCategoryProgress] = None
    peso: Optional[ReportCategoryProgress] = None
    # Adicionar outras categorias conforme necessário

class ReportMonthlyDetailItem(BaseModel):
    descricao: str = Field(..., example="Realizar caminhadas 4x por semana")
    semanas_concluidas: Optional[int] = Field(None, example=3)
    total_semanas: Optional[int] = Field(None, example=4)
    # Outros detalhes relevantes da meta

class ReportMonthlyDetail(BaseModel):
    mes: str = Field(..., example="Setembro/2023")
    pontos: int = Field(..., example=400)
    metas_concluidas: int = Field(..., example=5)
    metas_detalhadas: List[ReportMonthlyDetailItem] = []

class GamificationReportResponse(BaseModel):
    animal: ReportAnimalInfo
    periodo: ReportPeriod
    resumo: ReportSummary
    progresso_por_categoria: ReportProgressByCategory
    detalhamento_mensal: List[ReportMonthlyDetail] = []
    recomendacoes: List[str] = Field([], example=["Aumentar frequência de atividades aeróbicas"]) 