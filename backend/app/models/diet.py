from pydantic import BaseModel, UUID4, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time

# Modelo para criação/atualização de dietas
class DietCreate(BaseModel):
    """Modelo para criação de dietas para pets"""
    nome: str
    tipo: str = Field(..., description="'caseira' ou 'ração'")
    objetivo: str = Field(..., description="Ex: 'Emagrecimento', 'Doença Renal', 'Nutrição'")
    data_inicio: date
    data_fim: Optional[date] = None
    status: str = "ativa"  # ativo, inativo, concluído
    refeicoes_por_dia: int
    calorias_totais_dia: Optional[int] = None
    valor_mensal_estimado: Optional[float] = None
    alimento_id: Optional[int] = None
    quantidade_gramas: Optional[int] = None
    horario: Optional[str] = None

class DietUpdate(BaseModel):
    """Modelo para atualização de dietas para pets"""
    nome: Optional[str] = None
    tipo: Optional[str] = None
    objetivo: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    status: Optional[str] = None
    refeicoes_por_dia: Optional[int] = None
    calorias_totais_dia: Optional[int] = None
    valor_mensal_estimado: Optional[float] = None
    alimento_id: Optional[int] = None
    quantidade_gramas: Optional[int] = None
    horario: Optional[time] = None

# Modelo para alimentos a evitar
class RestrictedFoodCreate(BaseModel):
    """Modelo para criação de alimentos a evitar"""
    nome: str
    motivo: Optional[str] = None

class RestrictedFoodUpdate(BaseModel):
    """Modelo para atualização de alimentos a evitar"""
    nome: Optional[str] = None
    motivo: Optional[str] = None

# Modelos de resposta
class RestrictedFoodResponse(BaseModel):
    """Modelo para resposta de alimentos a evitar"""
    id: UUID4
    animal_id: UUID4
    nome: str
    motivo: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class DietResponse(BaseModel):
    """Modelo para resposta de dietas"""
    id: UUID4
    animal_id: UUID4
    clinic_id: UUID4
    nome: str
    tipo: str
    objetivo: str
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    status: str
    refeicoes_por_dia: Optional[int] = None
    calorias_totais_dia: Optional[int] = None
    valor_mensal_estimado: Optional[float] = None
    alimento_id: Optional[int] = None
    alimento_nome: Optional[str] = None
    quantidade_gramas: Optional[int] = None
    horario: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Pydantic v2 - substitui orm_mode

# Modelo para progresso da dieta
class DietProgressCreate(BaseModel):
    """Modelo para criação de progresso de dieta"""
    animal_id: str
    dieta_id: str
    opcao_dieta_id: Optional[str] = None
    data: date
    refeicao_completa: Optional[bool] = None
    horario_realizado: Optional[time] = None
    quantidade_consumida: Optional[str] = None
    observacoes_tutor: Optional[str] = None
    pontos_ganhos: Optional[int] = None

class DietProgressUpdate(BaseModel):
    """Modelo para atualização de progresso de dieta"""
    opcao_dieta_id: Optional[str] = None
    data: Optional[date] = None
    refeicao_completa: Optional[bool] = None
    horario_realizado: Optional[time] = None
    quantidade_consumida: Optional[str] = None
    observacoes_tutor: Optional[str] = None
    pontos_ganhos: Optional[int] = None

class DietProgressResponse(BaseModel):
    """Modelo para resposta de registro de progresso da dieta"""
    id: UUID4
    animal_id: UUID4
    dieta_id: UUID4
    data: date
    refeicao_completa: bool
    horario_realizado: Optional[str] = None
    quantidade_consumida: Optional[str] = None
    observacoes_tutor: Optional[str] = None
    pontos_ganhos: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Pydantic v2 - substitui orm_mode

# Modelos para alimentos base
class AlimentoBaseCreate(BaseModel):
    """Modelo para criação de alimentos base"""
    nome: str
    tipo: str
    especie_destino: str
    marca: Optional[str] = None
    linha: Optional[str] = None
    subtipo: Optional[str] = None
    kcal_por_kg: Optional[float] = None
    kcal_por_100g: Optional[float] = None
    kcal_por_50g: Optional[float] = None
    origem_caloria: Optional[str] = None
    fonte: Optional[str] = None
    fonte_url: Optional[str] = None
    observacoes: Optional[str] = None

class AlimentoBaseUpdate(BaseModel):
    """Modelo para atualização de alimentos base"""
    nome: Optional[str] = None
    tipo: Optional[str] = None
    especie_destino: Optional[str] = None
    marca: Optional[str] = None
    linha: Optional[str] = None
    subtipo: Optional[str] = None
    kcal_por_kg: Optional[float] = None
    kcal_por_100g: Optional[float] = None
    kcal_por_50g: Optional[float] = None
    origem_caloria: Optional[str] = None
    fonte: Optional[str] = None
    fonte_url: Optional[str] = None
    observacoes: Optional[str] = None

class AlimentoBaseResponse(BaseModel):
    """Modelo para resposta de alimentos base"""
    id: Optional[UUID4] = None
    alimento_id: Optional[int] = None
    nome: str
    tipo: str
    especie_destino: str
    # Alinhar com colunas existentes na tabela (kcal_por_*). Tornar opcional para evitar 500.
    calorias_por_100g: Optional[float] = None
    kcal_por_100g: Optional[float] = None
    kcal_por_50g: Optional[float] = None
    kcal_por_kg: Optional[float] = None
    proteinas_por_100g: Optional[float] = None
    gorduras_por_100g: Optional[float] = None
    carboidratos_por_100g: Optional[float] = None
    fibras_por_100g: Optional[float] = None
    minerais: Optional[Dict[str, float]] = None
    vitaminas: Optional[Dict[str, float]] = None
    marca: Optional[str] = None
    linha: Optional[str] = None
    subtipo: Optional[str] = None
    origem_caloria: Optional[str] = None
    fonte: Optional[str] = None
    fonte_url: Optional[str] = None
    observacoes: Optional[str] = None
    contraindicacoes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Pydantic v2 - substitui orm_mode
