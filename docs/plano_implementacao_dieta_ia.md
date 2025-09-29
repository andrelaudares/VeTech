# Plano de Implementação: Migração da Funcionalidade de Dieta para IA

Este documento detalha o plano de implementação para migrar a funcionalidade de dieta de um processo manual para um sistema baseado em IA. O plano está dividido em 5 etapas principais, conforme solicitado.

## Visão Geral

A migração envolve transformar o processo atual de criação de dietas, que é feito manualmente pelo veterinário, para um sistema onde um agente de IA gera recomendações de dieta personalizadas para cada animal. Esta mudança requer modificações significativas no banco de dados e nas rotas da API.

## Etapa 1: Organização do Banco de Dados

### Alterações no Banco de Dados

1. **Adição de colunas na tabela `public.animals`**:
   - `altura`: Armazena a altura do animal em centímetros (tipo NUMERIC)
   - `sexo`: Armazena o sexo do animal (tipo VARCHAR(10))

2. **Adição de colunas na tabela `public.preferencias_pet`**:
   - `objetivo`: Armazena o objetivo da dieta (tipo VARCHAR(50))
   - `tipo_alimento_preferencia`: Armazena o tipo de alimento preferido (caseiro ou ração) (tipo VARCHAR(20))

3. **Unificação das tabelas de dieta**:
   - Unificar as tabelas `dietas`, `opcoes_dieta`, `alimentos_dieta` e `alimentos_evitar` em uma única tabela `public.dietas`
   - A nova tabela conterá campos como: nome da dieta, objetivo, tipo, refeições por dia, data de início, data de fim, status, quantidade em gramas, alimento (FK da tabela `alimentos_base`) e calorias

4. **Importação de tabelas fixas**:
   - `alimentos_base_v2.sql`: Contém dados sobre alimentos caseiros e rações
   - `racas_caninas_seed.sql`: Contém informações sobre raças de cachorro, peso ideal e outras informações contextuais

### Scripts de Migração

- `add_columns_to_animals.sql`: Adiciona as colunas 'altura' e 'sexo' na tabela `public.animals`
- `add_columns_to_preferencias_pet.sql`: Adiciona as colunas 'objetivo' e 'tipo_alimento_preferencia' na tabela `public.preferencias_pet`
- `unify_dietas_tables.sql`: Unifica as tabelas de dieta em uma única tabela `public.dietas`
- `import_fixed_tables.sql`: Importa as tabelas fixas `alimentos_base_v2.sql` e `racas_caninas_seed.sql`

## Etapa 2: Mapeamento e Ajuste de Arquivos Afetados

### Arquivos Afetados

1. **`backend/app/api/animals.py`**:
   - Atualizar para suportar os novos campos `altura` e `sexo`
   - Modificar os modelos e rotas relacionados

2. **`backend/app/models/animal.py`**:
   - Atualizar o modelo `AnimalCreate` e `AnimalResponse` para incluir os novos campos

3. **`backend/app/api/preferences.py`** (se existir):
   - Atualizar para suportar os novos campos `objetivo` e `tipo_alimento_preferencia`

4. **`backend/app/models/animal_preferences.py`**:
   - Atualizar os modelos `PetPreferencesCreate`, `PetPreferencesUpdate` e `PetPreferencesResponse` para incluir os novos campos

### Ajustes Necessários

- Atualizar validações de dados
- Atualizar documentação de API (se existir)
- Atualizar testes unitários e de integração

## Etapa 3: Planejamento da Nova Rota de Dietas e Agente IA

### Estrutura da Nova Rota de Dietas

1. **Endpoints necessários**:
   - `POST /dietas`: Criar uma nova dieta (agora gerada pela IA)
   - `GET /dietas/{animal_id}`: Obter dietas de um animal
   - `GET /dietas/{dieta_id}`: Obter detalhes de uma dieta específica
   - `PUT /dietas/{dieta_id}`: Atualizar uma dieta
   - `DELETE /dietas/{dieta_id}`: Excluir uma dieta

2. **Fluxo de dados**:
   - Receber dados do animal e preferências
   - Enviar para o agente IA
   - Receber recomendação de dieta
   - Salvar no banco de dados
   - Retornar para o cliente

### Agente IA

1. **Requisitos do agente**:
   - Acesso aos dados do animal (incluindo altura e sexo)
   - Acesso às preferências do pet (incluindo objetivo e tipo de alimento preferido)
   - Acesso à tabela de alimentos base
   - Acesso à tabela de raças caninas

2. **Funcionalidades do agente**:
   - Analisar dados do animal e preferências
   - Considerar raça, peso, altura, sexo e idade
   - Recomendar dieta personalizada
   - Calcular calorias e quantidades

## Etapa 4: Implementação das Rotas de Dietas

### Modificações no arquivo `backend/app/api/diets.py`

1. **Atualização dos modelos**:
   - Criar novos modelos para a tabela unificada de dietas
   - Atualizar os modelos existentes conforme necessário

2. **Atualização das rotas**:
   - Modificar as rotas existentes para trabalhar com a nova estrutura de banco de dados
   - Adicionar novas rotas conforme necessário

3. **Integração com o agente IA**:
   - Adicionar código para chamar o agente IA
   - Processar a resposta do agente IA
   - Salvar a dieta recomendada no banco de dados

## Etapa 5: Criação do Agente IA

### Desenvolvimento do Agente IA

1. **Arquitetura do agente**:
   - Definir a arquitetura do agente (modelo de linguagem, regras, etc.)
   - Definir os parâmetros de entrada e saída

2. **Treinamento e configuração**:
   - Configurar o agente com conhecimento sobre nutrição animal
   - Treinar o agente com dados específicos (se necessário)

3. **Integração**:
   - Integrar o agente com a API
   - Testar a geração de dietas

4. **Refinamento**:
   - Ajustar parâmetros do agente
   - Melhorar a qualidade das recomendações

## Cronograma Sugerido

- **Etapa 1**: 1-2 semanas
- **Etapa 2**: 1 semana
- **Etapa 3**: 1 semana
- **Etapa 4**: 2 semanas
- **Etapa 5**: 2-3 semanas

## Considerações Adicionais

- **Backup de dados**: Realizar backup completo antes de iniciar as migrações
- **Testes**: Implementar testes extensivos para cada etapa
- **Rollback**: Preparar planos de rollback em caso de problemas
- **Documentação**: Manter documentação atualizada durante todo o processo
- **Treinamento**: Preparar material de treinamento para os usuários finais

## Próximos Passos

1. Revisar e aprovar o plano de implementação
2. Iniciar a Etapa 1: Organização do Banco de Dados
3. Agendar reuniões de acompanhamento para cada etapa