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
