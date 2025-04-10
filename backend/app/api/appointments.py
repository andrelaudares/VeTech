from fastapi import APIRouter, HTTPException, Query, Body, Path
from typing import Dict, Any, List, Optional
from ..models.appointment import AppointmentCreate, AppointmentResponse, AppointmentUpdate
from ..db.supabase import supabase_admin
from uuid import UUID
import logging
from datetime import date, time
import httpx

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Definir o router
router = APIRouter()

# Rota de teste para verificar se o router está funcionando
@router.get("/test", response_model=Dict[str, str])
async def test_appointment_router():
    """
    Testa se o router de agendamentos está funcionando.
    """
    return {"status": "Router de agendamentos funcionando!"}

@router.post("", response_model=AppointmentResponse)
async def create_appointment(
    appointment: AppointmentCreate = Body(...),
    clinic_id: UUID = Query(..., description="ID da clínica")
) -> Dict[str, Any]:
    """
    Cria um novo agendamento para um animal.
    """
    logger.info(f"Requisição para criar agendamento para clinic_id: {clinic_id}")
    
    try:
        # 1. Verificar se o animal existe
        animal_id = str(appointment.animal_id)
        logger.info(f"Verificando animal ID: {animal_id}")
        
        # Consulta direta usando supabase_admin._request
        animal_result = await supabase_admin._request(
            "GET", 
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{str(clinic_id)}&select=*"
        )
        
        if not animal_result or len(animal_result) == 0:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")
        
        # 2. Verificar conflitos de horário
        appointments_result = await supabase_admin._request(
            "GET",
            f"/rest/v1/appointments?clinic_id=eq.{str(clinic_id)}&date=eq.{appointment.date.isoformat()}&status=eq.scheduled&select=*"
        )
        
        # Verificação manual de conflito
        if appointments_result:
            for existing in appointments_result:
                if (existing["start_time"] <= appointment.end_time.isoformat() and
                    existing["end_time"] >= appointment.start_time.isoformat()):
                    raise HTTPException(status_code=400, detail="Já existe um agendamento neste horário")
        
        # 3. Inserir o agendamento
        appointment_data = {
            "clinic_id": str(clinic_id),
            "animal_id": animal_id,
            "date": appointment.date.isoformat(),
            "start_time": appointment.start_time.isoformat(),
            "end_time": appointment.end_time.isoformat(),
            "description": appointment.description,
            "status": appointment.status
        }
        
        new_appointment = await supabase_admin._request(
            "POST",
            "/rest/v1/appointments",
            json=appointment_data
        )
        
        if new_appointment and len(new_appointment) > 0:
            return new_appointment[0]
        else:
            raise HTTPException(status_code=500, detail="Erro ao criar agendamento")
            
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")

@router.get("", response_model=List[AppointmentResponse])
async def get_appointments(
    clinic_id: UUID = Query(..., description="ID da clínica"),
    date_from: Optional[date] = Query(None, description="Filtrar a partir desta data"),
    status: Optional[str] = Query(None, description="Filtrar por status")
) -> List[Dict[str, Any]]:
    """
    Obtém todos os agendamentos de uma clínica.
    """
    try:
        # Construir a query
        query = f"/rest/v1/appointments?clinic_id=eq.{str(clinic_id)}"
        
        if date_from:
            query += f"&date=gte.{date_from.isoformat()}"
            
        if status:
            query += f"&status=eq.{status}"
            
        # Adicionar ordenação
        query += "&order=date.asc,start_time.asc"
        query += "&select=*"
        
        result = await supabase_admin._request("GET", query)
        
        if not result:
            return []
            
        return result
        
    except Exception as e:
        logger.error(f"Erro ao buscar agendamentos: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar agendamentos: {str(e)}")

@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: UUID = Path(..., description="ID do agendamento"),
    clinic_id: UUID = Query(..., description="ID da clínica")
) -> Dict[str, Any]:
    """
    Obtém um agendamento específico pelo ID.
    """
    try:
        result = await supabase_admin._request(
            "GET",
            f"/rest/v1/appointments?id=eq.{str(appointment_id)}&clinic_id=eq.{str(clinic_id)}&select=*"
        )
            
        if not result or len(result) == 0:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
            
        return result[0]
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao buscar agendamento: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar agendamento: {str(e)}")

@router.delete("/{appointment_id}", response_model=Dict[str, str])
async def delete_appointment(
    appointment_id: UUID = Path(..., description="ID do agendamento"),
    clinic_id: UUID = Query(..., description="ID da clínica")
) -> Dict[str, str]:
    """
    Remove um agendamento pelo ID.
    """
    try:
        # Verificar se existe
        appointment = await supabase_admin._request(
            "GET",
            f"/rest/v1/appointments?id=eq.{str(appointment_id)}&clinic_id=eq.{str(clinic_id)}&select=id"
        )
            
        if not appointment or len(appointment) == 0:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
        
        # Deletar
        await supabase_admin._request(
            "DELETE", 
            f"/rest/v1/appointments?id=eq.{str(appointment_id)}"
        )
        
        return {"message": "Agendamento removido com sucesso"}
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao deletar agendamento: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao deletar agendamento: {str(e)}")

@router.patch("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_update: AppointmentUpdate,
    appointment_id: UUID = Path(..., description="ID do agendamento"),
    clinic_id: UUID = Query(..., description="ID da clínica")
) -> Dict[str, Any]:
    """
    Atualiza um agendamento existente.
    """
    try:
        # Verificar se existe
        current = await supabase_admin._request(
            "GET",
            f"/rest/v1/appointments?id=eq.{str(appointment_id)}&clinic_id=eq.{str(clinic_id)}&select=*"
        )
            
        if not current or len(current) == 0:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
        
        current_appointment = current[0]
        
        # Preparar dados para atualização
        update_data = {}
        for field, value in appointment_update.model_dump(exclude_unset=True).items():
            if value is not None:
                if isinstance(value, (date, time)):
                    update_data[field] = value.isoformat()
                else:
                    update_data[field] = value
                    
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")
        
        # Verificar conflito de horário, se necessário
        if "date" in update_data or "start_time" in update_data or "end_time" in update_data:
            new_date = update_data.get("date", current_appointment["date"])
            new_start = update_data.get("start_time", current_appointment["start_time"])
            new_end = update_data.get("end_time", current_appointment["end_time"])
            
            # Buscar outros agendamentos no mesmo dia
            other_appointments = await supabase_admin._request(
                "GET",
                f"/rest/v1/appointments?clinic_id=eq.{str(clinic_id)}&date=eq.{new_date}&status=eq.scheduled&select=*"
            )
            
            # Verificar conflitos
            for app in other_appointments:
                if app["id"] == str(appointment_id):
                    continue  # Pular o próprio agendamento
                    
                if (app["start_time"] <= new_end and app["end_time"] >= new_start):
                    raise HTTPException(status_code=400, detail="Horário conflita com outro agendamento")
        
        # Atualizar
        await supabase_admin._request(
            "PATCH",
            f"/rest/v1/appointments?id=eq.{str(appointment_id)}",
            json=update_data
        )
        
        # Buscar dados atualizados
        updated = await supabase_admin._request(
            "GET",
            f"/rest/v1/appointments?id=eq.{str(appointment_id)}&select=*"
        )
        
        if not updated or len(updated) == 0:
            raise HTTPException(status_code=500, detail="Erro ao buscar agendamento atualizado")
            
        return updated[0]
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao atualizar agendamento: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar agendamento: {str(e)}") 