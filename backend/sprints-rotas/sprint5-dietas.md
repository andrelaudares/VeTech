# Sprint 5 - Novas Funcionalidades de Dietas

## Visão Geral

Esta documentação descreve as novas rotas implementadas para o sistema de dietas, incluindo o progresso de dietas, alimentos base e atualização de dieta atual no animal.

## Estrutura das Rotas

Todas as rotas estão implementadas no arquivo `backend/app/api/diets.py` e seguem o padrão RESTful.

---

## 1. Progresso da Dieta

O progresso da dieta permite registrar e acompanhar o consumo alimentar do animal ao longo do tempo, incluindo informações como refeições completas, horários, quantidades consumidas e observações do tutor.

### `POST /diets/{diet_id}/progress`
Registra um novo progresso para uma dieta específica.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/diets/uuid/progress
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `diet_id`: ID UUID da dieta (obrigatório)

**Request Body:**
```json
{
  "data": "2023-10-15",
  "refeicao_completa": true,
  "horario_realizado": "08:30",
  "quantidade_consumida": 250,
  "observacoes_tutor": "O animal comeu toda a ração com entusiasmo"
}
```

**Responses:**
- `201 Created`: Progresso registrado com sucesso.
- `404 Not Found`: Dieta não encontrada.
- `401 Unauthorized`: Usuário não autenticado.

### `GET /diets/{diet_id}/progress`
Lista todos os registros de progresso de uma dieta específica.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/diets/uuid/progress
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `diet_id`: ID UUID da dieta (obrigatório)

**Responses:**
- `200 OK`: Lista de registros de progresso.
- `404 Not Found`: Dieta não encontrada.
- `401 Unauthorized`: Usuário não autenticado.

### `PUT /diet-progress/{progress_id}`
Atualiza um registro de progresso específico.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/diet-progress/uuid
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `progress_id`: ID UUID do registro de progresso (obrigatório)

**Request Body:**
```json
{
  "refeicao_completa": false,
  "quantidade_consumida": 150,
  "observacoes_tutor": "O animal comeu apenas parte da ração"
}
```

**Responses:**
- `200 OK`: Registro de progresso atualizado com sucesso.
- `404 Not Found`: Registro de progresso não encontrado.
- `403 Forbidden`: Sem permissão para atualizar este registro.
- `401 Unauthorized`: Usuário não autenticado.

### `DELETE /diet-progress/{progress_id}`
Remove um registro de progresso específico.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/diet-progress/uuid
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `progress_id`: ID UUID do registro de progresso (obrigatório)

**Responses:**
- `200 OK`: Registro de progresso removido com sucesso.
- `404 Not Found`: Registro de progresso não encontrado.
- `403 Forbidden`: Sem permissão para remover este registro.
- `401 Unauthorized`: Usuário não autenticado.

---

## 2. Alimentos Base

Os alimentos base são os ingredientes que podem ser utilizados na composição de dietas. Estas rotas permitem criar, listar, atualizar, excluir e filtrar os alimentos disponíveis.

### `POST /alimentos-base`
Cria um novo alimento base.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/alimentos-base
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Permissões:**
- Apenas usuários com perfil `admin` ou `ai_agent`

**Request Body:**
```json
{
  "nome": "Ração Premium Canina",
  "tipo": "ração",
  "especie_destino": "canino",
  "valores_nutricionais": {
    "proteina": 25.5,
    "gordura": 15.2,
    "fibra": 3.1,
    "calorias": 350
  }
}
```

**Responses:**
- `201 Created`: Alimento base criado com sucesso.
- `401 Unauthorized`: Usuário não autenticado.
- `403 Forbidden`: Sem permissão para criar alimentos base.

### `GET /alimentos-base`
Lista todos os alimentos base disponíveis com opções de filtro.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/alimentos-base?nome=arroz&tipo=carboidrato&especie=canino
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Query Parameters:**
- `nome`: Filtro por nome do alimento (opcional)
- `tipo`: Filtro por tipo de alimento (opcional)
- `especie`: Filtro por espécie destino (opcional)

**Responses:**
- `200 OK`: Lista de alimentos base.
- `401 Unauthorized`: Usuário não autenticado.

### `GET /alimentos-base/{alimento_id}`
Obtém detalhes de um alimento base específico.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/alimentos-base/uuid
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `alimento_id`: ID UUID do alimento base (obrigatório)

**Responses:**
- `200 OK`: Detalhes do alimento base.
- `404 Not Found`: Alimento base não encontrado.
- `401 Unauthorized`: Usuário não autenticado.

### `PUT /alimentos-base/{alimento_id}`
Atualiza um alimento base existente.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/alimentos-base/uuid
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `alimento_id`: ID UUID do alimento base (obrigatório)

**Permissões:**
- Apenas usuários com perfil `admin` ou `ai_agent`

**Request Body:**
```json
{
  "nome": "Ração Premium Canina Atualizada",
  "valores_nutricionais": {
    "proteina": 26.0,
    "gordura": 14.8,
    "fibra": 3.5,
    "calorias": 345
  }
}
```

**Responses:**
- `200 OK`: Alimento base atualizado com sucesso.
- `404 Not Found`: Alimento base não encontrado.
- `401 Unauthorized`: Usuário não autenticado.
- `403 Forbidden`: Sem permissão para atualizar alimentos base.

### `DELETE /alimentos-base/{alimento_id}`
Remove um alimento base existente.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/alimentos-base/uuid
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `alimento_id`: ID UUID do alimento base (obrigatório)

**Permissões:**
- Apenas usuários com perfil `admin` ou `ai_agent`

**Responses:**
- `200 OK`: Alimento base removido com sucesso.
- `404 Not Found`: Alimento base não encontrado.
- `401 Unauthorized`: Usuário não autenticado.
- `403 Forbidden`: Sem permissão para excluir alimentos base.

### `GET /alimentos-base/tipos`
Obtém a lista de tipos de alimentos disponíveis.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/alimentos-base/tipos
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Responses:**
- `200 OK`: Lista de tipos de alimentos.
- `401 Unauthorized`: Usuário não autenticado.

### `GET /alimentos-base/especies`
Obtém a lista de espécies destino disponíveis nos alimentos.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/alimentos-base/especies
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Responses:**
- `200 OK`: Lista de espécies destino.
- `401 Unauthorized`: Usuário não autenticado.

---

## 3. Atualização de Dieta no Animal

Esta rota permite atualizar as informações da dieta atual diretamente no registro do animal.

### `PUT /animals/{animal_id}/dieta-atual`
Atualiza as informações de dieta atual no registro do animal.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/dieta-atual
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Request Body:**
```json
{
  "dieta_atual_id": "uuid-da-dieta",
  "dieta_atual_nome": "Dieta de Emagrecimento",
  "dieta_atual_status": "ativa",
  "dieta_atual_data_inicio": "2023-10-01",
  "dieta_atual_data_fim": "2023-11-01"
}
```

**Responses:**
- `200 OK`: Informações de dieta atualizadas com sucesso.
- `404 Not Found`: Animal não encontrado.
- `401 Unauthorized`: Usuário não autenticado.

---

## Modelos de Dados

### DietProgressCreate
```python
class DietProgressCreate(BaseModel):
    data: date
    refeicao_completa: bool
    horario_realizado: str
    quantidade_consumida: float
    observacoes_tutor: Optional[str] = None
```

### DietProgressUpdate
```python
class DietProgressUpdate(BaseModel):
    data: Optional[date] = None
    refeicao_completa: Optional[bool] = None
    horario_realizado: Optional[str] = None
    quantidade_consumida: Optional[float] = None
    observacoes_tutor: Optional[str] = None
    pontos_ganhos: Optional[int] = None
```

### DietProgressResponse
```python
class DietProgressResponse(BaseModel):
    id: UUID
    animal_id: UUID
    dieta_id: UUID
    data: date
    refeicao_completa: bool
    horario_realizado: str
    quantidade_consumida: float
    observacoes_tutor: Optional[str] = None
    pontos_ganhos: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
```

### Campos adicionados ao modelo Animal
```python
class AnimalResponse(BaseModel):
    # Campos existentes...
    dieta_atual_id: Optional[UUID] = None
    dieta_atual_nome: Optional[str] = None
    dieta_atual_status: Optional[str] = None
    dieta_atual_data_inicio: Optional[date] = None
    dieta_atual_data_fim: Optional[date] = None
```

## Funcionamento do Progresso de Dieta

O sistema de progresso de dieta permite:

1. **Registro diário**: Os tutores podem registrar diariamente o consumo alimentar do pet.
2. **Acompanhamento**: Veterinários podem acompanhar a evolução da dieta ao longo do tempo.
3. **Análise de padrões**: Identificar padrões de consumo e comportamento alimentar.
4. **Ajustes**: Realizar ajustes na dieta com base nos dados de progresso.
5. **Gamificação**: Sistema de pontos para incentivar o tutor a seguir corretamente a dieta prescrita.

O fluxo típico de uso é:

1. Veterinário cria uma dieta para o animal (`POST /animals/{animal_id}/diets`).
2. Veterinário atualiza o registro do animal com a dieta atual (`PUT /animals/{animal_id}/dieta-atual`).
3. Tutor registra diariamente o progresso da dieta (`POST /diets/{diet_id}/progress`).
4. Veterinário consulta o histórico de progresso (`GET /diets/{diet_id}/progress`) durante consultas de acompanhamento.
5. Se necessário, o veterinário pode atualizar registros específicos (`PUT /diet-progress/{progress_id}`) ou removê-los (`DELETE /diet-progress/{progress_id}`).

Este sistema integra-se com o agente de IA, que utilizará os dados de progresso para fazer recomendações e ajustes na dieta do animal.

---

## 4. Rotas Relacionadas para Testes

Para testar completamente o sistema de dietas, você deve considerar as seguintes rotas relacionadas que foram afetadas ou são necessárias para o fluxo completo:

### Criação e Gerenciamento de Dietas

#### `POST /animals/{animal_id}/diets`
Cria uma nova dieta para um animal.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/diets
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

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

#### `GET /animals/{animal_id}/diets`
Lista todas as dietas de um animal.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/diets
```

#### `PUT /diets/{diet_id}`
Atualiza uma dieta existente.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/diets/uuid
```

**Request Body:**
```json
{
  "status": "finalizada"
}
```

### Opções de Dieta

#### `POST /diets/{diet_id}/options`
Cria uma opção de dieta.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/diets/uuid/options
```

**Request Body:**
```json
{
  "nome": "Ração Premium Light",
  "valor_mensal_estimado": 150.00,
  "calorias_totais_dia": 2000,
  "porcao_refeicao": "250g",
  "refeicoes_por_dia": 3,
  "indicacao": "Ideal para cães com sobrepeso. Administrar com água fresca sempre disponível."
}
```

#### `POST /diet-options/{option_id}/foods`
Adiciona um alimento a uma opção de dieta.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/diet-options/uuid/foods
```

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

### Preferências e Restrições Alimentares

#### `POST /animals/{animal_id}/preferences`
Cria ou atualiza as preferências alimentares de um pet.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/preferences
```

**Request Body:**
```json
{
  "gosta_de": "Frango, arroz, cenoura, petiscos de fígado",
  "nao_gosta_de": "Peixe, verduras cruas, medicamentos"
}
```

#### `POST /animals/{animal_id}/restricted-foods`
Adiciona um alimento que o pet deve evitar.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/restricted-foods
```

**Request Body:**
```json
{
  "nome": "Chocolate",
  "motivo": "Tóxico para cães"
}
```

#### `POST /animals/{animal_id}/snacks`
Adiciona um snack permitido entre refeições.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/snacks
```

**Request Body:**
```json
{
  "nome": "Bifinho de Frango",
  "frequencia_semanal": 3,
  "quantidade": "1 unidade",
  "observacoes": "Dar após exercícios"
}
```

### Fluxo de Teste Completo

Para testar completamente o sistema de dietas, siga este fluxo:

1. Crie uma dieta para um animal (`POST /animals/{animal_id}/diets`)
2. Adicione opções de dieta (`POST /diets/{diet_id}/options`)
3. Adicione alimentos às opções (`POST /diet-options/{option_id}/foods`)
4. Configure preferências do pet (`POST /animals/{animal_id}/preferences`)
5. Defina alimentos restritos (`POST /animals/{animal_id}/restricted-foods`)
6. Configure snacks permitidos (`POST /animals/{animal_id}/snacks`)
7. Atualize a dieta atual no animal (`PUT /animals/{animal_id}/dieta-atual`)
8. Registre progressos da dieta (`POST /diets/{diet_id}/progress`)
9. Consulte os progressos registrados (`GET /diets/{diet_id}/progress`)
10. Teste a criação e gerenciamento de alimentos base (`POST /alimentos-base`, etc.)

Este fluxo completo permite testar todas as funcionalidades do sistema de dietas.