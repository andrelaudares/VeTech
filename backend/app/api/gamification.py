from fastapi import APIRouter, HTTPException, Depends, Path, Query
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging
from datetime import date, datetime, timedelta
from collections import defaultdict

# Importar modelos Pydantic da Sprint 6
from ..models.gamification_goal import GamificationGoalCreate, GamificationGoalUpdate, GamificationGoalResponse
from ..models.gamification_score import GamificationScoreCreate, GamificationScoreResponse
from ..models.gamification_reward import GamificationRewardCreate, GamificationRewardUpdate, GamificationRewardResponse
from ..models.gamification_assigned_reward import AssignedRewardCreate, AssignedRewardResponse
from ..models.gamification_ranking import RankingResponse, RankingEntry
from ..models.gamification_stats import GamificationStatsResponse, PointsHistory, GoalProgress
from ..models.gamification_report import GamificationReportResponse, ReportAnimalInfo, ReportPeriod, ReportSummary, ReportCategoryProgress, ReportMonthlyDetail, ReportMonthlyDetailItem

from ..db.supabase import supabase_admin
from ..api.auth import get_current_user

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# --- Funções Auxiliares ---
def get_period_dates(periodo: str, data_inicio: Optional[date], data_fim: Optional[date]) -> tuple[date, date]:
    """Determina as datas de início e fim com base nos parâmetros."""
    today = date.today()
    end_date = data_fim or today

    if data_inicio:
        start_date = data_inicio
    elif periodo == "semanal":
        # Ajuste: Pegar a semana atual ou anterior completa
        start_of_current_week = today - timedelta(days=today.weekday())
        if end_date >= start_of_current_week:
             start_date = start_of_current_week
        else:
             # Se data_fim for na semana passada, pega a semana da data_fim
             start_date = end_date - timedelta(days=end_date.weekday())
    elif periodo == "trimestral":
        # Aproximação: últimos 90 dias a partir da data fim
        start_date = end_date - timedelta(days=90)
    elif periodo == "total":
        # Para 'total', definimos uma data inicial muito antiga
        start_date = date(1970, 1, 1)
    else: # Mensal (default)
        start_date = end_date.replace(day=1)

    # Garante que data_inicio não seja maior que data_fim
    if start_date > end_date:
        start_date = end_date

    return start_date, end_date

# --- Seção 1: Metas de Gamificação ---

@router.post("/gamificacao/metas", response_model=GamificationGoalResponse, status_code=201)
async def create_gamification_goal(
    goal_data: GamificationGoalCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    ''' Cria uma nova meta de gamificação. '''
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Garante que a meta seja criada para a clínica do usuário logado
        if str(goal_data.clinic_id) != clinic_id:
             logger.warning(f"Tentativa de criar meta para clinic_id {goal_data.clinic_id} pelo usuário da clínica {clinic_id}. Usando {clinic_id} no lugar.")
             goal_data.clinic_id = UUID(clinic_id)

        insert_data = goal_data.dict()
        insert_data["clinic_id"] = str(insert_data["clinic_id"]) # Garante que clinic_id seja string para JSON

        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"

        response = await supabase_admin._request(
            "POST",
            "/rest/v1/gamificacao_metas",
            json=insert_data,
            headers=headers
        )

        created_goal = supabase_admin.process_response(response, single_item=True)
        if not created_goal:
            logger.error(f"Erro ao criar meta de gamificação: Resposta inesperada: {response}")
            raise HTTPException(status_code=500, detail="Erro ao criar meta: dados não retornados")

        logger.info(f"Meta de gamificação criada com sucesso: {created_goal.get('id')} para clínica {clinic_id}")
        return created_goal

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao criar meta de gamificação para clínica {clinic_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao criar meta: {str(e)}")

@router.get("/gamificacao/metas", response_model=List[GamificationGoalResponse])
async def list_gamification_goals(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de meta (atividade, alimentacao, etc)"),
    status: Optional[str] = Query(None, description="Filtrar por status (ativa, inativa)"),
    periodo: Optional[str] = Query(None, description="Filtrar por período (diario, semanal, mensal)"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    ''' Lista todas as metas de gamificação disponíveis para a clínica logada. '''
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        query = f"/rest/v1/gamificacao_metas?clinic_id=eq.{clinic_id}&select=*"
        if tipo:
            query += f"&tipo=eq.{tipo}"
        if status:
            query += f"&status=eq.{status}"
        if periodo:
            query += f"&periodo=eq.{periodo}"

        query += "&order=descricao.asc"

        response = await supabase_admin._request("GET", query)
        goals = supabase_admin.process_response(response)

        logger.info(f"Listando {len(goals)} metas de gamificação para a clínica {clinic_id}")
        return goals

    except Exception as e:
        logger.error(f"Erro ao listar metas de gamificação para clínica {clinic_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao listar metas: {str(e)}")

@router.get("/gamificacao/metas/{meta_id}", response_model=GamificationGoalResponse)
async def get_gamification_goal(
    meta_id: UUID = Path(..., description="ID UUID da meta"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    ''' Obtém detalhes de uma meta específica da clínica logada. '''
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        query = f"/rest/v1/gamificacao_metas?id=eq.{meta_id}&clinic_id=eq.{clinic_id}&select=*"
        response = await supabase_admin._request("GET", query)
        goal = supabase_admin.process_response(response, single_item=True)

        if not goal:
            logger.warning(f"Meta {meta_id} não encontrada ou não pertence à clínica {clinic_id}.")
            raise HTTPException(status_code=404, detail="Meta não encontrada ou não pertence a esta clínica")

        logger.info(f"Meta de gamificação {meta_id} encontrada para clínica {clinic_id}.")
        return goal

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao buscar meta {meta_id} para clínica {clinic_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao buscar meta: {str(e)}")

@router.put("/gamificacao/metas/{meta_id}", response_model=GamificationGoalResponse)
async def update_gamification_goal(
    meta_id: UUID,
    goal_update: GamificationGoalUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    ''' Atualiza uma meta de gamificação existente. '''
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # 1. Verificar se a meta existe e pertence à clínica
        get_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/gamificacao_metas?id=eq.{meta_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(get_response):
            raise HTTPException(status_code=404, detail="Meta não encontrada ou não pertence a esta clínica")

        # 2. Preparar dados para atualização
        update_data = goal_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        # 3. Executar atualização
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"

        response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/gamificacao_metas?id=eq.{meta_id}&clinic_id=eq.{clinic_id}",
            json=update_data,
            headers=headers
        )

        updated_goal = supabase_admin.process_response(response, single_item=True)

        # 4. Verificar e retornar
        if not updated_goal:
            get_again_response = await supabase_admin._request(
                 "GET",
                 f"/rest/v1/gamificacao_metas?id=eq.{meta_id}&clinic_id=eq.{clinic_id}&select=*"
            )
            updated_goal = supabase_admin.process_response(get_again_response, single_item=True)
            if not updated_goal:
                logger.error(f"Erro ao atualizar meta {meta_id}: não encontrada após PATCH.")
                raise HTTPException(status_code=500, detail="Erro ao atualizar meta: registro não encontrado após atualização")

        logger.info(f"Meta de gamificação {meta_id} atualizada com sucesso para clínica {clinic_id}.")
        return updated_goal

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao atualizar meta {meta_id} para clínica {clinic_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao atualizar meta: {str(e)}")

@router.delete("/gamificacao/metas/{meta_id}", status_code=204)
async def delete_gamification_goal(
    meta_id: UUID = Path(..., description="ID UUID da meta"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> None:
    '''
    Remove uma meta de gamificação do sistema.
    Nota: Pode falhar se houver pontuações (`gamificacao_pontuacoes`) associadas a esta meta.
    '''
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # 1. Verificar se a meta existe e pertence à clínica
        get_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/gamificacao_metas?id=eq.{meta_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(get_response):
            raise HTTPException(status_code=404, detail="Meta não encontrada ou não pertence a esta clínica")

        # 2. Tentar deletar
        await supabase_admin._request(
            "DELETE",
            f"/rest/v1/gamificacao_metas?id=eq.{meta_id}&clinic_id=eq.{clinic_id}"
        )

        # 3. Verificar se foi deletado (opcional)
        get_again_response = await supabase_admin._request(
             "GET",
             f"/rest/v1/gamificacao_metas?id=eq.{meta_id}&select=id"
         )
        if supabase_admin.process_response(get_again_response):
             logger.error(f"Erro ao deletar meta {meta_id}: ainda encontrada após DELETE.")
             raise HTTPException(status_code=500, detail="Erro ao remover meta: Falha na exclusão.")

        logger.info(f"Meta de gamificação {meta_id} removida com sucesso pela clínica {clinic_id}.")
        return None

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        if "violates foreign key constraint" in str(e).lower() and "gamificacao_pontuacoes" in str(e).lower():
            logger.warning(f"Tentativa de deletar meta {meta_id} falhou devido a pontuações associadas.")
            raise HTTPException(status_code=400, detail="Não é possível remover a meta pois existem pontuações associadas a ela. Remova as pontuações primeiro ou altere o status da meta para inativa.")
        logger.error(f"Erro ao remover meta {meta_id} pela clínica {clinic_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao remover meta: {str(e)}")

# --- Seção 2: Pontuações ---

@router.post("/gamificacao/pontuacoes", response_model=GamificationScoreResponse, status_code=201)
async def create_gamification_score(
    score_data: GamificationScoreCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    ''' Atribui pontuação a um animal por meta alcançada ou atividade realizada. '''
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # 1. Verificar se o animal pertence à clínica
        animal_resp = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{score_data.animal_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(animal_resp):
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")

        # 2. (Opcional) Verificar se a meta (se fornecida) pertence à clínica
        meta_description = None
        if score_data.meta_id:
            meta_resp = await supabase_admin._request(
                "GET",
                f"/rest/v1/gamificacao_metas?id=eq.{score_data.meta_id}&clinic_id=eq.{clinic_id}&select=id,descricao"
            )
            meta_info = supabase_admin.process_response(meta_resp, single_item=True)
            if not meta_info:
                raise HTTPException(status_code=404, detail="Meta não encontrada ou não pertence a esta clínica")
            meta_description = meta_info.get("descricao")

        # 3. Preparar dados para inserção
        insert_data = score_data.dict()
        # Garantir que UUIDs sejam strings
        insert_data["animal_id"] = str(insert_data["animal_id"])
        if insert_data.get("meta_id"):
            insert_data["meta_id"] = str(insert_data["meta_id"])
        if insert_data.get("atividade_realizada_id"):
            insert_data["atividade_realizada_id"] = str(insert_data["atividade_realizada_id"])
        # Converter data para ISO 8601
        insert_data["data"] = insert_data["data"].isoformat()

        # 4. Executar inserção
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"

        response = await supabase_admin._request(
            "POST",
            "/rest/v1/gamificacao_pontuacoes",
            json=insert_data,
            headers=headers
        )

        created_score = supabase_admin.process_response(response, single_item=True)
        if not created_score:
            logger.error(f"Erro ao registrar pontuação: Resposta inesperada: {response}")
            raise HTTPException(status_code=500, detail="Erro ao registrar pontuação: dados não retornados")

        # Adicionar descrição da meta, se aplicável
        created_score["meta_descricao"] = meta_description

        logger.info(f"Pontuação registrada com sucesso: {created_score.get('id')} para animal {score_data.animal_id}")
        return created_score

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao registrar pontuação para animal {score_data.animal_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao registrar pontuação: {str(e)}")

@router.get("/animals/{animal_id}/gamificacao/pontuacoes", response_model=List[GamificationScoreResponse])
async def list_animal_scores(
    animal_id: UUID = Path(..., description="ID do animal"),
    data_inicio: Optional[date] = Query(None, description="Filtrar a partir desta data (YYYY-MM-DD)"),
    data_fim: Optional[date] = Query(None, description="Filtrar até esta data (YYYY-MM-DD)"),
    meta_id: Optional[UUID] = Query(None, description="Filtrar por meta específica"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    ''' Visualiza o histórico de pontuações de um animal. '''
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # 1. Verificar se o animal pertence à clínica
        animal_resp = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(animal_resp):
            # Retorna lista vazia em vez de 404 se o animal não for da clínica
            logger.warning(f"Tentativa de listar pontuações para animal {animal_id} que não pertence à clínica {clinic_id}")
            return []

        # 2. Montar query para pontuações
        query = f"/rest/v1/gamificacao_pontuacoes?animal_id=eq.{animal_id}"
        if data_inicio:
            query += f"&data=gte.{data_inicio.isoformat()}"
        if data_fim:
            # Adicionar um dia e usar 'lt' para incluir a data final
            query += f"&data=lt.{(data_fim + timedelta(days=1)).isoformat()}"
        if meta_id:
            query += f"&meta_id=eq.{meta_id}"

        # Selecionar campos da pontuação e a descrição da meta associada
        query += "&select=*,gamificacao_metas(descricao)&order=data.desc"

        response = await supabase_admin._request("GET", query)
        scores_raw = supabase_admin.process_response(response)

        # 3. Processar para incluir meta_descricao no nível raiz
        scores = []
        for score_raw in scores_raw:
            meta_info = score_raw.pop('gamificacao_metas', None)
            score_raw['meta_descricao'] = meta_info.get('descricao') if meta_info else None
            scores.append(score_raw)

        logger.info(f"Listando {len(scores)} pontuações para animal {animal_id}.")
        return scores

    except Exception as e:
        logger.error(f"Erro ao listar pontuações para animal {animal_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao listar pontuações: {str(e)}")

@router.delete("/gamificacao/pontuacoes/{pontuacao_id}", status_code=204)
async def delete_gamification_score(
    pontuacao_id: UUID = Path(..., description="ID da pontuação a ser removida"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> None:
    ''' Remove um registro de pontuação. '''
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # 1. Verificar se a pontuação existe e obter o animal_id
        score_resp = await supabase_admin._request(
            "GET",
            f"/rest/v1/gamificacao_pontuacoes?id=eq.{pontuacao_id}&select=id,animal_id"
        )
        score_info = supabase_admin.process_response(score_resp, single_item=True)
        if not score_info:
            raise HTTPException(status_code=404, detail="Registro de pontuação não encontrado")

        animal_id = score_info.get("animal_id")

        # 2. Verificar se o animal associado pertence à clínica
        animal_resp = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(animal_resp):
            raise HTTPException(status_code=403, detail="Acesso negado: A pontuação pertence a um animal de outra clínica.")

        # 3. Tentar deletar a pontuação
        await supabase_admin._request(
            "DELETE",
            f"/rest/v1/gamificacao_pontuacoes?id=eq.{pontuacao_id}"
        )

        # 4. Verificar se foi deletado (opcional)
        get_again_resp = await supabase_admin._request(
            "GET",
            f"/rest/v1/gamificacao_pontuacoes?id=eq.{pontuacao_id}&select=id"
        )
        if supabase_admin.process_response(get_again_resp):
            logger.error(f"Erro ao deletar pontuação {pontuacao_id}: ainda encontrada após DELETE.")
            raise HTTPException(status_code=500, detail="Erro ao remover pontuação: Falha na exclusão.")

        logger.info(f"Pontuação {pontuacao_id} removida com sucesso pela clínica {clinic_id}.")
        return None

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao remover pontuação {pontuacao_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao remover pontuação: {str(e)}")

# --- Seção 3: Recompensas ---

@router.post("/gamificacao/recompensas", response_model=GamificationRewardResponse, status_code=201)
async def create_gamification_reward(
    reward_data: GamificationRewardCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    ''' Cria uma nova recompensa para ser desbloqueada por pontos. '''
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            # Embora recompensas não sejam diretamente ligadas à clínica na tabela,
            # apenas usuários autenticados (clínicas) podem criá-las.
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        insert_data = reward_data.dict()

        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"

        response = await supabase_admin._request(
            "POST",
            "/rest/v1/gamificacao_recompensas",
            json=insert_data,
            headers=headers
        )

        created_reward = supabase_admin.process_response(response, single_item=True)
        if not created_reward:
            logger.error(f"Erro ao criar recompensa: Resposta inesperada: {response}")
            raise HTTPException(status_code=500, detail="Erro ao criar recompensa: dados não retornados")

        logger.info(f"Recompensa criada com sucesso: {created_reward.get('id')}")
        return created_reward

    except Exception as e:
        logger.error(f"Erro ao criar recompensa: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao criar recompensa: {str(e)}")

@router.get("/gamificacao/recompensas", response_model=List[GamificationRewardResponse])
async def list_gamification_rewards(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de recompensa"),
    pontos_min: Optional[int] = Query(None, alias="pontos_min", description="Filtrar por pontos mínimos necessários"),
    pontos_max: Optional[int] = Query(None, alias="pontos_max", description="Filtrar por pontos máximos necessários"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    ''' Lista todas as recompensas disponíveis. '''
    try:
        if not current_user.get("id"):
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        query = "/rest/v1/gamificacao_recompensas?select=*"
        if tipo:
            query += f"&tipo=eq.{tipo}"
        if pontos_min is not None:
            query += f"&pontos_necessarios=gte.{pontos_min}"
        if pontos_max is not None:
            query += f"&pontos_necessarios=lte.{pontos_max}"

        query += "&order=pontos_necessarios.asc"

        response = await supabase_admin._request("GET", query)
        rewards = supabase_admin.process_response(response)

        logger.info(f"Listando {len(rewards)} recompensas.")
        return rewards

    except Exception as e:
        logger.error(f"Erro ao listar recompensas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao listar recompensas: {str(e)}")

@router.get("/gamificacao/recompensas/{recompensa_id}", response_model=GamificationRewardResponse)
async def get_gamification_reward(
    recompensa_id: UUID = Path(..., description="ID UUID da recompensa"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    ''' Obtém detalhes de uma recompensa específica. '''
    try:
        if not current_user.get("id"):
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        query = f"/rest/v1/gamificacao_recompensas?id=eq.{recompensa_id}&select=*"
        response = await supabase_admin._request("GET", query)
        reward = supabase_admin.process_response(response, single_item=True)

        if not reward:
            logger.warning(f"Recompensa {recompensa_id} não encontrada.")
            raise HTTPException(status_code=404, detail="Recompensa não encontrada")

        logger.info(f"Recompensa {recompensa_id} encontrada.")
        return reward

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao buscar recompensa {recompensa_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao buscar recompensa: {str(e)}")

@router.put("/gamificacao/recompensas/{recompensa_id}", response_model=GamificationRewardResponse)
async def update_gamification_reward(
    recompensa_id: UUID,
    reward_update: GamificationRewardUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    ''' Atualiza uma recompensa existente. '''
    try:
        if not current_user.get("id"):
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # 1. Verificar se a recompensa existe
        get_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/gamificacao_recompensas?id=eq.{recompensa_id}&select=id"
        )
        if not supabase_admin.process_response(get_response):
            raise HTTPException(status_code=404, detail="Recompensa não encontrada")

        # 2. Preparar dados
        update_data = reward_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        # 3. Atualizar
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"

        response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/gamificacao_recompensas?id=eq.{recompensa_id}",
            json=update_data,
            headers=headers
        )
        updated_reward = supabase_admin.process_response(response, single_item=True)

        # 4. Verificar e retornar
        if not updated_reward:
            get_again_response = await supabase_admin._request(
                "GET",
                f"/rest/v1/gamificacao_recompensas?id=eq.{recompensa_id}&select=*"
            )
            updated_reward = supabase_admin.process_response(get_again_response, single_item=True)
            if not updated_reward:
                 logger.error(f"Erro ao atualizar recompensa {recompensa_id}: não encontrada após PATCH.")
                 raise HTTPException(status_code=500, detail="Erro ao atualizar recompensa: registro não encontrado")

        logger.info(f"Recompensa {recompensa_id} atualizada com sucesso.")
        return updated_reward

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao atualizar recompensa {recompensa_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao atualizar recompensa: {str(e)}")

@router.delete("/gamificacao/recompensas/{recompensa_id}", status_code=204)
async def delete_gamification_reward(
    recompensa_id: UUID = Path(..., description="ID UUID da recompensa"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> None:
    ''' Remove uma recompensa do sistema. '''
    try:
        if not current_user.get("id"):
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # 1. Verificar se existe
        get_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/gamificacao_recompensas?id=eq.{recompensa_id}&select=id"
        )
        if not supabase_admin.process_response(get_response):
            raise HTTPException(status_code=404, detail="Recompensa não encontrada")

        # 2. Tentar deletar (Pode falhar se houver FK para recompensas atribuídas no futuro)
        await supabase_admin._request(
            "DELETE",
            f"/rest/v1/gamificacao_recompensas?id=eq.{recompensa_id}"
        )

        # 3. Verificar (Opcional)
        get_again_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/gamificacao_recompensas?id=eq.{recompensa_id}&select=id"
        )
        if supabase_admin.process_response(get_again_response):
            logger.error(f"Erro ao deletar recompensa {recompensa_id}: ainda encontrada após DELETE.")
            raise HTTPException(status_code=500, detail="Erro ao remover recompensa: Falha na exclusão.")

        logger.info(f"Recompensa {recompensa_id} removida com sucesso.")
        return None

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        # Adicionar tratamento para FK constraint se/quando a tabela de atribuição for criada
        logger.error(f"Erro ao remover recompensa {recompensa_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao remover recompensa: {str(e)}")

# --- Seção 4: Atribuição de Recompensas ---

@router.post("/animals/{animal_id}/gamificacao/recompensas", response_model=AssignedRewardResponse, status_code=201)
async def assign_reward_to_animal(
    animal_id: UUID = Path(..., description="ID do animal"),
    assignment_data: AssignedRewardCreate = ..., # Body com recompensa_id, etc.
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """ Atribui uma recompensa a um animal se ele tiver pontos suficientes. """
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # 1. Verificar se o animal pertence à clínica
        animal_resp = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(animal_resp):
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")

        # 2. Verificar se a recompensa existe
        reward_resp = await supabase_admin._request(
            "GET",
            f"/rest/v1/gamificacao_recompensas?id=eq.{assignment_data.recompensa_id}&select=id,nome,pontos_necessarios"
        )
        reward_info = supabase_admin.process_response(reward_resp, single_item=True)
        if not reward_info:
            raise HTTPException(status_code=404, detail="Recompensa não encontrada")

        pontos_necessarios = reward_info.get("pontos_necessarios", 0)
        recompensa_nome = reward_info.get("nome")

        # 3. Calcular pontos totais ganhos
        points_resp = await supabase_admin._request(
            "GET",
            f"/rest/v1/gamificacao_pontuacoes?animal_id=eq.{animal_id}&select=pontos_obtidos"
        )
        scores = supabase_admin.process_response(points_resp)
        pontos_totais_ganhos = sum(score.get("pontos_obtidos", 0) for score in scores)

        # 4. Calcular pontos totais utilizados
        used_points_resp = await supabase_admin._request(
            "GET",
            f"/rest/v1/gamificacao_recompensas_atribuidas?animal_id=eq.{animal_id}&select=pontos_utilizados"
        )
        assigned_rewards_data = supabase_admin.process_response(used_points_resp)
        pontos_totais_utilizados = sum(reward.get("pontos_utilizados", 0) for reward in assigned_rewards_data)

        # 5. Calcular pontos disponíveis reais
        pontos_disponiveis = pontos_totais_ganhos - pontos_totais_utilizados

        # 6. Verificar se há pontos suficientes
        if pontos_disponiveis < pontos_necessarios:
            raise HTTPException(status_code=400, detail=f"Pontos insuficientes. Necessários: {pontos_necessarios}, Disponíveis: {pontos_disponiveis}")

        # 7. Preparar dados para inserção na nova tabela
        insert_data = {
            "animal_id": str(animal_id),
            "recompensa_id": str(assignment_data.recompensa_id),
            "pontos_utilizados": pontos_necessarios, # Custo da recompensa atual
            "status": "disponivel", # Status inicial
            "codigo_verificacao": assignment_data.codigo_verificacao,
            "data_expiracao": assignment_data.data_expiracao.isoformat() if assignment_data.data_expiracao else None,
            "observacoes": assignment_data.observacoes,
            # data_atribuicao, created_at, updated_at são definidos pelo DB
        }

        # 8. Inserir o registro da atribuição
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"

        assign_response = await supabase_admin._request(
            "POST",
            "/rest/v1/gamificacao_recompensas_atribuidas",
            json={k: v for k, v in insert_data.items() if v is not None}, # Remover Nones para não sobrescrever defaults
            headers=headers
        )

        created_assignment = supabase_admin.process_response(assign_response, single_item=True)
        if not created_assignment:
            logger.error(f"Erro ao registrar atribuição de recompensa: Resposta inesperada: {assign_response}")
            raise HTTPException(status_code=500, detail="Erro ao registrar atribuição de recompensa: dados não retornados")

        # 9. Preparar e retornar a resposta formatada
        response_data = AssignedRewardResponse(
            id=created_assignment["id"],
            animal_id=UUID(created_assignment["animal_id"]),
            recompensa_id=UUID(created_assignment["recompensa_id"]),
            recompensa_nome=recompensa_nome, # Obtido da verificação da recompensa
            pontos_utilizados=created_assignment["pontos_utilizados"],
            data_atribuicao=created_assignment["data_atribuicao"],
            codigo_verificacao=created_assignment.get("codigo_verificacao"),
            data_expiracao=created_assignment.get("data_expiracao"),
            observacoes=created_assignment.get("observacoes"),
            status=created_assignment["status"]
        )

        logger.info(f"Recompensa {assignment_data.recompensa_id} atribuída ao animal {animal_id} (Registro: {created_assignment['id']}).")
        return response_data.dict()

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao atribuir recompensa para animal {animal_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao atribuir recompensa: {str(e)}")

@router.get("/animals/{animal_id}/gamificacao/recompensas", response_model=List[AssignedRewardResponse])
async def list_animal_assigned_rewards(
    animal_id: UUID = Path(..., description="ID do animal"),
    status: Optional[str] = Query(None, description="Filtrar por status (disponivel, utilizada, expirada)"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """ Lista as recompensas atribuídas a um animal. """
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # 1. Verificar se o animal pertence à clínica
        animal_resp = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(animal_resp):
            logger.warning(f"Tentativa de listar recompensas atribuídas para animal {animal_id} que não pertence à clínica {clinic_id}")
            return []

        # 2. Consultar a tabela de recompensas atribuídas
        query = f"/rest/v1/gamificacao_recompensas_atribuidas?animal_id=eq.{animal_id}"
        if status:
            query += f"&status=eq.{status}"

        # Selecionar campos da atribuição e o nome da recompensa relacionada
        query += "&select=*,recompensa:gamificacao_recompensas(nome)&order=data_atribuicao.desc"

        response = await supabase_admin._request("GET", query)
        assigned_rewards_raw = supabase_admin.process_response(response)

        # 3. Processar e formatar a resposta
        assigned_rewards = []
        for raw_data in assigned_rewards_raw:
            reward_info = raw_data.pop('recompensa', None) # Extrai o objeto aninhado
            recompensa_nome = reward_info.get('nome') if reward_info else None

            # Montar o objeto de resposta
            assigned_rewards.append(AssignedRewardResponse(
                id=raw_data["id"],
                animal_id=UUID(raw_data["animal_id"]),
                recompensa_id=UUID(raw_data["recompensa_id"]),
                recompensa_nome=recompensa_nome,
                pontos_utilizados=raw_data.get("pontos_utilizados"),
                data_atribuicao=raw_data.get("data_atribuicao"),
                codigo_verificacao=raw_data.get("codigo_verificacao"),
                data_expiracao=raw_data.get("data_expiracao"),
                observacoes=raw_data.get("observacoes"),
                status=raw_data.get("status", "desconhecido") # Default caso status seja null
            ).dict())

        logger.info(f"Listando {len(assigned_rewards)} recompensas atribuídas para animal {animal_id}.")
        return assigned_rewards

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao listar recompensas atribuídas para animal {animal_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao listar recompensas atribuídas: {str(e)}")

# --- Seção 5: Ranking e Estatísticas ---

@router.get("/gamificacao/ranking", response_model=RankingResponse)
async def get_gamification_ranking(
    periodo: str = Query("total", description="Período para cálculo (semanal, mensal, trimestral, total)", pattern="^(semanal|mensal|trimestral|total)$"),
    data_inicio: Optional[date] = Query(None, description="Data inicial para cálculo (YYYY-MM-DD, sobrescreve periodo)"),
    data_fim: Optional[date] = Query(None, description="Data final para cálculo (YYYY-MM-DD, default: hoje)"),
    limite: int = Query(20, description="Número máximo de resultados", ge=1, le=100),
    clinic_id_filter: Optional[UUID] = Query(None, alias="clinic_id", description="Filtrar por clínica específica (requer permissão adequada)"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """ Visualiza ranking de pontuação entre os pets. """
    try:
        requesting_clinic_id = current_user.get("id")
        if not requesting_clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        target_clinic_id = requesting_clinic_id
        if clinic_id_filter:
            target_clinic_id = str(clinic_id_filter)
            logger.info(f"Usuário {requesting_clinic_id} solicitando ranking para clínica {target_clinic_id}")
        else:
             logger.info(f"Usuário {requesting_clinic_id} solicitando ranking para sua própria clínica")

        start_date, end_date = get_period_dates(periodo, data_inicio, data_fim)

        animal_query = f"/rest/v1/animals?select=id,name,clinic_id"
        if target_clinic_id:
             animal_query += f"&clinic_id=eq.{target_clinic_id}"

        animal_resp = await supabase_admin._request("GET", animal_query)
        animals_data = supabase_admin.process_response(animal_resp)
        animal_map = {a['id']: {"name": a['name'], "clinic_id": a['clinic_id']} for a in animals_data}

        if not animal_map:
            return RankingResponse(ranking=[]).dict()

        animal_ids = list(animal_map.keys())

        total_scores_query = (
            f"/rest/v1/gamificacao_pontuacoes?select=animal_id,pontos_obtidos"
            f"&animal_id=in.({','.join(map(str, animal_ids))})"
        )
        if periodo != 'total':
             total_scores_query += (
                 f"&data=gte.{start_date.isoformat()}"
                 f"&data=lt.{(end_date + timedelta(days=1)).isoformat()}"
             )

        total_scores_resp = await supabase_admin._request("GET", total_scores_query)
        total_scores_data = supabase_admin.process_response(total_scores_resp)

        total_points_by_animal = defaultdict(int)
        for score in total_scores_data:
            total_points_by_animal[score["animal_id"]] += score.get("pontos_obtidos", 0)

        used_points_query = (
             f"/rest/v1/gamificacao_recompensas_atribuidas?select=animal_id,pontos_utilizados"
             f"&animal_id=in.({','.join(map(str, animal_ids))})"
        )
        used_points_resp = await supabase_admin._request("GET", used_points_query)
        used_points_data = supabase_admin.process_response(used_points_resp)

        used_points_by_animal = defaultdict(int)
        for used in used_points_data:
             used_points_by_animal[used["animal_id"]] += used.get("pontos_utilizados", 0)

        net_total_points = {}
        for animal_id in animal_ids:
            net_total_points[animal_id] = total_points_by_animal[animal_id] - used_points_by_animal[animal_id]

        ranking_list = []
        for animal_id, total_pts in net_total_points.items():
            animal_info = animal_map.get(animal_id)
            if animal_info:
                ranking_list.append({
                    "animal_id": animal_id,
                    "animal_nome": animal_info["name"],
                    "pontos_totais": total_pts,
                    "clinic_id": animal_info["clinic_id"]
                })

        ranking_list.sort(key=lambda x: x["pontos_totais"], reverse=True)

        ranked_results = []
        clinic_ids_in_ranking = {entry["clinic_id"] for entry in ranking_list if entry["clinic_id"]}
        clinic_names = {}
        if clinic_ids_in_ranking:
            clinic_query = f"/rest/v1/clinics?id=in.({','.join(map(str, clinic_ids_in_ranking))})&select=id,name"
            clinic_resp = await supabase_admin._request("GET", clinic_query)
            clinic_data = supabase_admin.process_response(clinic_resp)
            clinic_names = {c['id']: c['name'] for c in clinic_data}

        for i, entry in enumerate(ranking_list[:limite]):
            entry["posicao"] = i + 1
            entry["clinic_nome"] = clinic_names.get(entry["clinic_id"])
            ranked_results.append(RankingEntry(**entry))

        return RankingResponse(ranking=ranked_results).dict()

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao gerar ranking: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao gerar ranking: {str(e)}")

@router.get("/animals/{animal_id}/gamificacao/estatisticas", response_model=GamificationStatsResponse)
async def get_animal_gamification_stats(
    animal_id: UUID = Path(..., description="ID do animal"),
    periodo: str = Query("mensal", description="Período para cálculo (semanal, mensal, trimestral)", pattern="^(semanal|mensal|trimestral)$"),
    data_inicio: Optional[date] = Query(None, description="Data inicial para cálculo (YYYY-MM-DD, sobrescreve periodo)"),
    data_fim: Optional[date] = Query(None, description="Data final para cálculo (YYYY-MM-DD, default: hoje)"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """ Obtém estatísticas e progresso do pet nas metas de gamificação. """
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        animal_resp = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id,name"
        )
        animal_info = supabase_admin.process_response(animal_resp, single_item=True)
        if not animal_info:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")

        start_date, end_date = get_period_dates(periodo, data_inicio, data_fim)
        start_datetime_str = datetime.combine(start_date, datetime.min.time()).isoformat()
        end_datetime_str = datetime.combine(end_date + timedelta(days=1), datetime.min.time()).isoformat()

        total_scores_resp = await supabase_admin._request(
            "GET", f"/rest/v1/gamificacao_pontuacoes?animal_id=eq.{animal_id}&select=pontos_obtidos"
        )
        total_scores_data = supabase_admin.process_response(total_scores_resp)
        pontos_totais = sum(s.get("pontos_obtidos", 0) for s in total_scores_data)

        used_points_resp = await supabase_admin._request(
            "GET", f"/rest/v1/gamificacao_recompensas_atribuidas?animal_id=eq.{animal_id}&select=pontos_utilizados"
        )
        used_points_data = supabase_admin.process_response(used_points_resp)
        pontos_utilizados_total = sum(r.get("pontos_utilizados", 0) for r in used_points_data)

        pontos_disponiveis = pontos_totais - pontos_utilizados_total

        period_scores_resp = await supabase_admin._request(
            "GET",
            f"/rest/v1/gamificacao_pontuacoes?animal_id=eq.{animal_id}"
            f"&data=gte.{start_datetime_str}&data=lt.{end_datetime_str}"
            f"&select=pontos_obtidos,data,meta_id"
            f"&order=data.asc"
        )
        period_scores_data = supabase_admin.process_response(period_scores_resp)
        pontos_periodo = sum(s.get("pontos_obtidos", 0) for s in period_scores_data)

        recompensas_resgatadas = len(used_points_data)

        historico_pontos = []
        metas_ids_periodo = set()
        for score in period_scores_data:
            historico_pontos.append(PointsHistory(data=datetime.fromisoformat(score["data"]), pontos=score["pontos_obtidos"]))
            if score.get("meta_id"):
                metas_ids_periodo.add(score["meta_id"])

        progresso_metas = []
        metas_concluidas = 0
        metas_em_andamento = 0

        if metas_ids_periodo:
            goals_query = (
                f"/rest/v1/gamificacao_metas?id=in.({','.join(map(str, metas_ids_periodo))})"
                f"&select=id,descricao,quantidade,tipo"
            )
            goals_resp = await supabase_admin._request("GET", goals_query)
            goals_data = supabase_admin.process_response(goals_resp)

            for goal in goals_data:
                 status_meta = "concluida"
                 metas_concluidas += 1
                 progresso_metas.append(GoalProgress(
                     meta_id=UUID(goal["id"]),
                     descricao=goal["descricao"],
                     progresso_atual=None,
                     meta_total=goal.get("quantidade"),
                     percentual=None,
                     status=status_meta
                 ))
            metas_em_andamento = len(progresso_metas)

        stats = GamificationStatsResponse(
            pontos_totais=pontos_totais,
            pontos_periodo=pontos_periodo,
            pontos_disponiveis=pontos_disponiveis,
            recompensas_resgatadas=recompensas_resgatadas,
            metas_concluidas=metas_concluidas,
            metas_em_andamento=metas_em_andamento,
            progresso_metas=progresso_metas,
            historico_pontos=historico_pontos
        )

        logger.info(f"Estatísticas de gamificação calculadas para animal {animal_id}.")
        return stats.dict()

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao calcular estatísticas para animal {animal_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao calcular estatísticas: {str(e)}")

@router.get("/animals/{animal_id}/gamificacao/relatorios", response_model=GamificationReportResponse)
async def get_animal_gamification_report(
    animal_id: UUID = Path(..., description="ID do animal"),
    tipo_relatorio: str = Query("json", alias="tipo", description="Formato do relatório (json, pdf, csv)", pattern="^(json|pdf|csv)$"),
    periodo: str = Query("mensal", description="Período para o relatório (semanal, mensal, trimestral, anual)", pattern="^(semanal|mensal|trimestral|anual)$"),
    data_inicio: Optional[date] = Query(None, description="Data inicial para cálculo (YYYY-MM-DD, sobrescreve periodo)"),
    data_fim: Optional[date] = Query(None, description="Data final para cálculo (YYYY-MM-DD, default: hoje)"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """ Gera relatórios de progresso do pet nas metas. (JSON implementado) """
    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        animal_resp = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id,name,tutor_name"
        )
        animal_info_raw = supabase_admin.process_response(animal_resp, single_item=True)
        if not animal_info_raw:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")

        if tipo_relatorio != "json":
            logger.warning(f"Geração de relatório {tipo_relatorio} não implementada.")
            raise HTTPException(status_code=501, detail=f"Geração de relatório no formato {tipo_relatorio} não implementada.")

        start_date, end_date = get_period_dates(periodo, data_inicio, data_fim)
        start_datetime_str = datetime.combine(start_date, datetime.min.time()).isoformat()
        end_datetime_str = datetime.combine(end_date + timedelta(days=1), datetime.min.time()).isoformat()

        scores_resp = await supabase_admin._request(
            "GET",
            f"/rest/v1/gamificacao_pontuacoes?animal_id=eq.{animal_id}"
            f"&data=gte.{start_datetime_str}&data=lt.{end_datetime_str}"
            f"&select=pontos_obtidos,data,meta:gamificacao_metas(id,descricao,tipo)"
            f"&order=data.asc"
        )
        scores_data = supabase_admin.process_response(scores_resp)

        rewards_resp = await supabase_admin._request(
            "GET",
            f"/rest/v1/gamificacao_recompensas_atribuidas?animal_id=eq.{animal_id}"
            f"&data_atribuicao=gte.{start_datetime_str}&data_atribuicao=lt.{end_datetime_str}"
            f"&select=id"
        )
        rewards_data = supabase_admin.process_response(rewards_resp)

        pontos_acumulados_periodo = sum(s.get("pontos_obtidos", 0) for s in scores_data)
        recompensas_resgatadas_periodo = len(rewards_data)
        progresso_por_categoria = defaultdict(lambda: {"total_metas": 0, "concluidas": 0, "percentual": 0.0})
        metas_tocadas_ids = set()

        for score in scores_data:
            meta_info = score.get("meta")
            if meta_info and meta_info.get("id"):
                metas_tocadas_ids.add(meta_info["id"])

        metas_concluidas_total = len(metas_tocadas_ids)

        if metas_tocadas_ids:
            goals_details_resp = await supabase_admin._request(
                "GET",
                f"/rest/v1/gamificacao_metas?id=in.({','.join(map(str, metas_tocadas_ids))})&select=id,tipo,descricao"
            )
            goals_details_data = supabase_admin.process_response(goals_details_resp)
            goal_details_map = {g["id"]: g for g in goals_details_data}

            for meta_id_str in metas_tocadas_ids:
                 goal_detail = goal_details_map.get(meta_id_str)
                 if goal_detail:
                     tipo_meta = goal_detail.get("tipo", "desconhecido").lower()
                     progresso_por_categoria[tipo_meta]["total_metas"] += 1
                     progresso_por_categoria[tipo_meta]["concluidas"] += 1
                     progresso_por_categoria[tipo_meta]["percentual"] = 100.0

        detalhamento_mensal_data = defaultdict(lambda: {"pontos": 0, "metas_concluidas": 0, "metas_ids": set()})
        for score in scores_data:
            score_dt = datetime.fromisoformat(score["data"])
            month_year = score_dt.strftime("%B/%Y")
            detalhamento_mensal_data[month_year]["pontos"] += score.get("pontos_obtidos", 0)
            meta_info = score.get("meta")
            if meta_info and meta_info.get("id"):
                detalhamento_mensal_data[month_year]["metas_ids"].add(meta_info["id"])

        detalhamento_mensal = []
        if metas_tocadas_ids:
             goal_details_map_for_monthly = {g["id"]: g for g in goal_details_map.values()}
             for my, data in sorted(detalhamento_mensal_data.items()):
                 monthly_details_items = []
                 for meta_id_str in data["metas_ids"]:
                      detail = goal_details_map_for_monthly.get(meta_id_str)
                      if detail:
                          monthly_details_items.append(ReportMonthlyDetailItem(descricao=detail["descricao"]))

                 detalhamento_mensal.append(ReportMonthlyDetail(
                     mes=my,
                     pontos=data["pontos"],
                     metas_concluidas=len(data["metas_ids"]),
                     metas_detalhadas=monthly_details_items
                 ))

        animal_data = ReportAnimalInfo(
            id=UUID(animal_info_raw["id"]),
            nome=animal_info_raw.get("name"),
            tutor=animal_info_raw.get("tutor_name")
        )
        periodo_data = ReportPeriod(inicio=start_date, fim=end_date)
        resumo_data = ReportSummary(
            pontos_acumulados=pontos_acumulados_periodo,
            recompensas_resgatadas=recompensas_resgatadas_periodo,
            metas_concluidas=metas_concluidas_total
        )
        prog_cat_data = {cat: ReportCategoryProgress(**data) for cat, data in progresso_por_categoria.items()}

        report = GamificationReportResponse(
            animal=animal_data,
            periodo=periodo_data,
            resumo=resumo_data,
            progresso_por_categoria=ReportProgressByCategory(**prog_cat_data),
            detalhamento_mensal=detalhamento_mensal,
            recomendacoes=["Monitorar engajamento com novas metas", "Verificar recompensas disponíveis"]
        )

        logger.info(f"Relatório de gamificação gerado para animal {animal_id}.")
        return report.dict()

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao gerar relatório para animal {animal_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao gerar relatório: {str(e)}")

# --- Fim da Seção 5 --- 