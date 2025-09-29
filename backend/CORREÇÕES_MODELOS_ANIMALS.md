# Correções nos Modelos e Rotas de Animals

## Resumo das Alterações Realizadas

Este documento detalha as correções realizadas nos modelos e rotas de animais para alinhar com a estrutura real do banco de dados.

## Problemas Identificados

1. **Campos de dieta incorretos**: Os modelos continham campos relacionados à dieta que não existem na tabela `animals` do banco de dados
2. **Campos altura e sexo não incluídos**: Os campos `altura` e `sexo` existem no banco mas não estavam sendo utilizados nas operações POST e PATCH
3. **Inconsistência entre modelos e banco**: Os modelos não refletiam a estrutura real da tabela `animals`

## Estrutura Real da Tabela Animals

Baseado na consulta ao banco de dados, a tabela `public.animals` possui os seguintes campos:

- `id` (uuid, NOT NULL)
- `clinic_id` (uuid, NOT NULL)
- `name` (varchar, NOT NULL)
- `species` (varchar, NOT NULL)
- `breed` (varchar, nullable)
- `age` (integer, nullable)
- `weight` (numeric, nullable)
- `altura` (numeric, nullable) ✅
- `sexo` (varchar, nullable) ✅
- `medical_history` (text, nullable)
- `created_at` (timestamp, nullable)
- `updated_at` (timestamp, nullable)
- `date_birth` (date, nullable)
- `tutor_name` (text, nullable)
- `email` (text, nullable)
- `phone` (text, nullable)
- `senha` (text, nullable)
- `gamification_level` (integer, nullable)
- `total_points` (integer, nullable)
- `gamification_points` (integer, nullable)
- `client_active` (boolean, nullable)
- `client_activated_at` (timestamp, nullable)
- `client_last_login` (timestamp, nullable)
- `tutor_user_id` (uuid, nullable)

## Alterações Realizadas

### 1. Arquivo: `/backend/app/models/animal.py`

#### AnimalCreate
**Removido:**
```python
# Campos relacionados à dieta (INCORRETOS)
dieta_atual_id: Optional[UUID4] = None
dieta_atual_nome: Optional[str] = None
dieta_atual_status: Optional[str] = None
dieta_atual_data_inicio: Optional[date] = None
dieta_atual_data_fim: Optional[date] = None
```

**Mantido:**
```python
class AnimalCreate(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    altura: Optional[float] = None  # ✅ Campo existente no banco
    sexo: Optional[str] = None      # ✅ Campo existente no banco
    medical_history: Optional[str] = None
    date_birth: Optional[date] = None
    tutor_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    tutor_user_id: Optional[str] = None
```

#### AnimalUpdate
**Removido:**
```python
# Campos relacionados à dieta (INCORRETOS)
dieta_atual_id: Optional[UUID4] = None
dieta_atual_nome: Optional[str] = None
dieta_atual_status: Optional[str] = None
dieta_atual_data_inicio: Optional[date] = None
dieta_atual_data_fim: Optional[date] = None
```

**Mantido:**
```python
class AnimalUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    altura: Optional[float] = None  # ✅ Campo existente no banco
    sexo: Optional[str] = None      # ✅ Campo existente no banco
    medical_history: Optional[str] = None
    date_birth: Optional[date] = None
    tutor_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
```

#### AnimalResponse
**Removido:**
```python
# Campos relacionados à dieta (INCORRETOS)
dieta_atual_id: Optional[UUID4] = None
dieta_atual_nome: Optional[str] = None
dieta_atual_status: Optional[str] = None
dieta_atual_data_inicio: Optional[date] = None
dieta_atual_data_fim: Optional[date] = None
```

**Mantido:**
```python
class AnimalResponse(BaseModel):
    id: UUID4
    clinic_id: UUID4
    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    altura: Optional[float] = None  # ✅ Campo existente no banco
    sexo: Optional[str] = None      # ✅ Campo existente no banco
    medical_history: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    date_birth: Optional[date] = None
    tutor_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    tutor_user_id: Optional[UUID4] = None
    client_active: Optional[bool] = None
    client_activated_at: Optional[datetime] = None
    client_last_login: Optional[datetime] = None
    gamification_level: Optional[int] = None
    total_points: Optional[int] = None
    gamification_points: Optional[int] = None
```

### 2. Arquivo: `/backend/app/api/animals.py`

#### Rota POST - create_animal
**Adicionado:**
```python
animal_data = {
    "clinic_id": str(clinic_id),
    "name": animal.name,
    "species": animal.species,
    "breed": animal.breed,
    "age": animal.age,
    "weight": animal.weight,
    "altura": animal.altura,    # ✅ Novo campo adicionado
    "sexo": animal.sexo,        # ✅ Novo campo adicionado
    "medical_history": animal.medical_history,
    "date_birth": animal.date_birth.isoformat() if animal.date_birth else None,
    "tutor_name": animal.tutor_name,
    "email": animal.email,
    "phone": animal.phone
}
```

## Observações Importantes

1. **Campos de Dieta**: A gestão de dietas será feita exclusivamente através da tabela `public.dietas`, não através de campos na tabela `animals`

2. **Campos altura e sexo**: Agora estão corretamente incluídos em todas as operações (CREATE, UPDATE, RESPONSE)

3. **Compatibilidade**: As alterações mantêm compatibilidade com o banco de dados existente

4. **Validação**: Os campos `altura` e `sexo` são opcionais, permitindo flexibilidade na criação de registros

## Testes Recomendados

### 1. Teste de Criação de Animal (POST)
```json
{
    "name": "Rex",
    "species": "Cão",
    "breed": "Golden Retriever",
    "age": 3,
    "weight": 25.5,
    "altura": 60.0,
    "sexo": "Macho",
    "medical_history": "Vacinação em dia",
    "date_birth": "2021-01-15",
    "tutor_name": "João Silva",
    "email": "joao@email.com",
    "phone": "(11) 99999-9999"
}
```

### 2. Teste de Atualização de Animal (PATCH)
```json
{
    "weight": 26.0,
    "altura": 61.0,
    "sexo": "Macho"
}
```

### 3. Verificação de Resposta (GET)
A resposta deve incluir os campos `altura` e `sexo` sem campos de dieta incorretos.

## Status das Correções

- ✅ Modelo AnimalCreate corrigido
- ✅ Modelo AnimalUpdate corrigido  
- ✅ Modelo AnimalResponse corrigido
- ✅ Rota POST atualizada para incluir altura e sexo
- ✅ Documentação criada

Todas as correções foram implementadas e estão prontas para teste.