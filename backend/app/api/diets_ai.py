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
    user_input: Optional[Dict[str, Any]] = None,
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

    # Gerar proposta via IA (user_input é opcional e pode ser omitido)
    try:
        proposal = await generate_diet_proposal(animal, preferences, user_input or {})
    except DietAIError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Preencher campos faltantes da proposta com base no banco
    try:
        # Selecionar alimento_base se não vier do modelo
        if not proposal.get("alimento_id"):
            # Buscar opções recentes de alimentos base
            alimentos_resp = await supabase._request(
                "GET",
                "/rest/v1/alimentos_base?select=alimento_id,nome,tipo,especie_destino,kcal_por_100g&order=created_at.desc&limit=20",
            )
            alimentos = supabase.process_response(alimentos_resp) or []

            species = (animal.get("species") or "").lower()
            # Escolher primeiro compatível com espécie ou 'ambos'
            escolhido = None
            for a in alimentos:
                especie_destino = (a.get("especie_destino") or "").lower()
                if especie_destino in (species, "ambos"):
                    escolhido = a
                    break
            if not escolhido and alimentos:
                escolhido = alimentos[0]

            if escolhido and escolhido.get("alimento_id"):
                proposal["alimento_id"] = int(escolhido["alimento_id"]) if str(escolhido["alimento_id"]).isdigit() else None

                # Se calorias do dia e kcal/100g existirem, calcular quantidade em gramas
                kcal_100g = escolhido.get("kcal_por_100g")
                if (proposal.get("calorias_totais_dia") and kcal_100g):
                    try:
                        kcal_100g_val = float(kcal_100g)
                        calorias = int(proposal["calorias_totais_dia"]) if isinstance(proposal["calorias_totais_dia"], int) else int(float(proposal["calorias_totais_dia"]))
                        # gramas = calorias_totais_dia / (kcal_por_100g / 100)
                        gramas = round(calorias / (kcal_100g_val / 100))
                        proposal["quantidade_gramas"] = gramas
                    except Exception:
                        # Mantém None se não for possível calcular
                        pass

        # Preencher horários padrão se ausente
        if not proposal.get("horario"):
            refeicoes = proposal.get("refeicoes_por_dia") or 2
            if refeicoes >= 3:
                proposal["horario"] = "08:00,12:00,18:00"
            elif refeicoes == 2:
                proposal["horario"] = "08:00,16:00"
            else:
                proposal["horario"] = "08:00"
    except Exception as e:
        # Não bloquear criação se enriquecimento falhar; apenas log/propagar como detalhe
        print(f"Aviso: falha ao enriquecer proposta com alimentos base: {str(e)}")

    # Validar e persistir usando o mesmo contrato DietCreate
    try:
        diet_create = DietCreate(**proposal)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Saída da IA inválida para DietCreate: {str(e)}")

    # Criar dieta via REST usando token da clínica (não usa service key)
    body = diet_create.model_dump(exclude_none=True)
    body["animal_id"] = animal_id
    # Incluir clinic_id quando disponível e normalizar campos de data
    clinic_id = current_user.get("clinic_id") or current_user.get("id")
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
        # Garantir retorno de representação e evitar nulos
        headers = {**clinic_headers, "Prefer": "return=representation"}
        result = await supabase._request(
            "POST",
            "/rest/v1/dietas",
            json=body,
            headers=headers,
        )
        created = supabase.process_response(result, single_item=True)
        if not created:
            # Se não retornou representação, indicar erro para facilitar debug (RLS/validação)
            raise HTTPException(status_code=500, detail="Criação da dieta não retornou representação; verifique RLS, clinic_id e campos obrigatórios.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao criar dieta no Supabase: {str(e)}")

    return {"diet": created, "proposal": proposal}