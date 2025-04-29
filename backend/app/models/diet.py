from pydantic import BaseModel, UUID4, Field
from typing import Optional, List
from datetime import datetime, date

# Modelo para criação/atualização de dietas
class DietCreate(BaseModel):
    """Modelo para criação de dietas para pets"""
    tipo: str = Field(..., description="'caseira' ou 'ração'")
    objetivo: str = Field(..., description="Ex: 'Emagrecimento', 'Doença Renal', 'Nutrição'")
    observacoes: Optional[str] = None
    data_inicio: date
    data_fim: Optional[date] = None
    status: str = Field(default="ativa", description="'ativa', 'finalizada', 'aguardando_aprovacao'")

class DietUpdate(BaseModel):
    """Modelo para atualização de dietas para pets"""
    tipo: Optional[str] = None
    objetivo: Optional[str] = None
    observacoes: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    status: Optional[str] = None

# Modelo para opções de dieta
class DietOptionCreate(BaseModel):
    """Modelo para criação de opções de dieta"""
    nome: str = Field(..., description="Nome da opção (ex: 'Ração Premium Light')")
    valor_mensal_estimado: float
    calorias_totais_dia: int
    porcao_refeicao: str = Field(..., description="Ex: '200g ou 2 scoops por refeição'")
    refeicoes_por_dia: int
    indicacao: Optional[str] = None

class DietOptionUpdate(BaseModel):
    """Modelo para atualização de opções de dieta"""
    nome: Optional[str] = None
    valor_mensal_estimado: Optional[float] = None
    calorias_totais_dia: Optional[int] = None
    porcao_refeicao: Optional[str] = None
    refeicoes_por_dia: Optional[int] = None
    indicacao: Optional[str] = None

# Modelo para alimentos da dieta
class DietFoodCreate(BaseModel):
    """Modelo para criação de alimentos da dieta"""
    nome: str
    tipo: str = Field(..., description="'ração', 'caseira', 'complemento'")
    quantidade: str = Field(..., description="Ex: '200g', '2 scoops'")
    calorias: int
    horario: str = Field(..., description="Ex: 'Café', 'Almoço', 'Jantar'")

class DietFoodUpdate(BaseModel):
    """Modelo para atualização de alimentos da dieta"""
    nome: Optional[str] = None
    tipo: Optional[str] = None
    quantidade: Optional[str] = None
    calorias: Optional[int] = None
    horario: Optional[str] = None

# Modelo para alimentos a evitar
class RestrictedFoodCreate(BaseModel):
    """Modelo para criação de alimentos a evitar"""
    nome: str
    motivo: Optional[str] = None

class RestrictedFoodUpdate(BaseModel):
    """Modelo para atualização de alimentos a evitar"""
    nome: Optional[str] = None
    motivo: Optional[str] = None

# Modelo para snacks entre refeições
class SnackCreate(BaseModel):
    """Modelo para criação de snacks entre refeições"""
    nome: str
    frequencia_semanal: int
    quantidade: str = Field(..., description="Ex: '1 bifinho', '50g'")
    observacoes: Optional[str] = None

class SnackUpdate(BaseModel):
    """Modelo para atualização de snacks entre refeições"""
    nome: Optional[str] = None
    frequencia_semanal: Optional[int] = None
    quantidade: Optional[str] = None
    observacoes: Optional[str] = None

# Modelos de resposta
class DietOptionResponse(BaseModel):
    """Modelo para resposta de opções de dieta"""
    id: UUID4
    dieta_id: UUID4
    nome: str
    valor_mensal_estimado: float
    calorias_totais_dia: int
    porcao_refeicao: str
    refeicoes_por_dia: int
    indicacao: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class DietFoodResponse(BaseModel):
    """Modelo para resposta de alimentos da dieta"""
    id: UUID4
    opcao_dieta_id: UUID4
    nome: str
    tipo: str
    quantidade: str
    calorias: int
    horario: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class RestrictedFoodResponse(BaseModel):
    """Modelo para resposta de alimentos a evitar"""
    id: UUID4
    animal_id: UUID4
    nome: str
    motivo: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class SnackResponse(BaseModel):
    """Modelo para resposta de snacks entre refeições"""
    id: UUID4
    animal_id: UUID4
    nome: str
    frequencia_semanal: int
    quantidade: str
    observacoes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class DietResponse(BaseModel):
    """Modelo para resposta de dietas"""
    id: UUID4
    animal_id: UUID4
    clinic_id: UUID4
    tipo: str
    objetivo: str
    observacoes: Optional[str] = None
    data_inicio: date
    data_fim: Optional[date] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    opcoes_dieta: Optional[List[DietOptionResponse]] = None 