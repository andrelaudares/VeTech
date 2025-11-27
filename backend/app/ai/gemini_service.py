from typing import Any, Dict, Optional
from datetime import date

try:
    import google.generativeai as genai
except Exception:
    genai = None

from ..core.config import GOOGLE_API_KEY, GEMINI_MODEL

# Usar versão "-latest" por compatibilidade e permitir fallback automático
DEFAULT_MODEL = "gemini-2.0-flash-lite"
FALLBACK_MODEL = "gemini-2.0-flash-lite"


class DietAIError(Exception):
    pass


def _build_prompt(animal: Dict[str, Any], preferences: Optional[Dict[str, Any]], user_input: Dict[str, Any]) -> str:
    species = animal.get("species") or "cão"
    name = animal.get("name") or "Pet"
    weight = animal.get("weight")
    breed = animal.get("breed")

    objetivo = user_input.get("objetivo") or (preferences or {}).get("objetivo") or "Nutrição"
    refeicoes_por_dia = user_input.get("refeicoes_por_dia") or 2
    tipo = user_input.get("tipo_alimento_preferencia") or (preferences or {}).get("tipo_alimento_preferencia") or "ração"
    valor_mensal_estimado = user_input.get("valor_mensal_estimado")
    horario = user_input.get("horario")
    condicao_peso = user_input.get("condicao_peso")  # acima/abaixo/saudavel/indefinido
    breed_weight_range = user_input.get("breed_weight_range")
    calorias_alvo_estimadas = user_input.get("calorias_alvo_estimadas")

    context = {
        "animal": {
            "name": name,
            "species": species,
            "breed": breed,
            "weight": weight,
        },
        "preferences": preferences or {},
        "request": {
            "objetivo": objetivo,
            "refeicoes_por_dia": refeicoes_por_dia,
            "tipo": tipo,
            "valor_mensal_estimado": valor_mensal_estimado,
            "horario": horario,
            "data_inicio": str(date.today()),
            "condicao_peso": condicao_peso,
            "breed_weight_range": breed_weight_range,
            "calorias_alvo_estimadas": calorias_alvo_estimadas,
        },
        "expected_output_fields": [
            "nome", "tipo", "objetivo", "data_inicio", "data_fim", "status",
            "refeicoes_por_dia", "calorias_totais_dia", "valor_mensal_estimado",
            "alimento_id", "quantidade_gramas", "horario", "justificativa"
        ]
    }

    system = (
        "Você é um nutricionista veterinário. Gere um plano de dieta seguro e objetivo para o pet, "
        "em JSON puro (application/json) e SEM explicações. Regras:\n"
        "- Linguagem neutra.\n"
        "- Evitar alimentos proibidos.\n"
        "- Considere a condição de peso (acima/abaixo/saudável) e a faixa saudável da raça, se fornecida.\n"
        "- Se faltar peso, não estimar gramas.\n"
        "- Respeitar objetivo e preferências quando disponíveis (ex.: tipo do alimento).\n"
        "- Se 'calorias_alvo_estimadas' for fornecida, priorize essa meta diária.\n"
        "- Estruture horários compatíveis com o número de refeições, evitando valores idênticos para todos os pets.\n"
        "- Não fixar sempre o mesmo 'alimento_id'; escolher conforme espécie/objetivo e calorias.\n"
        "- A saída deve ser um ÚNICO objeto JSON com os campos especificados."
    )

    prompt = (
        f"{system}\n\nContexto: {context}\n\n"
        "Gere o objeto JSON final de DietCreate contendo também o campo 'justificativa' com 1-2 frases explicando o motivo e critérios da dieta."
    )
    return prompt


def _estimate_calories(species: Optional[str], weight: Optional[float]) -> Optional[int]:
    if not weight or weight <= 0:
        return None
    try:
        rer = 70 * (weight ** 0.75)
    except Exception:
        return None
    mult = 1.6 if (species or "").lower().startswith("dog") or (species or "").lower().startswith("cão") else 1.2
    return int(rer * mult)


def _parse_json_response(content: str) -> Dict[str, Any]:
    """Parse texto possivelmente com fences ```json e listas, retornando dict.
    - Remove fences e extrai o primeiro objeto JSON válido.
    - Se a raiz for lista, retorna o primeiro item que seja dict.
    - Em falha, retorna {}.
    """
    import json

    if not content:
        return {}

    text = content.strip()

    # Remover code fences ```json ... ```
    if text.startswith("```"):
        start_obj = text.find("{")
        end_obj = text.rfind("}")
        start_list = text.find("[")
        end_list = text.rfind("]")
        if start_obj != -1 and end_obj != -1 and end_obj > start_obj:
            text = text[start_obj:end_obj + 1]
        elif start_list != -1 and end_list != -1 and end_list > start_list:
            text = text[start_list:end_list + 1]

    try:
        data = json.loads(text)
    except Exception:
        return {}

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                return item
        return {}

    return data if isinstance(data, dict) else {}


async def generate_diet_proposal(animal: Dict[str, Any], preferences: Optional[Dict[str, Any]], user_input: Dict[str, Any]) -> tuple[Dict[str, Any], str]:
    if not GOOGLE_API_KEY:
        raise DietAIError("GOOGLE_API_KEY não configurada no ambiente.")
    if genai is None:
        raise DietAIError("Dependência google-generativeai ausente. Adicione ao requirements e instale.")

    # Configurar SDK
    genai.configure(api_key=GOOGLE_API_KEY)

    # Construir prompt
    prompt = _build_prompt(animal, preferences, user_input)

    # Inicializar modelo com fallback quando necessário
    try:
        model = genai.GenerativeModel(DEFAULT_MODEL)
    except Exception:
        model = genai.GenerativeModel(FALLBACK_MODEL)

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "response_mime_type": "application/json",
            },
        )
        content = response.text or "{}"
    except Exception as e:
        # Se o modelo atual não suportar generateContent, tentar novamente com fallback
        if DEFAULT_MODEL != FALLBACK_MODEL:
            try:
                model = genai.GenerativeModel(FALLBACK_MODEL)
                response = model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.3,
                        "response_mime_type": "application/json",
                    },
                )
                content = response.text or "{}"
            except Exception as e2:
                raise DietAIError(f"Falha ao chamar Gemini: {str(e2)}")
        else:
            raise DietAIError(f"Falha ao chamar Gemini: {str(e)}")

    data = _parse_json_response(content)

    nome = data.get("nome") or f"Dieta AI para {animal.get('name') or 'Pet'}"
    tipo = data.get("tipo") or user_input.get("tipo_alimento_preferencia") or "ração"
    objetivo = data.get("objetivo") or user_input.get("objetivo") or (preferences or {}).get("objetivo") or "Nutrição"
    data_inicio = data.get("data_inicio") or str(date.today())
    status = data.get("status") or "ativa"

    refeicoes_por_dia = data.get("refeicoes_por_dia") or user_input.get("refeicoes_por_dia") or 2
    calorias_totais_dia = (
        data.get("calorias_totais_dia")
        or user_input.get("calorias_alvo_estimadas")
        or _estimate_calories(animal.get("species"), animal.get("weight"))
    )
    valor_mensal_estimado = data.get("valor_mensal_estimado") or user_input.get("valor_mensal_estimado")
    alimento_id = data.get("alimento_id")
    quantidade_gramas = data.get("quantidade_gramas")
    horario = _normalize_horario(data.get("horario") or user_input.get("horario"))

    proposal = {
        "nome": nome,
        "tipo": tipo,
        "objetivo": objetivo,
        "data_inicio": data_inicio,
        "data_fim": data.get("data_fim"),
        "status": status,
        "refeicoes_por_dia": int(refeicoes_por_dia),
        "calorias_totais_dia": int(calorias_totais_dia) if calorias_totais_dia else None,
        "valor_mensal_estimado": float(valor_mensal_estimado) if valor_mensal_estimado is not None else None,
        "alimento_id": int(alimento_id) if isinstance(alimento_id, (int, str)) and str(alimento_id).isdigit() else None,
        "quantidade_gramas": int(quantidade_gramas) if quantidade_gramas is not None else None,
        "horario": horario,
    }
    justificativa = data.get("justificativa")
    if not justificativa:
        species = animal.get("species") or "pet"
        weight = animal.get("weight")
        prefs_obj = (preferences or {}).get("objetivo")
        tipo_pref = (preferences or {}).get("tipo_alimento_preferencia")
        parts = []
        parts.append(f"Dieta focada em {objetivo.lower()} para {species}.")
        if weight:
            parts.append(f"Considera peso atual de {weight} kg.")
        if tipo_pref:
            parts.append(f"Preferência alimentar: {tipo_pref}.")
        if prefs_obj and prefs_obj.lower() != objetivo.lower():
            parts.append(f"Histórico de objetivo informado: {prefs_obj}.")
        justificativa = " ".join(parts)

    return proposal, justificativa
def _normalize_horario(value: Any) -> Optional[str]:
    """Converte diferentes formatos de horário para string esperada pelo modelo DietCreate.
    - Lista de strings → "HH:MM,HH:MM,..."
    - Dict com chaves comuns → usa 'hora'/'time'/'value' se string
    - Número/str → str direta
    """
    if value is None:
        return None
    try:
        # Lista de horários
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
        # Dicionário único
        if isinstance(value, dict):
            s = value.get("hora") or value.get("time") or value.get("value")
            return s if isinstance(s, str) else None
        # Número ou string
        if isinstance(value, (int, float, str)):
            return str(value)
        return None
    except Exception:
        return None
