"""
Rotas de solicitações de agendamento específicas para clientes/tutores
Utiliza a tabela 'appointments' com campos específicos para solicitações de clientes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import date, datetime, time
from pydantic import BaseModel, UUID4
from ..auth import get_current_user
from ...db.supabase import supabase_admin as supabase

router = APIRouter()

class AppointmentRequestCreate(BaseModel):
    """Modelo para criação de solicitação de agendamento"""
    animal_id: UUID4
    service_type: str  # Tipo de serviço solicitado
    date: str  # Data do agendamento (formato: YYYY-MM-DD)
    start_time: str  # Hora de início (formato: HH:MM:SS)
    end_time: Optional[str] = None  # Hora de fim (formato: HH:MM:SS)
    notes: Optional[str] = None
    priority: Optional[str] = "normal"

class AppointmentRequestResponse(BaseModel):
    """Modelo de resposta para solicitações de agendamento"""
    id: str  # UUID
    animal_id: str
    animal_name: str
    service_type: str
    date: str
    start_time: str
    end_time: Optional[str] = None
    status: str  # Status do agendamento
    status_solicitacao: str  # Status específico da solicitação
    priority: Optional[str] = None
    notes: Optional[str] = None
    observacoes_cliente: Optional[str] = None
    created_at: str
    updated_at: str
    clinic_id: str

@router.post("/", response_model=AppointmentRequestResponse)
async def create_appointment_request(
    request_data: AppointmentRequestCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Cria uma nova solicitação de agendamento na tabela appointments
    """
    try:
        # Verificar se o animal pertence ao tutor e obter clinic_id
        animal_result = await supabase.get_by_eq(
            "animals", 
            "id", 
            str(request_data.animal_id),
            select="id,name,clinic_id,email"
        )
        
        if not animal_result:
            raise HTTPException(status_code=404, detail="Animal não encontrado")
        
        animal = animal_result[0]
        
        # Verificar se o email do animal corresponde ao usuário atual
        if animal["email"] != current_user.get("email"):
            raise HTTPException(status_code=403, detail="Acesso negado a este animal")
        
        # Verificar conflitos de horário usando a função SQL
        conflict_check = await supabase.select(
            "appointments",
            columns="id",
            filters={
                "clinic_id": f"eq.{animal['clinic_id']}",
                "date": f"eq.{request_data.date}",
                "start_time": f"eq.{request_data.start_time}",
                "status": "in.(scheduled,confirmed)"
            }
        )
        
        if conflict_check:
            raise HTTPException(
                status_code=409, 
                detail="Já existe um agendamento para este horário"
            )
        
        # Criar solicitação na tabela appointments
        new_appointment = {
            "clinic_id": animal["clinic_id"],
            "animal_id": str(request_data.animal_id),
            "date": request_data.date,
            "start_time": request_data.start_time,
            "end_time": request_data.end_time,
            "description": request_data.service_type,
            "status": "pending",
            "solicitado_por_cliente": True,
            "status_solicitacao": "aguardando_aprovacao",
            "observacoes_cliente": request_data.notes,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        created_appointment = await supabase.insert("appointments", new_appointment)
        
        if not created_appointment:
            raise HTTPException(status_code=500, detail="Erro ao criar solicitação")
        
        return AppointmentRequestResponse(
            id=str(created_appointment["id"]),
            animal_id=str(created_appointment["animal_id"]),
            animal_name=animal["name"],
            service_type=created_appointment["description"],
            date=created_appointment["date"],
            start_time=created_appointment["start_time"],
            end_time=created_appointment.get("end_time"),
            status=created_appointment["status"],
            status_solicitacao=created_appointment["status_solicitacao"],
            priority=request_data.priority,
            notes=request_data.notes,
            observacoes_cliente=created_appointment.get("observacoes_cliente"),
            created_at=created_appointment["created_at"],
            updated_at=created_appointment["updated_at"],
            clinic_id=str(created_appointment["clinic_id"])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar solicitação: {str(e)}")

@router.get("/", response_model=List[AppointmentRequestResponse])
async def get_client_appointment_requests(
    current_user: dict = Depends(get_current_user),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    status_solicitacao: Optional[str] = Query(None, description="Filtrar por status da solicitação"),
    animal_id: Optional[UUID4] = Query(None, description="Filtrar por animal"),
    limit: int = Query(50, description="Limite de resultados")
):
    """
    Lista todas as solicitações de agendamento do cliente da tabela appointments
    """
    try:
        # Primeiro, buscar todos os animais do cliente
        animals_result = await supabase.select(
            "animals",
            columns="id,name,clinic_id",
            filters={
                "email": f"eq.{current_user.get('email')}",
                "client_active": "eq.true"
            }
        )
        
        if not animals_result:
            return []
        
        # Extrair IDs dos animais
        animal_ids = [animal["id"] for animal in animals_result]
        animal_names = {animal["id"]: animal["name"] for animal in animals_result}
        animal_clinics = {animal["id"]: animal["clinic_id"] for animal in animals_result}
        
        # Construir filtros para appointments
        filters = {
            "solicitado_por_cliente": "eq.true",
            "animal_id": f"in.({','.join(animal_ids)})"
        }
        
        if status:
            filters["status"] = f"eq.{status}"
            
        if status_solicitacao:
            filters["status_solicitacao"] = f"eq.{status_solicitacao}"
            
        if animal_id:
            filters["animal_id"] = f"eq.{animal_id}"
        
        # Buscar agendamentos/solicitações
        appointments_result = await supabase.select(
            "appointments",
            columns="id,animal_id,description,date,start_time,end_time,status,status_solicitacao,observacoes_cliente,created_at,updated_at,clinic_id",
            filters=filters
        )
        
        if not appointments_result:
            return []
        
        # Construir resposta
        requests = []
        for apt in appointments_result:
            animal_name = animal_names.get(apt["animal_id"], "Animal não encontrado")
            
            requests.append(AppointmentRequestResponse(
                id=str(apt["id"]),
                animal_id=str(apt["animal_id"]),
                animal_name=animal_name,
                service_type=apt["description"] or "Consulta",
                date=apt["date"],
                start_time=apt["start_time"],
                end_time=apt.get("end_time"),
                status=apt["status"],
                status_solicitacao=apt["status_solicitacao"] or "aguardando_aprovacao",
                priority="normal",  # Campo não existe na tabela appointments
                notes=apt.get("observacoes_cliente"),
                observacoes_cliente=apt.get("observacoes_cliente"),
                created_at=apt["created_at"],
                updated_at=apt["updated_at"],
                clinic_id=str(apt["clinic_id"])
            ))
        
        return requests
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar solicitações: {str(e)}")

@router.get("/{request_id}", response_model=AppointmentRequestResponse)
async def get_appointment_request_details(
    request_id: UUID4,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtém detalhes de uma solicitação específica da tabela appointments
    """
    try:
        # Buscar o agendamento
        appointment_result = await supabase.get_by_eq(
            "appointments",
            "id",
            str(request_id)
        )
        
        if not appointment_result:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
        
        appointment = appointment_result[0]
        
        # Verificar se foi solicitado por cliente
        if not appointment.get("solicitado_por_cliente"):
            raise HTTPException(status_code=403, detail="Este agendamento não foi solicitado por cliente")
        
        # Verificar se o animal pertence ao cliente
        animal_result = await supabase.get_by_eq(
            "animals",
            "id",
            appointment["animal_id"]
        )
        
        if not animal_result:
            raise HTTPException(status_code=404, detail="Animal não encontrado")
        
        animal = animal_result[0]
        if animal["email"] != current_user.get("email"):
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        return AppointmentRequestResponse(
            id=str(appointment["id"]),
            animal_id=str(appointment["animal_id"]),
            animal_name=animal["name"],
            service_type=appointment["description"] or "Consulta",
            date=appointment["date"],
            start_time=appointment["start_time"],
            end_time=appointment.get("end_time"),
            status=appointment["status"],
            status_solicitacao=appointment["status_solicitacao"] or "aguardando_aprovacao",
            priority="normal",  # Campo não existe na tabela appointments
            notes=appointment.get("observacoes_cliente"),
            observacoes_cliente=appointment.get("observacoes_cliente"),
            created_at=appointment["created_at"],
            updated_at=appointment["updated_at"],
            clinic_id=str(appointment["clinic_id"])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar solicitação: {str(e)}")

@router.delete("/{request_id}")
async def cancel_appointment_request(
    request_id: UUID4,
    current_user: dict = Depends(get_current_user)
):
    """
    Cancela uma solicitação de agendamento na tabela appointments
    """
    try:
        # Verificar se o agendamento existe
        appointment_result = await supabase.get_by_eq(
            "appointments",
            "id",
            str(request_id)
        )
        
        if not appointment_result:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
        
        appointment_data = appointment_result[0]
        
        # Verificar se foi solicitado por cliente
        if not appointment_data.get("solicitado_por_cliente"):
            raise HTTPException(status_code=403, detail="Este agendamento não foi solicitado por cliente")
        
        # Verificar se o animal pertence ao cliente
        animal_result = await supabase.get_by_eq(
            "animals",
            "id",
            appointment_data["animal_id"]
        )
        
        if not animal_result:
            raise HTTPException(status_code=404, detail="Animal não encontrado")
        
        animal = animal_result[0]
        if animal["email"] != current_user.get("email"):
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        # Verificar se a solicitação pode ser cancelada
        if appointment_data["status"] in ["completed"]:
            raise HTTPException(
                status_code=400, 
                detail="Não é possível cancelar um agendamento já concluído"
            )
        
        if appointment_data.get("status_solicitacao") == "aprovada":
            raise HTTPException(
                status_code=400, 
                detail="Não é possível cancelar uma solicitação já aprovada. Entre em contato com a clínica."
            )
        
        # Cancelar a solicitação
        await supabase.update(
            "appointments",
            {
                "status": "cancelled",
                "status_solicitacao": "cancelada_cliente"
            },
            {"id": f"eq.{request_id}"}
        )
        
        return {"message": "Solicitação cancelada com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cancelar solicitação: {str(e)}")