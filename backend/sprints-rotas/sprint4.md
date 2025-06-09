
## Nutrição e Dietas

### Fluxo Recomendado para Criação de Dietas Completas

1. **Criar a dieta** usando `POST /animals/{animal_id}/diets`
2. **Adicionar opções de dieta** usando `POST /diets/{diet_id}/options`
3. **Adicionar alimentos específicos** usando `POST /diet-options/{option_id}/foods`
4. **Configurar preferências do pet** usando `POST /animals/{animal_id}/preferences`
5. **Definir alimentos restritos** usando `POST /animals/{animal_id}/restricted-foods`
6. **Configurar snacks permitidos** usando `POST /animals/{animal_id}/snacks`

Este fluxo garante que o tutor tenha informações completas e detalhadas sobre a alimentação do pet.

---

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

As opções de dieta são os detalhes específicos de como implementar um plano alimentar. Cada dieta pode ter múltiplas opções (ex: "Ração Premium", "Ração Econômica", "Alimentação Caseira"), permitindo que o tutor escolha a mais adequada.

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
  "valor_mensal_estimado": 150.00,
  "calorias_totais_dia": 2000,
  "porcao_refeicao": "250g",
  "refeicoes_por_dia": 3,
  "indicacao": "Ideal para cães com sobrepeso. Administrar com água fresca sempre disponível."
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

---

### 6. Preferências do Pet

#### `POST /animals/{animal_id}/preferences`
Cria ou atualiza as preferências alimentares de um pet.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/preferences
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Request Body:**
```json
{
  "gosta_de": "Frango, arroz, cenoura, petiscos de fígado",
  "nao_gosta_de": "Peixe, verduras cruas, medicamentos"
}
```

**Responses:**
- `200 OK`: Preferências criadas ou atualizadas com sucesso.

#### `GET /animals/{animal_id}/preferences`
Obtém as preferências alimentares de um pet.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/preferences
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Responses:**
- `200 OK`: Preferências do pet.
- `404 Not Found`: Pet não possui preferências cadastradas.

#### `PATCH /animals/{animal_id}/preferences`
Atualiza as preferências alimentares de um pet.

**Exemplo de URL:**
```
http://localhost:8000/api/v1/animals/uuid/preferences
```

**Header Parameters:**
- `Authorization`: Token JWT no formato "Bearer {token}" (obrigatório)

**Path Parameters:**
- `animal_id`: ID UUID do animal (obrigatório)

**Request Body:**
```json
{
  "gosta_de": "Frango, arroz, cenoura, petiscos de fígado, biscoitos",
  "nao_gosta_de": "Peixe, verduras cruas"
}
```

**Responses:**
- `200 OK`: Preferências atualizadas com sucesso.
```
