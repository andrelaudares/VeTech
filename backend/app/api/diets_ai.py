from fastapi import APIRouter, Depends, HTTPException, status, Header
from typing import Dict, Any, Optional, List
from datetime import time

from ..db.supabase import supabase_admin as supabase
from ..api.auth import get_current_user
from ..models.diet import DietCreate
from ..ai.gemini_service import generate_diet_proposal, DietAIError
from ..api.diets import get_alimentos_base
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


async def _get_breed_weight_range(clinic_headers: Dict[str, str], species: Optional[str], breed: Optional[str]) -> Optional[Dict[str, Any]]:
    """Busca faixa de peso saudável da raça na tabela 'racas' (peso_min_kg/peso_max_kg).
    Faz correspondência por nome, nome_popular ou nome_oficial.
    """
    if not breed:
        return None
    try:
        # Buscar por variações de nome (case-insensitive)
        params = {
            "select": "nome,nome_popular,nome_oficial,peso_min_kg,peso_max_kg",
            # Usar OR para cobrir diferentes colunas de nome
            "or": f"(nome.ilike.%{breed}%,nome_popular.ilike.%{breed}%,nome_oficial.ilike.%{breed}%)",
            "limit": "1",
        }
        racas_resp = await supabase._request(
            "GET",
            "/rest/v1/racas",
            params=params,
            headers=clinic_headers,
        )
        racas = supabase.process_response(racas_resp) or []
        if not racas:
            return None
        r = racas[0]
        min_kg = r.get("peso_min_kg")
        max_kg = r.get("peso_max_kg")
        if min_kg is None or max_kg is None:
            return None
        return {
            "peso_min_kg": float(min_kg),
            "peso_max_kg": float(max_kg),
            "nome": r.get("nome") or r.get("nome_popular") or r.get("nome_oficial") or breed,
        }
    except Exception:
        return None


def _classificar_condicao_peso(weight: Optional[float], faixa: Optional[Dict[str, Any]]) -> str:
    """Retorna 'acima', 'abaixo', 'saudavel' ou 'indefinido'."""
    if not weight or not faixa:
        return "indefinido"
    try:
        w = float(weight)
        if w > float(faixa["peso_max_kg"]):
            return "acima"
        if w < float(faixa["peso_min_kg"]):
            return "abaixo"
        return "saudavel"
    except Exception:
        return "indefinido"


def _estimate_calories_with_goal(species: Optional[str], weight: Optional[float], condicao: str, objetivo: Optional[str]) -> Optional[int]:
    """Calcula calorias diárias considerando espécie, peso e objetivo/condição.
    Base: RER = 70 * peso^0.75; MER: multiplicador por espécie.
    Ajustes: acima -> 0.8x, abaixo -> 1.2x, manutenção -> 1.0x. Objetivo pode reforçar ajuste.
    """
    if not weight or weight <= 0:
        return None
    try:
        rer = 70 * (float(weight) ** 0.75)
    except Exception:
        return None
    sp = (species or "").lower()
    base_mult = 1.6 if (sp.startswith("dog") or sp.startswith("cão") or sp.startswith("cachorro")) else 1.2
    ajuste = 1.0
    if condicao == "acima":
        ajuste = 0.85
    elif condicao == "abaixo":
        ajuste = 1.15
    # Objetivo informado reforça ajuste
    obj = (objetivo or "").lower()
    if "emagrec" in obj:
        ajuste = min(ajuste, 0.80)
    elif "ganho" in obj or "massa" in obj:
        ajuste = max(ajuste, 1.20)
    return int(rer * base_mult * ajuste)


def _personalize_schedule(animal_id: str, refeicoes_por_dia: int, species: Optional[str]) -> str:
    """Gera horários com leve variação determinística baseada no UUID do animal.
    Mantém janelas típicas para cães/gatos e evita padrão idêntico.
    """
    try:
        # Extrair um offset determinístico em minutos (0-29) a partir do UUID
        digits = [int(c) for c in animal_id if c.isdigit()]
        offset = (sum(digits) % 30)
    except Exception:
        offset = 0

    sp = (species or "").lower()
    # Base de horários por espécie
    if sp in ("cat", "gato"):
        base = [time(7, 30), time(12, 45), time(19, 15)]
    else:
        base = [time(8, 0), time(12, 30), time(18, 30)]

    def add_offset(t: time, m: int) -> time:
        total = t.hour * 60 + t.minute + m
        h = (total // 60) % 24
        mm = total % 60
        return time(h, mm)

    if refeicoes_por_dia <= 1:
        horarios = [add_offset(base[0], offset)]
    elif refeicoes_por_dia == 2:
        horarios = [add_offset(base[0], offset), add_offset(base[2], offset)]
    elif refeicoes_por_dia == 3:
        horarios = [add_offset(base[0], offset), add_offset(base[1], offset), add_offset(base[2], offset)]
    else:
        # Para 4+ refeições, distribuímos adicionando um lanche à tarde
        extra = add_offset(time(15, 0), offset)
        horarios = [add_offset(base[0], offset), add_offset(base[1], offset), extra, add_offset(base[2], offset)]

    return ",".join([f"{h.hour:02d}:{h.minute:02d}" for h in horarios])


def _normalize_horario_value(value: Any) -> Optional[str]:
    """Normaliza o campo 'horario' para string conforme DietCreate."""
    try:
        from typing import Any as _Any  # evitar conflito de nome
    except Exception:
        pass
    if value is None:
        return None
    try:
        if isinstance(value, list):
            items = []
            for item in value:
                if isinstance(item, str):
                    items.append(item)
                elif isinstance(item, (int, float)):
                    items.append(str(item))
                elif isinstance(item, dict):
                    s = item.get("hora") or item.get("time") or item.get("value")
                    if isinstance(s, str):
                        items.append(s)
            return ",".join(items) if items else None
        if isinstance(value, dict):
            s = value.get("hora") or value.get("time") or value.get("value")
            return s if isinstance(s, str) else None
        if isinstance(value, (int, float, str)):
            return str(value)
        return None
    except Exception:
        return None

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

    # Preparar contexto de peso/raça para orientar a IA e enriquecer cálculo
    try:
        species = (animal.get("species") or "").lower()
        breed = animal.get("breed")
        faixa = await _get_breed_weight_range(clinic_headers, species, breed)
        condicao = _classificar_condicao_peso(animal.get("weight"), faixa)

        # Refeições: respeitar entrada; caso contrário, heurística por condição
        refeicoes_preferidas = (user_input or {}).get("refeicoes_por_dia")
        if not refeicoes_preferidas:
            if condicao == "acima":
                refeicoes_preferidas = 2
            elif condicao == "abaixo":
                refeicoes_preferidas = 3
            else:
                refeicoes_preferidas = 2

        objetivo_in = (user_input or {}).get("objetivo") or (preferences or {}).get("objetivo")
        calorias_alvo_estimadas = _estimate_calories_with_goal(
            animal.get("species"),
            animal.get("weight"),
            condicao,
            objetivo_in,
        )

        enriched_user_input = {
            **(user_input or {}),
            "refeicoes_por_dia": refeicoes_preferidas,
            "condicao_peso": condicao,
            "breed_weight_range": faixa,
            "calorias_alvo_estimadas": calorias_alvo_estimadas,
        }

        # Gerar proposta via IA com contexto enriquecido
        proposal, justificativa = await generate_diet_proposal(animal, preferences, enriched_user_input)
    except DietAIError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Preencher campos faltantes da proposta com base no banco e personalizações
    try:
        # Selecionar alimento_base usando a rota de alimentos-base para diversificar
        species = (animal.get("species") or "").lower()
        tipo_pref = (user_input or {}).get("tipo_alimento_preferencia") or (preferences or {}).get("tipo_alimento_preferencia")
        alimentos: List[Dict[str, Any]] = []
        try:
            alimentos_especie = await get_alimentos_base(
                nome=None,
                tipo=tipo_pref,
                especie_destino=species,
                current_user=current_user,
            )
            alimentos_ambos = await get_alimentos_base(
                nome=None,
                tipo=tipo_pref,
                especie_destino="ambos",
                current_user=current_user,
            )
            alimentos = (alimentos_especie or []) + (alimentos_ambos or [])
        except Exception:
            alimentos = []

        def escolher_alimento(alims: List[Dict[str, Any]], condicao_local: str) -> Optional[Dict[str, Any]]:
            if not alims:
                return None
            com_kcal = [a for a in alims if a.get("kcal_por_100g") is not None]
            sem_kcal = [a for a in alims if a.get("kcal_por_100g") is None]
            candidatos = com_kcal or alims
            try:
                if candidatos and candidatos[0].get("kcal_por_100g") is not None:
                    if condicao_local == "acima":
                        candidatos.sort(key=lambda x: float(x.get("kcal_por_100g", 9999)))
                    elif condicao_local == "abaixo":
                        candidatos.sort(key=lambda x: float(x.get("kcal_por_100g", 0)), reverse=True)
                    else:
                        candidatos.sort(key=lambda x: float(x.get("kcal_por_100g", 9999)))
                        mid = len(candidatos) // 2
                        candidatos = candidatos[max(0, mid-1):min(len(candidatos), mid+2)]
            except Exception:
                pass

            try:
                digits = [int(c) for c in animal_id if c.isdigit()]
                idx = sum(digits) % len(candidatos)
            except Exception:
                idx = 0
            escolhido = candidatos[idx] if candidatos else (sem_kcal[0] if sem_kcal else alims[0])
            return escolhido

        if not proposal.get("alimento_id"):
            escolhido = escolher_alimento(alimentos, condicao)
            if escolhido and escolhido.get("alimento_id"):
                proposal["alimento_id"] = int(escolhido["alimento_id"]) if str(escolhido["alimento_id"]).isdigit() else None
                kcal_100g = escolhido.get("kcal_por_100g")
                alvo = proposal.get("calorias_totais_dia") or calorias_alvo_estimadas
                if (alvo and kcal_100g):
                    try:
                        kcal_100g_val = float(kcal_100g)
                        calorias = int(alvo) if isinstance(alvo, int) else int(float(alvo))
                        gramas = round(calorias / (kcal_100g_val / 100))
                        proposal["quantidade_gramas"] = gramas
                    except Exception:
                        pass

        if not proposal.get("calorias_totais_dia") and calorias_alvo_estimadas:
            proposal["calorias_totais_dia"] = calorias_alvo_estimadas

        # Normalizar horário se veio como lista/objeto da IA
        if proposal.get("horario"):
            proposal["horario"] = _normalize_horario_value(proposal.get("horario"))
        else:
            refeicoes = proposal.get("refeicoes_por_dia") or refeicoes_preferidas or 2
            proposal["horario"] = _personalize_schedule(animal_id, int(refeicoes), animal.get("species"))
    except Exception as e:
        # Não bloquear criação se enriquecimento falhar; apenas log/propagar como detalhe
        print(f"Aviso: falha ao enriquecer proposta com alimentos base: {str(e)}")

    # Garantir normalização de 'horario' antes da validação de DietCreate,
    # mesmo que o bloco de enriquecimento acima tenha falhado.
    try:
        hor_val = proposal.get("horario") if isinstance(proposal, dict) else None
        norm_hor = _normalize_horario_value(hor_val) if hor_val is not None else None
        if norm_hor is not None:
            proposal["horario"] = norm_hor
        elif not hor_val:
            refeicoes = proposal.get("refeicoes_por_dia") or refeicoes_preferidas or 2
            proposal["horario"] = _personalize_schedule(animal_id, int(refeicoes), animal.get("species"))
    except Exception:
        # Em último caso, não derrubar a criação por falha de normalização; deixar None ou gerar padrão.
        try:
            refeicoes = proposal.get("refeicoes_por_dia") or refeicoes_preferidas or 2
            proposal["horario"] = _personalize_schedule(animal_id, int(refeicoes), animal.get("species"))
        except Exception:
            pass

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

    return {"diet": created, "proposal": proposal, "justificativa": justificativa}
