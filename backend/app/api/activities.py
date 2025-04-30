from fastapi import APIRouter, HTTPException, Depends, Path, Query
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging
from datetime import date, datetime, timedelta # Importar datetime e timedelta
from collections import defaultdict # Importar defaultdict

from ..models.activity import (
    ActivityCreate, ActivityUpdate, ActivityResponse
)
from ..models.activity_plan import (
    ActivityPlanCreate, ActivityPlanUpdate, ActivityPlanResponse
)
# Adicionar imports dos modelos de Log
from ..models.activity_log import (
    ActivityLogCreate, ActivityLogUpdate, ActivityLogResponse
)
# Adicionar imports dos modelos de Métricas
from ..models.activity_metrics import (
    ActivityMetricsResponse, WeeklyProgress
)

from ..db.supabase import supabase_admin
from ..api.auth import get_current_user

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# --- Funções Auxiliares (podem ser movidas para utils se crescerem) ---

def get_period_dates(periodo: str, data_inicio: Optional[date], data_fim: Optional[date]) -> tuple[date, date]:
    """Determina as datas de início e fim com base nos parâmetros."""
    today = date.today()
    end_date = data_fim or today

    if data_inicio:
        start_date = data_inicio
    elif periodo == "semanal":
        start_date = end_date - timedelta(days=end_date.weekday() + 7) # Início da semana anterior
    elif periodo == "trimestral":
        start_date = end_date - timedelta(days=90) # Aproximação
    else: # Mensal (default)
        # Se hoje for início do mês, pega o mês anterior completo
        if end_date.day == 1:
            last_day_prev_month = end_date - timedelta(days=1)
            start_date = last_day_prev_month.replace(day=1)
        else:
            start_date = end_date.replace(day=1)

    # Garante que data_inicio não seja maior que data_fim
    if start_date > end_date:
        start_date = end_date

    return start_date, end_date

def get_start_of_week(d: date) -> date:
    """Retorna a data da segunda-feira da semana de uma data."""
    return d - timedelta(days=d.weekday())

# --- Seção 1: Atividades Disponíveis (`atividades`) ---

@router.post("/atividades", response_model=ActivityResponse, status_code=201)
async def create_activity(
    activity: ActivityCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Cadastra um novo tipo de atividade física disponível.
    """
    try:
        # Verificar se o usuário está autenticado (embora não seja usado para filtrar, garante acesso)
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        activity_data = activity.dict()

        # Adicionando cabeçalho Prefer para retornar representação
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"

        response = await supabase_admin._request(
            "POST",
            "/rest/v1/atividades",
            json=activity_data,
            headers=headers
        )

        created_activity = supabase_admin.process_response(response, single_item=True)
        if not created_activity:
            logger.error(f"Erro ao criar atividade: Resposta inesperada: {response}")
            raise HTTPException(status_code=500, detail="Erro ao criar atividade: dados não retornados")

        logger.info(f"Atividade criada com sucesso: {created_activity.get('id')}")
        return created_activity

    except Exception as e:
        logger.error(f"Erro ao criar atividade: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao criar atividade: {str(e)}")


@router.get("/atividades", response_model=List[ActivityResponse])
async def list_activities(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de atividade"),
    calorias_gt: Optional[int] = Query(None, alias="calorias_gt", description="Filtrar por calorias estimadas por minuto maior que"),
    calorias_lt: Optional[int] = Query(None, alias="calorias_lt", description="Filtrar por calorias estimadas por minuto menor que"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Lista todas as atividades físicas disponíveis.
    """
    try:
        # Verificar autenticação
        if not current_user.get("id"):
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        query = "/rest/v1/atividades?select=*"
        if tipo:
            query += f"&tipo=eq.{tipo}"
        if calorias_gt is not None:
            query += f"&calorias_estimadas_por_minuto=gt.{calorias_gt}"
        if calorias_lt is not None:
            query += f"&calorias_estimadas_por_minuto=lt.{calorias_lt}"

        query += "&order=nome.asc"

        response = await supabase_admin._request("GET", query)
        activities = supabase_admin.process_response(response)

        logger.info(f"Listando {len(activities)} atividades com filtros tipo={tipo}, calorias_gt={calorias_gt}, calorias_lt={calorias_lt}")
        return activities

    except Exception as e:
        logger.error(f"Erro ao listar atividades: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao listar atividades: {str(e)}")


@router.get("/atividades/{atividade_id}", response_model=ActivityResponse)
async def get_activity(
    atividade_id: UUID = Path(..., description="ID UUID da atividade"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Obtém detalhes de uma atividade específica.
    """
    try:
        # Verificar autenticação
        if not current_user.get("id"):
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        query = f"/rest/v1/atividades?id=eq.{atividade_id}&select=*"
        response = await supabase_admin._request("GET", query)
        activity = supabase_admin.process_response(response, single_item=True)

        if not activity:
            logger.warning(f"Atividade {atividade_id} não encontrada.")
            raise HTTPException(status_code=404, detail="Atividade não encontrada")

        logger.info(f"Atividade {atividade_id} encontrada.")
        return activity

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao buscar atividade {atividade_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao buscar atividade: {str(e)}")


@router.put("/atividades/{atividade_id}", response_model=ActivityResponse)
async def update_activity(
    atividade_id: UUID,
    activity_update: ActivityUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza uma atividade existente.
    """
    try:
        # Verificar autenticação
        if not current_user.get("id"):
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Verificar se a atividade existe
        get_response = await supabase_admin._request("GET", f"/rest/v1/atividades?id=eq.{atividade_id}&select=id")
        if not supabase_admin.process_response(get_response):
            raise HTTPException(status_code=404, detail="Atividade não encontrada")

        update_data = activity_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"

        response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/atividades?id=eq.{atividade_id}",
            json=update_data,
            headers=headers
        )

        updated_activity = supabase_admin.process_response(response, single_item=True)
        if not updated_activity:
             # Tentar buscar novamente caso a representação não retorne
            get_again_response = await supabase_admin._request("GET", f"/rest/v1/atividades?id=eq.{atividade_id}&select=*")
            updated_activity = supabase_admin.process_response(get_again_response, single_item=True)
            if not updated_activity:
                logger.error(f"Erro ao atualizar atividade {atividade_id}: não encontrada após PATCH.")
                raise HTTPException(status_code=500, detail="Erro ao atualizar atividade: registro não encontrado após atualização")


        logger.info(f"Atividade {atividade_id} atualizada com sucesso.")
        return updated_activity

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao atualizar atividade {atividade_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao atualizar atividade: {str(e)}")


@router.delete("/atividades/{atividade_id}", status_code=204)
async def delete_activity(
    atividade_id: UUID = Path(..., description="ID UUID da atividade"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> None:
    """
    Remove uma atividade do sistema.
    """
    try:
        # Verificar autenticação
        if not current_user.get("id"):
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Verificar se a atividade existe antes de tentar deletar
        get_response = await supabase_admin._request("GET", f"/rest/v1/atividades?id=eq.{atividade_id}&select=id")
        if not supabase_admin.process_response(get_response):
            raise HTTPException(status_code=404, detail="Atividade não encontrada")

        # Tentar deletar a atividade
        # Nota: O Supabase pode retornar um erro se houver FK constraints (ex: planos_atividade usando esta atividade)
        await supabase_admin._request(
            "DELETE",
            f"/rest/v1/atividades?id=eq.{atividade_id}"
        )

        # Verificar se realmente foi deletado (opcional, mas bom para garantir)
        get_again_response = await supabase_admin._request("GET", f"/rest/v1/atividades?id=eq.{atividade_id}&select=id")
        if supabase_admin.process_response(get_again_response):
             logger.error(f"Erro ao deletar atividade {atividade_id}: ainda encontrada após DELETE.")
             raise HTTPException(status_code=500, detail="Erro ao remover atividade: Falha na exclusão.")


        logger.info(f"Atividade {atividade_id} removida com sucesso.")
        return None # FastAPI retorna 204 No Content

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
         # Verifica se o erro é de chave estrangeira (um palpite comum)
        if "violates foreign key constraint" in str(e).lower() and "planos_atividade" in str(e).lower() :
             logger.warning(f"Tentativa de deletar atividade {atividade_id} falhou devido a planos associados.")
             raise HTTPException(status_code=400, detail="Não é possível remover a atividade pois existem planos de atividade associados a ela.")
        logger.error(f"Erro ao remover atividade {atividade_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao remover atividade: {str(e)}")

# --- Seção 2: Planos de Atividade (`planos_atividade`) ---

@router.post("/animals/{animal_id}/planos-atividade", response_model=ActivityPlanResponse, status_code=201)
async def create_activity_plan(
    animal_id: UUID,
    plan: ActivityPlanCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Cria um novo plano de atividade (incluindo a programação) para um animal.
    """
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Verificar se o animal pertence à clínica
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(animal_response):
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")

        # Verificar se a atividade existe
        activity_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/atividades?id=eq.{plan.atividade_id}&select=id,nome" # Pega o nome também
        )
        activity_data = supabase_admin.process_response(activity_response, single_item=True)
        if not activity_data:
            raise HTTPException(status_code=404, detail="Atividade base não encontrada")

        # Montar dados para inserção, garantindo que clinic_id do token seja usado
        plan_data = plan.dict()
        plan_data["clinic_id"] = clinic_id # Sobrescreve se enviado no body
        plan_data["animal_id"] = str(animal_id) # Garante que é o animal do path param
        plan_data["atividade_id"] = str(plan.atividade_id)
        plan_data["data_inicio"] = plan.data_inicio.isoformat()
        if plan.data_fim:
            plan_data["data_fim"] = plan.data_fim.isoformat()
        else:
            # Garante que o campo não seja enviado como None se não for fornecido
            plan_data.pop("data_fim", None)


        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"

        response = await supabase_admin._request(
            "POST",
            "/rest/v1/planos_atividade",
            json=plan_data,
            headers=headers
        )

        created_plan = supabase_admin.process_response(response, single_item=True)
        if not created_plan:
            logger.error(f"Erro ao criar plano de atividade: Resposta inesperada: {response}")
            raise HTTPException(status_code=500, detail="Erro ao criar plano de atividade: dados não retornados")

        # Adicionar nome da atividade à resposta
        created_plan["nome_atividade"] = activity_data.get("nome")

        logger.info(f"Plano de atividade criado com sucesso para animal {animal_id}: {created_plan.get('id')}")
        return created_plan

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao criar plano de atividade para animal {animal_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao criar plano: {str(e)}")


@router.get("/animals/{animal_id}/planos-atividade", response_model=List[ActivityPlanResponse])
async def list_activity_plans_for_animal(
    animal_id: UUID,
    status: Optional[str] = Query(None, description="Filtrar por status do plano (ativo, inativo, concluido)"),
    atividade_id: Optional[UUID] = Query(None, description="Filtrar por ID da atividade programada"),
    intensidade: Optional[str] = Query(None, description="Filtrar por intensidade programada"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Lista todos os planos de atividade (com suas programações) de um animal.
    """
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Verificar se o animal pertence à clínica (opcional, mas bom para consistência)
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(animal_response):
             # Se o animal não pertence à clínica, retorna lista vazia em vez de 404
             logger.warning(f"Tentativa de listar planos para animal {animal_id} que não pertence à clínica {clinic_id}.")
             return []


        # Montar query para planos
        query = f"/rest/v1/planos_atividade?animal_id=eq.{animal_id}&clinic_id=eq.{clinic_id}" # Filtra por animal e clínica
        if status:
            query += f"&status=eq.{status}"
        if atividade_id:
            query += f"&atividade_id=eq.{atividade_id}"
        if intensidade:
            query += f"&intensidade=eq.{intensidade}"

        # Selecionar campos do plano e o nome da atividade relacionada
        query += "&select=*,atividades(nome)&order=data_inicio.desc"

        response = await supabase_admin._request("GET", query)
        plans_raw = supabase_admin.process_response(response)

        # Processar para incluir nome_atividade no nível raiz
        plans = []
        for plan_raw in plans_raw:
            activity_info = plan_raw.pop('atividades', None) # Remove a chave 'atividades'
            plan_raw['nome_atividade'] = activity_info.get('nome') if activity_info else None
            plans.append(plan_raw)


        logger.info(f"Listando {len(plans)} planos de atividade para animal {animal_id}.")
        return plans

    except Exception as e:
        logger.error(f"Erro ao listar planos de atividade para animal {animal_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao listar planos: {str(e)}")

@router.get("/planos-atividade/{plano_id}", response_model=ActivityPlanResponse)
async def get_activity_plan(
    plano_id: UUID = Path(..., description="ID UUID do plano"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Obtém detalhes de um plano de atividade específico (incluindo sua programação).
    """
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Buscar plano e verificar se pertence à clínica, incluindo nome da atividade
        query = f"/rest/v1/planos_atividade?id=eq.{plano_id}&clinic_id=eq.{clinic_id}&select=*,atividades(nome)"
        response = await supabase_admin._request("GET", query)
        plan_raw = supabase_admin.process_response(response, single_item=True)

        if not plan_raw:
            logger.warning(f"Plano de atividade {plano_id} não encontrado ou não pertence à clínica {clinic_id}.")
            raise HTTPException(status_code=404, detail="Plano de atividade não encontrado ou não pertence a esta clínica")

        # Processar para incluir nome_atividade no nível raiz
        activity_info = plan_raw.pop('atividades', None)
        plan_raw['nome_atividade'] = activity_info.get('nome') if activity_info else None


        logger.info(f"Plano de atividade {plano_id} encontrado.")
        return plan_raw

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao buscar plano de atividade {plano_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao buscar plano: {str(e)}")


@router.put("/planos-atividade/{plano_id}", response_model=ActivityPlanResponse)
async def update_activity_plan(
    plano_id: UUID,
    plan_update: ActivityPlanUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza um plano de atividade existente (incluindo sua programação).
    """
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Verificar se o plano existe e pertence à clínica
        get_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/planos_atividade?id=eq.{plano_id}&clinic_id=eq.{clinic_id}&select=id,atividade_id" # Pega atividade_id original
        )
        existing_plan = supabase_admin.process_response(get_response, single_item=True)
        if not existing_plan:
            raise HTTPException(status_code=404, detail="Plano de atividade não encontrado ou não pertence a esta clínica")

        update_data = plan_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        # Se atividade_id está sendo atualizada, verificar se a nova atividade existe
        new_activity_id = update_data.get("atividade_id")
        activity_name = None
        if new_activity_id:
             activity_response = await supabase_admin._request(
                 "GET",
                 f"/rest/v1/atividades?id=eq.{new_activity_id}&select=id,nome"
             )
             activity_data = supabase_admin.process_response(activity_response, single_item=True)
             if not activity_data:
                 raise HTTPException(status_code=404, detail="Nova atividade base não encontrada")
             activity_name = activity_data.get("nome")


        # Converter datas para ISO format se presentes
        if "data_inicio" in update_data and update_data["data_inicio"]:
            update_data["data_inicio"] = update_data["data_inicio"].isoformat()
        if "data_fim" in update_data and update_data["data_fim"]:
            update_data["data_fim"] = update_data["data_fim"].isoformat()
        elif "data_fim" in update_data and update_data["data_fim"] is None:
             # Permite remover a data fim setando para None
             pass
        # Converter UUID para string se presente
        if "atividade_id" in update_data and update_data["atividade_id"]:
            update_data["atividade_id"] = str(update_data["atividade_id"])


        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"

        response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/planos_atividade?id=eq.{plano_id}&clinic_id=eq.{clinic_id}",
            json=update_data,
            headers=headers
        )

        updated_plan = supabase_admin.process_response(response, single_item=True)

        if not updated_plan:
             # Tentar buscar novamente caso a representação não retorne
            get_again_response = await supabase_admin._request("GET", f"/rest/v1/planos_atividade?id=eq.{plano_id}&clinic_id=eq.{clinic_id}&select=*,atividades(nome)")
            updated_plan_raw = supabase_admin.process_response(get_again_response, single_item=True)
            if not updated_plan_raw:
                 logger.error(f"Erro ao atualizar plano {plano_id}: não encontrado após PATCH.")
                 raise HTTPException(status_code=500, detail="Erro ao atualizar plano: registro não encontrado após atualização")
             # Processar para incluir nome_atividade
            activity_info = updated_plan_raw.pop('atividades', None)
            updated_plan_raw['nome_atividade'] = activity_info.get('nome') if activity_info else None
            updated_plan = updated_plan_raw
        else:
             # Se a representação retornou, precisamos buscar o nome da atividade separadamente
             # (a menos que a atividade_id tenha sido atualizada, nesse caso já temos 'activity_name')
            if not activity_name:
                current_activity_id = updated_plan.get("atividade_id", existing_plan.get("atividade_id"))
                if current_activity_id:
                    act_name_resp = await supabase_admin._request("GET", f"/rest/v1/atividades?id=eq.{current_activity_id}&select=nome")
                    act_name_data = supabase_admin.process_response(act_name_resp, single_item=True)
                    activity_name = act_name_data.get("nome") if act_name_data else None

            updated_plan["nome_atividade"] = activity_name


        logger.info(f"Plano de atividade {plano_id} atualizado com sucesso.")
        return updated_plan

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao atualizar plano de atividade {plano_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao atualizar plano: {str(e)}")


@router.delete("/planos-atividade/{plano_id}", status_code=204)
async def delete_activity_plan(
    plano_id: UUID = Path(..., description="ID UUID do plano"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> None:
    """
    Remove um plano de atividade (e sua programação associada).
    Atenção: Isso PODE remover as atividades realizadas associadas, dependendo da configuração do DB (ON DELETE CASCADE).
    """
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Verificar se o plano existe e pertence à clínica antes de tentar deletar
        get_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/planos_atividade?id=eq.{plano_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(get_response):
            raise HTTPException(status_code=404, detail="Plano de atividade não encontrado ou não pertence a esta clínica")

        # Tentar deletar o plano
        await supabase_admin._request(
            "DELETE",
            f"/rest/v1/planos_atividade?id=eq.{plano_id}&clinic_id=eq.{clinic_id}"
        )

         # Verificar se realmente foi deletado
        get_again_response = await supabase_admin._request("GET", f"/rest/v1/planos_atividade?id=eq.{plano_id}&select=id")
        if supabase_admin.process_response(get_again_response):
             logger.error(f"Erro ao deletar plano {plano_id}: ainda encontrado após DELETE.")
             raise HTTPException(status_code=500, detail="Erro ao remover plano: Falha na exclusão.")


        logger.info(f"Plano de atividade {plano_id} removido com sucesso.")
        return None # FastAPI retorna 204 No Content

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
         # Verifica erro de FK (atividades_realizadas pode impedir)
        if "violates foreign key constraint" in str(e).lower() and "atividades_realizadas" in str(e).lower():
            logger.warning(f"Tentativa de deletar plano {plano_id} falhou devido a atividades realizadas associadas.")
            raise HTTPException(status_code=400, detail="Não é possível remover o plano pois existem atividades realizadas associadas a ele. Remova as atividades realizadas primeiro.")
        logger.error(f"Erro ao remover plano de atividade {plano_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao remover plano: {str(e)}")

# --- Seção 3: Atividades Realizadas (`atividades_realizadas`) ---

@router.post("/planos-atividade/{plano_id}/atividades-realizadas", response_model=ActivityLogResponse, status_code=201)
async def create_activity_log(
    plano_id: UUID,
    log_data: ActivityLogCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Registra uma atividade física realizada associada a um plano.
    """
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Verificar se o plano existe e pertence à clínica
        plan_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/planos_atividade?id=eq.{plano_id}&clinic_id=eq.{clinic_id}&select=id,animal_id,atividade_id,atividades(nome)" # Pega IDs e nome da atividade
        )
        plan_info = supabase_admin.process_response(plan_response, single_item=True)
        if not plan_info:
            raise HTTPException(status_code=404, detail="Plano de atividade não encontrado ou não pertence a esta clínica")

        # Validar se o animal_id do body corresponde ao do plano (se fornecido no body)
        if log_data.animal_id != UUID(plan_info['animal_id']):
             logger.warning(f"animal_id no body ({log_data.animal_id}) diferente do animal_id do plano ({plan_info['animal_id']})")
             # Poderia lançar erro 400, mas vamos usar o do plano por segurança
             # raise HTTPException(status_code=400, detail="animal_id no corpo da requisição não corresponde ao do plano.")

        # Validar se o plano_id do body corresponde ao do path (se fornecido no body)
        if log_data.plano_id != plano_id:
             logger.warning(f"plano_id no body ({log_data.plano_id}) diferente do plano_id do path ({plano_id})")
             # raise HTTPException(status_code=400, detail="plano_id no corpo da requisição não corresponde ao do path.")


        # Montar dados para inserção usando IDs do plano encontrado
        insert_data = {
            "plano_id": str(plano_id),
            "animal_id": plan_info['animal_id'],
            "data": log_data.data.isoformat(),
            "realizado": log_data.realizado,
            "duracao_realizada_minutos": log_data.duracao_realizada_minutos,
            "observacao_tutor": log_data.observacao_tutor
        }

        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"

        response = await supabase_admin._request(
            "POST",
            "/rest/v1/atividades_realizadas",
            json=insert_data,
            headers=headers
        )

        created_log = supabase_admin.process_response(response, single_item=True)
        if not created_log:
            logger.error(f"Erro ao registrar atividade realizada para o plano {plano_id}: Resposta inesperada: {response}")
            raise HTTPException(status_code=500, detail="Erro ao registrar atividade realizada: dados não retornados")

        # Adicionar nome da atividade à resposta
        activity_info = plan_info.get('atividades')
        created_log["nome_atividade"] = activity_info.get("nome") if activity_info else None


        logger.info(f"Atividade realizada registrada com sucesso para o plano {plano_id}: {created_log.get('id')}")
        return created_log

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao registrar atividade realizada para o plano {plano_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao registrar atividade: {str(e)}")


@router.get("/animals/{animal_id}/atividades-realizadas", response_model=List[ActivityLogResponse])
async def list_activity_logs_for_animal(
    animal_id: UUID,
    data_inicio: Optional[date] = Query(None, description="Filtrar a partir desta data (YYYY-MM-DD)"),
    data_fim: Optional[date] = Query(None, description="Filtrar até esta data (YYYY-MM-DD)"),
    realizado: Optional[bool] = Query(None, description="Filtrar por status de realização (true, false)"),
    plano_id: Optional[UUID] = Query(None, description="Filtrar por plano específico"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Visualiza o histórico de atividades realizadas de um pet.
    """
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Verificar se o animal pertence à clínica
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(animal_response):
            # Retorna lista vazia se o animal não for da clínica
            logger.warning(f"Tentativa de listar logs para animal {animal_id} que não pertence à clínica {clinic_id}.")
            return []

        # Montar query para logs
        query = f"/rest/v1/atividades_realizadas?animal_id=eq.{animal_id}" # Filtra por animal
        if data_inicio:
            query += f"&data=gte.{data_inicio.isoformat()}"
        if data_fim:
            query += f"&data=lte.{data_fim.isoformat()}"
        if realizado is not None:
            query += f"&realizado=is.{str(realizado).lower()}" # Supabase usa 'is.true' ou 'is.false'
        if plano_id:
            query += f"&plano_id=eq.{plano_id}"

        # Selecionar campos do log e o nome da atividade via plano
        query += "&select=*,planos_atividade!inner(atividade_id,atividades(nome))&order=data.desc"

        response = await supabase_admin._request("GET", query)
        logs_raw = supabase_admin.process_response(response)

        # Processar para incluir nome_atividade no nível raiz
        logs = []
        for log_raw in logs_raw:
            plan_info = log_raw.pop('planos_atividade', None)
            activity_info = plan_info.get('atividades') if plan_info else None
            log_raw['nome_atividade'] = activity_info.get('nome') if activity_info else None
            logs.append(log_raw)

        logger.info(f"Listando {len(logs)} logs de atividade para animal {animal_id}.")
        return logs

    except Exception as e:
        logger.error(f"Erro ao listar logs de atividade para animal {animal_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao listar logs: {str(e)}")


@router.get("/planos-atividade/{plano_id}/atividades-realizadas", response_model=List[ActivityLogResponse])
async def list_activity_logs_for_plan(
    plano_id: UUID,
    data_inicio: Optional[date] = Query(None, description="Filtrar a partir desta data (YYYY-MM-DD)"),
    data_fim: Optional[date] = Query(None, description="Filtrar até esta data (YYYY-MM-DD)"),
    realizado: Optional[bool] = Query(None, description="Filtrar por status de realização (true, false)"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Lista todas as atividades realizadas de um plano específico.
    """
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Verificar se o plano pertence à clínica
        plan_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/planos_atividade?id=eq.{plano_id}&clinic_id=eq.{clinic_id}&select=id,atividades(nome)" # Pega nome da atividade também
        )
        plan_info = supabase_admin.process_response(plan_response, single_item=True)
        if not plan_info:
            raise HTTPException(status_code=404, detail="Plano de atividade não encontrado ou não pertence a esta clínica")

        activity_info = plan_info.get('atividades')
        activity_name = activity_info.get("nome") if activity_info else None

        # Montar query para logs
        query = f"/rest/v1/atividades_realizadas?plano_id=eq.{plano_id}" # Filtra por plano
        if data_inicio:
            query += f"&data=gte.{data_inicio.isoformat()}"
        if data_fim:
            query += f"&data=lte.{data_fim.isoformat()}"
        if realizado is not None:
            query += f"&realizado=is.{str(realizado).lower()}"

        query += "&select=*&order=data.desc"

        response = await supabase_admin._request("GET", query)
        logs = supabase_admin.process_response(response)

        # Adicionar nome da atividade a cada log
        for log in logs:
            log['nome_atividade'] = activity_name

        logger.info(f"Listando {len(logs)} logs de atividade para o plano {plano_id}.")
        return logs

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao listar logs de atividade para o plano {plano_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao listar logs do plano: {str(e)}")


@router.put("/atividades-realizadas/{realizacao_id}", response_model=ActivityLogResponse)
async def update_activity_log(
    realizacao_id: UUID,
    log_update: ActivityLogUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza uma atividade realizada específica.
    """
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Verificar se o log existe e obter o plano_id associado
        get_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/atividades_realizadas?id=eq.{realizacao_id}&select=id,plano_id"
        )
        existing_log = supabase_admin.process_response(get_response, single_item=True)
        if not existing_log:
            raise HTTPException(status_code=404, detail="Registro de atividade realizada não encontrado")

        plano_id = existing_log.get("plano_id")

        # Verificar se o plano associado pertence à clínica
        plan_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/planos_atividade?id=eq.{plano_id}&clinic_id=eq.{clinic_id}&select=id,atividades(nome)"
        )
        plan_info = supabase_admin.process_response(plan_response, single_item=True)
        if not plan_info:
            raise HTTPException(status_code=403, detail="Acesso negado: O plano desta atividade não pertence à sua clínica.")

        activity_info = plan_info.get('atividades')
        activity_name = activity_info.get("nome") if activity_info else None

        # Preparar dados para atualização
        update_data = log_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        if "data" in update_data and update_data["data"]:
            update_data["data"] = update_data["data"].isoformat()
        if "realizado" in update_data and update_data["realizado"] is not None:
            # Supabase espera boolean diretamente, não string 'true'/'false' no JSON
             pass

        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"

        response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/atividades_realizadas?id=eq.{realizacao_id}",
            json=update_data,
            headers=headers
        )

        updated_log = supabase_admin.process_response(response, single_item=True)
        if not updated_log:
            # Tentar buscar novamente
            get_again_response = await supabase_admin._request("GET", f"/rest/v1/atividades_realizadas?id=eq.{realizacao_id}&select=*")
            updated_log = supabase_admin.process_response(get_again_response, single_item=True)
            if not updated_log:
                logger.error(f"Erro ao atualizar log {realizacao_id}: não encontrado após PATCH.")
                raise HTTPException(status_code=500, detail="Erro ao atualizar log: registro não encontrado após atualização")

        # Adicionar nome da atividade à resposta
        updated_log["nome_atividade"] = activity_name

        logger.info(f"Registro de atividade realizada {realizacao_id} atualizado com sucesso.")
        return updated_log

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao atualizar registro de atividade realizada {realizacao_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao atualizar log: {str(e)}")


@router.delete("/atividades-realizadas/{realizacao_id}", status_code=204)
async def delete_activity_log(
    realizacao_id: UUID = Path(..., description="ID UUID da atividade realizada"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> None:
    """
    Remove um registro de atividade realizada.
    """
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Verificar se o log existe e obter o plano_id
        get_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/atividades_realizadas?id=eq.{realizacao_id}&select=id,plano_id"
        )
        existing_log = supabase_admin.process_response(get_response, single_item=True)
        if not existing_log:
            raise HTTPException(status_code=404, detail="Registro de atividade realizada não encontrado")

        plano_id = existing_log.get("plano_id")

        # Verificar se o plano associado pertence à clínica
        plan_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/planos_atividade?id=eq.{plano_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(plan_response):
            raise HTTPException(status_code=403, detail="Acesso negado: O plano desta atividade não pertence à sua clínica.")

        # Tentar deletar o log
        await supabase_admin._request(
            "DELETE",
            f"/rest/v1/atividades_realizadas?id=eq.{realizacao_id}"
        )

        # Verificar se realmente foi deletado
        get_again_response = await supabase_admin._request("GET", f"/rest/v1/atividades_realizadas?id=eq.{realizacao_id}&select=id")
        if supabase_admin.process_response(get_again_response):
             logger.error(f"Erro ao deletar log {realizacao_id}: ainda encontrado após DELETE.")
             raise HTTPException(status_code=500, detail="Erro ao remover log: Falha na exclusão.")

        logger.info(f"Registro de atividade realizada {realizacao_id} removido com sucesso.")
        return None # FastAPI retorna 204 No Content

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao remover registro de atividade realizada {realizacao_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao remover log: {str(e)}")

# --- Seção 4: Métricas e Estatísticas ---

@router.get("/animals/{animal_id}/activity-metrics", response_model=ActivityMetricsResponse)
async def get_activity_metrics(
    animal_id: UUID,
    periodo: str = Query("mensal", description="Período para cálculo (semanal, mensal, trimestral)", pattern="^(semanal|mensal|trimestral)$"),
    data_inicio: Optional[date] = Query(None, description="Data inicial para cálculo (YYYY-MM-DD, sobrescreve periodo)"),
    data_fim: Optional[date] = Query(None, description="Data final para cálculo (YYYY-MM-DD, default: hoje)"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Obtém métricas e estatísticas das atividades físicas de um animal.
    """
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Verificar se o animal pertence à clínica
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(animal_response):
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")

        # Determinar datas do período
        start_date, end_date = get_period_dates(periodo, data_inicio, data_fim)
        logger.info(f"Calculando métricas para animal {animal_id} no período {start_date} a {end_date}")

        # Buscar atividades realizadas no período com dados da atividade e plano
        query_logs = (
            f"/rest/v1/atividades_realizadas?animal_id=eq.{animal_id}"
            f"&data=gte.{start_date.isoformat()}&data=lte.{end_date.isoformat()}"
            # Seleciona dados do log, e do plano: frequencia, e da atividade: nome, calorias
            f"&select=*,planos_atividade!inner(frequencia_semanal,atividades(nome,calorias_estimadas_por_minuto))"
        )

        logs_response = await supabase_admin._request("GET", query_logs)
        activity_logs = supabase_admin.process_response(logs_response)

        # Calcular métricas básicas
        total_atividades = len(activity_logs)
        total_minutos = sum(log.get('duracao_realizada_minutos', 0) or 0 for log in activity_logs)
        media_minutos_por_atividade = (total_minutos / total_atividades) if total_atividades > 0 else 0

        # Calcular calorias e agrupar por tipo
        calorias_estimadas = 0.0
        atividades_por_tipo = defaultdict(int)
        progresso_semanal_data = defaultdict(lambda: {"minutos": 0, "atividades": 0})

        # Para completude, precisamos dos dias únicos com atividade
        dias_com_atividade = set()

        for log in activity_logs:
            plano = log.get('planos_atividade')
            atividade = plano.get('atividades') if plano else None
            log_date = datetime.fromisoformat(log['data']).date() # Converter string para date

            if atividade and log.get('duracao_realizada_minutos') and atividade.get('calorias_estimadas_por_minuto'):
                calorias_estimadas += (log['duracao_realizada_minutos'] * atividade['calorias_estimadas_por_minuto'])

            activity_name = atividade.get('nome', 'Desconhecida') if atividade else 'Desconhecida'
            atividades_por_tipo[activity_name] += 1

            # Progresso semanal
            start_of_week = get_start_of_week(log_date)
            progresso_semanal_data[start_of_week]["minutos"] += log.get('duracao_realizada_minutos', 0) or 0
            progresso_semanal_data[start_of_week]["atividades"] += 1

            # Completude
            dias_com_atividade.add(log_date)

        # Formatar progresso semanal
        progresso_semanal = [
            WeeklyProgress(semana=week_start, **data).dict()
            for week_start, data in sorted(progresso_semanal_data.items())
        ]

        # Calcular Completude (simplificado: % de dias no período com atividade vs total de dias)
        # Uma métrica mais precisa exigiria analisar a frequência de cada plano ativo no período.
        dias_no_periodo = (end_date - start_date).days + 1
        completude_plano = (len(dias_com_atividade) / dias_no_periodo) * 100 if dias_no_periodo > 0 else 0
        # Simplificação adicional: Se não houver logs, a completude é 0.
        if total_atividades == 0:
            completude_plano = 0.0


        # Construir a resposta final
        metrics = ActivityMetricsResponse(
            total_atividades=total_atividades,
            total_minutos=total_minutos,
            media_minutos_por_atividade=round(media_minutos_por_atividade, 1) if media_minutos_por_atividade else 0,
            calorias_estimadas=round(calorias_estimadas, 1) if calorias_estimadas else 0,
            completude_plano=round(completude_plano, 1) if completude_plano else 0,
            atividades_por_tipo=dict(atividades_por_tipo),
            progresso_semanal=[WeeklyProgress(**item) for item in progresso_semanal] # Converte dicts para o modelo
        )

        logger.info(f"Métricas calculadas com sucesso para animal {animal_id}.")
        return metrics.dict()

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao calcular métricas para animal {animal_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao calcular métricas: {str(e)}")