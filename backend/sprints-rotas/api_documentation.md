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
http://localhost:8000/api/v1/animals
```

**Query Parameters:**
- ~~`clinic_id`: ID UUID da clínica que está cadastrando o animal (obrigatório)~~ REMOVIDO (obtido via JWT)

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

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
http://localhost:8000/api/v1/animals
```

**Query Parameters:**
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO (obtido via JWT)

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Responses:**
- `200 OK`: Lista de animais da clínica autenticada
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
http://localhost:8000/api/v1/animals/3e2ce4a2-f75b-468c-9353-04ba4996f548
```

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO (verificação via JWT)

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

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
- `404 Not Found`: Animal não encontrado ou não pertence à clínica autenticada
- `500 Internal Server Error`: Erro ao buscar animal

### `PATCH /api/v1/animals/{animal_id}`

Atualiza um animal existente.

**URL de Exemplo:**
```
http://localhost:8000/api/v1/animals/3e2ce4a2-f75b-468c-9353-04ba4996f548
```

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO (verificação via JWT)

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

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
- `404 Not Found`: Animal não encontrado ou não pertence à clínica autenticada
- `500 Internal Server Error`: Erro ao atualizar animal

### `DELETE /api/v1/animals/{animal_id}`

Remove um animal pelo ID.

**URL de Exemplo:**
```
http://localhost:8000/api/v1/animals/3e2ce4a2-f75b-468c-9353-04ba4996f548
```

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Query Parameters:**
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO (verificação via JWT)

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Responses:**
- `204 No Content`: Animal removido com sucesso.
- `404 Not Found`: Animal não encontrado ou não pertence à clínica autenticada
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
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO (verificação via JWT)

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

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
- `404 Not Found`: Animal não encontrado ou não pertence à clínica autenticada
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
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO (verificação via JWT)

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

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
- `404 Not Found`: Animal não encontrado ou não pertence à clínica autenticada / Preferências não encontradas
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
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO (verificação via JWT)

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

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
- `404 Not Found`: Animal não encontrado ou não pertence à clínica autenticada / Preferências não encontradas
- `500 Internal Server Error`: Erro ao atualizar preferências

## Agendamentos

### `POST /api/v1/appointments`

Cria um novo agendamento para um animal.

**URL de Exemplo:**
```
http://localhost:8000/api/v1/appointments
```

**Query Parameters:**
- ~~`clinic_id`: ID UUID da clínica que está criando o agendamento (obrigatório)~~ REMOVIDO (obtido via JWT)

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

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
- `400 Bad Request`: Horário já ocupado pela clínica ou dados inválidos
- `404 Not Found`: Animal não encontrado ou não pertence à clínica autenticada
- `500 Internal Server Error`: Erro ao criar agendamento

### `GET /api/v1/appointments`

Obtém todos os agendamentos de uma clínica, ordenados por data e hora.

**URL de Exemplo:**
```
http://localhost:8000/api/v1/appointments?date_from=2023-05-15&status=scheduled
```

**Query Parameters:**
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO (obtido via JWT)
- `date_from`: Filtrar agendamentos a partir desta data (opcional)
- `status`: Filtrar por status (opcional) - valores: scheduled, completed, cancelled

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Responses:**
- `200 OK`: Lista de agendamentos da clínica autenticada
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
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO (verificação via JWT)

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

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
- `404 Not Found`: Agendamento não encontrado ou não pertence à clínica autenticada
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
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO (verificação via JWT)

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Responses:**
- `200 OK`: Agendamento removido com sucesso
  ```json
  {
    "message": "Agendamento removido com sucesso."
  }
  ```
- `404 Not Found`: Agendamento não encontrado ou não pertence à clínica autenticada
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
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO (verificação via JWT)

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

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
- `400 Bad Request`: Horário já ocupado pela clínica ou dados inválidos
- `404 Not Found`: Agendamento não encontrado ou não pertence à clínica autenticada
- `500 Internal Server Error`: Erro ao atualizar agendamento

## Consultas

### `POST /api/v1/consultations`

Cria uma nova consulta para um animal.

**URL de Exemplo:**
```
http://localhost:8000/api/v1/consultations
```

**Query Parameters:**
- ~~`clinic_id`: ID UUID da clínica que está criando a consulta (obrigatório)~~ REMOVIDO (obtido via JWT)

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

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
- `404 Not Found`: Animal não encontrado ou não pertence à clínica autenticada
- `500 Internal Server Error`: Erro ao criar consulta

### `GET /api/v1/consultations`

Obtém todas as consultas de uma clínica, opcionalmente filtradas por animal.

**URL de Exemplo:**
```
http://localhost:8000/api/v1/consultations?animal_id=c7020821-b8fe-4608-9f7f-2bad17877ca4
```

**Query Parameters:**
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO (obtido via JWT)
- `animal_id`: Filtrar consultas por ID do animal (opcional)

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Responses:**
- `200 OK`: Lista de consultas da clínica autenticada
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
http://localhost:8000/api/v1/consultations/78901234-23cf-443d-b7a6-529e7ea5f234
```

**Path Parameters:**
- `consultation_id`: ID UUID da consulta (obrigatório)

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

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
- `404 Not Found`: Consulta não encontrada ou não pertence à clínica autenticada
- `500 Internal Server Error`: Erro ao atualizar consulta

### `DELETE /api/v1/consultations/{consultation_id}`

Remove uma consulta pelo ID.

**URL de Exemplo:**
```
http://localhost:8000/api/v1/consultations/78901234-23cf-443d-b7a6-529e7ea5f234
```

**Path Parameters:**
- `consultation_id`: ID UUID da consulta (obrigatório)

**Query Parameters:**
- ~~`clinic_id`: ID UUID da clínica (obrigatório)~~ REMOVIDO (verificação via JWT)

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Responses:**
- `204 No Content`: Consulta removida com sucesso.
- `404 Not Found`: Consulta não encontrada ou não pertence à clínica autenticada
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
