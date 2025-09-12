# Mapeamento de Arquivos Afetados pelas Mudanças no Banco de Dados

Este documento identifica os arquivos que serão afetados pelas mudanças no banco de dados relacionadas à migração da funcionalidade de dieta para IA.

## Arquivos Principais Afetados

### Backend

#### Modelos

1. **`backend/app/models/animal.py`**
   - **Mudanças necessárias**: Adicionar os campos `altura` e `sexo` aos modelos `AnimalCreate`, `AnimalUpdate` e `AnimalResponse`
   - **Impacto**: Médio - Requer atualização dos modelos e validações

2. **`backend/app/models/animal_preferences.py`**
   - **Mudanças necessárias**: Adicionar os campos `objetivo` e `tipo_alimento_preferencia` aos modelos `PetPreferencesCreate`, `PetPreferencesUpdate` e `PetPreferencesResponse`
   - **Impacto**: Médio - Requer atualização dos modelos e validações

3. **`backend/app/models/diet.py`** (se existir, ou criar novo)
   - **Mudanças necessárias**: Criar novos modelos para a tabela unificada de dietas
   - **Impacto**: Alto - Requer redesenho completo dos modelos de dieta

#### Rotas API

1. **`backend/app/api/animals.py`**
   - **Mudanças necessárias**: Atualizar para suportar os novos campos `altura` e `sexo`
   - **Impacto**: Médio - Requer atualização das rotas de criação e atualização de animais

2. **`backend/app/api/preferences.py`** (se existir)
   - **Mudanças necessárias**: Atualizar para suportar os novos campos `objetivo` e `tipo_alimento_preferencia`
   - **Impacto**: Médio - Requer atualização das rotas de preferências

3. **`backend/app/api/diets.py`**
   - **Mudanças necessárias**: Redesenhar completamente para trabalhar com a nova estrutura de banco de dados e integrar com o agente IA
   - **Impacto**: Alto - Requer reescrita significativa

#### Banco de Dados

1. **`backend/app/db/supabase.py`** (ou equivalente)
   - **Mudanças necessárias**: Possível atualização para suportar novas consultas ou operações
   - **Impacto**: Baixo - Provavelmente não requer mudanças significativas

### Frontend (se aplicável)

1. **Formulários de cadastro de animais**
   - **Mudanças necessárias**: Adicionar campos para altura e sexo
   - **Impacto**: Médio - Requer atualização de formulários e validações

2. **Formulários de preferências de pet**
   - **Mudanças necessárias**: Adicionar campos para objetivo e tipo de alimento preferido
   - **Impacto**: Médio - Requer atualização de formulários e validações

3. **Telas de dieta**
   - **Mudanças necessárias**: Redesenhar para mostrar as dietas geradas pela IA
   - **Impacto**: Alto - Requer redesenho significativo

## Novos Arquivos Necessários

1. **`backend/app/ai/diet_agent.py`** (ou similar)
   - **Propósito**: Implementar o agente IA para geração de dietas
   - **Funcionalidades**: Processamento de dados do animal, análise de preferências, geração de recomendações de dieta

2. **`backend/app/models/alimentos_base.py`**
   - **Propósito**: Modelos para a tabela de alimentos base
   - **Funcionalidades**: Definição de esquemas para alimentos base

3. **`backend/app/models/racas.py`**
   - **Propósito**: Modelos para a tabela de raças caninas
   - **Funcionalidades**: Definição de esquemas para raças caninas

## Arquivos de Migração

1. **`migrations/add_columns_to_animals.sql`** (já criado)
   - **Propósito**: Adicionar colunas 'altura' e 'sexo' na tabela public.animals

2. **`migrations/add_columns_to_preferencias_pet.sql`** (já criado)
   - **Propósito**: Adicionar colunas 'objetivo' e 'tipo_alimento_preferencia' na tabela public.preferencias_pet

3. **`migrations/unify_dietas_tables.sql`** (já criado)
   - **Propósito**: Unificar as tabelas de dieta em uma única tabela public.dietas

4. **`migrations/import_fixed_tables.sql`** (já criado)
   - **Propósito**: Importar as tabelas fixas alimentos_base_v2.sql e racas_caninas_seed.sql

## Arquivos de Teste

1. **`tests/test_animals.py`** (se existir)
   - **Mudanças necessárias**: Atualizar para testar os novos campos
   - **Impacto**: Médio - Requer atualização dos testes

2. **`tests/test_preferences.py`** (se existir)
   - **Mudanças necessárias**: Atualizar para testar os novos campos
   - **Impacto**: Médio - Requer atualização dos testes

3. **`tests/test_diets.py`** (se existir)
   - **Mudanças necessárias**: Redesenhar completamente para testar a nova estrutura
   - **Impacto**: Alto - Requer reescrita significativa

4. **`tests/test_diet_agent.py`** (novo)
   - **Propósito**: Testar o agente IA de dietas
   - **Funcionalidades**: Testes para geração de dietas, cálculo de calorias, etc.

## Documentação

1. **`docs/plano_implementacao_dieta_ia.md`** (já criado)
   - **Propósito**: Documentar o plano de implementação

2. **`docs/arquivos_afetados.md`** (este arquivo)
   - **Propósito**: Mapear os arquivos afetados pelas mudanças

3. **`docs/diagrama_relacionamento.md`** (a ser criado)
   - **Propósito**: Documentar o diagrama de relacionamento entre as tabelas

4. **`docs/api_dieta_ia.md`** (a ser criado)
   - **Propósito**: Documentar a nova API de dietas com IA