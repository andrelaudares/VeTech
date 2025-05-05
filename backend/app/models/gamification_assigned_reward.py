from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime, date

class AssignedRewardBase(BaseModel):
    animal_id: UUID
    recompensa_id: UUID
    pontos_utilizados: Optional[int] = Field(None, description="Pontos que foram usados para resgatar esta recompensa")
    data_atribuicao: Optional[datetime] = Field(None, description="Data em que a recompensa foi atribuída/resgatada")
    codigo_verificacao: Optional[str] = Field(None, example="DISCOUNT-123456", description="Código para validar a recompensa, se aplicável")
    data_expiracao: Optional[date] = Field(None, example="2023-12-31", description="Data de expiração da recompensa, se aplicável")
    observacoes: Optional[str] = Field(None, example="Apresentar código na clínica para receber o desconto")
    status: str = Field(..., example="disponivel", description="Status da recompensa atribuída (disponivel, utilizada, expirada)")

class AssignedRewardCreate(BaseModel):
    recompensa_id: UUID = Field(..., description="ID da recompensa a ser atribuída")
    codigo_verificacao: Optional[str] = Field(None, example="DISCOUNT-123456")
    data_expiracao: Optional[date] = Field(None, example="2023-12-31")
    observacoes: Optional[str] = Field(None, example="Apresentar código na clínica para receber o desconto")
    # animal_id vem do path, status é definido internamente
    # pontos_utilizados é definido internamente

class AssignedRewardResponse(AssignedRewardBase):
    id: UUID # ID do registro da atribuição (se for criada uma tabela)
    recompensa_nome: Optional[str] = Field(None, example="Desconto de 15% em banho", description="Nome da recompensa (populado no endpoint)")

    class Config:
        orm_mode = True 