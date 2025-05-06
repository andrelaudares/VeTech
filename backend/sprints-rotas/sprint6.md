# Módulo de Gamificação e Sistema de Recompensas

## 1. Metas de Gamificação

### `POST /api/v1/gamificacao/metas`
Cria uma nova meta de gamificação.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/gamificacao/metas
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Request Body:**
```json
{
  "clinic_id": "2e956d70-1f8a-47ce-8fbf-5fb84410b6ee", // ID da clínica do usuário logado
  "descricao": "Realizar caminhadas 5x por semana",
  "tipo": "atividade",
  "quantidade": 5,
  "unidade": "caminhadas",
  "periodo": "semanal",
  "pontos_recompensa": 100,
  "status": "ativa"
}
```

**Responses:**
- `201 Created`: Meta criada com sucesso
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "clinic_id": "2e956d70-1f8a-47ce-8fbf-5fb84410b6ee",
    "descricao": "Realizar caminhadas 5x por semana",
    "tipo": "atividade",
    "quantidade": 5,
    "unidade": "caminhadas",
    "periodo": "semanal",
    "pontos_recompensa": 100,
    "status": "ativa",
    "created_at": "2023-11-10T14:30:00Z",
    "updated_at": "2023-11-10T14:30:00Z"
  }
  ```
- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Token inválido ou expirado
- `500 Internal Server Error`: Erro ao criar meta

### `GET /api/v1/gamificacao/metas`
Lista todas as metas de gamificação disponíveis para a clínica.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/gamificacao/metas?tipo=atividade&status=ativa
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Query Parameters:**
- `tipo`: Filtrar por tipo de meta (opcional) - valores: atividade, alimentacao, peso, consulta
- `status`: Filtrar por status (opcional) - valores: ativa, inativa
- `periodo`: Filtrar por período (opcional) - valores: diario, semanal, mensal

**Responses:**
- `200 OK`: Lista de metas
  ```json
  [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "clinic_id": "2e956d70-1f8a-47ce-8fbf-5fb84410b6ee",
      "descricao": "Realizar caminhadas 5x por semana",
      "tipo": "atividade",
      "quantidade": 5,
      "unidade": "caminhadas",
      "periodo": "semanal",
      "pontos_recompensa": 100,
      "status": "ativa",
      "created_at": "2023-11-10T14:30:00Z",
      "updated_at": "2023-11-10T14:30:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "clinic_id": "2e956d70-1f8a-47ce-8fbf-5fb84410b6ee",
      "descricao": "Seguir dieta sem falhas por 7 dias",
      "tipo": "alimentacao",
      "quantidade": 7,
      "unidade": "dias",
      "periodo": "semanal",
      "pontos_recompensa": 150,
      "status": "ativa",
      "created_at": "2023-11-10T14:35:00Z",
      "updated_at": "2023-11-10T14:35:00Z"
    }
  ]
  ```
- `401 Unauthorized`: Token inválido ou expirado
- `500 Internal Server Error`: Erro ao listar metas

### `GET /api/v1/gamificacao/metas/{meta_id}`
Obtém detalhes de uma meta específica.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/gamificacao/metas/550e8400-e29b-41d4-a716-446655440000
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `meta_id`: ID UUID da meta (obrigatório)

**Responses:**
- `200 OK`: Detalhes da meta
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "clinic_id": "2e956d70-1f8a-47ce-8fbf-5fb84410b6ee",
    "descricao": "Realizar caminhadas 5x por semana",
    "tipo": "atividade",
    "quantidade": 5,
    "unidade": "caminhadas",
    "periodo": "semanal",
    "pontos_recompensa": 100,
    "status": "ativa",
    "created_at": "2023-11-10T14:30:00Z",
    "updated_at": "2023-11-10T14:30:00Z"
  }
  ```
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Meta não encontrada
- `500 Internal Server Error`: Erro ao buscar meta

### `PUT /api/v1/gamificacao/metas/{meta_id}`
Atualiza uma meta existente.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/gamificacao/metas/550e8400-e29b-41d4-a716-446655440000
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `meta_id`: ID UUID da meta (obrigatório)

**Request Body:**
```json
{
  "descricao": "Realizar caminhadas 4x por semana",
  "quantidade": 4,
  "pontos_recompensa": 80,
  "status": "ativa"
}
```

**Responses:**
- `200 OK`: Meta atualizada com sucesso
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "clinic_id": "2e956d70-1f8a-47ce-8fbf-5fb84410b6ee",
    "descricao": "Realizar caminhadas 4x por semana",
    "tipo": "atividade",
    "quantidade": 4,
    "unidade": "caminhadas",
    "periodo": "semanal",
    "pontos_recompensa": 80,
    "status": "ativa",
    "created_at": "2023-11-10T14:30:00Z",
    "updated_at": "2023-11-10T15:45:00Z"
  }
  ```
- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Meta não encontrada
- `500 Internal Server Error`: Erro ao atualizar meta

### `DELETE /api/v1/gamificacao/metas/{meta_id}`
Remove uma meta do sistema.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/gamificacao/metas/550e8400-e29b-41d4-a716-446655440000
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `meta_id`: ID UUID da meta (obrigatório)

**Responses:**
- `204 No Content`: Meta removida com sucesso
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Meta não encontrada
- `500 Internal Server Error`: Erro ao remover meta

---

## 2. Pontuações

### `POST /api/v1/gamificacao/pontuacoes`
Atribui pontuação a um animal por meta alcançada ou atividade realizada.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/gamificacao/pontuacoes
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Request Body:**
```json
{
  "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
  "meta_id": "550e8400-e29b-41d4-a716-446655440000",
  "atividade_realizada_id": null,
  "pontos_obtidos": 100,
  "data": "2023-11-12T10:30:00Z",
  "descricao": "Meta semanal de caminhadas alcançada"
}
```

**Responses:**
- `201 Created`: Pontuação registrada com sucesso
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
    "meta_id": "550e8400-e29b-41d4-a716-446655440000",
    "atividade_realizada_id": null,
    "pontos_obtidos": 100,
    "data": "2023-11-12T10:30:00Z",
    "descricao": "Meta semanal de caminhadas alcançada",
    "created_at": "2023-11-12T10:30:00Z"
  }
  ```
- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Animal ou meta não encontrados
- `500 Internal Server Error`: Erro ao registrar pontuação

### `GET /api/v1/animals/{animal_id}/gamificacao/pontuacoes`
Visualiza o histórico de pontuações de um animal.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/c7020821-b8fe-4608-9f7f-2bad17877ca4/gamificacao/pontuacoes?data_inicio=2023-11-01&data_fim=2023-11-15
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- `data_inicio`: Filtrar a partir desta data (YYYY-MM-DD) (opcional)
- `data_fim`: Filtrar até esta data (YYYY-MM-DD) (opcional)
- `meta_id`: Filtrar por meta específica (opcional)

**Responses:**
- `200 OK`: Histórico de pontuações
  ```json
  [
    {
      "id": "550e8400-e29b-41d4-a716-446655440002",
      "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
      "meta_id": "550e8400-e29b-41d4-a716-446655440000",
      "meta_descricao": "Realizar caminhadas 4x por semana",
      "atividade_realizada_id": null,
      "pontos_obtidos": 100,
      "data": "2023-11-12T10:30:00Z",
      "descricao": "Meta semanal de caminhadas alcançada",
      "created_at": "2023-11-12T10:30:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440003",
      "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
      "meta_id": "550e8400-e29b-41d4-a716-446655440001",
      "meta_descricao": "Seguir dieta sem falhas por 7 dias",
      "atividade_realizada_id": null,
      "pontos_obtidos": 150,
      "data": "2023-11-14T09:45:00Z",
      "descricao": "Meta semanal de alimentação alcançada",
      "created_at": "2023-11-14T09:45:00Z"
    }
  ]
  ```
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Animal não encontrado
- `500 Internal Server Error`: Erro ao buscar histórico

### `DELETE /api/v1/gamificacao/pontuacoes/{pontuacao_id}`
Remove um registro de pontuação.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/gamificacao/pontuacoes/550e8400-e29b-41d4-a716-446655440002
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `pontuacao_id`: ID UUID da pontuação (obrigatório)

**Responses:**
- `204 No Content`: Pontuação removida com sucesso
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Pontuação não encontrada
- `500 Internal Server Error`: Erro ao remover pontuação

---

## 3. Recompensas

### `POST /api/v1/gamificacao/recompensas`
Cria uma nova recompensa para ser desbloqueada por pontos.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/gamificacao/recompensas
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Request Body:**
```json
{
  "nome": "Desconto de 10% em banho",
  "pontos_necessarios": 500,
  "tipo": "desconto",
  "descricao": "Desconto de 10% em serviço de banho e tosa na clínica"
}
```

**Responses:**
- `201 Created`: Recompensa criada com sucesso
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440004",
    "nome": "Desconto de 10% em banho",
    "pontos_necessarios": 500,
    "tipo": "desconto",
    "descricao": "Desconto de 10% em serviço de banho e tosa na clínica",
    "created_at": "2023-11-15T11:30:00Z",
    "updated_at": "2023-11-15T11:30:00Z"
  }
  ```
- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Token inválido ou expirado
- `500 Internal Server Error`: Erro ao criar recompensa

### `GET /api/v1/gamificacao/recompensas`
Lista todas as recompensas disponíveis.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/gamificacao/recompensas?tipo=desconto
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Query Parameters:**
- `tipo`: Filtrar por tipo de recompensa (opcional)
- `pontos_min`: Filtrar por pontos mínimos necessários (opcional)
- `pontos_max`: Filtrar por pontos máximos necessários (opcional)

**Responses:**
- `200 OK`: Lista de recompensas
  ```json
  [
    {
      "id": "550e8400-e29b-41d4-a716-446655440004",
      "nome": "Desconto de 10% em banho",
      "pontos_necessarios": 500,
      "tipo": "desconto",
      "descricao": "Desconto de 10% em serviço de banho e tosa na clínica",
      "created_at": "2023-11-15T11:30:00Z",
      "updated_at": "2023-11-15T11:30:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440005",
      "nome": "Desconto de 15% em consulta",
      "pontos_necessarios": 800,
      "tipo": "desconto",
      "descricao": "Desconto de 15% em consulta veterinária",
      "created_at": "2023-11-15T11:35:00Z",
      "updated_at": "2023-11-15T11:35:00Z"
    }
  ]
  ```
- `401 Unauthorized`: Token inválido ou expirado
- `500 Internal Server Error`: Erro ao listar recompensas

### `GET /api/v1/gamificacao/recompensas/{recompensa_id}`
Obtém detalhes de uma recompensa específica.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/gamificacao/recompensas/550e8400-e29b-41d4-a716-446655440004
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `recompensa_id`: ID UUID da recompensa (obrigatório)

**Responses:**
- `200 OK`: Detalhes da recompensa
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440004",
    "nome": "Desconto de 10% em banho",
    "pontos_necessarios": 500,
    "tipo": "desconto",
    "descricao": "Desconto de 10% em serviço de banho e tosa na clínica",
    "created_at": "2023-11-15T11:30:00Z",
    "updated_at": "2023-11-15T11:30:00Z"
  }
  ```
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Recompensa não encontrada
- `500 Internal Server Error`: Erro ao buscar recompensa

### `PUT /api/v1/gamificacao/recompensas/{recompensa_id}`
Atualiza uma recompensa existente.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/gamificacao/recompensas/550e8400-e29b-41d4-a716-446655440004
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `recompensa_id`: ID UUID da recompensa (obrigatório)

**Request Body:**
```json
{
  "nome": "Desconto de 15% em banho",
  "pontos_necessarios": 600,
  "descricao": "Desconto de 15% em serviço de banho e tosa na clínica"
}
```

**Responses:**
- `200 OK`: Recompensa atualizada com sucesso
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440004",
    "nome": "Desconto de 15% em banho",
    "pontos_necessarios": 600,
    "tipo": "desconto",
    "descricao": "Desconto de 15% em serviço de banho e tosa na clínica",
    "created_at": "2023-11-15T11:30:00Z",
    "updated_at": "2023-11-15T13:45:00Z"
  }
  ```
- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Recompensa não encontrada
- `500 Internal Server Error`: Erro ao atualizar recompensa

### `DELETE /api/v1/gamificacao/recompensas/{recompensa_id}`
Remove uma recompensa do sistema.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/gamificacao/recompensas/550e8400-e29b-41d4-a716-446655440004
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `recompensa_id`: ID UUID da recompensa (obrigatório)

**Responses:**
- `204 No Content`: Recompensa removida com sucesso
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Recompensa não encontrada
- `500 Internal Server Error`: Erro ao remover recompensa

---

## 4. Atribuição de Recompensas

### `POST /api/v1/animals/{animal_id}/gamificacao/recompensas`
Atribui recompensas aos pets que atingirem pontuação necessária.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/c7020821-b8fe-4608-9f7f-2bad17877ca4/gamificacao/recompensas
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Request Body:**
```json
{
  "recompensa_id": "550e8400-e29b-41d4-a716-446655440004",
  "codigo_verificacao": "DISCOUNT-123456",
  "data_expiracao": "2023-12-31",
  "observacoes": "Apresentar código na clínica para receber o desconto"
}
```

**Responses:**
- `201 Created`: Recompensa atribuída com sucesso
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440006",
    "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
    "recompensa_id": "550e8400-e29b-41d4-a716-446655440004",
    "pontos_utilizados": 500,
    "data_atribuicao": "2023-11-16T09:30:00Z",
    "codigo_verificacao": "DISCOUNT-123456",
    "data_expiracao": "2023-12-31",
    "observacoes": "Apresentar código na clínica para receber o desconto",
    "status": "disponivel"
  }
  ```
- `400 Bad Request`: Dados inválidos ou pontos insuficientes
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Animal ou recompensa não encontrados
- `500 Internal Server Error`: Erro ao atribuir recompensa

**Nota:** Como não há uma tabela específica para recompensas atribuídas no banco de dados, esta operação seria implementada criando registros que relacionam animais e recompensas, possivelmente em uma tabela intermediária que precisaria ser criada.

### `GET /api/v1/animals/{animal_id}/gamificacao/recompensas`
Lista todas as recompensas atribuídas a um animal.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/c7020821-b8fe-4608-9f7f-2bad17877ca4/gamificacao/recompensas?status=disponivel
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- `status`: Filtrar por status da recompensa (opcional) - valores: disponivel, utilizada, expirada
- `data_inicio`: Filtrar a partir desta data de atribuição (opcional)
- `data_fim`: Filtrar até esta data de atribuição (opcional)

**Responses:**
- `200 OK`: Lista de recompensas atribuídas
  ```json
  [
    {
      "id": "550e8400-e29b-41d4-a716-446655440006",
      "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
      "recompensa_id": "550e8400-e29b-41d4-a716-446655440004",
      "recompensa_nome": "Desconto de 15% em banho",
      "pontos_utilizados": 500,
      "data_atribuicao": "2023-11-16T09:30:00Z",
      "codigo_verificacao": "DISCOUNT-123456",
      "data_expiracao": "2023-12-31",
      "observacoes": "Apresentar código na clínica para receber o desconto",
      "status": "disponivel"
    }
  ]
  ```
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Animal não encontrado
- `500 Internal Server Error`: Erro ao listar recompensas atribuídas

---

## 5. Ranking e Estatísticas

### `GET /api/v1/gamificacao/ranking`
Visualiza ranking de pontuação entre os pets.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/gamificacao/ranking?periodo=mensal&limite=10
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Query Parameters:**
- `periodo`: Período para cálculo do ranking (opcional) - valores: semanal, mensal, trimestral, total (default: total)
- `data_inicio`: Data inicial para cálculo (YYYY-MM-DD) (opcional, sobrescreve `periodo`)
- `data_fim`: Data final para cálculo (YYYY-MM-DD) (opcional, default: hoje)
- `limite`: Número máximo de resultados (opcional, default: 20)
- `clinic_id`: Filtrar por clínica específica (opcional, default: todas)

**Responses:**
- `200 OK`: Ranking de pets
  ```json
  [
    {
      "posicao": 1,
      "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
      "animal_nome": "Rex",
      "pontos_totais": 750,
      "clinic_id": "2e956d70-1f8a-47ce-8fbf-5fb84410b6ee",
      "clinic_nome": "Clínica VetExemplo"
    },
    {
      "posicao": 2,
      "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca5",
      "animal_nome": "Luna",
      "pontos_totais": 600,
      "clinic_id": "2e956d70-1f8a-47ce-8fbf-5fb84410b6ee",
      "clinic_nome": "Clínica VetExemplo"
    }
  ]
  ```
- `401 Unauthorized`: Token inválido ou expirado
- `500 Internal Server Error`: Erro ao gerar ranking

### `GET /api/v1/animals/{animal_id}/gamificacao/estatisticas`
Obtém estatísticas e progresso do pet nas metas de gamificação.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/c7020821-b8fe-4608-9f7f-2bad17877ca4/gamificacao/estatisticas?periodo=mensal
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- `periodo`: Período para cálculo das estatísticas (opcional) - valores: semanal, mensal, trimestral (default: mensal)
- `data_inicio`: Data inicial para cálculo (YYYY-MM-DD) (opcional, sobrescreve `periodo`)
- `data_fim`: Data final para cálculo (YYYY-MM-DD) (opcional, default: hoje)

**Responses:**
- `200 OK`: Estatísticas de gamificação
  ```json
  {
    "pontos_totais": 750,
    "pontos_periodo": 250,
    "pontos_disponiveis": 500,
    "recompensas_resgatadas": 1,
    "metas_concluidas": 5,
    "metas_em_andamento": 2,
    "progresso_metas": [
      {
        "meta_id": "550e8400-e29b-41d4-a716-446655440000",
        "descricao": "Realizar caminhadas 4x por semana",
        "progresso_atual": 3,
        "meta_total": 4,
        "percentual": 75,
        "status": "em_andamento"
      },
      {
        "meta_id": "550e8400-e29b-41d4-a716-446655440001",
        "descricao": "Seguir dieta sem falhas por 7 dias",
        "progresso_atual": 7,
        "meta_total": 7,
        "percentual": 100,
        "status": "concluida"
      }
    ],
    "historico_pontos": [
      {"data": "2023-11-01", "pontos": 50},
      {"data": "2023-11-08", "pontos": 100},
      {"data": "2023-11-12", "pontos": 100},
      {"data": "2023-11-14", "pontos": 150},
      {"data": "2023-11-15", "pontos": 50}
    ]
  }
  ```
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Animal não encontrado
- `500 Internal Server Error`: Erro ao calcular estatísticas

### `GET /api/v1/animals/{animal_id}/gamificacao/relatorios`
Gera relatórios de progresso do pet nas metas.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/c7020821-b8fe-4608-9f7f-2bad17877ca4/gamificacao/relatorios?tipo=pdf&periodo=trimestral
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- `tipo`: Formato do relatório (opcional) - valores: json, pdf, csv (default: json)
- `periodo`: Período para o relatório (opcional) - valores: semanal, mensal, trimestral, anual (default: mensal)
- `data_inicio`: Data inicial para o relatório (YYYY-MM-DD) (opcional, sobrescreve `periodo`)
- `data_fim`: Data final para o relatório (YYYY-MM-DD) (opcional, default: hoje)

**Responses:**
- `200 OK`: Relatório gerado
  ```json
  {
    "animal": {
      "id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
      "nome": "Rex",
      "tutor": "João Silva"
    },
    "periodo": {
      "inicio": "2023-09-01",
      "fim": "2023-11-30"
    },
    "resumo": {
      "pontos_acumulados": 1250,
      "recompensas_resgatadas": 2,
      "metas_concluidas": 15
    },
    "progresso_por_categoria": {
      "atividade": {
        "total_metas": 6,
        "concluidas": 5,
        "percentual": 83
      },
      "alimentacao": {
        "total_metas": 8,
        "concluidas": 7,
        "percentual": 88
      },
      "consulta": {
        "total_metas": 3,
        "concluidas": 3,
        "percentual": 100
      }
    },
    "detalhamento_mensal": [
      {
        "mes": "Setembro/2023",
        "pontos": 400,
        "metas_concluidas": 5,
        "metas_detalhadas": [
          {"descricao": "Realizar caminhadas 4x por semana", "semanas_concluidas": 3, "total_semanas": 4}
        ]
      },
      {
        "mes": "Outubro/2023",
        "pontos": 450,
        "metas_concluidas": 5,
        "metas_detalhadas": [
          {"descricao": "Realizar caminhadas 4x por semana", "semanas_concluidas": 4, "total_semanas": 4}
        ]
      },
      {
        "mes": "Novembro/2023",
        "pontos": 400,
        "metas_concluidas": 5,
        "metas_detalhadas": [
          {"descricao": "Realizar caminhadas 4x por semana", "semanas_concluidas": 3, "total_semanas": 4}
        ]
      }
    ],
    "recomendacoes": [
      "Aumentar frequência de atividades aeróbicas",
      "Manter padrão de alimentação saudável",
      "Continuar com visitas regulares à clínica"
    ]
  }
  ```
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Animal não encontrado
- `500 Internal Server Error`: Erro ao gerar relatório
