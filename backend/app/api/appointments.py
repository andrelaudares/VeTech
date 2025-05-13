from fastapi import APIRouter, HTTPException, Query, Body, Path, Depends
from typing import Dict, Any, List, Optional
from ..models.appointment import AppointmentCreate, AppointmentResponse, AppointmentUpdate
from ..db.supabase import supabase_admin
from uuid import UUID
import logging
from datetime import date, time, datetime
import httpx
from ..api.auth import get_current_user

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
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Cria um novo agendamento para um animal da clínica autenticada.
    """
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID da clínica não encontrado no token")

    logger.info(f"Requisição para criar agendamento para clinic_id: {clinic_id}")
    
    try:
        # 1. Verificar se o animal existe
        animal_id = str(appointment.animal_id)
        logger.info(f"Verificando animal ID: {animal_id}")
        
        # Consulta direta usando supabase_admin._request
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{str(clinic_id)}&select=id"
        )
        
        # Tratar a resposta para verificar se o animal existe
        animal_result = supabase_admin.process_response(animal_response)

        if not animal_result:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")
        
        # 2. Verificar conflitos de horário
        appointments_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/appointments?clinic_id=eq.{str(clinic_id)}&date=eq.{appointment.date.isoformat()}&status=eq.scheduled&select=*"
        )
        
        # Tratar a resposta para verificar conflitos
        appointments_result = supabase_admin.process_response(appointments_response)
        
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
        new_appointment = supabase_admin.process_response(new_appointment_response, single_item=True)
        
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
    animal_id: Optional[UUID] = Query(None, description="Filtrar por ID do animal"),
    date_from: Optional[date] = Query(None, description="Filtrar a partir desta data"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Obtém todos os agendamentos da clínica autenticada, com filtros opcionais.
    """
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID da clínica não encontrado no token")

    logger.info(f"Listando agendamentos para clinic_id: {clinic_id} com filtros animal_id={animal_id}, date_from={date_from}, status={status}")

    try:
        # Construir a query base
        query = f"/rest/v1/appointments?clinic_id=eq.{str(clinic_id)}"
        
        # Adicionar filtros opcionais
        if animal_id:
            query += f"&animal_id=eq.{str(animal_id)}"
        if date_from:
            query += f"&date=gte.{date_from.isoformat()}"
        if status:
            query += f"&status=eq.{status}"
            
        # Adicionar ordenação
        query += "&order=date.asc,start_time.asc"
        query += "&select=*"
        
        # Log da query final
        logger.debug(f"Executando query Supabase: {query}")

        response = await supabase_admin._request("GET", query)
        
        # Tratar a resposta para garantir que retornamos uma lista
        result = supabase_admin.process_response(response)
        
        logger.info(f"Encontrados {len(result)} agendamentos com os filtros aplicados")
        return result
        
    except Exception as e:
        logger.error(f"Erro ao buscar agendamentos: {e}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_detail = f"{error_detail} - Response: {e.response.text}"
        raise HTTPException(status_code=500, detail=f"Erro ao buscar agendamentos: {error_detail}")

@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: UUID = Path(..., description="ID do agendamento"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Obtém um agendamento específico pelo ID, verificando se pertence à clínica.
    """
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID da clínica não encontrado no token")

    logger.info(f"Buscando agendamento {appointment_id} para clinic_id: {clinic_id}")

    try:
        # Buscar pelo ID do agendamento, **filtrando também por clinic_id**
        response = await supabase_admin._request(
            "GET",
            f"/rest/v1/appointments?id=eq.{str(appointment_id)}&clinic_id=eq.{str(clinic_id)}&select=*"
        )
        
        # Tratar a resposta para extrair o agendamento
        appointment_data = supabase_admin.process_response(response, single_item=True)

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
    appointment_id: UUID = Path(..., description="ID do agendamento"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Remove um agendamento pelo ID, verificando se pertence à clínica.
    """
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID da clínica não encontrado no token")

    logger.info(f"Deletando agendamento {appointment_id} da clinic_id: {clinic_id}")

    try:
        # Verificar se o agendamento existe **e pertence à clínica**
        appointment_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/appointments?id=eq.{str(appointment_id)}&clinic_id=eq.{str(clinic_id)}&select=id"
        )
        
        # Tratar a resposta para verificar se o agendamento existe
        appointment = supabase_admin.process_response(appointment_response)

        if not appointment:
            logger.warning(f"Agendamento {appointment_id} não encontrado ou não pertence à clínica {clinic_id}.")
            raise HTTPException(status_code=404, detail="Agendamento não encontrado ou não pertence à clínica")
        
        # Deletar o agendamento **filtrando por clinic_id**
        await supabase_admin._request(
            "DELETE",
            f"/rest/v1/appointments?id=eq.{str(appointment_id)}&clinic_id=eq.{str(clinic_id)}"
        )
        
        # Verificar se realmente foi deletado (opcional)
        get_again_response = await supabase_admin._request("GET", f"/rest/v1/appointments?id=eq.{str(appointment_id)}&clinic_id=eq.{str(clinic_id)}&select=id")
        if supabase_admin.process_response(get_again_response):
            logger.error(f"Erro ao deletar agendamento {appointment_id}: ainda encontrado após DELETE.")
            raise HTTPException(status_code=500, detail="Erro interno: Falha ao deletar o agendamento.")

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
    appointment_update: AppointmentUpdate = Body(...),
    appointment_id: UUID = Path(..., description="ID do agendamento"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza um agendamento existente, verificando se pertence à clínica.
    """
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID da clínica não encontrado no token")

    logger.info(f"Atualizando agendamento {appointment_id} para clinic_id: {clinic_id}")

    try:
        # Verificar se o agendamento existe **e pertence à clínica**
        current_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/appointments?id=eq.{str(appointment_id)}&clinic_id=eq.{str(clinic_id)}&select=*"
        )
        current = supabase_admin.process_response(current_response)

        if not current:
            logger.warning(f"Agendamento {appointment_id} não encontrado ou não pertence à clínica {clinic_id} para atualização.")
            raise HTTPException(status_code=404, detail="Agendamento não encontrado ou não pertence à clínica")

        current_appointment = current[0]
        # clinic_id já foi verificado acima e obtido do token
        # clinic_id = current_appointment.get("clinic_id")

        update_data = {}
        for field, value in appointment_update.model_dump(exclude_unset=True).items():
            if isinstance(value, (date, time)):
                 update_data[field] = value.isoformat()
            else:
                 update_data[field] = value

        # Serializar date e time para string ISO format se presentes
        if 'date' in update_data and update_data['date'] is not None:
            try:
                # Validar e converter a string de data recebida
                parsed_date = date.fromisoformat(update_data['date'])
                update_data['date'] = parsed_date.isoformat() # Manter como string ISO para Supabase
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Formato de data inválido para '{update_data['date']}'. Use YYYY-MM-DD.")
        elif 'date' in update_data and update_data['date'] is None:
            # Se o cliente enviou date: null, remover ou converter para None
            # A API Supabase espera 'null' literal, mas vamos remover por segurança
             del update_data['date']

        if 'start_time' in update_data and isinstance(update_data['start_time'], time):
            update_data['start_time'] = update_data['start_time'].isoformat()

        if not update_data:
            logger.warning(f"Nenhum dado fornecido para atualização do agendamento {appointment_id}")
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        # Verificar conflito de horário, se data/hora forem atualizados
        if "date" in update_data or "start_time" in update_data:
            new_date = update_data.get("date", current_appointment["date"])
            new_start_str = update_data.get("start_time", current_appointment["start_time"])
            # A lógica de verificação de conflito precisa ser robusta
            # Buscando outros agendamentos no mesmo dia para a clínica
            if clinic_id:
                conflict_check_query = (
                    f"/rest/v1/appointments?clinic_id=eq.{clinic_id}"
                    f"&date=eq.{new_date}"
                    f"&status=eq.scheduled" # Apenas conflita com agendamentos ativos
                    f"&id=neq.{appointment_id}" # Exclui o próprio agendamento
                    f"&select=id,start_time,end_time"
                )
                other_apps_resp = await supabase_admin._request("GET", conflict_check_query)
                other_apps = supabase_admin.process_response(other_apps_resp)

                new_start_time_obj = datetime.strptime(new_start_str, '%H:%M:%S').time()
                new_end_time_str = update_data.get("end_time", current_appointment.get("end_time"))
                new_end_time_obj = datetime.strptime(new_end_time_str, '%H:%M:%S').time() if new_end_time_str else None

                for app in other_apps:
                    app_start_time = datetime.strptime(app["start_time"], '%H:%M:%S').time()
                    app_end_time_str = app.get("end_time")
                    app_end_time = datetime.strptime(app_end_time_str, '%H:%M:%S').time() if app_end_time_str else None

                    # Lógica de verificação de sobreposição
                    # Caso 1: Ambos têm hora de fim
                    if new_end_time_obj and app_end_time:
                        if max(new_start_time_obj, app_start_time) < min(new_end_time_obj, app_end_time):
                             logger.warning(f"Conflito de horário detectado para {appointment_id} com {app['id']}")
                             raise HTTPException(status_code=400, detail="Horário conflita com outro agendamento")
                    # Caso 2: Um ou ambos não têm hora de fim (considera conflito se início for igual)
                    elif new_start_time_obj == app_start_time:
                         logger.warning(f"Conflito de horário (início igual) detectado para {appointment_id} com {app['id']}")
                         raise HTTPException(status_code=400, detail="Horário de início conflita com outro agendamento")

        # Atualizar usando PATCH e Prefer: return=representation
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"
        update_response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/appointments?id=eq.{str(appointment_id)}&clinic_id=eq.{clinic_id}",
            json=update_data,
            headers=headers
        )

        updated_appointment_data = supabase_admin.process_response(update_response)

        if not updated_appointment_data:
            logger.error(f"Agendamento {appointment_id} não encontrado após atualização ou erro na resposta.")
            # Tentar buscar novamente como fallback?
            fallback_get = await supabase_admin._request("GET", f"/rest/v1/appointments?id=eq.{str(appointment_id)}&clinic_id=eq.{clinic_id}&select=*")
            fallback_data = supabase_admin.process_response(fallback_get)
            if not fallback_data:
                raise HTTPException(status_code=500, detail="Erro ao buscar agendamento após atualização")

        logger.info(f"Agendamento {appointment_id} atualizado com sucesso.")
        return updated_appointment_data[0]

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao atualizar agendamento {appointment_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar agendamento: {str(e)}") 