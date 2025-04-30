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
