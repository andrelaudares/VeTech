from fastapi import APIRouter, Depends, HTTPException, status, Header
from typing import Dict, Any, Optional

from ..db.supabase import supabase_admin as supabase
from ..api.auth import get_current_user
from ..models.diet import DietCreate
from ..ai.gemini_service import generate_diet_proposal, DietAIError
from ..core.config import SUPABASE_KEY

router = APIRouter()

async def _get_animal_and_preferences(clinic_headers: Dict[str, str], animal_id: str) -> tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
    # Busca animal
    animal_result = await supabase._request(
        "GET",
        "/rest/v1/animals",
        params={"id": f"eq.{animal_id}", "select": "*"},
        headers=clinic_headers,
    )
    animal_list = supabase.process_response(animal_result)
    if not animal_list:
        raise HTTPException(status_code=404, detail="Animal não encontrado")
    animal = animal_list[0]

    # Busca preferências do pet
    prefs_result = await supabase._request(
        "GET",
        "/rest/v1/preferencias_pet",
        params={"animal_id": f"eq.{animal_id}", "select": "*"},
        headers=clinic_headers,
    )
    prefs_list = supabase.process_response(prefs_result)
    preferences = prefs_list[0] if isinstance(prefs_list, list) and len(prefs_list) > 0 else None

    return animal, preferences

@router.post("/animals/{animal_id}/diets/ai", response_model=Dict[str, Any])
async def create_diet_ai(
    animal_id: str,
    user_input: Dict[str, Any],
    authorization: str = Header(None),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Validar se usuário é clínica
    if current_user.get("user_type") != "clinic":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Apenas clínicas podem gerar dietas com IA")

    # Extrair token Bearer do cabeçalho Authorization
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Cabeçalho Authorization Bearer é obrigatório")
    clinic_token = authorization.split(" ", 1)[1].strip()

    clinic_headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {clinic_token}"
    }

    # Verificar animal e preferências via token da clínica
    try:
        animal, preferences = await _get_animal_and_preferences(clinic_headers, animal_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados do Supabase: {str(e)}")

    # Gerar proposta via OpenAI
    try:
        proposal = await generate_diet_proposal(animal, preferences, user_input)
    except DietAIError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Validar e persistir usando o mesmo contrato DietCreate
    try:
        diet_create = DietCreate(**proposal)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Saída da IA inválida para DietCreate: {str(e)}")

    # Criar dieta via REST usando token da clínica (não usa service key)
    body = diet_create.model_dump(exclude_none=True)
    body["animal_id"] = animal_id
    # Incluir clinic_id quando disponível e normalizar campos de data
    clinic_id = current_user.get("id")
    if clinic_id:
        body["clinic_id"] = clinic_id

    # Normalizar datas para ISO 8601 se vierem como objetos date
    for key in ("data_inicio", "data_fim"):
        if key in body and body[key] is not None:
            try:
                body[key] = body[key].isoformat()
            except AttributeError:
                # já é string ou formato não compatível; mantém como está
                pass

    try:
        result = await supabase._request(
            "POST",
            "/rest/v1/dietas",
            json=body,
            params={"return": "representation"},
            headers=clinic_headers,
        )
        created = supabase.process_response(result, single_item=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao criar dieta no Supabase: {str(e)}")

    return {"diet": created, "proposal": proposal}