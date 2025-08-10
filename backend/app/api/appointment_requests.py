"""
API routes for appointment requests management.
Handles appointment requests from tutors and management by clinics.
Uses the appointments table with client-specific fields.
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Path
from typing import List, Dict, Any, Optional
from datetime import date as Date, datetime as DateTime, time as Time
from pydantic import BaseModel, Field, UUID4
import logging

from .auth import get_current_user
from ..db.supabase import supabase_admin

# Configurar logging
logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic models for appointment requests
class AppointmentRequestCreate(BaseModel):
    animal_id: UUID4 = Field(..., description="ID do animal")
    service: str = Field(..., description="Tipo de serviço solicitado")
    date: Date = Field(..., description="Data desejada")
    start_time: Time = Field(..., description="Horário desejado")
    end_time: Optional[Time] = Field(None, description="Horário de término")
    notes: Optional[str] = Field(None, description="Observações adicionais")
    priority: Optional[str] = Field("normal", description="Prioridade da solicitação")

class AppointmentRequestUpdate(BaseModel):
    service: Optional[str] = Field(None, description="Tipo de serviço")
    date: Optional[Date] = Field(None, description="Data")
    start_time: Optional[Time] = Field(None, description="Horário de início")
    end_time: Optional[Time] = Field(None, description="Horário de término")
    notes: Optional[str] = Field(None, description="Observações")
    priority: Optional[str] = Field(None, description="Prioridade")
    status: Optional[str] = Field(None, description="Status da solicitação")

class AppointmentRequestResponse(BaseModel):
    id: str  # UUID
    animal_id: str
    animal_name: Optional[str] = None
    tutor_name: Optional[str] = None
    tutor_email: Optional[str] = None
    service: str
    date: Date
    start_time: Time
    end_time: Optional[Time] = None
    notes: Optional[str] = None
    priority: str
    status: str
    status_solicitacao: str
    created_at: DateTime
    updated_at: Optional[DateTime] = None

@router.post("/", response_model=AppointmentRequestResponse)
async def create_appointment_request(
    request_data: AppointmentRequestCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Cria uma nova solicitação de agendamento na tabela appointments.
    Endpoint para tutores solicitarem agendamentos.
    """
    user_id = current_user.get("id")
    user_email = current_user.get("email")
    
    logger.info(f"Criando solicitação de agendamento para animal_id: {request_data.animal_id} por user: {user_email}")

    try:
        # Verificar se o animal pertence ao tutor
        animal_query = f"/rest/v1/animals?id=eq.{request_data.animal_id}&email=eq.{user_email}"
        animal_response = await supabase_admin._request("GET", animal_query)
        animal_data = supabase_admin.process_response(animal_response)
        
        if not animal_data:
            raise HTTPException(status_code=403, detail="Animal não encontrado ou não pertence ao usuário")
        
        animal = animal_data[0]
        
        # Verificar conflitos de horário básico
        end_time = request_data.end_time or Time(hour=request_data.start_time.hour + 1)
        
        conflict_query = f"/rest/v1/appointments?clinic_id=eq.{animal['clinic_id']}"
        conflict_query += f"&date=eq.{request_data.date.isoformat()}"
        conflict_query += f"&start_time=eq.{request_data.start_time.isoformat()}"
        conflict_query += "&status=in.(scheduled,confirmed)"
        
        conflict_response = await supabase_admin._request("GET", conflict_query)
        conflict_data = supabase_admin.process_response(conflict_response)
        
        if conflict_data:
            raise HTTPException(
                status_code=409, 
                detail="Já existe um agendamento para este horário"
            )
        
        # Preparar dados para inserção na tabela appointments
        insert_data = {
            "clinic_id": animal["clinic_id"],
            "animal_id": str(request_data.animal_id),
            "date": request_data.date.isoformat(),
            "start_time": request_data.start_time.isoformat(),
            "end_time": end_time.isoformat() if end_time else None,
            "description": request_data.service,
            "status": "pending",
            "solicitado_por_cliente": True,
            "status_solicitacao": "aguardando_aprovacao",
            "observacoes_cliente": request_data.notes,
            "created_at": DateTime.now().isoformat(),
            "updated_at": DateTime.now().isoformat()
        }
        
        # Inserir na tabela appointments
        insert_query = "/rest/v1/appointments"
        insert_response = await supabase_admin._request("POST", insert_query, json=insert_data)
        created_request = supabase_admin.process_response(insert_response)
        
        if not created_request:
            raise HTTPException(status_code=500, detail="Erro ao criar solicitação de agendamento")
        
        appointment = created_request[0]
        
        # Retornar resposta formatada
        response = AppointmentRequestResponse(
            id=str(appointment["id"]),
            animal_id=str(appointment["animal_id"]),
            animal_name=animal["name"],
            tutor_name=animal.get("tutor_name"),
            tutor_email=animal.get("email"),
            service=appointment["description"],
            date=appointment["date"],
            start_time=appointment["start_time"],
            end_time=appointment.get("end_time"),
            notes=appointment.get("observacoes_cliente"),
            priority=request_data.priority,
            status=appointment["status"],
            status_solicitacao=appointment["status_solicitacao"],
            created_at=appointment["created_at"],
            updated_at=appointment.get("updated_at")
        )
        
        logger.info(f"Solicitação de agendamento criada com sucesso: ID {appointment['id']}")
        return response

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao criar solicitação de agendamento: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar solicitação: {str(e)}")

@router.get("/", response_model=List[AppointmentRequestResponse])
async def list_appointment_requests(
    status: Optional[str] = Query(None, description="Filtrar por status"),
    status_solicitacao: Optional[str] = Query(None, description="Filtrar por status da solicitação"),
    date_from: Optional[Date] = Query(None, description="Data inicial"),
    date_to: Optional[Date] = Query(None, description="Data final"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Lista solicitações de agendamento da tabela appointments.
    Mostra apenas agendamentos solicitados por clientes.
    """
    user_email = current_user.get("email")
    user_type = current_user.get("user_type", "tutor")
    
    logger.info(f"Listando solicitações de agendamento para user: {user_email}, tipo: {user_type}")

    try:
        # Query base para appointments solicitados por clientes
        query = "/rest/v1/appointments?solicitado_por_cliente=eq.true"
        query += "&select=*"
        
        # Filtrar baseado no tipo de usuário
        if user_type == "tutor":
            # Buscar animais do tutor
            animals_query = f"/rest/v1/animals?email=eq.{user_email}&select=id"
            animals_response = await supabase_admin._request("GET", animals_query)
            animals_data = supabase_admin.process_response(animals_response)
            
            if not animals_data:
                return []
            
            animal_ids = [str(animal["id"]) for animal in animals_data]
            query += f"&animal_id=in.({','.join(animal_ids)})"
            
        elif user_type == "clinic":
            # Para clínicas, buscar pelo clinic_id
            clinic_id = current_user.get("clinic_id")
            if not clinic_id:
                logger.warning(f"Clínica {user_email} não possui clinic_id")
                return []
            
            query += f"&clinic_id=eq.{clinic_id}"
        
        # Aplicar filtros
        if status:
            query += f"&status=eq.{status}"
        
        if status_solicitacao:
            query += f"&status_solicitacao=eq.{status_solicitacao}"
        
        if date_from:
            query += f"&date=gte.{date_from.isoformat()}"
        
        if date_to:
            query += f"&date=lte.{date_to.isoformat()}"
        
        # Ordenar por data e hora
        query += "&order=date.desc,start_time.desc"
        
        # Executar query
        response = await supabase_admin._request("GET", query)
        appointments_data = supabase_admin.process_response(response)
        
        if not appointments_data:
            return []
        
        # Buscar informações dos animais para cada appointment
        detailed_requests = []
        for appointment in appointments_data:
            try:
                # Buscar dados do animal
                animal_query = f"/rest/v1/animals?id=eq.{appointment['animal_id']}"
                animal_response = await supabase_admin._request("GET", animal_query)
                animal_data = supabase_admin.process_response(animal_response)
                
                animal = animal_data[0] if animal_data else {}
                
                # Criar resposta formatada
                request_response = AppointmentRequestResponse(
                    id=str(appointment["id"]),
                    animal_id=str(appointment["animal_id"]),
                    animal_name=animal.get("name"),
                    tutor_name=animal.get("tutor_name"),
                    tutor_email=animal.get("email"),
                    service=appointment.get("description", ""),
                    date=appointment["date"],
                    start_time=appointment["start_time"],
                    end_time=appointment.get("end_time"),
                    notes=appointment.get("observacoes_cliente"),
                    priority="normal",  # Default priority
                    status=appointment["status"],
                    status_solicitacao=appointment.get("status_solicitacao", "aguardando_aprovacao"),
                    created_at=appointment["created_at"],
                    updated_at=appointment.get("updated_at")
                )
                
                detailed_requests.append(request_response)
                
            except Exception as e:
                logger.warning(f"Erro ao processar appointment {appointment['id']}: {e}")
                continue
        
        logger.info(f"Encontradas {len(detailed_requests)} solicitações de agendamento")
        return detailed_requests

    except Exception as e:
        logger.error(f"Erro ao listar solicitações de agendamento: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar solicitações: {str(e)}")

@router.get("/{request_id}", response_model=AppointmentRequestResponse)
async def get_appointment_request(
    request_id: str = Path(..., description="ID da solicitação"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Obtém detalhes de uma solicitação específica na tabela appointments.
    """
    user_email = current_user.get("email")
    user_type = current_user.get("user_type", "tutor")
    
    logger.info(f"Buscando solicitação {request_id} para user: {user_email}")

    try:
        # Buscar o appointment
        appointment_query = f"/rest/v1/appointments?id=eq.{request_id}&solicitado_por_cliente=eq.true"
        appointment_response = await supabase_admin._request("GET", appointment_query)
        appointment_data = supabase_admin.process_response(appointment_response)
        
        if not appointment_data:
            raise HTTPException(status_code=404, detail="Solicitação de agendamento não encontrada")
        
        appointment = appointment_data[0]
        
        # Buscar dados do animal
        animal_query = f"/rest/v1/animals?id=eq.{appointment['animal_id']}"
        animal_response = await supabase_admin._request("GET", animal_query)
        animal_data = supabase_admin.process_response(animal_response)
        
        if not animal_data:
            raise HTTPException(status_code=404, detail="Animal não encontrado")
        
        animal = animal_data[0]
        
        # Verificar permissões baseado no tipo de usuário
        if user_type == "tutor":
            # Verificar se o animal pertence ao tutor
            animal_query = f"/rest/v1/animals?id=eq.{appointment['animal_id']}&email=eq.{user_email}"
            animal_response = await supabase_admin._request("GET", animal_query)
            animal_data = supabase_admin.process_response(animal_response)
            
            if not animal_data:
                raise HTTPException(status_code=403, detail="Acesso negado a esta solicitação")
                
        elif user_type == "clinic":
            # Verificar se o agendamento pertence à clínica
            clinic_id = current_user.get("clinic_id")
            if not clinic_id or appointment.get("clinic_id") != clinic_id:
                raise HTTPException(status_code=403, detail="Acesso negado a esta solicitação")
        
        # Criar resposta formatada
        response = AppointmentRequestResponse(
            id=str(appointment["id"]),
            animal_id=str(appointment["animal_id"]),
            animal_name=animal.get("name"),
            tutor_name=animal.get("tutor_name"),
            tutor_email=animal.get("email"),
            service=appointment.get("description", ""),
            date=appointment["date"],
            start_time=appointment["start_time"],
            end_time=appointment.get("end_time"),
            notes=appointment.get("observacoes_cliente"),
            priority="normal",  # Default priority
            status=appointment["status"],
            status_solicitacao=appointment.get("status_solicitacao", "aguardando_aprovacao"),
            created_at=appointment["created_at"],
            updated_at=appointment.get("updated_at")
        )
        
        return response

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao buscar solicitação {request_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao buscar solicitação: {str(e)}")

@router.put("/{request_id}", response_model=AppointmentRequestResponse)
async def update_appointment_request(
    request_id: str,
    update_data: AppointmentRequestUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza uma solicitação de agendamento na tabela appointments.
    Tutores podem editar suas solicitações pendentes.
    Clínicas podem alterar status e outros campos.
    """
    user_email = current_user.get("email")
    user_type = current_user.get("user_type", "tutor")
    
    logger.info(f"Atualizando solicitação {request_id} por user: {user_email}")

    try:
        # Buscar solicitação atual
        appointment_query = f"/rest/v1/appointments?id=eq.{request_id}&solicitado_por_cliente=eq.true"
        appointment_response = await supabase_admin._request("GET", appointment_query)
        appointment_data = supabase_admin.process_response(appointment_response)
        
        if not appointment_data:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada")
        
        appointment = appointment_data[0]
        
        # Verificar permissões baseado no tipo de usuário
        if user_type == "tutor":
            # Verificar se o animal pertence ao tutor
            animal_query = f"/rest/v1/animals?id=eq.{appointment['animal_id']}&email=eq.{user_email}"
            animal_response = await supabase_admin._request("GET", animal_query)
            animal_data = supabase_admin.process_response(animal_response)
            
            if not animal_data:
                raise HTTPException(status_code=403, detail="Acesso negado")
            
            # Tutores só podem editar solicitações aguardando aprovação
            if appointment.get("status_solicitacao") != "aguardando_aprovacao":
                raise HTTPException(status_code=400, detail="Só é possível editar solicitações aguardando aprovação")
            
            # Tutores não podem alterar status
            if update_data.status is not None:
                raise HTTPException(status_code=403, detail="Tutores não podem alterar o status da solicitação")
                
        elif user_type == "clinic":
            # Verificar se o agendamento pertence à clínica
            clinic_id = current_user.get("clinic_id")
            if not clinic_id or appointment.get("clinic_id") != clinic_id:
                raise HTTPException(status_code=403, detail="Acesso negado")
        
        # Preparar dados para atualização
        update_fields = {}
        if update_data.service is not None:
            update_fields["description"] = update_data.service
        if update_data.date is not None:
            update_fields["date"] = update_data.date.isoformat()
        if update_data.start_time is not None:
            update_fields["start_time"] = update_data.start_time.isoformat()
        if update_data.end_time is not None:
            update_fields["end_time"] = update_data.end_time.isoformat()
        if update_data.notes is not None:
            update_fields["observacoes_cliente"] = update_data.notes
        if update_data.status is not None and user_type == "clinic":
            update_fields["status"] = update_data.status
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        update_fields["updated_at"] = DateTime.now().isoformat()
        
        # Executar atualização
        update_query = f"/rest/v1/appointments?id=eq.{request_id}"
        update_response = await supabase_admin._request("PATCH", update_query, json=update_fields)
        updated_data = supabase_admin.process_response(update_response)
        
        if not updated_data:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada")
        
        # Buscar dados do animal para resposta
        animal_query = f"/rest/v1/animals?id=eq.{appointment['animal_id']}"
        animal_response = await supabase_admin._request("GET", animal_query)
        animal_data = supabase_admin.process_response(animal_response)
        
        animal = animal_data[0] if animal_data else {}
        updated_appointment = updated_data[0]
        
        # Criar resposta formatada
        response = AppointmentRequestResponse(
            id=str(updated_appointment["id"]),
            animal_id=str(updated_appointment["animal_id"]),
            animal_name=animal.get("name"),
            tutor_name=animal.get("tutor_name"),
            tutor_email=animal.get("email"),
            service=updated_appointment.get("description", ""),
            date=updated_appointment["date"],
            start_time=updated_appointment["start_time"],
            end_time=updated_appointment.get("end_time"),
            notes=updated_appointment.get("observacoes_cliente"),
            priority="normal",
            status=updated_appointment["status"],
            status_solicitacao=updated_appointment.get("status_solicitacao", "aguardando_aprovacao"),
            created_at=updated_appointment["created_at"],
            updated_at=updated_appointment.get("updated_at")
        )
        
        logger.info(f"Solicitação {request_id} atualizada com sucesso")
        return response

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao atualizar solicitação {request_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar solicitação: {str(e)}")

@router.post("/{request_id}/approve")
async def approve_appointment_request(
    request_id: str = Path(..., description="ID da solicitação"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Aprova uma solicitação de agendamento na tabela appointments.
    Apenas clínicas podem aprovar solicitações.
    """
    user_type = current_user.get("user_type", "tutor")
    clinic_id = current_user.get("clinic_id")
    
    if user_type != "clinic":
        raise HTTPException(status_code=403, detail="Apenas clínicas podem aprovar solicitações")
    
    if not clinic_id:
        raise HTTPException(status_code=403, detail="Clínica não identificada")
    
    logger.info(f"Aprovando solicitação {request_id} pela clínica {clinic_id}")

    try:
        # Buscar solicitação
        appointment_query = f"/rest/v1/appointments?id=eq.{request_id}&solicitado_por_cliente=eq.true"
        appointment_response = await supabase_admin._request("GET", appointment_query)
        appointment_data = supabase_admin.process_response(appointment_response)
        
        if not appointment_data:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada")
        
        appointment = appointment_data[0]
        
        # Verificar se a solicitação pertence à clínica
        if appointment.get("clinic_id") != clinic_id:
            raise HTTPException(status_code=403, detail="Esta solicitação não pertence à sua clínica")
        
        if appointment.get("status_solicitacao") != "aguardando_aprovacao":
            raise HTTPException(status_code=400, detail="Apenas solicitações aguardando aprovação podem ser aprovadas")
        
        # Verificar conflitos de horário novamente
        if appointment.get("end_time"):
            conflict_query = f"/rest/v1/appointments?clinic_id=eq.{appointment['clinic_id']}"
            conflict_query += f"&date=eq.{appointment['date']}"
            conflict_query += f"&start_time=lt.{appointment['end_time']}"
            conflict_query += f"&end_time=gt.{appointment['start_time']}"
            conflict_query += "&status=in.(scheduled,confirmed)"
            conflict_query += f"&id=neq.{request_id}"
            
            conflict_response = await supabase_admin._request("GET", conflict_query)
            conflict_data = supabase_admin.process_response(conflict_response)
            
            if conflict_data:
                raise HTTPException(status_code=409, detail="Conflito de horário detectado")
        
        # Atualizar status da solicitação para aprovada
        update_query = f"/rest/v1/appointments?id=eq.{request_id}"
        update_data = {
            "status": "scheduled",
            "status_solicitacao": "aprovada",
            "updated_at": DateTime.now().isoformat()
        }
        update_response = await supabase_admin._request("PATCH", update_query, json=update_data)
        updated_appointment = supabase_admin.process_response(update_response)
        
        if not updated_appointment:
            raise HTTPException(status_code=500, detail="Erro ao aprovar solicitação")
        
        logger.info(f"Solicitação {request_id} aprovada com sucesso")
        return {
            "message": "Solicitação aprovada com sucesso",
            "appointment_id": request_id,
            "request_id": request_id
        }

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao aprovar solicitação {request_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao aprovar solicitação: {str(e)}")

@router.post("/{request_id}/reject")
async def reject_appointment_request(
    request_id: str = Path(..., description="ID da solicitação"),
    reason: Optional[str] = Query(None, description="Motivo da rejeição"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Rejeita uma solicitação de agendamento na tabela appointments.
    Apenas clínicas podem rejeitar solicitações.
    """
    user_type = current_user.get("user_type", "tutor")
    clinic_id = current_user.get("clinic_id")
    
    if user_type != "clinic":
        raise HTTPException(status_code=403, detail="Apenas clínicas podem rejeitar solicitações")
    
    if not clinic_id:
        raise HTTPException(status_code=403, detail="Clínica não identificada")
    
    logger.info(f"Rejeitando solicitação {request_id} pela clínica {clinic_id}")

    try:
        # Buscar solicitação
        appointment_query = f"/rest/v1/appointments?id=eq.{request_id}&solicitado_por_cliente=eq.true"
        appointment_response = await supabase_admin._request("GET", appointment_query)
        appointment_data = supabase_admin.process_response(appointment_response)
        
        if not appointment_data:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada")
        
        appointment = appointment_data[0]
        
        # Verificar se a solicitação pertence à clínica
        if appointment.get("clinic_id") != clinic_id:
            raise HTTPException(status_code=403, detail="Esta solicitação não pertence à sua clínica")
        
        if appointment.get("status_solicitacao") != "aguardando_aprovacao":
            raise HTTPException(status_code=400, detail="Apenas solicitações aguardando aprovação podem ser rejeitadas")
        
        # Atualizar status para rejeitada
        update_query = f"/rest/v1/appointments?id=eq.{request_id}"
        update_data = {
            "status": "cancelled",
            "status_solicitacao": "rejeitada",
            "updated_at": DateTime.now().isoformat()
        }
        
        if reason:
            current_notes = appointment.get("observacoes_cliente", "")
            rejection_note = f"Rejeitado: {reason}"
            updated_notes = f"{current_notes} | {rejection_note}".strip(" |") if current_notes else rejection_note
            update_data["observacoes_cliente"] = updated_notes
        
        update_response = await supabase_admin._request("PATCH", update_query, json=update_data)
        updated_data = supabase_admin.process_response(update_response)
        
        if not updated_data:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada")
        
        logger.info(f"Solicitação {request_id} rejeitada")
        return {
            "message": "Solicitação rejeitada com sucesso",
            "request_id": request_id,
            "reason": reason
        }

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao rejeitar solicitação {request_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao rejeitar solicitação: {str(e)}")