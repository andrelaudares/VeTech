# Correções dos Modelos e Rotas de Dietas

## Resumo das Alterações

Foram realizadas correções nos modelos e rotas relacionados a dietas para alinhar com a estrutura real das tabelas no banco de dados Supabase.

## Problemas Identificados

1. **Modelos DietCreate/DietUpdate**: Faltavam campos obrigatórios como `data_inicio` e `refeicoes_por_dia`
2. **Modelos DietProgress**: Faltava campo `opcao_dieta_id` e tipo incorreto para `horario_realizado`
3. **Modelos AlimentoBase**: Faltavam vários campos da tabela `alimentos_base`
4. **Rotas**: Não estavam usando todos os campos dos modelos corretamente

## Estrutura das Tabelas

### Tabela `public.dietas`
- `id` (uuid, não nulo)
- `animal_id` (uuid, não nulo)
- `clinic_id` (uuid, não nulo)
- `nome` (character varying, não nulo)
- `tipo` (character varying, não nulo)
- `objetivo` (character varying, não nulo)
- `data_inicio` (date, não nulo)
- `data_fim` (date, nulo)
- `status` (character varying, não nulo)
- `refeicoes_por_dia` (integer, não nulo)
- `calorias_totais_dia` (integer, nulo)
- `valor_mensal_estimado` (numeric, nulo)
- `alimento_id` (bigint, nulo)
- `quantidade_gramas` (integer, nulo)
- `horario` (time without time zone, nulo)
- `created_at` (timestamp with time zone, nulo)
- `updated_at` (timestamp with time zone, nulo)

### Tabela `public.dieta_progresso`
- `id` (uuid, não nulo)
- `animal_id` (uuid, não nulo)
- `dieta_id` (uuid, não nulo)
- `opcao_dieta_id` (uuid, nulo)
- `data` (date, não nulo)
- `refeicao_completa` (boolean, nulo)
- `horario_realizado` (time without time zone, nulo)
- `quantidade_consumida` (character varying, nulo)
- `observacoes_tutor` (text, nulo)
- `pontos_ganhos` (integer, nulo)
- `created_at` (timestamp with time zone, nulo)
- `updated_at` (timestamp with time zone, nulo)

### Tabela `public.alimentos_base`
- `alimento_id` (bigint, não nulo)
- `nome` (USER-DEFINED, não nulo)
- `tipo` (USER-DEFINED, não nulo)
- `especie_destino` (USER-DEFINED, não nulo)
- `marca` (USER-DEFINED, nulo)
- `linha` (USER-DEFINED, nulo)
- `subtipo` (USER-DEFINED, nulo)
- `kcal_por_kg` (numeric, nulo)
- `kcal_por_100g` (numeric, nulo)
- `kcal_por_50g` (numeric, nulo)
- `origem_caloria` (USER-DEFINED, nulo)
- `fonte` (text, nulo)
- `fonte_url` (text, nulo)
- `observacoes` (text, nulo)
- `created_at` (timestamp with time zone, não nulo)

## Correções Realizadas

### 1. Arquivo `backend/app/models/diet.py`

#### DietCreate
- ✅ Adicionados campos `animal_id` e `clinic_id` como obrigatórios
- ✅ Campo `data_inicio` alterado de opcional para obrigatório
- ✅ Campo `refeicoes_por_dia` alterado de opcional para obrigatório
- ✅ Adicionados campos `alimento_id`, `quantidade_gramas` e `horario`

#### DietUpdate
- ✅ Adicionados todos os campos da tabela como opcionais
- ✅ Incluídos campos `data_inicio`, `refeicoes_por_dia`, `alimento_id`, `quantidade_gramas` e `horario`

#### DietProgressCreate
- ✅ Adicionado campo `opcao_dieta_id` como opcional
- ✅ Campo `horario_realizado` alterado de `str` para `time`
- ✅ Adicionado campo `pontos_ganhos`

#### DietProgressUpdate
- ✅ Adicionado campo `opcao_dieta_id` como opcional
- ✅ Campo `horario_realizado` alterado de `str` para `time`
- ✅ Adicionado campo `pontos_ganhos`

#### AlimentoBaseCreate
- ✅ Adicionados campos `marca`, `linha`, `subtipo`
- ✅ Adicionados campos `kcal_por_kg`, `kcal_por_50g`
- ✅ Adicionados campos `origem_caloria`, `fonte`, `fonte_url`
- ✅ Removidos campos inexistentes (`proteinas_por_100g`, `gorduras_por_100g`, etc.)

#### AlimentoBaseUpdate
- ✅ Mesmas correções do AlimentoBaseCreate aplicadas como campos opcionais

### 2. Arquivo `backend/app/api/diets.py`

#### Rota POST `/animals/{animal_id}/diets`
- ✅ Atualizada para usar `diet.animal_id` e `diet.clinic_id` do modelo
- ✅ Campo `data_inicio` agora obrigatório (sem verificação de None)
- ✅ Adicionada conversão correta para `horario` (time para string)

#### Rota POST `/diets/{diet_id}/progress`
- ✅ Atualizada para usar todos os campos do modelo `DietProgressCreate`
- ✅ Adicionados campos `opcao_dieta_id` e `pontos_ganhos`
- ✅ Conversão correta para `horario_realizado` (time para string)

## Observações Importantes

1. **Tipos de Dados**: Campos `time` são convertidos para string ISO format nas rotas
2. **Campos Obrigatórios**: `data_inicio` e `refeicoes_por_dia` agora são obrigatórios em DietCreate
3. **Tabela Correta**: As rotas de progresso usam a tabela `dieta_progresso` corretamente
4. **Alimentos Base**: Modelo agora reflete a estrutura real da tabela `alimentos_base`

## Testes Recomendados

1. **Criação de Dieta**:
```json
{
  "animal_id": "uuid-do-animal",
  "clinic_id": "uuid-da-clinica",
  "nome": "Dieta para Emagrecimento",
  "tipo": "ração",
  "objetivo": "Emagrecimento",
  "data_inicio": "2024-01-15",
  "refeicoes_por_dia": 3,
  "status": "ativa"
}
```

2. **Progresso de Dieta**:
```json
{
  "animal_id": "uuid-do-animal",
  "dieta_id": "uuid-da-dieta",
  "data": "2024-01-15",
  "refeicao_completa": true,
  "horario_realizado": "08:30:00",
  "quantidade_consumida": "100g",
  "observacoes_tutor": "Animal comeu tudo",
  "pontos_ganhos": 10
}
```

3. **Alimento Base**:
```json
{
  "nome": "Ração Premium",
  "tipo": "ração seca",
  "especie_destino": "cão",
  "marca": "Royal Canin",
  "linha": "Size Health Nutrition",
  "kcal_por_100g": 350.5
}
```

## Status das Correções

- ✅ Modelos de dieta corrigidos
- ✅ Modelos de progresso de dieta corrigidos  
- ✅ Modelos de alimentos base corrigidos
- ✅ Rotas de criação atualizadas
- ✅ Documentação criada

Todas as correções foram implementadas e os modelos agora estão alinhados com a estrutura real das tabelas no banco de dados.