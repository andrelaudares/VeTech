"""
Rotas de consultas específicas para clientes/tutores
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import date, datetime as DateTime
from pydantic import BaseModel
from ..auth import get_current_user
from ...db.supabase import supabase_admin as supabase

router = APIRouter()

class ConsultationResponse(BaseModel):
    """Modelo de resposta para consultas do cliente"""
    id: int
    animal_id: int
    animal_name: str
    veterinarian_name: str
    date: str
    time: str
    reason: str
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    observations: Optional[str] = None
    next_appointment: Optional[str] = None
    status: str
    created_at: str
    updated_at: str

class ConsultationSummary(BaseModel):
    """Modelo de resumo de consultas"""
    total_consultations: int
    recent_consultations: List[ConsultationResponse]
    animals_with_consultations: int
    last_consultation_date: Optional[str] = None

@router.get("/", response_model=List[ConsultationResponse])
async def get_client_consultations(
    current_user: dict = Depends(get_current_user),
    animal_id: Optional[int] = Query(None, description="Filtrar por animal específico"),
    date_from: Optional[date] = Query(None, description="Data inicial"),
    date_to: Optional[date] = Query(None, description="Data final"),
    limit: int = Query(50, description="Limite de resultados")
):
    """
    Lista todas as consultas dos animais do cliente/tutor
    """
    try:
        query = supabase.table("consultations").select("""
            id,
            animal_id,
            veterinarian_name,
            date,
            time,
            reason,
            diagnosis,
            treatment,
            observations,
            next_appointment,
            status,
            created_at,
            updated_at,
            animals!inner(
                id,
                name,
                tutor_id
            )
        """).eq("animals.tutor_id", current_user["id"])
        
        # Aplicar filtros
        if animal_id:
            query = query.eq("animal_id", animal_id)
            
        if date_from:
            query = query.gte("date", date_from.isoformat())
            
        if date_to:
            query = query.lte("date", date_to.isoformat())
        
        # Ordenar por data (mais recentes primeiro)
        query = query.order("date", desc=True).order("time", desc=True)
        
        # Aplicar limite
        query = query.limit(limit)
        
        result = query.execute()
        
        # Formatar resposta
        consultations = []
        for consultation in result.data:
            consultations.append(ConsultationResponse(
                id=consultation["id"],
                animal_id=consultation["animal_id"],
                animal_name=consultation["animals"]["name"],
                veterinarian_name=consultation["veterinarian_name"],
                date=consultation["date"],
                time=consultation["time"],
                reason=consultation["reason"],
                diagnosis=consultation.get("diagnosis"),
                treatment=consultation.get("treatment"),
                observations=consultation.get("observations"),
                next_appointment=consultation.get("next_appointment"),
                status=consultation["status"],
                created_at=consultation["created_at"],
                updated_at=consultation["updated_at"]
            ))
        
        return consultations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consultas: {str(e)}")

@router.get("/{consultation_id}", response_model=ConsultationResponse)
async def get_consultation_details(
    consultation_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtém detalhes de uma consulta específica
    """
    try:
        result = supabase.table("consultations").select("""
            id,
            animal_id,
            veterinarian_name,
            date,
            time,
            reason,
            diagnosis,
            treatment,
            observations,
            next_appointment,
            status,
            created_at,
            updated_at,
            animals!inner(
                id,
                name,
                tutor_id
            )
        """).eq("id", consultation_id).eq("animals.tutor_id", current_user["id"]).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Consulta não encontrada")
        
        consultation = result.data[0]
        
        return ConsultationResponse(
            id=consultation["id"],
            animal_id=consultation["animal_id"],
            animal_name=consultation["animals"]["name"],
            veterinarian_name=consultation["veterinarian_name"],
            date=consultation["date"],
            time=consultation["time"],
            reason=consultation["reason"],
            diagnosis=consultation.get("diagnosis"),
            treatment=consultation.get("treatment"),
            observations=consultation.get("observations"),
            next_appointment=consultation.get("next_appointment"),
            status=consultation["status"],
            created_at=consultation["created_at"],
            updated_at=consultation["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consulta: {str(e)}")

@router.get("/animal/{animal_id}", response_model=List[ConsultationResponse])
async def get_animal_consultations(
    animal_id: int,
    current_user: dict = Depends(get_current_user),
    limit: int = Query(20, description="Limite de resultados")
):
    """
    Lista consultas de um animal específico
    """
    try:
        # Verificar se o animal pertence ao tutor
        animal_check = supabase.table("animals").select("id").eq(
            "id", animal_id
        ).eq("tutor_id", current_user["id"]).execute()
        
        if not animal_check.data:
            raise HTTPException(status_code=404, detail="Animal não encontrado")
        
        result = supabase.table("consultations").select("""
            id,
            animal_id,
            veterinarian_name,
            date,
            time,
            reason,
            diagnosis,
            treatment,
            observations,
            next_appointment,
            status,
            created_at,
            updated_at,
            animals!inner(
                id,
                name,
                tutor_id
            )
        """).eq("animal_id", animal_id).order("date", desc=True).limit(limit).execute()
        
        # Formatar resposta
        consultations = []
        for consultation in result.data:
            consultations.append(ConsultationResponse(
                id=consultation["id"],
                animal_id=consultation["animal_id"],
                animal_name=consultation["animals"]["name"],
                veterinarian_name=consultation["veterinarian_name"],
                date=consultation["date"],
                time=consultation["time"],
                reason=consultation["reason"],
                diagnosis=consultation.get("diagnosis"),
                treatment=consultation.get("treatment"),
                observations=consultation.get("observations"),
                next_appointment=consultation.get("next_appointment"),
                status=consultation["status"],
                created_at=consultation["created_at"],
                updated_at=consultation["updated_at"]
            ))
        
        return consultations
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consultas do animal: {str(e)}")

@router.get("/summary/overview", response_model=ConsultationSummary)
async def get_consultations_summary(
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna um resumo das consultas do cliente
    """
    try:
        # Contar total de consultas
        total_result = supabase.table("consultations").select("id", count="exact").eq(
            "animals.tutor_id", current_user["id"]
        ).execute()
        
        # Buscar consultas recentes (últimas 5)
        recent_result = supabase.table("consultations").select("""
            id,
            animal_id,
            veterinarian_name,
            date,
            time,
            reason,
            diagnosis,
            treatment,
            observations,
            next_appointment,
            status,
            created_at,
            updated_at,
            animals!inner(
                id,
                name,
                tutor_id
            )
        """).eq("animals.tutor_id", current_user["id"]).order(
            "date", desc=True
        ).limit(5).execute()
        
        # Contar animais com consultas
        animals_result = supabase.table("consultations").select(
            "animal_id", count="exact"
        ).eq("animals.tutor_id", current_user["id"]).execute()
        
        # Última consulta
        last_consultation = None
        if recent_result.data:
            last_consultation = recent_result.data[0]["date"]
        
        # Formatar consultas recentes
        recent_consultations = []
        for consultation in recent_result.data:
            recent_consultations.append(ConsultationResponse(
                id=consultation["id"],
                animal_id=consultation["animal_id"],
                animal_name=consultation["animals"]["name"],
                veterinarian_name=consultation["veterinarian_name"],
                date=consultation["date"],
                time=consultation["time"],
                reason=consultation["reason"],
                diagnosis=consultation.get("diagnosis"),
                treatment=consultation.get("treatment"),
                observations=consultation.get("observations"),
                next_appointment=consultation.get("next_appointment"),
                status=consultation["status"],
                created_at=consultation["created_at"],
                updated_at=consultation["updated_at"]
            ))
        
        # Contar animais únicos com consultas
        unique_animals = len(set(c.animal_id for c in recent_consultations))
        
        return ConsultationSummary(
            total_consultations=total_result.count or 0,
            recent_consultations=recent_consultations,
            animals_with_consultations=unique_animals,
            last_consultation_date=last_consultation
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar resumo: {str(e)}")