# Teste de Endpoints de Autenticação

## Autenticação

### `POST /api/v1/auth/register`

Registra um novo usuário (clínica) no sistema.

**URL de Exemplo:**
```
http://localhost:8000/api/v1/auth/register
```

**Request Body:**
```json
{
  "name": "Clínica VetTest",
  "email": "clinica@teste.com",
  "password": "senha123",
  "phone": "11999887766",
  "subscription_tier": "basic"
}
```

**Responses:**
- `201 Created`: Usuário criado com sucesso
  ```json
  {
    "id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
    "name": "Clínica VetTest",
    "email": "clinica@teste.com",
    "phone": "11999887766",
    "subscription_tier": "basic",
    "created_at": "2023-04-07T23:50:00.000Z"
  }
  ```
- `400 Bad Request`: Dados inválidos ou email já existe
- `500 Internal Server Error`: Erro interno

### `POST /api/v1/auth/login`

Realiza login tradicional para clínicas.

**URL de Exemplo:**
```
http://localhost:8000/api/v1/auth/login
```

**Request Body:**
```json
{
  "email": "clinica@teste.com",
  "password": "senha123"
}
```

**Responses:**
- `200 OK`: Login bem-sucedido
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "clinic": {
      "id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
      "name": "Clínica VetTest",
      "email": "clinica@teste.com"
    }
  }
  ```
- `401 Unauthorized`: Credenciais inválidas
- `500 Internal Server Error`: Erro interno

### `POST /api/v1/auth/check-user-type`

Verifica se o email pertence a uma clínica ou cliente (tutor).

**URL de Exemplo:**
```
http://localhost:8000/api/v1/auth/check-user-type
```

**Request Body:**
```json
{
  "email": "teste@teste.com"
}
```

**Responses:**
- `200 OK`: Usuário encontrado (Clínica)
  ```json
  {
    "user_type": "clinic",
    "user_id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
    "email": "clinica@teste.com",
    "name": "Clínica VetTest",
    "redirect_url": "/clinic/dashboard"
  }
  ```
- `200 OK`: Usuário encontrado (Cliente)
  ```json
  {
    "user_type": "client",
    "user_id": "3e2ce4a2-f75b-468c-9353-04ba4996f548",
    "email": "tutor@teste.com",
    "name": "João Silva",
    "redirect_url": "/client/dashboard"
  }
  ```
- `404 Not Found`: Usuário não encontrado
- `500 Internal Server Error`: Erro interno

### `POST /api/v1/auth/dual-login`

Login unificado que funciona para clínicas e clientes.

**URL de Exemplo:**
```
http://localhost:8000/api/v1/auth/dual-login
```

**Request Body:**
```json
{
  "email": "teste@teste.com",
  "password": "senha123"
}
```

**Responses:**
- `200 OK`: Login bem-sucedido (Clínica)
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user_type": "clinic",
    "redirect_url": "/clinic/dashboard",
    "clinic": {
      "id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
      "name": "Clínica VetTest",
      "email": "clinica@teste.com"
    }
  }
  ```
- `200 OK`: Login bem-sucedido (Cliente)
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user_type": "client",
    "redirect_url": "/client/dashboard",
    "client": {
      "id": "3e2ce4a2-f75b-468c-9353-04ba4996f548",
      "name": "João Silva",
      "email": "tutor@teste.com"
    }
  }
  ```
- `401 Unauthorized`: Credenciais inválidas
- `404 Not Found`: Usuário não encontrado
- `500 Internal Server Error`: Erro interno

### `POST /api/v1/auth/logout`

Realiza logout do usuário.

**URL de Exemplo:**
```
http://localhost:8000/api/v1/auth/logout
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (opcional)

**Responses:**
- `200 OK`: Logout bem-sucedido
  ```json
  {
    "message": "Logout bem-sucedido. Por favor, descarte o token no cliente."
  }
  ```

### `GET /api/v1/auth/clinic/profile`

Obtém os dados de perfil da clínica atualmente logada.

**URL de Exemplo:**
```
http://localhost:8000/api/v1/auth/clinic/profile
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Responses:**
- `200 OK`: Perfil obtido com sucesso
  ```json
  {
    "id": "bd330f0a-23cf-443d-b7a6-529e7ea5f234",
    "name": "Clínica VetTest",
    "email": "clinica@teste.com",
    "phone": "11999887766",
    "subscription_tier": "basic",
    "created_at": "2023-04-07T23:50:00.000Z"
  }
  ```
- `401 Unauthorized`: Token inválido ou ausente
- `500 Internal Server Error`: Erro interno

## Exemplos de Teste no Postman

### 1. Testar Registro de Clínica
```
POST http://localhost:8000/api/v1/auth/register
Content-Type: application/json

{
  "name": "Clínica Teste Postman",
  "email": "postman@teste.com",
  "password": "senha123",
  "phone": "11999887766",
  "subscription_tier": "basic"
}
```

### 2. Testar Login Dual (Clínica)
```
POST http://localhost:8000/api/v1/auth/dual-login
Content-Type: application/json

{
  "email": "postman@teste.com",
  "password": "senha123"
}
```

### 3. Testar Login Dual (Cliente)
```
POST http://localhost:8000/api/v1/auth/dual-login
Content-Type: application/json

{
  "email": "teste@teste.com",
  "password": "senha123"
}
```

### 4. Verificar Tipo de Usuário
```
POST http://localhost:8000/api/v1/auth/check-user-type
Content-Type: application/json

{
  "email": "teste@teste.com"
}
```

### 5. Obter Perfil da Clínica (com token)
```
GET http://localhost:8000/api/v1/auth/clinic/profile
Authorization: Bearer SEU_TOKEN_AQUI
```

## Notas Importantes

1. **Dual Login**: O endpoint `/dual-login` é o principal para autenticação, pois funciona tanto para clínicas quanto para clientes.

2. **Tokens**: Todos os tokens retornados devem ser usados no header `Authorization: Bearer {token}` para endpoints protegidos.

3. **Tipos de Usuário**: 
   - `clinic`: Usuários registrados na tabela `clinics`
   - `client`: Tutores com animais na tabela `animals` (campo `client_active = true`)

4. **Redirecionamento**: O campo `redirect_url` indica para onde o frontend deve redirecionar após login bem-sucedido.

5. **Erro Comum**: Se o `clientData` estiver como "undefined" no localStorage, verifique se o endpoint está retornando os dados corretos no campo `client`.