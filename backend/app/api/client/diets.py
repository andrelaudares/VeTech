"""
Rotas de dietas para clientes/tutores

Permite ao tutor listar as dietas do seu animal sem precisar informar o animal_id.
O animal é resolvido pelo `tutor_user_id` presente no JWT do tutor.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime, date
import logging

from ..auth import get_current_user
from ...db.supabase import supabase_admin as supabase

router = APIRouter()
logger = logging.getLogger(__name__)


# Helper: obter nome do alimento base pelo alimento_id (ou id como fallback)
async def _get_alimento_nome(alimento_id: Optional[int]) -> Optional[str]:
    if not alimento_id:
        return None
    try:
        # Tenta por coluna 'alimento_id'
        resp = await supabase._request(
            "GET",
            f"/rest/v1/alimentos_base?alimento_id=eq.{alimento_id}&select=nome"
        )
        data = supabase.process_response(resp)
        if isinstance(data, list) and len(data) > 0:
            return data[0].get("nome")

        # Fallback: tenta por coluna 'id'
        resp2 = await supabase._request(
            "GET",
            f"/rest/v1/alimentos_base?id=eq.{alimento_id}&select=nome"
        )
        data2 = supabase.process_response(resp2)
        if isinstance(data2, list) and len(data2) > 0:
            return data2[0].get("nome")
    except Exception:
        pass
    return None


@router.get("/diets", response_model=List[Dict[str, Any]])
async def get_tutor_diets(
    status: Optional[str] = Query(None, description="Filtrar por status da dieta"),
    limit: int = Query(20, ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    """
    Lista dietas do animal vinculado ao tutor autenticado.

    - Resolve `animal_id` via `animals.tutor_user_id = current_user['id']`
    - Opcionalmente filtra por `status`
    - Ordena por `created_at` desc
    """
    try:
        tutor_id = current_user.get("id")
        if not tutor_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Encontrar o animal vinculado ao tutor
        animals_resp = await supabase._request(
            "GET",
            f"/rest/v1/animals?tutor_user_id=eq.{tutor_id}&select=id,name,species,breed&limit=1",
        )
        animals = supabase.process_response(animals_resp)
        if not animals:
            return []

        animal = animals[0]
        animal_id = animal.get("id")
        if not animal_id:
            return []

        # Construir query de dietas
        query = f"/rest/v1/dietas?animal_id=eq.{animal_id}"
        if status:
            query += f"&status=eq.{status}"
        query += "&order=created_at.desc"
        query += f"&limit={limit}"

        diets_resp = await supabase._request("GET", query)
        diets = supabase.process_response(diets_resp) or []

        # Enriquecer cada dieta com o nome do alimento
        enriched: List[Dict[str, Any]] = []
        for d in diets:
            try:
                aid = d.get("alimento_id")
                d["alimento_nome"] = await _get_alimento_nome(aid)
            except Exception:
                d["alimento_nome"] = None
            enriched.append(d)

        return enriched

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao listar dietas do tutor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar dietas do tutor: {str(e)}")


# ==== Progresso diário da dieta do tutor ====

class DietProgressInput(BaseModel):
    refeicao_completa: Optional[bool] = True
    horario_realizado: Optional[str] = None  # formato HH:MM:SS
    quantidade_gramas: Optional[int] = None
    observacoes_tutor: Optional[str] = None


async def _resolve_tutor_animal_and_active_diet(current_user: Dict[str, Any]) -> Dict[str, Any]:
    """
    Resolve animal vinculado ao tutor e a dieta ativa mais recente.
    Retorna dict com chaves: animal_id, animal, dieta
    """
    tutor_id = current_user.get("id")
    if not tutor_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    # Encontrar animal do tutor
    animals_resp = await supabase._request(
        "GET",
        f"/rest/v1/animals?tutor_user_id=eq.{tutor_id}&select=id,name,species,breed&limit=1",
    )
    animals = supabase.process_response(animals_resp)
    if not animals:
        raise HTTPException(status_code=404, detail="Nenhum animal vinculado ao tutor")

    animal = animals[0]
    animal_id = animal.get("id")
    if not animal_id:
        raise HTTPException(status_code=404, detail="Animal inválido")

    # Dieta ativa mais recente
    # Suporta status 'ativa' e 'ativo' para compatibilidade entre sprints
    diet_query = (
        f"/rest/v1/dietas?animal_id=eq.{animal_id}&status=in.(ativa,ativo)"
        "&order=created_at.desc&limit=1"
    )
    diet_resp = await supabase._request("GET", diet_query)
    diets = supabase.process_response(diet_resp)
    if not diets:
        raise HTTPException(status_code=404, detail="Nenhuma dieta ativa para o animal")

    dieta = diets[0]
    return {"animal_id": animal_id, "animal": animal, "dieta": dieta}


@router.get("/diets/progress/today", response_model=Dict[str, Any])
async def get_today_progress(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Retorna o resumo do progresso de hoje para a dieta ativa do tutor.

    - Conta registros de hoje em `public.dieta_progresso`
    - Calcula `completed_count` e `remaining_count` com base em `refeicoes_por_dia`
    """
    try:
        resolved = await _resolve_tutor_animal_and_active_diet(current_user)
        animal_id = resolved["animal_id"]
        dieta = resolved["dieta"]

        today_str = date.today().isoformat()

        # Buscar entradas de progresso de hoje
        prog_query = (
            f"/rest/v1/dieta_progresso?animal_id=eq.{animal_id}&dieta_id=eq.{dieta['id']}"
            f"&data=eq.{today_str}&order=created_at.asc"
        )
        prog_resp = await supabase._request("GET", prog_query)
        entries = supabase.process_response(prog_resp) or []

        refeicoes_por_dia = int(dieta.get("refeicoes_por_dia", 0) or 0)
        completed_count = len(entries)
        remaining_count = max(refeicoes_por_dia - completed_count, 0)
        last_refeicao_index = max([e.get("refeicao_index") or 0 for e in entries], default=0)

        return {
            "date": today_str,
            "animal_id": animal_id,
            "dieta_id": dieta["id"],
            "refeicoes_por_dia": refeicoes_por_dia,
            "completed_count": completed_count,
            "remaining_count": remaining_count,
            "entries": entries,
            "last_refeicao_index": last_refeicao_index,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter progresso de hoje: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter progresso: {str(e)}")


@router.post("/diets/progress", response_model=Dict[str, Any])
async def register_meal_progress(
    input_data: DietProgressInput,
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Registra uma refeição realizada hoje pelo tutor na dieta ativa.

    - Incrementa o count diário em `dieta_progresso`
    - Limita ao máximo `refeicoes_por_dia`
    - Retorna o item criado e o resumo atualizado
    """
    try:
        resolved = await _resolve_tutor_animal_and_active_diet(current_user)
        animal_id = resolved["animal_id"]
        dieta = resolved["dieta"]
        today_str = date.today().isoformat()

        # Contagem atual de hoje
        prog_query = (
            f"/rest/v1/dieta_progresso?animal_id=eq.{animal_id}&dieta_id=eq.{dieta['id']}"
            f"&data=eq.{today_str}"
        )
        prog_resp = await supabase._request("GET", prog_query)
        today_entries = supabase.process_response(prog_resp) or []

        refeicoes_por_dia = int(dieta.get("refeicoes_por_dia", 0) or 0)
        completed_count = len(today_entries)
        if refeicoes_por_dia and completed_count >= refeicoes_por_dia:
            raise HTTPException(status_code=400, detail="Todas as refeições de hoje já foram registradas")

        # Montar payload
        horario = input_data.horario_realizado or datetime.now().strftime("%H:%M:%S")
        pontos = 10 if (input_data.refeicao_completa is None or input_data.refeicao_completa) else 0
        next_index = completed_count + 1 if refeicoes_por_dia else None

        # Payload principal (conforme colunas atuais da tabela)
        extended_payload: Dict[str, Any] = {
            "animal_id": animal_id,
            "dieta_id": dieta["id"],
            "data": today_str,
            "refeicao_completa": bool(input_data.refeicao_completa) if input_data.refeicao_completa is not None else True,
            "horario_realizado": horario,
            "pontos_ganhos": pontos,
        }
        # Campos extras caso existam na tabela
        if next_index is not None:
            extended_payload["refeicao_index"] = next_index
        if input_data.quantidade_gramas is not None:
            # armazenar como texto amigável na coluna existente
            extended_payload["quantidade_consumida"] = f"{input_data.quantidade_gramas}g"
        if input_data.observacoes_tutor is not None:
            extended_payload["observacoes_tutor"] = input_data.observacoes_tutor

        # Tentar inserir com payload estendido; se falhar, fazer fallback para payload básico
        created_resp = await supabase._request("POST", "/rest/v1/dieta_progresso", json=extended_payload)
        created_item = supabase.process_response(created_resp, single_item=True)
        if not created_item:
            # Fallback básico
            basic_payload = {
                "animal_id": animal_id,
                "dieta_id": dieta["id"],
                "data": today_str,
                "refeicao_completa": bool(input_data.refeicao_completa) if input_data.refeicao_completa is not None else True,
                "horario_realizado": horario,
                "pontos_ganhos": pontos,
            }
            if next_index is not None:
                basic_payload["refeicao_index"] = next_index
            if input_data.quantidade_gramas is not None:
                basic_payload["quantidade_consumida"] = f"{input_data.quantidade_gramas}g"
            if input_data.observacoes_tutor is not None:
                basic_payload["observacoes_tutor"] = input_data.observacoes_tutor

            created_resp = await supabase._request("POST", "/rest/v1/dieta_progresso", json=basic_payload)
            created_item = supabase.process_response(created_resp, single_item=True)
            if not created_item:
                raise HTTPException(status_code=500, detail="Falha ao registrar progresso no Supabase")

        # Resumo atualizado
        updated_resp = await supabase._request("GET", prog_query)
        updated_entries = supabase.process_response(updated_resp) or []
        updated_completed = len(updated_entries)
        remaining_count = max(refeicoes_por_dia - updated_completed, 0)

        return {
            "created": created_item,
            "summary": {
                "date": today_str,
                "animal_id": animal_id,
                "dieta_id": dieta["id"],
                "refeicoes_por_dia": refeicoes_por_dia,
                "completed_count": updated_completed,
                "remaining_count": remaining_count,
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao registrar progresso da dieta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao registrar progresso: {str(e)}")
