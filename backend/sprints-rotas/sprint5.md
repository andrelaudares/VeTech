# Módulo de Atividades Físicas (Revisado com Base no Schema DB Real)

## 1. Atividades Disponíveis (`atividades`)

### `POST /api/v1/atividades`
Cadastra um novo tipo de atividade física disponível. **Nota:** A tabela `atividades` atual não possui campos para descrição, intensidade, indicações, contraindicações ou clinic_id.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/atividades
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Request Body:**
```json
{
  "nome": "Caminhada",
  "tipo": "cardiovascular",
  "calorias_estimadas_por_minuto": 5
}
```

**Responses:**
- `201 Created`: Atividade cadastrada com sucesso
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "nome": "Caminhada",
    "tipo": "cardiovascular",
    "calorias_estimadas_por_minuto": 5,
    "created_at": "2023-10-25T15:30:00Z",
    "updated_at": "2023-10-25T15:30:00Z"
  }
  ```
- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Token inválido ou expirado
- `500 Internal Server Error`: Erro ao criar atividade

### `GET /api/v1/atividades`
Lista todas as atividades físicas disponíveis.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/atividades?tipo=cardiovascular
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Query Parameters:**
- `tipo`: Filtrar por tipo de atividade (opcional)
- `calorias_gt`: Filtrar por calorias estimadas por minuto maior que (opcional)
- `calorias_lt`: Filtrar por calorias estimadas por minuto menor que (opcional)

**Responses:**
- `200 OK`: Lista de atividades
  ```json
  [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "nome": "Caminhada",
      "tipo": "cardiovascular",
      "calorias_estimadas_por_minuto": 5,
      "created_at": "2023-10-25T15:30:00Z",
      "updated_at": "2023-10-25T15:30:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "nome": "Natação",
      "tipo": "cardiovascular",
      "calorias_estimadas_por_minuto": 8,
      "created_at": "2023-10-25T15:35:00Z",
      "updated_at": "2023-10-25T15:35:00Z"
    }
  ]
  ```
- `401 Unauthorized`: Token inválido ou expirado
- `500 Internal Server Error`: Erro ao listar atividades

### `GET /api/v1/atividades/{atividade_id}`
Obtém detalhes de uma atividade específica.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/atividades/550e8400-e29b-41d4-a716-446655440000
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `atividade_id`: ID UUID da atividade (obrigatório)

**Responses:**
- `200 OK`: Detalhes da atividade
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "nome": "Caminhada",
    "tipo": "cardiovascular",
    "calorias_estimadas_por_minuto": 5,
    "created_at": "2023-10-25T15:30:00Z",
    "updated_at": "2023-10-25T15:30:00Z"
  }
  ```
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Atividade não encontrada
- `500 Internal Server Error`: Erro ao buscar atividade

### `PUT /api/v1/atividades/{atividade_id}`
Atualiza uma atividade existente.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/atividades/550e8400-e29b-41d4-a716-446655440000
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `atividade_id`: ID UUID da atividade (obrigatório)

**Request Body:**
```json
{
  "nome": "Caminhada Leve",
  "calorias_estimadas_por_minuto": 4
}
```

**Responses:**
- `200 OK`: Atividade atualizada com sucesso
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "nome": "Caminhada Leve",
    "tipo": "cardiovascular",
    "calorias_estimadas_por_minuto": 4,
    "created_at": "2023-10-25T15:30:00Z",
    "updated_at": "2023-10-25T16:15:00Z"
  }
  ```
- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Atividade não encontrada
- `500 Internal Server Error`: Erro ao atualizar atividade

### `DELETE /api/v1/atividades/{atividade_id}`
Remove uma atividade do sistema.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/atividades/550e8400-e29b-41d4-a716-446655440000
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `atividade_id`: ID UUID da atividade (obrigatório)

**Responses:**
- `204 No Content`: Atividade removida com sucesso
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Atividade não encontrada
- `500 Internal Server Error`: Erro ao remover atividade (pode falhar se houver planos de atividade associados)

---

## 2. Planos de Atividade (`planos_atividade`)

**Importante:** A tabela `planos_atividade` armazena tanto as informações gerais do plano quanto os detalhes da atividade programada (qual atividade, frequência, duração, etc.). Não há uma tabela separada para "atividades programadas". Os campos `nome` e `objetivo` não existem na tabela atual.

### `POST /api/v1/animals/{animal_id}/planos-atividade`
Cria um novo plano de atividade (incluindo a programação) para um animal.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/c7020821-b8fe-4608-9f7f-2bad17877ca4/planos-atividade
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Request Body:**
```json
{
  "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4", // Redundante com path, mas necessário no modelo
  "clinic_id": "2e956d70-1f8a-47ce-8fbf-5fb84410b6ee", // ID da clínica do usuário logado (obrigatório)
  "data_inicio": "2023-11-01",
  "data_fim": "2023-12-01",
  "orientacoes": "Aumentar gradualmente a intensidade", // Campo 'observacoes' mapeado para 'orientacoes'
  "status": "ativo",
  "atividade_id": "550e8400-e29b-41d4-a716-446655440000", // ID da atividade a ser programada
  "frequencia_semanal": 3,
  "duracao_minutos": 20,
  "intensidade": "leve"
}
```

**Responses:**
- `201 Created`: Plano criado com sucesso
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
    "clinic_id": "2e956d70-1f8a-47ce-8fbf-5fb84410b6ee",
    "data_inicio": "2023-11-01",
    "data_fim": "2023-12-01",
    "orientacoes": "Aumentar gradualmente a intensidade",
    "status": "ativo",
    "atividade_id": "550e8400-e29b-41d4-a716-446655440000",
    "frequencia_semanal": 3,
    "duracao_minutos": 20,
    "intensidade": "leve",
    "nome_atividade": "Caminhada", // Nome buscado da tabela 'atividades'
    "created_at": "2023-10-25T16:45:00Z",
    "updated_at": "2023-10-25T16:45:00Z"
  }
  ```
- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Animal ou Atividade não encontrados
- `500 Internal Server Error`: Erro ao criar plano

### `GET /api/v1/animals/{animal_id}/planos-atividade`
Lista todos os planos de atividade (com suas programações) de um animal.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/c7020821-b8fe-4608-9f7f-2bad17877ca4/planos-atividade?status=ativo
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- `status`: Filtrar por status do plano (opcional) - valores: ativo, inativo, concluido
- `atividade_id`: Filtrar por ID da atividade programada (opcional)
- `intensidade`: Filtrar por intensidade programada (opcional)

**Responses:**
- `200 OK`: Lista de planos
  ```json
  [
    {
      "id": "550e8400-e29b-41d4-a716-446655440002",
      "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
      "clinic_id": "2e956d70-1f8a-47ce-8fbf-5fb84410b6ee",
      "data_inicio": "2023-11-01",
      "data_fim": "2023-12-01",
      "orientacoes": "Aumentar gradualmente a intensidade",
      "status": "ativo",
      "atividade_id": "550e8400-e29b-41d4-a716-446655440000",
      "frequencia_semanal": 3,
      "duracao_minutos": 20,
      "intensidade": "leve",
      "nome_atividade": "Caminhada",
      "created_at": "2023-10-25T16:45:00Z",
      "updated_at": "2023-10-25T16:45:00Z"
    }
    // ... outros planos
  ]
  ```
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Animal não encontrado
- `500 Internal Server Error`: Erro ao listar planos

### `GET /api/v1/planos-atividade/{plano_id}`
Obtém detalhes de um plano de atividade específico (incluindo sua programação).

**Exemplo de URL:**
```
http://localhost:8000/api/v1/planos-atividade/550e8400-e29b-41d4-a716-446655440002
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `plano_id`: ID UUID do plano (obrigatório)

**Responses:**
- `200 OK`: Detalhes do plano
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
    "clinic_id": "2e956d70-1f8a-47ce-8fbf-5fb84410b6ee",
    "data_inicio": "2023-11-01",
    "data_fim": "2023-12-01",
    "orientacoes": "Aumentar gradualmente a intensidade",
    "status": "ativo",
    "atividade_id": "550e8400-e29b-41d4-a716-446655440000",
    "frequencia_semanal": 3,
    "duracao_minutos": 20,
    "intensidade": "leve",
    "nome_atividade": "Caminhada",
    "created_at": "2023-10-25T16:45:00Z",
    "updated_at": "2023-10-25T16:45:00Z"
  }
  ```
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Plano não encontrado
- `500 Internal Server Error`: Erro ao buscar plano

### `PUT /api/v1/planos-atividade/{plano_id}`
Atualiza um plano de atividade existente (incluindo sua programação).

**Exemplo de URL:**
```
http://localhost:8000/api/v1/planos-atividade/550e8400-e29b-41d4-a716-446655440002
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `plano_id`: ID UUID do plano (obrigatório)

**Request Body:** (Apenas os campos a serem alterados)
```json
{
  "orientacoes": "Aumentar a frequência para 4x por semana após a segunda semana. Manter duração e intensidade.",
  "data_fim": "2024-01-01",
  "frequencia_semanal": 4
}
```

**Responses:**
- `200 OK`: Plano atualizado com sucesso
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
    "clinic_id": "2e956d70-1f8a-47ce-8fbf-5fb84410b6ee",
    "data_inicio": "2023-11-01", // Mantido
    "data_fim": "2024-01-01",   // Atualizado
    "orientacoes": "Aumentar a frequência para 4x por semana após a segunda semana. Manter duração e intensidade.", // Atualizado
    "status": "ativo",         // Mantido
    "atividade_id": "550e8400-e29b-41d4-a716-446655440000", // Mantido
    "frequencia_semanal": 4,  // Atualizado
    "duracao_minutos": 20,    // Mantido
    "intensidade": "leve",    // Mantido
    "nome_atividade": "Caminhada",
    "created_at": "2023-10-25T16:45:00Z",
    "updated_at": "2023-10-25T17:20:00Z" // Atualizado
  }
  ```
- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Plano ou (se alterada) Atividade não encontrados
- `500 Internal Server Error`: Erro ao atualizar plano

### `DELETE /api/v1/planos-atividade/{plano_id}`
Remove um plano de atividade (e sua programação associada). **Atenção:** Isso também removerá as atividades realizadas (`atividades_realizadas`) associadas a este plano devido à relação de chave estrangeira (se configurada com `ON DELETE CASCADE`).

**Exemplo de URL:**
```
http://localhost:8000/api/v1/planos-atividade/550e8400-e29b-41d4-a716-446655440002
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `plano_id`: ID UUID do plano (obrigatório)

**Responses:**
- `204 No Content`: Plano removido com sucesso
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Plano não encontrado
- `500 Internal Server Error`: Erro ao remover plano

---

## 3. Atividades Realizadas (`atividades_realizadas`)

**Importante:** A tabela `atividades_realizadas` não possui o campo `intensidade_real`. A coluna `concluida` foi mapeada para `realizado`, `duracao_minutos` para `duracao_realizada_minutos` e `observacoes` para `observacao_tutor`. A ligação é feita diretamente com `plano_id`.

### `POST /api/v1/planos-atividade/{plano_id}/atividades-realizadas`
Registra uma atividade física realizada associada a um plano.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/planos-atividade/550e8400-e29b-41d4-a716-446655440002/atividades-realizadas
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `plano_id`: ID UUID do plano ao qual esta execução pertence (obrigatório)

**Request Body:**
```json
{
  "plano_id": "550e8400-e29b-41d4-a716-446655440002", // Redundante, mas no modelo
  "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4", // Necessário obter do plano ou passar explicitamente
  "data": "2023-11-02",
  "duracao_realizada_minutos": 22,
  "observacao_tutor": "Animal apresentou boa disposição durante toda atividade",
  "realizado": true
}
```

**Responses:**
- `201 Created`: Atividade realizada registrada com sucesso
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440004",
    "plano_id": "550e8400-e29b-41d4-a716-446655440002",
    "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
    "nome_atividade": "Caminhada", // Buscado via plano_id -> atividade_id
    "data": "2023-11-02",
    "duracao_realizada_minutos": 22,
    "observacao_tutor": "Animal apresentou boa disposição durante toda atividade",
    "realizado": true,
    "created_at": "2023-11-02T10:30:00Z",
    "updated_at": "2023-11-02T10:30:00Z"
  }
  ```
- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Plano não encontrado
- `500 Internal Server Error`: Erro ao registrar atividade realizada

### `GET /api/v1/animals/{animal_id}/atividades-realizadas`
Visualiza o histórico de atividades realizadas de um pet.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/c7020821-b8fe-4608-9f7f-2bad17877ca4/atividades-realizadas?data_inicio=2023-11-01&data_fim=2023-11-07
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- `data_inicio`: Filtrar a partir desta data (YYYY-MM-DD) (opcional)
- `data_fim`: Filtrar até esta data (YYYY-MM-DD) (opcional)
- `realizado`: Filtrar por status de realização (opcional) - valores: true, false
- `plano_id`: Filtrar por plano específico (opcional)

**Responses:**
- `200 OK`: Histórico de atividades realizadas
  ```json
  [
    {
      "id": "550e8400-e29b-41d4-a716-446655440004",
      "plano_id": "550e8400-e29b-41d4-a716-446655440002",
      "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
      "nome_atividade": "Caminhada",
      "data": "2023-11-02",
      "duracao_realizada_minutos": 22,
      "observacao_tutor": "Animal apresentou boa disposição durante toda atividade",
      "realizado": true,
      "created_at": "2023-11-02T10:30:00Z",
      "updated_at": "2023-11-02T10:30:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440005",
      "plano_id": "550e8400-e29b-41d4-a716-446655440002",
      "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
      "nome_atividade": "Caminhada",
      "data": "2023-11-04",
      "duracao_realizada_minutos": 25,
      "observacao_tutor": "Aumentou o ritmo no meio da atividade",
      "realizado": true,
      "created_at": "2023-11-04T11:15:00Z",
      "updated_at": "2023-11-04T11:15:00Z"
    }
    // ... outras atividades realizadas
  ]
  ```
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Animal não encontrado
- `500 Internal Server Error`: Erro ao buscar histórico

### `GET /api/v1/planos-atividade/{plano_id}/atividades-realizadas`
Lista todas as atividades realizadas de um plano específico.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/planos-atividade/550e8400-e29b-41d4-a716-446655440002/atividades-realizadas
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `plano_id`: ID UUID do plano (obrigatório)

**Query Parameters:**
- `data_inicio`: Filtrar a partir desta data (YYYY-MM-DD) (opcional)
- `data_fim`: Filtrar até esta data (YYYY-MM-DD) (opcional)
- `realizado`: Filtrar por status de realização (opcional) - valores: true, false

**Responses:**
- `200 OK`: Lista de atividades realizadas para o plano
  ```json
  [
    {
      "id": "550e8400-e29b-41d4-a716-446655440004",
      "plano_id": "550e8400-e29b-41d4-a716-446655440002",
      "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4", // Incluído para contexto
      "nome_atividade": "Caminhada",
      "data": "2023-11-02",
      "duracao_realizada_minutos": 22,
      "observacao_tutor": "Animal apresentou boa disposição durante toda atividade",
      "realizado": true,
      "created_at": "2023-11-02T10:30:00Z",
      "updated_at": "2023-11-02T10:30:00Z"
    }
    // ... outras atividades realizadas do plano
  ]
  ```
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Plano não encontrado
- `500 Internal Server Error`: Erro ao listar atividades realizadas

### `PUT /api/v1/atividades-realizadas/{realizacao_id}`
Atualiza uma atividade realizada específica.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/atividades-realizadas/550e8400-e29b-41d4-a716-446655440004
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `realizacao_id`: ID UUID da atividade realizada (obrigatório)

**Request Body:** (Apenas campos a serem alterados)
```json
{
  "duracao_realizada_minutos": 25,
  "observacao_tutor": "Animal apresentou melhora no fôlego após 10 minutos",
  "realizado": true
}
```

**Responses:**
- `200 OK`: Atividade realizada atualizada com sucesso
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440004",
    "plano_id": "550e8400-e29b-41d4-a716-446655440002",
    "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
    "nome_atividade": "Caminhada",
    "data": "2023-11-02", // Mantido
    "duracao_realizada_minutos": 25, // Atualizado
    "observacao_tutor": "Animal apresentou melhora no fôlego após 10 minutos", // Atualizado
    "realizado": true, // Atualizado (ou mantido)
    "created_at": "2023-11-02T10:30:00Z",
    "updated_at": "2023-11-02T11:45:00Z" // Atualizado
  }
  ```
- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Atividade realizada não encontrada (ou não pertence à clínica)
- `500 Internal Server Error`: Erro ao atualizar atividade realizada

### `DELETE /api/v1/atividades-realizadas/{realizacao_id}`
Remove um registro de atividade realizada.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/atividades-realizadas/550e8400-e29b-41d4-a716-446655440004
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `realizacao_id`: ID UUID da atividade realizada (obrigatório)

**Responses:**
- `204 No Content`: Atividade realizada removida com sucesso
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Atividade realizada não encontrada (ou não pertence à clínica)
- `500 Internal Server Error`: Erro ao remover atividade realizada

---

## 4. Métricas e Estatísticas

**Importante:** A lógica para calcular essas métricas precisará ser ajustada no backend para refletir a nova estrutura de dados (sem atividades programadas separadas e com os nomes de colunas corretos em `atividades_realizadas`). A estrutura do endpoint e da resposta permanece a mesma por enquanto.

### `GET /api/v1/animals/{animal_id}/activity-metrics`
Obtém métricas e estatísticas das atividades físicas de um animal, calculadas com base nos dados de `planos_atividade` e `atividades_realizadas`.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/c7020821-b8fe-4608-9f7f-2bad17877ca4/activity-metrics?periodo=mensal
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- `periodo`: Período para cálculo das métricas (opcional) - valores: semanal, mensal, trimestral (default: mensal)
- `data_inicio`: Data inicial para cálculo (YYYY-MM-DD) (opcional, sobrescreve `periodo`)
- `data_fim`: Data final para cálculo (YYYY-MM-DD) (opcional, default: hoje)

**Responses:**
- `200 OK`: Métricas de atividade
  ```json
  {
    "total_atividades": 12, // Total de registros em atividades_realizadas no período
    "total_minutos": 280, // Soma de duracao_realizada_minutos no período
    "media_minutos_por_atividade": 23.3,
    "calorias_estimadas": 1400, // Calculado com base na atividade (via plano_id) e duracao_realizada_minutos
    "completude_plano": 85, // % de dias com atividade realizada vs. dias esperados (calculado a partir da frequencia_semanal do plano)
    "atividades_por_tipo": { // Agrupado pelo nome da atividade (via plano_id)
      "caminhada": 8,
      "natação": 2,
      "brincadeira": 2
    },
    "progresso_semanal": [ // Agrupado por semana com base na data da atividade_realizada
      {"semana": "2023-10-30", "minutos": 60, "atividades": 3},
      {"semana": "2023-11-06", "minutos": 70, "atividades": 3},
      {"semana": "2023-11-13", "minutos": 75, "atividades": 3},
      {"semana": "2023-11-20", "minutos": 75, "atividades": 3}
    ]
  }
  ```
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Animal não encontrado
- `500 Internal Server Error`: Erro ao calcular métricas
