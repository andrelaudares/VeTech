from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime

# Modelo para criar uma nova consulta
class ConsultationCreate(BaseModel):
    animal_id: UUID4
    description: Optional[str] = None
    # A data será definida como padrão no servidor, mas pode ser enviada opcionalmente
    date: Optional[datetime] = Field(default_factory=datetime.utcnow)

# Modelo para atualizar uma consulta (apenas descrição por enquanto)
class ConsultationUpdate(BaseModel):
    description: Optional[str] = None
    date: Optional[datetime] = None

# Modelo para a resposta da API
class ConsultationResponse(BaseModel):
    id: UUID4
    clinic_id: UUID4 # Adicionando clinic_id na resposta
    animal_id: UUID4
    date: datetime
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True # Compatibilidade com ORM, embora estejamos usando cliente direto 