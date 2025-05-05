## Alterações na API - Sprint 3 (Consultations)

Esta seção documenta as alterações feitas nas rotas de consulta para corrigir problemas e melhorar a segurança.

### `PATCH /api/v1/consultations/{consultation_id}`

Atualiza uma consulta existente.

**Alteração Principal:** O parâmetro de query `clinic_id` foi **removido**. A verificação da clínica agora é feita internamente usando o ID da clínica associado ao token JWT do usuário autenticado.

**Nova URL de Exemplo:**
```
http://localhost:8000/api/v1/consultations/78901234-23cf-443d-b7a6-529e7ea5f234
```

**Path Parameters:**
- `consultation_id`: ID UUID da consulta (obrigatório)

**Query Parameters:**
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ **REMOVIDO**

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório e agora usado para verificar a posse da consulta)

**Request Body (Exemplo):**
```json
{
  "description": "Atualização da descrição da consulta.",
  "date": "2023-10-27T11:00:00Z"
}
```

**Responses:**
- `200 OK`: Consulta atualizada com sucesso (a estrutura da resposta permanece a mesma).
- `400 Bad Request`: Nenhum dado fornecido para atualização.
- `401 Unauthorized`: Token JWT inválido ou ausente.
- `404 Not Found`: Consulta não encontrada ou não pertence à clínica do usuário autenticado.
- `500 Internal Server Error`: Erro interno ao atualizar consulta. 