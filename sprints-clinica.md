# Backlog e Planejamento de Sprints — API VeTech (Clínica)

Este documento apresenta o backlog de requisitos (User Stories) focado nas funcionalidades da clínica e o planejamento de sprints para o desenvolvimento da API, alinhado com a estrutura atual do banco de dados e os fluxos de Nutrição, Atividades Físicas e Gamificação.

---

## 📋 Backlog de Requisitos (User Stories)

| ID   | User Story                                                                 | Critérios de Aceitação (Exemplos)                                                                   | Rota(s) API (Conforme api_documentation.md ou a ser definida) | Status        |
|------|----------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|---------------------------------------------------------------|---------------|
| **Sprint 1: Autenticação e Perfil** |||||
| US1  | Como clínica, quero fazer login para acessar o sistema.                      | - Receber email/senha. <br/> - Validar credenciais no Supabase Auth. <br/> - Retornar token JWT e dados básicos da clínica. | `POST /api/v1/auth/login`                                       | **Concluído** |
| US2  | Como clínica, quero fazer logout para encerrar minha sessão.                 | - Receber requisição (token no header). <br/> - Retornar mensagem de sucesso (cliente descarta token).      | `POST /api/v1/auth/logout`                                      | **Concluído** |
| US3  | Como clínica, quero visualizar e atualizar meu perfil (nome, telefone).       | - `GET`: Validar token, buscar dados da clínica logada na tabela `clinics`, retornar dados. <br/> - `PUT`: Validar token, receber dados (nome, telefone), atualizar na tabela `clinics`, retornar dados atualizados. | `GET /api/v1/clinic/profile`<br/>`PUT /api/v1/clinic/profile`   | **Concluído** |
| **Sprint 2: Gestão de Animais (Pets)** |||||
| US4  | Como clínica, quero cadastrar novos animais (pets).                        | - Receber dados do animal (incluindo `name`, `species`, `breed`, `date_birth`, `tutor_name`, `email`, `phone`, `weight`, `medical_history`). <br/> - Validar dados. <br/> - Inserir na tabela `animals` associado à `clinics_id`. <br/> - Retornar dados do animal criado. | `POST /api/v1/animals`        | **Concluído** |
| US5  | Como clínica, quero listar meus animais cadastrados.                       | - Receber `clinic_id` (via token/query param). <br/> - Buscar animais na tabela `animals` filtrando por `clinics_id`. <br/> - Retornar lista. | `GET /api/v1/animals`          | **Concluído** |
| US6  | Como clínica, quero ver detalhes de um animal específico.                   | - Receber `animal_id` (path param) e `clinic_id` (token/query). <br/> - Buscar animal específico verificando `clinics_id`. <br/> - Retornar detalhes. | `GET /api/v1/animals/{animal_id}` | **Concluído** |
| US7  | Como clínica, quero atualizar dados de um animal.                           | - Receber `animal_id` (path), `clinic_id` (token/query), e dados a atualizar. <br/> - Validar e atualizar na tabela `animals`. <br/> - Retornar dados atualizados. | `PATCH /api/v1/animals/{animal_id}` | **Concluído** |
| US8  | Como clínica, quero remover um animal do sistema.                           | - Receber `animal_id` (path) e `clinic_id` (token/query). <br/> - Remover da tabela `animals`. <br/> - Retornar confirmação. | `DELETE /api/v1/animals/{animal_id}` | **Concluído** |
| US9  | Como clínica, quero cadastrar as preferências alimentares de um pet.       | - Receber `animal_id` e dados de preferências (`gosta_de`, `nao_gosta_de`). <br/> - Inserir na tabela `preferencias_pet` associado ao `animal_id`. <br/> - Retornar dados das preferências. | `POST /api/v1/animals/{animal_id}/preferences` | **Concluído** |
| US10 | Como clínica, quero visualizar e atualizar as preferências de um pet.      | - Buscar/atualizar dados na tabela `preferencias_pet` para o `animal_id` específico. <br/> - Retornar dados atualizados. | `GET /api/v1/animals/{animal_id}/preferences`<br/>`PUT /api/v1/animals/{animal_id}/preferences` | **Concluído** |
| **Sprint 3: Consultas e Agendamentos** |||||
| US11 | Como clínica, quero criar agendamentos para animais.                     | - Receber dados de agendamento (incluindo `animal_id`, `date`, `start_time`, `end_time`, `description`, `status`). <br/> - Inserir na tabela `appointments`. <br/> - Retornar dados do agendamento. | `POST /api/v1/appointments`                                   | **Concluído** |
| US12 | Como clínica, quero listar todos os agendamentos com filtros.            | - Buscar agendamentos na tabela `appointments` com filtros opcionais (data, status). <br/> - Retornar lista filtrada. | `GET /api/v1/appointments`                                     | **Concluído** |
| US13 | Como clínica, quero visualizar detalhes de um agendamento.               | - Buscar agendamento específico por ID. <br/> - Retornar detalhes. | `GET /api/v1/appointments/{id}`                                | **Concluído** |
| US14 | Como clínica, quero atualizar um agendamento.                            | - Receber dados a atualizar e atualizar na tabela `appointments`. <br/> - Retornar dados atualizados. | `PATCH /api/v1/appointments/{id}`                              | **Concluído** |
| US15 | Como clínica, quero remover um agendamento.                              | - Remover agendamento da tabela `appointments`. <br/> - Retornar confirmação. | `DELETE /api/v1/appointments/{id}`                             | **Concluído** |
| US16 | Como clínica, quero registrar consultas/histórico médico para animais.   | - Receber dados da consulta (incluindo `animal_id`, `description`, `date`). <br/> - Inserir na tabela `consultations`. <br/> - Retornar dados da consulta. | `POST /api/v1/consultations`                                  | **Concluído** |
| US17 | Como clínica, quero listar consultas realizadas com filtro por animal.   | - Buscar consultas na tabela `consultations` com filtro opcional por `animal_id`. <br/> - Retornar lista filtrada. | `GET /api/v1/consultations`                                    | **Concluído** |
| US18 | Como clínica, quero atualizar uma consulta registrada.                   | - Receber dados a atualizar e atualizar na tabela `consultations`. <br/> - Retornar dados atualizados. | `PATCH /api/v1/consultations/{id}`                            | **Concluído** |
| US19 | Como clínica, quero remover uma consulta registrada.                     | - Remover consulta da tabela `consultations`. <br/> - Retornar confirmação. | `DELETE /api/v1/consultations/{id}`                           | **Concluído** |
| **Sprint 4: Módulo de Nutrição e Dietas** |||||
| US20 | Como clínica, quero criar um plano de dieta para um animal.             | - Receber dados da dieta (incluindo `pet_id`, `tipo`, `objetivo`, `peso_atual_pet`, `idade_pet`, etc). <br/> - Inserir na tabela `dietas`. <br/> - Retornar dados da dieta criada. | `POST /api/v1/animals/{animal_id}/diets`                     | Pendente      |
| US21 | Como clínica, quero listar todas as dietas de um animal.                | - Buscar dietas na tabela `dietas` filtrando por `pet_id`. <br/> - Retornar lista de dietas. | `GET /api/v1/animals/{animal_id}/diets`                       | Pendente      |
| US22 | Como clínica, quero visualizar detalhes de uma dieta específica.        | - Buscar dieta específica por ID. <br/> - Retornar detalhes incluindo opções de dieta associadas. | `GET /api/v1/diets/{diet_id}`                                 | Pendente      |
| US23 | Como clínica, quero atualizar uma dieta existente.                      | - Receber dados a atualizar e atualizar na tabela `dietas`. <br/> - Retornar dados atualizados. | `PUT /api/v1/diets/{diet_id}`                                 | Pendente      |
| US24 | Como clínica, quero adicionar opções de dieta a um plano.               | - Receber dados da opção (incluindo `dieta_id`, `nome`, `valor_mensal_estimado`, etc). <br/> - Inserir na tabela `opcoes_dieta`. <br/> - Retornar dados da opção criada. | `POST /api/v1/diets/{diet_id}/options`                        | Pendente      |
| US25 | Como clínica, quero adicionar alimentos a uma opção de dieta.           | - Receber dados dos alimentos (incluindo `opcao_dieta_id`, `nome`, `tipo`, `quantidade`, etc). <br/> - Inserir na tabela `alimentos_dieta`. <br/> - Retornar dados dos alimentos. | `POST /api/v1/diet-options/{option_id}/foods`                | Pendente      |
| US26 | Como clínica, quero gerenciar alimentos que o pet deve evitar.          | - CRUD para tabela `alimentos_evitar` associados a um `pet_id`. | `POST/GET/PUT/DELETE /api/v1/animals/{animal_id}/restricted-foods` | Pendente      |
| US27 | Como clínica, quero gerenciar snacks permitidos entre refeições.        | - CRUD para tabela `snacks_entre_refeicoes` associados a um `pet_id`. | `POST/GET/PUT/DELETE /api/v1/animals/{animal_id}/snacks`      | Pendente      |
| **Sprint 5: Módulo de Atividades Físicas** |||||
| US28 | Como clínica, quero cadastrar tipos de atividades disponíveis.          | - Receber dados da atividade (incluindo `nome`, `tipo`, `calorias_estimadas_por_minuto`). <br/> - Inserir na tabela `atividades`. <br/> - Retornar dados da atividade criada. | `POST /api/v1/activities`                                    | Pendente      |
| US29 | Como clínica, quero listar todas as atividades disponíveis.             | - Buscar atividades na tabela `atividades`. <br/> - Retornar lista. | `GET /api/v1/activities`                                     | Pendente      |
| US30 | Como clínica, quero criar um plano de atividades para um animal.        | - Receber dados do plano (incluindo `id_pet`, `atividade_id`, `frequencia_semanal`, `duracao_minutos`, etc). <br/> - Inserir na tabela `planos_atividade`. <br/> - Retornar dados do plano. | `POST /api/v1/animals/{animal_id}/activity-plans`            | Pendente      |
| US31 | Como clínica, quero listar todos os planos de atividade de um animal.   | - Buscar planos na tabela `planos_atividade` filtrando por `id_pet`. <br/> - Retornar lista. | `GET /api/v1/animals/{animal_id}/activity-plans`             | Pendente      |
| US32 | Como clínica, quero atualizar um plano de atividade existente.          | - Receber dados a atualizar e atualizar na tabela `planos_atividade`. <br/> - Retornar dados atualizados. | `PUT /api/v1/activity-plans/{plan_id}`                       | Pendente      |
| US33 | Como clínica, quero registrar atividades realizadas pelo pet.           | - Receber dados da atividade realizada (incluindo `plano_id`, `data`, `realizado`). <br/> - Inserir na tabela `atividades_realizadas`. <br/> - Retornar dados da atividade realizada. | `POST /api/v1/activity-plans/{plan_id}/activities`           | Pendente      |
| US34 | Como clínica, quero visualizar o histórico de atividades de um pet.     | - Buscar atividades realizadas na tabela `atividades_realizadas` filtrando por `plano_id`. <br/> - Retornar histórico. | `GET /api/v1/animals/{animal_id}/activity-history`           | Pendente      |
| **Sprint 6: Gamificação e Sistema de Recompensas** |||||
| US35 | Como clínica, quero criar metas de gamificação para pets.               | - Receber dados da meta (incluindo `descricao`, `tipo`, `quantidade`, `unidade`, `periodo`). <br/> - Inserir na tabela `gamificacao_metas`. <br/> - Retornar dados da meta. | `POST /api/v1/gamification/goals`                           | Pendente      |
| US36 | Como clínica, quero listar todas as metas de gamificação disponíveis.   | - Buscar metas na tabela `gamificacao_metas`. <br/> - Retornar lista de metas. | `GET /api/v1/gamification/goals`                            | Pendente      |
| US37 | Como clínica, quero atribuir pontuações a um pet por metas alcançadas.  | - Receber dados da pontuação (incluindo `id_pet`, `id_meta`, `pontos_obtidos`, `data`). <br/> - Inserir na tabela `gamificacao_pontuacoes`. <br/> - Retornar dados da pontuação. | `POST /api/v1/gamification/points`                          | Pendente      |
| US38 | Como clínica, quero visualizar o histórico de pontuações de um pet.     | - Buscar pontuações na tabela `gamificacao_pontuacoes` filtrando por `id_pet`. <br/> - Retornar histórico de pontuações. | `GET /api/v1/animals/{animal_id}/gamification/points`        | Pendente      |
| US39 | Como clínica, quero criar recompensas para serem desbloqueadas por pontos. | - Receber dados da recompensa (incluindo `nome`, `pontos_necessarios`, `tipo`). <br/> - Inserir na tabela `gamificacao_recompensas`. <br/> - Retornar dados da recompensa. | `POST /api/v1/gamification/rewards`                         | Pendente      |
| US40 | Como clínica, quero atribuir recompensas aos pets que atingirem pontuação. | - Verificar pontos do pet e atribuir recompensas disponíveis. <br/> - Retornar recompensas desbloqueadas. | `POST /api/v1/animals/{animal_id}/gamification/rewards`      | Pendente      |
| US41 | Como clínica, quero visualizar ranking de pontuação entre os pets.      | - Consultar pontuações agregadas por pet e ordenar. <br/> - Retornar ranking. | `GET /api/v1/gamification/ranking`                          | Pendente      |
| US42 | Como clínica, quero gerar relatórios de progresso dos pets nas metas.   | - Analisar dados de alimentação, atividades e pontuações. <br/> - Gerar estatísticas e relatórios. | `GET /api/v1/animals/{animal_id}/gamification/reports`       | Pendente      |

---

## 🚀 Planejamento de Sprints (Revisado)

Cada sprint terá duração de 2 semanas, com foco incremental nas funcionalidades.

### Sprint 1 — Autenticação e Perfil da Clínica (Status: Concluído)
- **US1**: Login da clínica - **Concluído**
- **US2**: Logout da clínica - **Concluído**
- **US3**: Visualização/edição de perfil da clínica - **Concluído**

_Foco:_ Autenticação, gerenciamento de sessão, CRUD básico do perfil da clínica.

### Sprint 2 — Gestão de Animais (Pets) e Preferências (Status: Concluído)
- **US4-US8**: CRUD completo de animais - **Concluído**
- **US9-US10**: Gerenciamento de preferências alimentares - **Concluído**

_Foco:_ Implementar endpoints para gerenciamento de animais e suas preferências, base para os módulos de nutrição e atividades.

### Sprint 3 — Consultas e Agendamentos (Status: Concluído)
- **US11-US15**: CRUD de Agendamentos - **Concluído**
- **US16-US19**: CRUD de Consultas - **Concluído**

_Foco:_ Implementar endpoints para gerenciamento de agendamentos e histórico de consultas veterinárias.

### Sprint 4 — Módulo de Nutrição e Dietas
- **US20-US23**: CRUD de Dietas
- **US24-US25**: Gerenciamento de opções de dieta e alimentos
- **US26-US27**: Gerenciamento de alimentos restritos e snacks

_Foco:_ Implementar toda a estrutura de nutrição, com planos de dieta, opções, alimentos e restrições alimentares.

### Sprint 5 — Módulo de Atividades Físicas
- **US28-US29**: Gerenciamento de tipos de atividades
- **US30-US32**: CRUD de planos de atividade
- **US33-US34**: Registro e histórico de atividades realizadas

_Foco:_ Implementar toda a estrutura de atividades físicas, com tipos, planos e acompanhamento.

### Sprint 6 — Gamificação e Sistema de Recompensas
- **US35-US36**: Criação e listagem de metas
- **US37-US38**: Atribuição e visualização de pontuações
- **US39-US40**: Gerenciamento de recompensas
- **US41-US42**: Ranking e relatórios de progresso

_Foco:_ Implementar o sistema de gamificação completo, com metas, pontuações, recompensas e relatórios.

---

## 📈 Fluxos Principais

### Fluxo de Dieta e Alimentação
1. Clínica acessa o painel e seleciona o pet.
2. Avalia peso, idade, condição clínica, objetivo e preferências.
3. Define dietas e cadastra até 3 opções de dieta.
4. Preenche os alimentos de cada opção.
5. Registra alimentos a evitar para aquele pet.
6. Cadastra snacks permitidos entre refeições.
7. Tutor visualiza no app:
   - As opções com valores, porções e recomendações.
   - Lista de alimentos proibidos.
   - Snacks liberados e frequência.
8. Tutor escolhe a dieta → App atualiza metas e gamificação.

### Fluxo de Atividades Físicas
1. Clínica acessa o painel e seleciona o pet.
2. Avalia peso, idade, condição clínica e nível de energia.
3. Define plano de atividades personalizado:
   - Tipo de atividade (caminhada, corrida, natação, brincadeira)
   - Frequência semanal
   - Duração por sessão
   - Intensidade
4. Registra preferências ou restrições do pet.
5. Tutor visualiza no app:
   - Plano semanal de atividades.
   - Orientações da clínica.
   - Calorias estimadas por atividade.
6. Tutor marca as atividades como "Realizadas".
7. Veterinário acompanha o histórico e ajusta o plano conforme evolução.
8. App atualiza o progresso nas metas de atividade física.

### Fluxo de Gamificação
1. Criação de Metas pela Clínica
2. Tutor realiza ações (alimentação, atividades)
3. Sistema calcula o progresso
4. Desbloqueio de recompensas
5. Tutor consulta ranking e histórico
6. Veterinário acompanha desempenho e adapta metas

---

**Observações Finais:**
- Sprints focadas na implementação incremental, das funcionalidades mais básicas para as mais avançadas.
- APIs bem definidas para cada funcionalidade, seguindo padrões REST.
- Atualização contínua da documentação conforme implementação.
- Testes unitários e de integração para cada endpoint.
- Todas as sprints estão alinhadas com as tabelas existentes no banco de dados.

Bom desenvolvimento! 🚀

