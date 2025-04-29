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
