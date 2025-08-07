"""
Rotas de agendamentos específicas para clientes/tutores
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import date, datetime as DateTime
from pydantic import BaseModel
from ..auth import get_current_user
from ...db.supabase import supabase_admin as supabase

router = APIRouter()

class AppointmentResponse(BaseModel):
    """Modelo de resposta para agendamentos do cliente"""
    id: int
    animal_id: int
    animal_name: str
    service: str
    date: str
    time: str
    status: str
    notes: Optional[str] = None
    created_at: str
    updated_at: str

@router.get("/", response_model=List[AppointmentResponse])
async def get_client_appointments(
    current_user: dict = Depends(get_current_user),
    animal_id: Optional[int] = Query(None, description="Filtrar por animal específico"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    date_from: Optional[date] = Query(None, description="Data inicial"),
    date_to: Optional[date] = Query(None, description="Data final"),
    limit: int = Query(50, description="Limite de resultados")
):
    """
    Lista todos os agendamentos do cliente/tutor
    """
    try:
        # Buscar agendamentos do tutor
        query = supabase.table("appointments").select("""
            id,
            animal_id,
            service,
            date,
            time,
            status,
            notes,
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
        
        if status:
            query = query.eq("status", status)
            
        if date_from:
            query = query.gte("date", date_from.isoformat())
            
        if date_to:
            query = query.lte("date", date_to.isoformat())
        
        # Ordenar por data e hora
        query = query.order("date", desc=True).order("time", desc=True)
        
        # Aplicar limite
        query = query.limit(limit)
        
        result = query.execute()
        
        # Formatar resposta
        appointments = []
        for appointment in result.data:
            appointments.append(AppointmentResponse(
                id=appointment["id"],
                animal_id=appointment["animal_id"],
                animal_name=appointment["animals"]["name"],
                service=appointment["service"],
                date=appointment["date"],
                time=appointment["time"],
                status=appointment["status"],
                notes=appointment.get("notes"),
                created_at=appointment["created_at"],
                updated_at=appointment["updated_at"]
            ))
        
        return appointments
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar agendamentos: {str(e)}")

@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment_details(
    appointment_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtém detalhes de um agendamento específico
    """
    try:
        # Verificar se o agendamento pertence ao tutor
        result = supabase.table("appointments").select("""
            id,
            animal_id,
            service,
            date,
            time,
            status,
            notes,
            created_at,
            updated_at,
            animals!inner(
                id,
                name,
                tutor_id
            )
        """).eq("id", appointment_id).eq("animals.tutor_id", current_user["id"]).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
        
        appointment = result.data[0]
        
        return AppointmentResponse(
            id=appointment["id"],
            animal_id=appointment["animal_id"],
            animal_name=appointment["animals"]["name"],
            service=appointment["service"],
            date=appointment["date"],
            time=appointment["time"],
            status=appointment["status"],
            notes=appointment.get("notes"),
            created_at=appointment["created_at"],
            updated_at=appointment["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar agendamento: {str(e)}")

@router.get("/upcoming/count")
async def get_upcoming_appointments_count(
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna a contagem de agendamentos futuros do cliente
    """
    try:
        today = DateTime.now().date().isoformat()
        
        result = supabase.table("appointments").select("id", count="exact").eq(
            "animals.tutor_id", current_user["id"]
        ).gte("date", today).eq("status", "scheduled").execute()
        
        return {"count": result.count}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar agendamentos: {str(e)}")