# Documentação da API VeTech

Esta documentação lista todas as rotas disponíveis na API VeTech, detalhando suas funcionalidades, parâmetros e respostas.

## Autenticação

### `POST /api/v1/auth/register`

Registra uma nova clínica na plataforma.

**Request Body:**
```json
{
  "name": "Clínica Veterinária Exemplo",
  "email": "clinica@exemplo.com",
  "phone": "11999999999",
  "password": "senha123",
  "subscription_tier": "basic"
}
```

**Responses:**
- `201 Created`: Clínica criada com sucesso
  ```json
  {
    "id": "uuid",
    "name": "Clínica Veterinária Exemplo",
    "email": "clinica@exemplo.com",
    "phone": "11999999999",
    "subscription_tier": "basic",
    "max_clients": 50,
    "created_at": "2023-04-07T22:50:00.000Z",
    "updated_at": "2023-04-07T22:50:00.000Z"
  }
  ```
- `400 Bad Request`: Email já registrado ou dados inválidos

### `POST /api/v1/auth/login`

Realiza login de uma clínica.

**Request Body:**
```json
{
  "email": "clinica@exemplo.com",
  "password": "senha123"
}
```

**Responses:**
- `200 OK`: Login com sucesso
  ```json
  {
    "access_token": "string",
    "token_type": "bearer",
    "clinic": {
      "id": "uuid",
      "name": "Clínica Veterinária Exemplo",
      "email": "clinica@exemplo.com"
    }
  }
  ```
- `401 Unauthorized`: Credenciais inválidas

### `POST /api/v1/auth/logout`

Realiza logout de uma clínica, invalidando a sessão atual.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Responses:**
- `200 OK`: Logout realizado com sucesso
  ```json
  {
    "message": "Logout bem-sucedido. Por favor, descarte o token no cliente."
  }
  ```
- `401 Unauthorized`: Token inválido ou ausente

## Perfil da Clínica

### `GET /api/v1/clinic/profile`

Obtém os dados de perfil da clínica atualmente logada.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Responses:**
- `200 OK`: Perfil obtido com sucesso
  ```json
  {
    "id": "uuid",
    "name": "Clínica Veterinária Exemplo",
    "email": "clinica@exemplo.com",
    "phone": "11999999999",
    "subscription_tier": "basic",
    "max_clients": 50,
    "created_at": "2023-04-07T22:50:00.000Z",
    "updated_at": "2023-04-07T22:50:00.000Z"
  }
  ```
- `401 Unauthorized`: Token inválido ou ausente
- `404 Not Found`: Perfil de clínica não encontrado
- `500 Internal Server Error`: Erro ao buscar dados do perfil

### `PUT /api/v1/clinic/profile`

Atualiza os dados de perfil da clínica atualmente logada.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Request Body:**
```json
{
  "name": "Novo Nome da Clínica",
  "phone": "11988888888"
}
```

**Responses:**
- `200 OK`: Perfil atualizado com sucesso
  ```json
  {
    "id": "uuid",
    "name": "Novo Nome da Clínica",
    "email": "clinica@exemplo.com",
    "phone": "11988888888",
    "subscription_tier": "basic",
    "max_clients": 50,
    "created_at": "2023-04-07T22:50:00.000Z",
    "updated_at": "2023-04-08T10:30:00.000Z",
    "message": "Perfil atualizado com sucesso"
  }
  ```
- `400 Bad Request`: Nenhum dado fornecido para atualização
- `401 Unauthorized`: Token inválido ou ausente
- `404 Not Found`: Perfil de clínica não encontrado
- `500 Internal Server Error`: Erro ao atualizar dados do perfil

## Animais

### `POST /api/v1/animals`

Cadastra um novo animal vinculado a uma clínica.

**Query Parameters:**
- `clinic_id`: ID UUID da clínica que está cadastrando o animal (obrigatório)

**Request Body:**
```json
{
  "name": "Rex",
  "species": "Cachorro",
  "breed": "Labrador",
  "age": 5,
  "weight": 25.5,
  "medical_history": "Animal saudável com vacinas em dia."
}
```

**Responses:**
- `200 OK`: Animal criado com sucesso
  ```json
  {
    "id": "uuid",
    "clinic_id": "uuid",
    "name": "Rex",
    "species": "Cachorro",
    "breed": "Labrador",
    "age": 5,
    "weight": 25.5,
    "medical_history": "Animal saudável com vacinas em dia.",
    "created_at": "2023-04-07T23:50:00.000Z",
    "updated_at": "2023-04-07T23:50:00.000Z"
  }
  ```
- `500 Internal Server Error`: Erro ao criar animal

### `GET /api/v1/animals`

Obtém todos os animais vinculados a uma clínica.

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)

**Responses:**
- `200 OK`: Lista de animais
  ```json
  [
    {
      "id": "uuid",
      "clinic_id": "uuid",
      "name": "Rex",
      "species": "Cachorro",
      "breed": "Labrador",
      "age": 5,
      "weight": 25.5,
      "medical_history": "Animal saudável com vacinas em dia.",
      "created_at": "2023-04-07T23:50:00.000Z",
      "updated_at": "2023-04-07T23:50:00.000Z"
    }
  ]
  ```
- `500 Internal Server Error`: Erro ao buscar animais

### `GET /api/v1/animals/{animal_id}`

Obtém detalhes de um animal específico.

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)

**Responses:**
- `200 OK`: Detalhes do animal
  ```json
  {
    "id": "uuid",
    "clinic_id": "uuid",
    "name": "Rex",
    "species": "Cachorro",
    "breed": "Labrador",
    "age": 5,
    "weight": 25.5,
    "medical_history": "Animal saudável com vacinas em dia.",
    "created_at": "2023-04-07T23:50:00.000Z",
    "updated_at": "2023-04-07T23:50:00.000Z"
  }
  ```
- `404 Not Found`: Animal não encontrado ou não pertence à clínica
- `500 Internal Server Error`: Erro ao buscar animal

### `PATCH /api/v1/animals/{animal_id}`

Atualiza um animal existente.

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)

**Request Body:**
```json
{
  "name": "Rex Atualizado",
  "breed": "Labrador Retriever",
  "age": 6,
  "weight": 26.0,
  "medical_history": "Atualização do histórico médico."
}
```

**Responses:**
- `200 OK`: Animal atualizado com sucesso
  ```json
  {
    "id": "uuid",
    "clinic_id": "uuid",
    "name": "Rex Atualizado",
    "species": "Cachorro",
    "breed": "Labrador Retriever",
    "age": 6,
    "weight": 26.0,
    "medical_history": "Atualização do histórico médico.",
    "created_at": "2023-04-07T23:50:00.000Z",
    "updated_at": "2023-04-08T11:00:00.000Z"
  }
  ```
- `400 Bad Request`: Nenhum dado fornecido para atualização
- `404 Not Found`: Animal não encontrado ou não pertence à clínica
- `500 Internal Server Error`: Erro ao atualizar animal

### `DELETE /api/v1/animals/{animal_id}`

Remove um animal pelo ID.

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)

**Responses:**
- `204 No Content`: Animal removido com sucesso.
- `404 Not Found`: Animal não encontrado ou não pertence à clínica
- `500 Internal Server Error`: Erro ao deletar animal

### `POST /api/v1/animals/{animal_id}/preferences`

Cadastra preferências alimentares para um animal.

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)

**Request Body:**
```json
{
  "gosta_de": "Ração Premium, Frango, Cenoura",
  "nao_gosta_de": "Ração de baixa qualidade, Vegetais verdes"
}
```

**Responses:**
- `200 OK`: Preferências criadas com sucesso
  ```json
  {
    "id": "uuid",
    "animal_id": "uuid",
    "gosta_de": "Ração Premium, Frango, Cenoura",
    "nao_gosta_de": "Ração de baixa qualidade, Vegetais verdes",
    "created_at": "2023-05-10T14:30:00.000Z",
    "updated_at": "2023-05-10T14:30:00.000Z"
  }
  ```
- `400 Bad Request`: Já existem preferências cadastradas para este animal
- `404 Not Found`: Animal não encontrado ou não pertence à clínica
- `500 Internal Server Error`: Erro ao criar preferências

### `GET /api/v1/animals/{animal_id}/preferences`

Obtém as preferências alimentares de um animal.

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)

**Responses:**
- `200 OK`: Preferências obtidas com sucesso
  ```json
  {
    "id": "uuid",
    "animal_id": "uuid",
    "gosta_de": "Ração Premium, Frango, Cenoura",
    "nao_gosta_de": "Ração de baixa qualidade, Vegetais verdes",
    "created_at": "2023-05-10T14:30:00.000Z",
    "updated_at": "2023-05-10T14:30:00.000Z"
  }
  ```
- `404 Not Found`: Animal não encontrado ou não pertence à clínica / Preferências não encontradas
- `500 Internal Server Error`: Erro ao obter preferências

### `PUT /api/v1/animals/{animal_id}/preferences`

Atualiza as preferências alimentares de um animal.

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)

**Request Body:**
```json
{
  "gosta_de": "Ração Premium, Frango, Cenoura, Petiscos",
  "nao_gosta_de": "Ração de baixa qualidade, Brócolis, Couve-flor"
}
```

**Responses:**
- `200 OK`: Preferências atualizadas com sucesso
  ```json
  {
    "id": "uuid",
    "animal_id": "uuid",
    "gosta_de": "Ração Premium, Frango, Cenoura, Petiscos",
    "nao_gosta_de": "Ração de baixa qualidade, Brócolis, Couve-flor",
    "created_at": "2023-05-10T14:30:00.000Z",
    "updated_at": "2023-05-10T15:00:00.000Z"
  }
  ```
- `400 Bad Request`: Nenhum dado fornecido para atualização
- `404 Not Found`: Animal não encontrado ou não pertence à clínica / Preferências não encontradas
- `500 Internal Server Error`: Erro ao atualizar preferências

## Agendamentos

### `POST /api/v1/appointments`

Cria um novo agendamento para um animal.

**Query Parameters:**
- `clinic_id`: ID UUID da clínica que está criando o agendamento (obrigatório)

**Request Body:**
```json
{
  "animal_id": "uuid",
  "date": "2023-05-15",
  "start_time": "14:30:00",
  "end_time": "15:00:00",
  "description": "Consulta de rotina",
  "status": "scheduled"
}
```

**Responses:**
- `200 OK`: Agendamento criado com sucesso
  ```json
  {
    "id": "uuid",
    "clinic_id": "uuid",
    "animal_id": "uuid",
    "date": "2023-05-15",
    "start_time": "14:30:00",
    "end_time": "15:00:00",
    "description": "Consulta de rotina",
    "status": "scheduled",
    "created_at": "2023-04-08T10:00:00.000Z",
    "updated_at": "2023-04-08T10:00:00.000Z"
  }
  ```
- `400 Bad Request`: Horário já ocupado ou dados inválidos
- `404 Not Found`: Animal não encontrado ou não pertence à clínica
- `500 Internal Server Error`: Erro ao criar agendamento

### `GET /api/v1/appointments`

Obtém todos os agendamentos de uma clínica, ordenados por data e hora.

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)
- `date_from`: Filtrar agendamentos a partir desta data (opcional)
- `status`: Filtrar por status (opcional) - valores: scheduled, completed, cancelled

**Responses:**
- `200 OK`: Lista de agendamentos
  ```json
  [
    {
      "id": "uuid",
      "clinic_id": "uuid",
      "animal_id": "uuid",
      "date": "2023-05-15",
      "start_time": "14:30:00",
      "end_time": "15:00:00",
      "description": "Consulta de rotina",
      "status": "scheduled",
      "created_at": "2023-04-08T10:00:00.000Z",
      "updated_at": "2023-04-08T10:00:00.000Z"
    }
  ]
  ```
- `500 Internal Server Error`: Erro ao buscar agendamentos

### `GET /api/v1/appointments/{appointment_id}`

Obtém um agendamento específico pelo ID.

**Path Parameters:**
- `appointment_id`: ID UUID do agendamento (obrigatório)

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)

**Responses:**
- `200 OK`: Detalhes do agendamento
  ```json
  {
    "id": "uuid",
    "clinic_id": "uuid",
    "animal_id": "uuid",
    "date": "2023-05-15",
    "start_time": "14:30:00",
    "end_time": "15:00:00",
    "description": "Consulta de rotina",
    "status": "scheduled",
    "created_at": "2023-04-08T10:00:00.000Z",
    "updated_at": "2023-04-08T10:00:00.000Z"
  }
  ```
- `404 Not Found`: Agendamento não encontrado
- `500 Internal Server Error`: Erro ao buscar agendamento

### `DELETE /api/v1/appointments/{appointment_id}`

Remove um agendamento pelo ID.

**Path Parameters:**
- `appointment_id`: ID UUID do agendamento (obrigatório)

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)

**Responses:**
- `200 OK`: Agendamento removido com sucesso
  ```json
  {
    "message": "Agendamento removido com sucesso."
  }
  ```
- `404 Not Found`: Agendamento não encontrado ou não pertence à clínica
- `500 Internal Server Error`: Erro ao deletar agendamento

### `PATCH /api/v1/appointments/{appointment_id}`

Atualiza um agendamento existente.

**Path Parameters:**
- `appointment_id`: ID UUID do agendamento (obrigatório)

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)

**Request Body:**
```json
{
  "date": "2023-05-20",
  "start_time": "15:30:00",
  "end_time": "16:00:00",
  "description": "Consulta de rotina atualizada",
  "status": "completed"
}
```

**Responses:**
- `200 OK`: Agendamento atualizado com sucesso
  ```json
  {
    "id": "uuid",
    "clinic_id": "uuid",
    "animal_id": "uuid",
    "date": "2023-05-20",
    "start_time": "15:30:00",
    "end_time": "16:00:00",
    "description": "Consulta de rotina atualizada",
    "status": "completed",
    "created_at": "2023-04-08T10:00:00.000Z",
    "updated_at": "2023-04-08T11:00:00.000Z"
  }
  ```
- `400 Bad Request`: Horário já ocupado ou dados inválidos
- `404 Not Found`: Agendamento não encontrado ou não pertence à clínica
- `500 Internal Server Error`: Erro ao atualizar agendamento

## Consultas

### `POST /api/v1/consultations`

Cria uma nova consulta para um animal.

**Query Parameters:**
- `clinic_id`: ID UUID da clínica que está criando a consulta (obrigatório)

**Request Body:**
```json
{
  "animal_id": "uuid",
  "description": "Consulta inicial, exame físico completo.",
  "date": "2023-10-26T10:00:00Z" // Opcional, padrão para data/hora atual
}
```

**Responses:**
- `200 OK`: Consulta criada com sucesso
  ```json
  {
    "id": "uuid",
    "clinic_id": "uuid",
    "animal_id": "uuid",
    "date": "2023-10-26T10:00:00Z",
    "description": "Consulta inicial, exame físico completo.",
    "created_at": "2023-10-26T10:00:00Z",
    "updated_at": "2023-10-26T10:00:00Z"
  }
  ```
- `404 Not Found`: Animal não encontrado ou não pertence à clínica
- `500 Internal Server Error`: Erro ao criar consulta

### `GET /api/v1/consultations`

Obtém todas as consultas de uma clínica, opcionalmente filtradas por animal.

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)
- `animal_id`: Filtrar consultas por ID do animal (opcional)

**Responses:**
- `200 OK`: Lista de consultas
  ```json
  [
    {
      "id": "uuid",
      "clinic_id": "uuid",
      "animal_id": "uuid",
      "date": "2023-10-26T10:00:00Z",
      "description": "Consulta inicial, exame físico completo.",
      "created_at": "2023-10-26T10:00:00Z",
      "updated_at": "2023-10-26T10:00:00Z"
    }
  ]
  ```
- `500 Internal Server Error`: Erro ao buscar consultas

### `PATCH /api/v1/consultations/{consultation_id}`

Atualiza uma consulta existente.

**Path Parameters:**
- `consultation_id`: ID UUID da consulta (obrigatório)

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)

**Request Body:**
```json
{
  "description": "Atualização da descrição da consulta.",
  "date": "2023-10-27T11:00:00Z"
}
```

**Responses:**
- `200 OK`: Consulta atualizada com sucesso
  ```json
  {
    "id": "uuid",
    "clinic_id": "uuid",
    "animal_id": "uuid",
    "date": "2023-10-27T11:00:00Z",
    "description": "Atualização da descrição da consulta.",
    "created_at": "2023-10-26T10:00:00Z",
    "updated_at": "2023-10-27T11:00:00Z"
  }
  ```
- `400 Bad Request`: Nenhum dado fornecido para atualização
- `404 Not Found`: Consulta não encontrada ou não pertence à clínica
- `500 Internal Server Error`: Erro ao atualizar consulta

### `DELETE /api/v1/consultations/{consultation_id}`

Remove uma consulta pelo ID.

**Path Parameters:**
- `consultation_id`: ID UUID da consulta (obrigatório)

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)

**Responses:**
- `204 No Content`: Consulta removida com sucesso.
- `404 Not Found`: Consulta não encontrada ou não pertence à clínica
- `500 Internal Server Error`: Erro ao deletar consulta

## Nutrição e Dietas

### `POST /api/v1/animals/{animal_id}/diets`

Cria um plano de dieta para um animal.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Request Body:**
```json
{
  "tipo": "ração",
  "objetivo": "Emagrecimento",
  "peso_atual_pet": 25.5,
  "idade_pet": 5,
  "raca_pet": "Labrador",
  "tamanho_pet": "grande",
  "observacoes": "Animal com sobrepeso, precisa reduzir calorias diárias",
  "data_inicio": "2023-08-01",
  "data_fim": "2023-10-01",
  "status": "ativa"
}
```

**Responses:**
- `200 OK`: Dieta criada com sucesso
  ```json
  {
    "id": "uuid",
    "pet_id": "uuid",
    "clinica_id": "uuid",
    "tipo": "ração",
    "objetivo": "Emagrecimento",
    "peso_atual_pet": 25.5,
    "idade_pet": 5,
    "raca_pet": "Labrador",
    "tamanho_pet": "grande",
    "observacoes": "Animal com sobrepeso, precisa reduzir calorias diárias",
    "data_inicio": "2023-08-01",
    "data_fim": "2023-10-01",
    "status": "ativa",
    "created_at": "2023-08-01T10:00:00.000Z",
    "updated_at": "2023-08-01T10:00:00.000Z",
    "opcoes_dieta": []
  }
  ```
- `401 Unauthorized`: Token inválido ou ausente
- `404 Not Found`: Animal não encontrado ou não pertence à clínica
- `500 Internal Server Error`: Erro ao criar dieta

### `GET /api/v1/animals/{animal_id}/diets`

Lista todas as dietas de um animal.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Responses:**
- `200 OK`: Lista de dietas
  ```json
  [
    {
      "id": "uuid",
      "pet_id": "uuid",
      "clinica_id": "uuid",
      "tipo": "ração",
      "objetivo": "Emagrecimento",
      "peso_atual_pet": 25.5,
      "idade_pet": 5,
      "raca_pet": "Labrador",
      "tamanho_pet": "grande",
      "observacoes": "Animal com sobrepeso, precisa reduzir calorias diárias",
      "data_inicio": "2023-08-01",
      "data_fim": "2023-10-01",
      "status": "ativa",
      "created_at": "2023-08-01T10:00:00.000Z",
      "updated_at": "2023-08-01T10:00:00.000Z",
      "opcoes_dieta": [
        {
          "id": "uuid",
          "dieta_id": "uuid",
          "nome": "Ração Premium Light",
          "valor_mensal_estimado": 300.0,
          "calorias_totais_dia": 1200,
          "porcao_refeicao": "200g por refeição",
          "refeicoes_por_dia": 2,
          "indicacao": "Recomendada para cães com sobrepeso",
          "created_at": "2023-08-01T10:05:00.000Z",
          "updated_at": "2023-08-01T10:05:00.000Z"
        }
      ]
    }
  ]
  ```
- `401 Unauthorized`: Token inválido ou ausente
- `500 Internal Server Error`: Erro ao listar dietas

### `GET /api/v1/diets/{diet_id}`

Obtém detalhes de uma dieta específica.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `diet_id`: ID UUID da dieta (obrigatório)

**Responses:**
- `200 OK`: Detalhes da dieta
  ```json
  {
    "id": "uuid",
    "pet_id": "uuid",
    "clinica_id": "uuid",
    "tipo": "ração",
    "objetivo": "Emagrecimento",
    "peso_atual_pet": 25.5,
    "idade_pet": 5,
    "raca_pet": "Labrador",
    "tamanho_pet": "grande",
    "observacoes": "Animal com sobrepeso, precisa reduzir calorias diárias",
    "data_inicio": "2023-08-01",
    "data_fim": "2023-10-01",
    "status": "ativa",
    "created_at": "2023-08-01T10:00:00.000Z",
    "updated_at": "2023-08-01T10:00:00.000Z",
    "opcoes_dieta": [
      {
        "id": "uuid",
        "dieta_id": "uuid",
        "nome": "Ração Premium Light",
        "valor_mensal_estimado": 300.0,
        "calorias_totais_dia": 1200,
        "porcao_refeicao": "200g por refeição",
        "refeicoes_por_dia": 2,
        "indicacao": "Recomendada para cães com sobrepeso",
        "created_at": "2023-08-01T10:05:00.000Z",
        "updated_at": "2023-08-01T10:05:00.000Z"
      }
    ]
  }
  ```
- `401 Unauthorized`: Token inválido ou ausente
- `404 Not Found`: Dieta não encontrada
- `500 Internal Server Error`: Erro ao obter dieta

### `PUT /api/v1/diets/{diet_id}`

Atualiza uma dieta existente.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `diet_id`: ID UUID da dieta (obrigatório)

**Request Body:**
```json
{
  "tipo": "caseira",
  "objetivo": "Manutenção",
  "observacoes": "Dieta atualizada para manutenção de peso",
  "status": "finalizada"
}
```

**Responses:**
- `200 OK`: Dieta atualizada com sucesso (com estrutura idêntica à resposta GET)
- `400 Bad Request`: Nenhum dado fornecido para atualização
- `401 Unauthorized`: Token inválido ou ausente
- `404 Not Found`: Dieta não encontrada ou não pertence à clínica
- `500 Internal Server Error`: Erro ao atualizar dieta

### `DELETE /api/v1/diets/{diet_id}`

Remove uma dieta pelo ID.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `diet_id`: ID UUID da dieta (obrigatório)

**Responses:**
- `200 OK`: Dieta removida com sucesso
  ```json
  {
    "message": "Dieta removida com sucesso"
  }
  ```
- `401 Unauthorized`: Token inválido ou ausente
- `404 Not Found`: Dieta não encontrada ou não pertence à clínica
- `500 Internal Server Error`: Erro ao remover dieta

### `POST /api/v1/diets/{diet_id}/options`

Adiciona uma opção de dieta a um plano.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `diet_id`: ID UUID da dieta (obrigatório)

**Request Body:**
```json
{
  "nome": "Ração Premium Light",
  "valor_mensal_estimado": 300.0,
  "calorias_totais_dia": 1200,
  "porcao_refeicao": "200g por refeição",
  "refeicoes_por_dia": 2,
  "indicacao": "Recomendada para cães com sobrepeso"
}
```

**Responses:**
- `200 OK`: Opção de dieta criada com sucesso
  ```json
  {
    "id": "uuid",
    "dieta_id": "uuid",
    "nome": "Ração Premium Light",
    "valor_mensal_estimado": 300.0,
    "calorias_totais_dia": 1200,
    "porcao_refeicao": "200g por refeição",
    "refeicoes_por_dia": 2,
    "indicacao": "Recomendada para cães com sobrepeso",
    "created_at": "2023-08-01T10:05:00.000Z",
    "updated_at": "2023-08-01T10:05:00.000Z"
  }
  ```
- `401 Unauthorized`: Token inválido ou ausente
- `404 Not Found`: Dieta não encontrada ou não pertence à clínica
- `500 Internal Server Error`: Erro ao criar opção de dieta

### `POST /api/v1/animals/{animal_id}/restricted-foods`

Adiciona um alimento que o pet deve evitar.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Request Body:**
```json
{
  "nome": "Chocolate",
  "motivo": "Tóxico para cães"
}
```

**Responses:**
- `200 OK`: Alimento a evitar adicionado com sucesso
  ```json
  {
    "id": "uuid",
    "pet_id": "uuid",
    "nome": "Chocolate",
    "motivo": "Tóxico para cães",
    "created_at": "2023-08-01T10:10:00.000Z",
    "updated_at": "2023-08-01T10:10:00.000Z"
  }
  ```
- `401 Unauthorized`: Token inválido ou ausente
- `404 Not Found`: Animal não encontrado ou não pertence à clínica
- `500 Internal Server Error`: Erro ao adicionar alimento a evitar

### `GET /api/v1/animals/{animal_id}/restricted-foods`

Lista todos os alimentos que o pet deve evitar.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Responses:**
- `200 OK`: Lista de alimentos a evitar
  ```json
  [
    {
      "id": "uuid",
      "pet_id": "uuid",
      "nome": "Chocolate",
      "motivo": "Tóxico para cães",
      "created_at": "2023-08-01T10:10:00.000Z",
      "updated_at": "2023-08-01T10:10:00.000Z"
    }
  ]
  ```
- `401 Unauthorized`: Token inválido ou ausente
- `404 Not Found`: Animal não encontrado ou não pertence à clínica
- `500 Internal Server Error`: Erro ao listar alimentos a evitar

### `POST /api/v1/animals/{animal_id}/snacks`

Adiciona um snack permitido entre refeições.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Request Body:**
```json
{
  "nome": "Bifinho de Frango",
  "frequencia_semanal": 3,
  "quantidade": "1 unidade",
  "observacoes": "Dar após exercícios"
}
```

**Responses:**
- `200 OK`: Snack adicionado com sucesso
  ```json
  {
    "id": "uuid",
    "pet_id": "uuid",
    "nome": "Bifinho de Frango",
    "frequencia_semanal": 3,
    "quantidade": "1 unidade",
    "observacoes": "Dar após exercícios",
    "created_at": "2023-08-01T10:15:00.000Z",
    "updated_at": "2023-08-01T10:15:00.000Z"
  }
  ```
- `401 Unauthorized`: Token inválido ou ausente
- `404 Not Found`: Animal não encontrado ou não pertence à clínica
- `500 Internal Server Error`: Erro ao adicionar snack

### `GET /api/v1/animals/{animal_id}/snacks`

Lista todos os snacks permitidos entre refeições.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Responses:**
- `200 OK`: Lista de snacks
  ```json
  [
    {
      "id": "uuid",
      "pet_id": "uuid",
      "nome": "Bifinho de Frango",
      "frequencia_semanal": 3,
      "quantidade": "1 unidade",
      "observacoes": "Dar após exercícios",
      "created_at": "2023-08-01T10:15:00.000Z",
      "updated_at": "2023-08-01T10:15:00.000Z"
    }
  ]
  ```
- `401 Unauthorized`: Token inválido ou ausente
- `404 Not Found`: Animal não encontrado ou não pertence à clínica
- `500 Internal Server Error`: Erro ao listar snacks

### `POST /api/v1/diet-options/{option_id}/foods`

Adiciona um alimento a uma opção de dieta.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `option_id`: ID UUID da opção de dieta (obrigatório)

**Request Body:**
```json
{
  "nome": "Ração Premium Light",
  "tipo": "ração",
  "quantidade": "200g",
  "calorias": 600,
  "horario": "Manhã"
}
```

**Responses:**
- `200 OK`: Alimento adicionado com sucesso
  ```json
  {
    "id": "uuid",
    "opcao_dieta_id": "uuid",
    "nome": "Ração Premium Light",
    "tipo": "ração",
    "quantidade": "200g",
    "calorias": 600,
    "horario": "Manhã",
    "created_at": "2023-08-01T10:20:00.000Z",
    "updated_at": "2023-08-01T10:20:00.000Z"
  }
  ```
- `401 Unauthorized`: Token inválido ou ausente
- `403 Forbidden`: Acesso negado a esta opção de dieta
- `404 Not Found`: Opção de dieta não encontrada
- `500 Internal Server Error`: Erro ao adicionar alimento

### `GET /api/v1/diet-options/{option_id}/foods`

Lista todos os alimentos de uma opção de dieta.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `option_id`: ID UUID da opção de dieta (obrigatório)

**Responses:**
- `200 OK`: Lista de alimentos
  ```json
  [
    {
      "id": "uuid",
      "opcao_dieta_id": "uuid",
      "nome": "Ração Premium Light",
      "tipo": "ração",
      "quantidade": "200g",
      "calorias": 600,
      "horario": "Manhã",
      "created_at": "2023-08-01T10:20:00.000Z",
      "updated_at": "2023-08-01T10:20:00.000Z"
    }
  ]
  ```
- `401 Unauthorized`: Token inválido ou ausente
- `403 Forbidden`: Acesso negado a esta opção de dieta
- `404 Not Found`: Opção de dieta não encontrada
- `500 Internal Server Error`: Erro ao listar alimentos

### `DELETE /api/v1/diet-options/{option_id}`

Remove uma opção de dieta específica.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `option_id`: ID UUID da opção de dieta (obrigatório)

**Responses:**
- `204 No Content`: Opção de dieta removida com sucesso.
- `401 Unauthorized`: Token inválido ou ausente
- `403 Forbidden`: Acesso negado a esta opção de dieta
- `404 Not Found`: Opção de dieta não encontrada
- `500 Internal Server Error`: Erro ao remover opção de dieta

### `PUT /api/v1/animals/{animal_id}/restricted-foods/{food_id}`

Atualiza um alimento que o pet deve evitar.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)
- `food_id`: ID UUID do alimento a evitar (obrigatório)

**Request Body:**
```json
{
  "nome": "Cebola",
  "motivo": "Altamente tóxico para cães e gatos"
}
```

**Responses:**
- `200 OK`: Alimento atualizado com sucesso (estrutura idêntica à resposta GET)
- `400 Bad Request`: Nenhum dado fornecido para atualização
- `401 Unauthorized`: Token inválido ou ausente
- `404 Not Found`: Animal ou alimento a evitar não encontrado
- `500 Internal Server Error`: Erro ao atualizar alimento a evitar

### `DELETE /api/v1/animals/{animal_id}/restricted-foods/{food_id}`

Remove um alimento que o pet deve evitar.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)
- `food_id`: ID UUID do alimento a evitar (obrigatório)

**Responses:**
- `204 No Content`: Alimento removido com sucesso.
- `401 Unauthorized`: Token inválido ou ausente
- `404 Not Found`: Animal ou alimento a evitar não encontrado
- `500 Internal Server Error`: Erro ao remover alimento a evitar

### `PUT /api/v1/animals/{animal_id}/snacks/{snack_id}`

Atualiza um snack permitido.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)
- `snack_id`: ID UUID do snack (obrigatório)

**Request Body:**
```json
{
  "frequencia_semanal": 2,
  "quantidade": "Meio bifinho",
  "observacoes": "Dar apenas após caminhadas longas"
}
```

**Responses:**
- `200 OK`: Snack atualizado com sucesso (estrutura idêntica à resposta GET)
- `400 Bad Request`: Nenhum dado fornecido para atualização
- `401 Unauthorized`: Token inválido ou ausente
- `404 Not Found`: Animal ou snack não encontrado
- `500 Internal Server Error`: Erro ao atualizar snack

### `DELETE /api/v1/animals/{animal_id}/snacks/{snack_id}`

Remove um snack permitido.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)
- `snack_id`: ID UUID do snack (obrigatório)

**Responses:**
- `204 No Content`: Snack removido com sucesso.
- `401 Unauthorized`: Token inválido ou ausente
- `404 Not Found`: Animal ou snack não encontrado
- `500 Internal Server Error`: Erro ao remover snack

### `PUT /api/v1/diet-foods/{food_id}`

Atualiza um alimento de uma opção de dieta.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `food_id`: ID UUID do alimento (obrigatório)

**Request Body:**
```json
{
  "quantidade": "250g",
  "calorias": 700,
  "horario": "Manhã e Noite"
}
```

**Responses:**
- `200 OK`: Alimento atualizado com sucesso (estrutura idêntica à resposta GET)
- `400 Bad Request`: Nenhum dado fornecido para atualização
- `401 Unauthorized`: Token inválido ou ausente
- `403 Forbidden`: Acesso negado a este alimento
- `404 Not Found`: Alimento não encontrado
- `500 Internal Server Error`: Erro ao atualizar alimento

### `DELETE /api/v1/diet-foods/{food_id}`

Remove um alimento de uma opção de dieta.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `food_id`: ID UUID do alimento (obrigatório)

**Responses:**
- `204 No Content`: Alimento removido com sucesso.
- `401 Unauthorized`: Token inválido ou ausente
- `403 Forbidden`: Acesso negado a este alimento
- `404 Not Found`: Alimento não encontrado
- `500 Internal Server Error`: Erro ao remover alimento

### `GET /api/v1/diet-foods/{food_id}`

Obtém detalhes de um alimento de uma opção de dieta.

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `food_id`: ID UUID do alimento (obrigatório)

**Responses:**
- `200 OK`: Detalhes do alimento
  ```json
  {
    "id": "uuid",
    "opcao_dieta_id": "uuid",
    "nome": "Ração Premium Light",
    "tipo": "ração",
    "quantidade": "250g",
    "calorias": 700,
    "horario": "Manhã e Noite",
    "created_at": "2023-08-01T10:20:00.000Z",
    "updated_at": "2023-08-01T10:20:00.000Z"
  }
  ```
- `401 Unauthorized`: Token inválido ou ausente
- `403 Forbidden`: Acesso negado a este alimento
- `404 Not Found`: Alimento não encontrado
- `500 Internal Server Error`: Erro ao obter detalhes do alimento 