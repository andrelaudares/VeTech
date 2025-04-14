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

## Animais

### `POST /api/v1/animals`

Cadastra um novo animal vinculado a uma clínica.

**Query Parameters:**
- `clinics_id`: ID UUID da clínica que está cadastrando o animal (obrigatório)

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
    "clinics_id": "uuid",
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
    "clinics_id": "uuid",
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