"""
Rotas de dietas para clientes/tutores

Permite ao tutor listar as dietas do seu animal sem precisar informar o animal_id.
O animal é resolvido pelo `tutor_user_id` presente no JWT do tutor.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
import logging

from ..auth import get_current_user
from ...db.supabase import supabase_admin as supabase

router = APIRouter()
logger = logging.getLogger(__name__)


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
        return diets

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao listar dietas do tutor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar dietas do tutor: {str(e)}")