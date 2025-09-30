from typing import Any, Dict, Optional
from datetime import date

try:
    from openai import OpenAI
except Exception:
    OpenAI = None  # Evita falha de import em ambientes sem dependência

from ..core.config import OPENAI_API_KEY, OPENAI_MODEL

DEFAULT_MODEL = OPENAI_MODEL or "gpt-3.5-turbo"

class DietAIError(Exception):
    pass

def _build_messages(animal: Dict[str, Any], preferences: Optional[Dict[str, Any]], user_input: Dict[str, Any]) -> list:
    species = animal.get("species") or "cão"
    name = animal.get("name") or "Pet"
    weight = animal.get("weight")

    objetivo = user_input.get("objetivo") or (preferences or {}).get("objetivo") or "Nutrição"
    refeicoes_por_dia = user_input.get("refeicoes_por_dia") or 2
    tipo = user_input.get("tipo_alimento_preferencia") or (preferences or {}).get("tipo_alimento_preferencia") or "ração"
    valor_mensal_estimado = user_input.get("valor_mensal_estimado")
    horario = user_input.get("horario")

    system = (
        "Você é um nutricionista veterinário. Gere um plano de dieta seguro e objetivo para o pet, "
        "com campos estritamente em JSON e SEM explicações. Siga estes requisitos:\n"
        "- Use linguagem neutra e profissional.\n"
        "- Evite alimentos proibidos para a espécie.\n"
        "- Se faltar peso, não estime porções em gramas.\n"
        "- Respeite objetivo e preferências quando disponíveis.\n"
        "- Saída DEVE ser um único objeto JSON com os campos abaixo."
    )

    user = {
        "animal": {
            "name": name,
            "species": species,
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
        },
        "expected_output_fields": [
            "nome", "tipo", "objetivo", "data_inicio", "data_fim", "status",
            "refeicoes_por_dia", "calorias_totais_dia", "valor_mensal_estimado",
            "alimento_id", "quantidade_gramas", "horario"
        ]
    }

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": (
            "Com base neste contexto, gere uma sugestão de DietCreate em JSON puro.\n"
            f"Contexto: {user}"
        )}
    ]

def _estimate_calories(species: Optional[str], weight: Optional[float]) -> Optional[int]:
    if not weight or weight <= 0:
        return None
    # RER = 70 * (peso^0.75)
    try:
        rer = 70 * (weight ** 0.75)
    except Exception:
        return None
    # MER simplificado por espécie
    mult = 1.6 if (species or "").lower().startswith("dog") or (species or "").lower().startswith("cão") else 1.2
    return int(rer * mult)

async def generate_diet_proposal(animal: Dict[str, Any], preferences: Optional[Dict[str, Any]], user_input: Dict[str, Any]) -> Dict[str, Any]:
    if not OPENAI_API_KEY:
        raise DietAIError("OPENAI_API_KEY não configurada no ambiente.")
    if OpenAI is None:
        raise DietAIError("Dependência openai ausente. Instale e reinicie o servidor.")

    client = OpenAI(api_key=OPENAI_API_KEY)

    messages = _build_messages(animal, preferences, user_input)
    try:
        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            temperature=0.3,
            response_format={"type": "json_object"}
        )
    except Exception as e:
        raise DietAIError(f"Falha ao chamar OpenAI: {str(e)}")

    content = completion.choices[0].message.content if completion and completion.choices else "{}"

    import json
    try:
        data = json.loads(content)
    except Exception:
        # Caso raro: não veio JSON; retorna estrutura mínima
        data = {}

    # Campos mínimos e defaults
    nome = data.get("nome") or f"Dieta AI para {animal.get('name') or 'Pet'}"
    tipo = data.get("tipo") or user_input.get("tipo_alimento_preferencia") or "ração"
    objetivo = data.get("objetivo") or user_input.get("objetivo") or (preferences or {}).get("objetivo") or "Nutrição"
    data_inicio = data.get("data_inicio") or str(date.today())
    status = data.get("status") or "ativa"

    refeicoes_por_dia = data.get("refeicoes_por_dia") or user_input.get("refeicoes_por_dia") or 2
    calorias_totais_dia = data.get("calorias_totais_dia") or _estimate_calories(animal.get("species"), animal.get("weight"))
    valor_mensal_estimado = data.get("valor_mensal_estimado") or user_input.get("valor_mensal_estimado")
    alimento_id = data.get("alimento_id")
    quantidade_gramas = data.get("quantidade_gramas")
    horario = data.get("horario") or user_input.get("horario")

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
        "horario": horario
    }

    return proposal