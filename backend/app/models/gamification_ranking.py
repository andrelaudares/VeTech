from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

class RankingEntry(BaseModel):
    posicao: int = Field(..., example=1)
    animal_id: UUID
    animal_nome: Optional[str] = Field(None, example="Rex")
    pontos_totais: int = Field(..., example=750)
    clinic_id: Optional[UUID] = None
    clinic_nome: Optional[str] = Field(None, example="Clínica VetExemplo")

class RankingResponse(BaseModel):
    ranking: List[RankingEntry] 