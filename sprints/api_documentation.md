# Documentação da API VeTech

Esta documentação lista todas as rotas disponíveis na API VeTech, detalhando suas funcionalidades, parâmetros e respostas.

## Autenticação

### `POST /api/v1/auth/register`

Registra uma nova clínica na plataforma.

**URL de Exemplo:**
```
http://localhost:8000/api/v1/auth/register
```

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
    "id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/auth/login
```

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
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "clinic": {
      "id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
      "name": "Clínica Veterinária Exemplo",
      "email": "clinica@exemplo.com"
    }
  }
  ```
- `401 Unauthorized`: Credenciais inválidas

### `POST /api/v1/auth/logout`

Realiza logout de uma clínica, invalidando a sessão atual.

**URL de Exemplo:**
```
http://localhost:8000/api/v1/auth/logout
```

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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/clinic/profile
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Responses:**
- `200 OK`: Perfil obtido com sucesso
  ```json
  {
    "id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/clinic/profile
```

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
    "id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/animals?clinic_id=bd330f0a-23cf-443d-b7a6-529e7ea5f234
```

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
    "id": "3e2ce4a2-f75b-468c-9353-04ba4996f548",
    "clinic_id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/animals?clinic_id=bd330f0a-23cf-443d-b7a6-529e7ea5f234
```

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)

**Responses:**
- `200 OK`: Lista de animais
  ```json
  [
    {
      "id": "3e2ce4a2-f75b-468c-9353-04ba4996f548",
      "clinic_id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/animals/3e2ce4a2-f75b-468c-9353-04ba4996f548?clinic_id=bd330f0a-23cf-443d-b7a6-529e7ea5f234
```

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)

**Responses:**
- `200 OK`: Detalhes do animal
  ```json
  {
    "id": "3e2ce4a2-f75b-468c-9353-04ba4996f548",
    "clinic_id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/animals/3e2ce4a2-f75b-468c-9353-04ba4996f548?clinic_id=bd330f0a-23cf-443d-b7a6-529e7ea5f234
```

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
    "id": "3e2ce4a2-f75b-468c-9353-04ba4996f548",
    "clinic_id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/animals/3e2ce4a2-f75b-468c-9353-04ba4996f548?clinic_id=bd330f0a-23cf-443d-b7a6-529e7ea5f234
```

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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/animals/3e2ce4a2-f75b-468c-9353-04ba4996f548/preferences
```

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO

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
    "id": "45678901-23cf-443d-b7a6-529e7ea5f234",
    "animal_id": "3e2ce4a2-f75b-468c-9353-04ba4996f548",
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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/animals/3e2ce4a2-f75b-468c-9353-04ba4996f548/preferences
```

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO

**Responses:**
- `200 OK`: Preferências obtidas com sucesso
  ```json
  {
    "id": "45678901-23cf-443d-b7a6-529e7ea5f234",
    "animal_id": "3e2ce4a2-f75b-468c-9353-04ba4996f548",
    "gosta_de": "Ração Premium, Frango, Cenoura",
    "nao_gosta_de": "Ração de baixa qualidade, Vegetais verdes",
    "created_at": "2023-05-10T14:30:00.000Z",
    "updated_at": "2023-05-10T14:30:00.000Z"
  }
  ```
- `404 Not Found`: Animal não encontrado ou não pertence à clínica / Preferências não encontradas
- `500 Internal Server Error`: Erro ao obter preferências

### `PATCH /api/v1/animals/{animal_id}/preferences`

Atualiza (parcialmente) as preferências alimentares de um animal. (Método alterado de PUT para PATCH).

**URL de Exemplo:**
```
http://localhost:8000/api/v1/animals/3e2ce4a2-f75b-468c-9353-04ba4996f548/preferences
```

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO

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
    "id": "45678901-23cf-443d-b7a6-529e7ea5f234",
    "animal_id": "3e2ce4a2-f75b-468c-9353-04ba4996f548",
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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/appointments?clinic_id=bd330f0a-23cf-443d-b7a6-529e7ea5f234
```

**Query Parameters:**
- `clinic_id`: ID UUID da clínica que está criando o agendamento (obrigatório)

**Request Body:**
```json
{
  "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
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
    "id": "12345678-23cf-443d-b7a6-529e7ea5f234",
    "clinic_id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
    "animal_id": "3e2ce4a2-f75b-468c-9353-04ba4996f548",
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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/appointments?clinic_id=bd330f0a-23cf-443d-b7a6-529e7ea5f234&date_from=2023-05-15&status=scheduled
```

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)
- `date_from`: Filtrar agendamentos a partir desta data (opcional)
- `status`: Filtrar por status (opcional) - valores: scheduled, completed, cancelled

**Responses:**
- `200 OK`: Lista de agendamentos
  ```json
  [
    {
      "id": "12345678-23cf-443d-b7a6-529e7ea5f234",
      "clinic_id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
      "animal_id": "3e2ce4a2-f75b-468c-9353-04ba4996f548",
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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/appointments/12345678-23cf-443d-b7a6-529e7ea5f234
```

**Path Parameters:**
- `appointment_id`: ID UUID do agendamento (obrigatório)

**Query Parameters:**
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO

**Responses:**
- `200 OK`: Detalhes do agendamento
  ```json
  {
    "id": "12345678-23cf-443d-b7a6-529e7ea5f234",
    "clinic_id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
    "animal_id": "3e2ce4a2-f75b-468c-9353-04ba4996f548",
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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/appointments/12345678-23cf-443d-b7a6-529e7ea5f234
```

**Path Parameters:**
- `appointment_id`: ID UUID do agendamento (obrigatório)

**Query Parameters:**
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO

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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/appointments/12345678-23cf-443d-b7a6-529e7ea5f234
```

**Path Parameters:**
- `appointment_id`: ID UUID do agendamento (obrigatório)

**Query Parameters:**
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO

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
    "id": "12345678-23cf-443d-b7a6-529e7ea5f234",
    "clinic_id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
    "animal_id": "3e2ce4a2-f75b-468c-9353-04ba4996f548",
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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/consultations?clinic_id=bd330f0a-23cf-443d-b7a6-529e7ea5f234
```

**Query Parameters:**
- `clinic_id`: ID UUID da clínica que está criando a consulta (obrigatório)

**Request Body:**
```json
{
  "animal_id": "c7020821-b8fe-4608-9f7f-2bad17877ca4",
  "description": "Consulta inicial, exame físico completo.",
  "date": "2023-10-26T10:00:00Z" // Opcional, padrão para data/hora atual
}
```

**Responses:**
- `200 OK`: Consulta criada com sucesso
  ```json
  {
    "id": "78901234-23cf-443d-b7a6-529e7ea5f234",
    "clinic_id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
    "animal_id": "3e2ce4a2-f75b-468c-9353-04ba4996f548",
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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/consultations?clinic_id=bd330f0a-23cf-443d-b7a6-529e7ea5f234&animal_id=c7020821-b8fe-4608-9f7f-2bad17877ca4
```

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)
- `animal_id`: Filtrar consultas por ID do animal (opcional)

**Responses:**
- `200 OK`: Lista de consultas
  ```json
  [
    {
      "id": "78901234-23cf-443d-b7a6-529e7ea5f234",
      "clinic_id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
      "animal_id": "3e2ce4a2-f75b-468c-9353-04ba4996f548",
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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/consultations/78901234-23cf-443d-b7a6-529e7ea5f234?clinic_id=bd330f0a-23cf-443d-b7a6-529e7ea5f234
```

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
    "id": "78901234-23cf-443d-b7a6-529e7ea5f234",
    "clinic_id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
    "animal_id": "3e2ce4a2-f75b-468c-9353-04ba4996f548",
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

**URL de Exemplo:**
```
http://localhost:8000/api/v1/consultations/78901234-23cf-443d-b7a6-529e7ea5f234?clinic_id=bd330f0a-23cf-443d-b7a6-529e7ea5f234
```

**Path Parameters:**
- `consultation_id`: ID UUID da consulta (obrigatório)

**Query Parameters:**
- `clinic_id`: ID UUID da clínica (obrigatório)

**Responses:**
- `204 No Content`: Consulta removida com sucesso.
- `404 Not Found`: Consulta não encontrada ou não pertence à clínica
- `500 Internal Server Error`: Erro ao deletar consulta 

## Nutrição e Dietas

### 1. Dietas

#### `POST /animals/{animal_id}/diets`
Criação de um plano alimentar.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/diets
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Request Body:**
```json
{
  "tipo": "caseira",
  "objetivo": "emagrecimento",
  "data_inicio": "2023-08-01",
  "data_fim": "2023-09-01",
  "status": "ativa"
}
```

**Responses:**
- `201 Created`: Dieta criada com sucesso.

#### `GET /animals/{animal_id}/diets`
Listagem de planos alimentares.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/diets
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Responses:**
- `200 OK`: Lista de dietas.

#### `GET /diets/{diet_id}`
Detalhes de uma dieta específica.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/diets/uuid
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `diet_id`: ID UUID da dieta (obrigatório)

**Responses:**
- `200 OK`: Detalhes da dieta.

#### `PUT /diets/{diet_id}`
Atualização de uma dieta.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/diets/uuid
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `diet_id`: ID UUID da dieta (obrigatório)

**Request Body:**
```json
{
  "status": "finalizada"
}
```

**Responses:**
- `200 OK`: Dieta atualizada com sucesso.

#### `DELETE /diets/{diet_id}`
Remoção de uma dieta.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/diets/uuid
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `diet_id`: ID UUID da dieta (obrigatório)

**Responses:**
- `204 No Content`: Dieta removida com sucesso.

---

### 2. Opções de Dieta

#### `POST /diets/{diet_id}/options`
Criação de uma opção de dieta.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/diets/uuid/options
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `diet_id`: ID UUID da dieta (obrigatório)

**Request Body:**
```json
{
  "nome": "Ração Premium Light",
  "valor_mensal": 150,
  "calorias_totais": 2000,
  "porcao_por_refeicao": "250g",
  "numero_refeicoes": 3
}
```

**Responses:**
- `201 Created`: Opção de dieta criada com sucesso.

#### `PUT /diet-options/{option_id}`
Atualização de uma opção de dieta.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/diet-options/uuid
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `option_id`: ID UUID da opção de dieta (obrigatório)

**Request Body:**
```json
{
  "valor_mensal": 160
}
```

**Responses:**
- `200 OK`: Opção de dieta atualizada com sucesso.

#### `DELETE /diet-options/{option_id}`
Remoção de uma opção de dieta.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/diet-options/uuid
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `option_id`: ID UUID da opção de dieta (obrigatório)

**Responses:**
- `204 No Content`: Opção de dieta removida com sucesso.

---

### 3. Alimentos da Dieta

#### `POST /diet-options/{option_id}/foods`
Adiciona um alimento a uma opção de dieta.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/diet-options/uuid/foods
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `option_id`: ID UUID da opção de dieta (obrigatório)

**Request Body:**
```json
{
  "nome": "Ração Seca XYZ",
  "tipo": "ração",
  "quantidade": "200g",
  "calorias": 750,
  "horario": "Almoço"
}
```

**Responses:**
- `200 OK`: Alimento adicionado com sucesso.

#### `GET /diet-options/{option_id}/foods`
Lista todos os alimentos de uma opção de dieta.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/diet-options/uuid/foods
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `option_id`: ID UUID da opção de dieta (obrigatório)

**Responses:**
- `200 OK`: Lista de alimentos.

#### `PUT /diet-foods/{food_id}`
Atualiza um alimento de uma opção de dieta.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/diet-foods/uuid
```

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
- `200 OK`: Alimento atualizado com sucesso.

#### `DELETE /diet-foods/{food_id}`
Remove um alimento de uma opção de dieta.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/diet-foods/uuid
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `food_id`: ID UUID do alimento (obrigatório)

**Responses:**
- `204 No Content`: Alimento removido com sucesso.

---

### 4. Alimentos Restritos

#### `POST /animals/{animal_id}/restricted-foods`
Adiciona um alimento que o pet deve evitar.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/restricted-foods
```

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
- `200 OK`: Alimento a evitar adicionado com sucesso.

#### `GET /animals/{animal_id}/restricted-foods`
Lista todos os alimentos que o pet deve evitar.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/restricted-foods
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Responses:**
- `200 OK`: Lista de alimentos a evitar.

#### `PUT /animals/{animal_id}/restricted-foods/{food_id}`
Atualiza um alimento que o pet deve evitar.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/restricted-foods/uuid
```

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
- `200 OK`: Alimento atualizado com sucesso.

#### `DELETE /animals/{animal_id}/restricted-foods/{food_id}`
Remove um alimento que o pet deve evitar.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/restricted-foods/uuid
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)
- `food_id`: ID UUID do alimento a evitar (obrigatório)

**Responses:**
- `204 No Content`: Alimento removido com sucesso.

---

### 5. Snacks

#### `POST /animals/{animal_id}/snacks`
Adiciona um snack permitido entre refeições.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/snacks
```

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
- `200 OK`: Snack adicionado com sucesso.

#### `GET /animals/{animal_id}/snacks`
Lista todos os snacks permitidos entre refeições.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/snacks
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Responses:**
- `200 OK`: Lista de snacks.

#### `PUT /animals/{animal_id}/snacks/{snack_id}`
Atualiza um snack permitido.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/snacks/uuid
```

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
- `200 OK`: Snack atualizado com sucesso.

#### `DELETE /animals/{animal_id}/snacks/{snack_id}`
Remove um snack permitido.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/snacks/uuid
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)
- `snack_id`: ID UUID do snack (obrigatório)

**Responses:**
- `204 No Content`: Snack removido com sucesso.
```
