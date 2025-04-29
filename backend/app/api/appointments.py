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
        animal_response = await supabase_admin._request(
            "GET", 
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{str(clinic_id)}&select=*"
        )
        
        # Tratar a resposta para verificar se o animal existe
        animal_result = []
        if isinstance(animal_response, list):
            animal_result = animal_response
        elif isinstance(animal_response, dict) and 'data' in animal_response and isinstance(animal_response['data'], list):
            animal_result = animal_response['data']
        
        if not animal_result or len(animal_result) == 0:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")
        
        # 2. Verificar conflitos de horário
        appointments_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/appointments?clinic_id=eq.{str(clinic_id)}&date=eq.{appointment.date.isoformat()}&status=eq.scheduled&select=*"
        )
        
        # Tratar a resposta para verificar conflitos
        appointments_result = []
        if isinstance(appointments_response, list):
            appointments_result = appointments_response
        elif isinstance(appointments_response, dict) and 'data' in appointments_response and isinstance(appointments_response['data'], list):
            appointments_result = appointments_response['data']
        
        # Verificação manual de conflito
        if appointments_result:
            for existing in appointments_result:
                # Verificar se end_time existe e não é nulo em ambos os registros
                existing_end_time = existing.get("end_time")
                appointment_end_time = appointment.end_time
                
                # Se algum dos horários de término for nulo, não podemos verificar conflito completamente
                if existing_end_time is None or appointment_end_time is None:
                    # Se os horários de início coincidem, consideramos conflito
                    if existing["start_time"] == appointment.start_time.isoformat():
                        raise HTTPException(status_code=400, detail="Já existe um agendamento neste horário de início")
                    # Caso contrário, permitimos o agendamento (risco de sobreposição)
                    continue
                
                # Verificação normal de conflito quando ambos end_time estão presentes
                if (existing["start_time"] <= appointment_end_time.isoformat() and
                    existing_end_time >= appointment.start_time.isoformat()):
                    raise HTTPException(status_code=400, detail="Já existe um agendamento neste horário")
        
        # 3. Inserir o agendamento
        appointment_data = {
            "clinic_id": str(clinic_id),
            "animal_id": animal_id,
            "date": appointment.date.isoformat(),
            "start_time": appointment.start_time.isoformat(),
            "description": appointment.description,
            "status": appointment.status
        }
        
        # Adicionar end_time apenas se não for nulo
        if appointment.end_time is not None:
            appointment_data["end_time"] = appointment.end_time.isoformat()
        
        new_appointment_response = await supabase_admin._request(
            "POST",
            "/rest/v1/appointments",
            json=appointment_data
        )
        
        # Tratar a resposta do POST
        new_appointment = None
        if isinstance(new_appointment_response, list) and len(new_appointment_response) > 0:
            new_appointment = new_appointment_response[0]
        elif isinstance(new_appointment_response, dict):
            if 'data' in new_appointment_response and isinstance(new_appointment_response['data'], list) and len(new_appointment_response['data']) > 0:
                new_appointment = new_appointment_response['data'][0]
            else:
                # Caso seja um objeto único diretamente
                new_appointment = new_appointment_response
        
        if new_appointment:
            logger.info(f"Agendamento criado com sucesso: {new_appointment}")
            return new_appointment
        else:
            logger.error(f"Erro ao criar agendamento. Resposta inesperada: {new_appointment_response}")
            raise HTTPException(status_code=500, detail="Erro ao criar agendamento. Resposta inesperada do servidor.")
            
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao criar agendamento: {e}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_detail = f"{error_detail} - Response: {e.response.text}"
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {error_detail}")

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
        
        response = await supabase_admin._request("GET", query)
        
        # Tratar a resposta para garantir que retornamos uma lista
        result = []
        if isinstance(response, list):
            result = response
        elif isinstance(response, dict) and 'data' in response and isinstance(response['data'], list):
            result = response['data']
        
        logger.info(f"Encontrados {len(result)} agendamentos")
        return result
        
    except Exception as e:
        logger.error(f"Erro ao buscar agendamentos: {e}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_detail = f"{error_detail} - Response: {e.response.text}"
        raise HTTPException(status_code=500, detail=f"Erro ao buscar agendamentos: {error_detail}")

@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: UUID = Path(..., description="ID do agendamento")
) -> Dict[str, Any]:
    """
    Obtém um agendamento específico pelo ID.
    """
    try:
        # Buscar pelo ID do agendamento, sem filtrar por clinic_id
        response = await supabase_admin._request(
            "GET",
            f"/rest/v1/appointments?id=eq.{str(appointment_id)}&select=*"
        )
        
        # Tratar a resposta para extrair o agendamento
        appointment_data = None
        if isinstance(response, list) and len(response) > 0:
            appointment_data = response[0]
        elif isinstance(response, dict) and 'data' in response and isinstance(response['data'], list) and len(response['data']) > 0:
            appointment_data = response['data'][0]
            
        if appointment_data:
            logger.info(f"Agendamento {appointment_id} encontrado: {appointment_data}")
            return appointment_data
        else:
            logger.warning(f"Agendamento {appointment_id} não encontrado. Resposta: {response}")
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao buscar agendamento {appointment_id}: {e}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_detail = f"{error_detail} - Response: {e.response.text}"
        raise HTTPException(status_code=500, detail=f"Erro ao buscar agendamento: {error_detail}")

@router.delete("/{appointment_id}", response_model=Dict[str, str])
async def delete_appointment(
    appointment_id: UUID = Path(..., description="ID do agendamento")
) -> Dict[str, str]:
    """
    Remove um agendamento pelo ID.
    """
    try:
        # Verificar se o agendamento existe (sem filtrar por clinic_id)
        appointment_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/appointments?id=eq.{str(appointment_id)}&select=id"
        )
        
        # Tratar a resposta para verificar se o agendamento existe
        appointment = []
        if isinstance(appointment_response, list):
            appointment = appointment_response
        elif isinstance(appointment_response, dict) and 'data' in appointment_response and isinstance(appointment_response['data'], list):
            appointment = appointment_response['data']
            
        if not appointment or len(appointment) == 0:
            logger.warning(f"Agendamento {appointment_id} não encontrado.")
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
        
        # Deletar o agendamento sem filtrar por clinic_id
        await supabase_admin._request(
            "DELETE", 
            f"/rest/v1/appointments?id=eq.{str(appointment_id)}"
        )
        
        logger.info(f"Agendamento {appointment_id} removido com sucesso")
        return {"message": "Agendamento removido com sucesso"}
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao deletar agendamento {appointment_id}: {e}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_detail = f"{error_detail} - Response: {e.response.text}"
        raise HTTPException(status_code=500, detail=f"Erro ao deletar agendamento: {error_detail}")

@router.patch("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_update: AppointmentUpdate,
    appointment_id: UUID = Path(..., description="ID do agendamento")
) -> Dict[str, Any]:
    """
    Atualiza um agendamento existente.
    """
    try:
        # Verificar se o agendamento existe
        current_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/appointments?id=eq.{str(appointment_id)}&select=*"
        )
        
        # Tratar a resposta para verificar se o agendamento existe
        current = []
        if isinstance(current_response, list):
            current = current_response
        elif isinstance(current_response, dict) and 'data' in current_response and isinstance(current_response['data'], list):
            current = current_response['data']
            
        if not current or len(current) == 0:
            logger.warning(f"Agendamento {appointment_id} não encontrado")
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
        
        current_appointment = current[0]
        clinic_id = current_appointment.get("clinic_id")  # Obtém o clinic_id do agendamento original
        
        # Preparar dados para atualização
        update_data = {}
        for field, value in appointment_update.model_dump(exclude_unset=True).items():
            if value is not None:
                if isinstance(value, (date, time)):
                    update_data[field] = value.isoformat()
                else:
                    update_data[field] = value
            # Caso especial: se o valor for explicitamente definido como None para end_time,
            # incluímos isso na atualização para permitir remover o horário de término
            elif field == "end_time" and field in appointment_update.model_dump():
                update_data[field] = None
                    
        if not update_data:
            logger.warning(f"Nenhum dado fornecido para atualização do agendamento {appointment_id}")
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")
        
        # Verificar conflito de horário, se necessário
        if "date" in update_data or "start_time" in update_data or "end_time" in update_data:
            new_date = update_data.get("date", current_appointment["date"])
            new_start = update_data.get("start_time", current_appointment["start_time"])
            new_end = update_data.get("end_time", current_appointment.get("end_time"))
            
            # Buscar outros agendamentos no mesmo dia para a clínica do agendamento original
            if clinic_id:
                other_appointments_response = await supabase_admin._request(
                    "GET",
                    f"/rest/v1/appointments?clinic_id=eq.{str(clinic_id)}&date=eq.{new_date}&status=eq.scheduled&select=*"
                )
                
                # Tratar a resposta
                other_appointments = []
                if isinstance(other_appointments_response, list):
                    other_appointments = other_appointments_response
                elif isinstance(other_appointments_response, dict) and 'data' in other_appointments_response and isinstance(other_appointments_response['data'], list):
                    other_appointments = other_appointments_response['data']
                
                # Verificar conflitos
                for app in other_appointments:
                    if app["id"] == str(appointment_id):
                        continue  # Pular o próprio agendamento
                    
                    # Verificar se end_time existe e não é nulo em ambos os registros
                    app_end_time = app.get("end_time")
                    
                    # Se algum dos horários de término for nulo, não podemos verificar conflito completamente
                    if app_end_time is None or new_end is None:
                        # Se os horários de início coincidem, consideramos conflito
                        if app["start_time"] == new_start:
                            logger.warning(f"Horário de início {new_start} conflita com agendamento existente {app['id']}")
                            raise HTTPException(status_code=400, detail="Horário de início conflita com outro agendamento")
                        # Caso contrário, permitimos o agendamento (risco de sobreposição)
                        continue
                        
                    # Verificação normal de conflito quando ambos end_time estão presentes
                    if (app["start_time"] <= new_end and app_end_time >= new_start):
                        logger.warning(f"Horário {new_start}-{new_end} conflita com agendamento existente {app['id']}")
                        raise HTTPException(status_code=400, detail="Horário conflita com outro agendamento")
        
        # Atualizar
        update_response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/appointments?id=eq.{str(appointment_id)}",
            json=update_data
        )
        
        # Tratar a resposta do PATCH
        updated_appointment = None
        if isinstance(update_response, list) and len(update_response) > 0:
            updated_appointment = update_response[0]
        elif isinstance(update_response, dict) and 'data' in update_response and isinstance(update_response['data'], list) and len(update_response['data']) > 0:
            updated_appointment = update_response['data'][0]
        
        # Se conseguimos obter a resposta diretamente do PATCH, retornamos ela
        if updated_appointment:
            logger.info(f"Agendamento {appointment_id} atualizado com sucesso: {updated_appointment}")
            return updated_appointment
        
        # Se não, fazemos um GET para buscar os dados atualizados
        updated_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/appointments?id=eq.{str(appointment_id)}&select=*"
        )
        
        # Tratar a resposta do GET
        updated = []
        if isinstance(updated_response, list):
            updated = updated_response
        elif isinstance(updated_response, dict) and 'data' in updated_response and isinstance(updated_response['data'], list):
            updated = updated_response['data']
        
        if not updated or len(updated) == 0:
            logger.error(f"Agendamento {appointment_id} não encontrado após atualização")
            raise HTTPException(status_code=500, detail="Erro ao buscar agendamento atualizado")
        
        logger.info(f"Agendamento {appointment_id} atualizado com sucesso: {updated[0]}")
        return updated[0]
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao atualizar agendamento {appointment_id}: {e}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_detail = f"{error_detail} - Response: {e.response.text}"
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar agendamento: {error_detail}") 