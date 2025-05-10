# Sprint 5: Atividades Físicas - Detalhamento Revisado e Ampliado

Esta sprint foca na construção de um módulo robusto e intuitivo para a gestão de atividades físicas em uma clínica veterinária, permitindo que os usuários (funcionários da clínica, como veterinários ou cuidadores) gerenciem planos de atividades, registrem exercícios realizados e acompanhem o progresso dos animais. O objetivo é oferecer uma interface fluida, visualmente atraente e funcional, que facilite o planejamento e monitoramento de rotinas físicas personalizadas. São implementadas **seis telas distintas**, cada uma como uma página independente no sistema, interligadas por uma navegação clara e lógica, e não como seções, cards ou grupos dentro de uma única "Tela de atividades". Este design assegura clareza, evita sobrecarga de informações e suporta o fluxo de trabalho da clínica.

**Feature Contínua:** Todas as telas incluem um **dropdown de busca de animais** no topo da página, permitindo que o usuário selecione rapidamente um animal para visualizar ou gerenciar suas informações. Este recurso é essencial para clínicas com múltiplos pacientes, atualizando dinamicamente o conteúdo da tela ao trocar de animal.

**Usabilidade Estratégica para Gamificação:** Embora esta sprint foque em atividades físicas, a próxima sprint (Sprint 6) abordará gamificação diretamente. Aqui, já começamos a incorporar elementos visuais incentivadores, como barras de progresso, ícones de conquista e cores vibrantes, para motivar os usuários a engajarem-se com os planos de atividades. Esses componentes preparam o terreno para a gamificação, promovendo uma experiência envolvente e recompensadora.

---

## Tela 1: Listagem de Tipos de Atividades

### Descrição
A Tela de Listagem de Tipos de Atividades é a porta de entrada para o gerenciamento de atividades físicas globais da clínica, funcionando como um painel administrativo centralizado. Esta página independente exibe todos os tipos de atividades disponíveis no sistema (ex: caminhada, corrida, natação), permitindo ao usuário visualizar, editar ou adicionar novos tipos que podem ser usados em planos personalizados. Projetada para ser prática e acessível, a tela utiliza uma tabela interativa com busca e filtros, garantindo eficiência no gerenciamento de atividades em clínicas com diversos animais. A interface incorpora elementos visuais motivacionais, como ícones representando cada tipo de atividade, para tornar a experiência mais dinâmica.

### Componentes
- **Tabela de Tipos de Atividades:** Uma tabela responsiva com colunas:
  - **Nome:** Ex: "Caminhada".
  - **Tipo:** Ex: "Aeróbico", "Força".
  - **Calorias por Hora:** Ex: "200 kcal/h".
  - **Ações:** Botões para "Editar" e "Excluir".
- **Campo de Busca:** Pesquisa textual por nome ou tipo em tempo real.
- **Botão "Novo Tipo":** No canto superior direito, destacado com um ícone de adição, leva à Tela de Cadastro de Tipo.
- **Paginação:** Exibe até 10 tipos por página, com controles de navegação (anterior/próximo).
- **Indicador de Carregamento:** Um spinner aparece durante o carregamento inicial ou busca.
- **Ícones Visuais:** Cada tipo de atividade tem um ícone correspondente (ex: pegada para "Caminhada"), reforçando a usabilidade estratégica.

### Funcionalidades
- **Carregamento Inicial:** Requisição GET para `/api/v1/activities` retorna a lista de tipos de atividades globais da clínica.
- **Busca:** Filtragem local ou via API com GET `/api/v1/activities?search={termo}`.
- **Ações por Tipo:**
  - **Editar:** Redireciona para a Tela de Cadastro com dados preenchidos.
  - **Excluir:** Exibe um modal de confirmação antes de enviar DELETE para `/api/v1/activities/{activity_id}`.
- **Autenticação:** Todas as requisições incluem token JWT no cabeçalho `Authorization`.

### Fluxo de Uso do Usuário
1. O usuário acessa o sistema com email e senha na tela de login.
2. Se esqueceu a senha, clica em "Recuperar Senha", insere o email, recebe um link de redefinição e redefine a senha.
3. Após login, no menu lateral, seleciona "Atividades Físicas" e escolhe "Tipos de Atividades".
4. A Tela de Listagem carrega com uma tabela mostrando tipos como "Caminhada" (Aeróbico, 200 kcal/h).
5. Digita "Caminhada" no campo de busca, e a tabela filtra para mostrar apenas esse tipo.
6. Clica em "Novo Tipo" para adicionar uma nova atividade, como "Natação".
7. Clica em "Editar" em "Caminhada" para ajustar as calorias ou "Excluir" para removê-la, confirmando no modal.

---

## Tela 2: Cadastro de Tipo de Atividade

### Descrição
A Tela de Cadastro de Tipo de Atividade é uma página dedicada à criação de novos tipos de atividades que podem ser usados em planos personalizados. Com um formulário simples e bem estruturado, ela permite ao usuário registrar atividades globais com informações detalhadas, como nome, tipo e calorias. Projetada para ser intuitiva, a tela inclui validações visíveis e feedback imediato, garantindo que os dados sejam consistentes. Elementos visuais, como uma pré-visualização do ícone da atividade, reforçam a usabilidade estratégica, incentivando o engajamento.

### Componentes
- **Formulário de Cadastro:**
  - **Nome:** Campo de texto (ex: "Natação", obrigatório).
  - **Tipo:** Dropdown com opções como "Aeróbico", "Força", "Flexibilidade" (obrigatório).
  - **Calorias por Hora:** Campo numérico (ex: "300", opcional).
  - **Ícone (Opcional):** Dropdown ou upload para selecionar um ícone representativo.
- **Botão "Salvar":** Envia os dados para o backend, destacado em verde para incentivar ação.
- **Botão "Cancelar":** Retorna à Listagem sem salvar, em cinza para contraste.
- **Mensagens de Erro:** Exibidas em vermelho abaixo dos campos (ex: "Nome é obrigatório").
- **Pré-visualização do Ícone:** Mostra o ícone selecionado ao lado do formulário, aumentando o apelo visual.

### Funcionalidades
- **Envio de Dados:** Requisição POST para `/api/v1/activities` com os dados do formulário.
- **Sucesso:** Redireciona para a Tela de Listagem com o novo tipo exibido.
- **Erro:** Exibe mensagens de validação, como "Campo obrigatório" ou "Calorias inválidas".
- **Validação no Frontend:** Usa bibliotecas como React Hook Form para verificar campos antes do envio.

### Fluxo de Uso do Usuário
1. Na Tela de Listagem de Tipos, o usuário clica em "Novo Tipo".
2. A tela de cadastro carrega com o formulário vazio.
3. Preenche Nome ("Natação"), Tipo ("Aeróbico"), Calorias por Hora ("300") e seleciona um ícone de nado.
4. Vê a pré-visualização do ícone ao selecioná-lo, confirmando a escolha.
5. Clica em "Salvar"; um spinner aparece, e, se bem-sucedido, retorna à Listagem com "Natação" na tabela.
6. Se esquece o Nome, uma mensagem de erro aparece ao tentar salvar.
7. Clica em "Cancelar" para voltar sem salvar.

---

## Tela 3: Listagem de Planos de Atividade

### Descrição
A Tela de Listagem de Planos de Atividade é uma página central que exibe os planos de atividades associados a um animal específico, funcionando como um painel de monitoramento personalizado. Com o **dropdown de busca de animais** no topo, o usuário pode alternar rapidamente entre pacientes, atualizando a tabela dinamicamente. A interface combina funcionalidade com elementos visuais incentivadores, como barras de progresso que mostram a adesão ao plano, motivando os usuários a manterem as rotinas. Esta tela é ideal para clínicas que precisam acompanhar múltiplos planos de exercícios.

### Componentes
- **Dropdown de Busca de Animais:** No topo, com busca incremental por nome, atualiza a tabela ao selecionar.
- **Tabela de Planos:** Colunas incluem:
  - **Atividade:** Ex: "Caminhada".
  - **Frequência Semanal:** Ex: "3x/semana".
  - **Duração por Sessão:** Ex: "30 min".
  - **Progresso:** Barra de progresso indicando % de conclusão (ex: 75% com base em atividades registradas).
  - **Ações:** Botões para "Visualizar", "Editar" e "Excluir".
- **Campo de Busca:** Filtra planos por nome da atividade.
- **Botão "Novo Plano":** No topo direito, leva ao cadastro.
- **Paginação:** Até 10 planos por página.
- **Indicador de Carregamento:** Spinner durante a troca de animal ou carregamento.

### Funcionalidades
- **Seleção de Animal:** GET `/api/v1/animals` para o dropdown; GET `/api/v1/animals/{animal_id}/activity-plans` para os planos.
- **Carregamento:** Exibe os planos do animal selecionado.
- **Ações:**
  - **Visualizar:** Leva à Tela de Detalhes do Plano.
  - **Editar:** Abre o formulário de cadastro com dados preenchidos.
  - **Excluir:** Modal de confirmação antes de DELETE `/api/v1/animals/{animal_id}/activity-plans/{plan_id}`.
- **Progresso:** Calculado com base em atividades registradas via API.

### Fluxo de Uso do Usuário
1. No menu lateral, o usuário seleciona "Planos de Atividade".
2. Escolhe "Rex" no dropdown de busca; a tabela carrega com os planos de "Rex".
3. Vê "Caminhada" (3x/semana, 30 min, 75% concluído) com uma barra de progresso verde.
4. Digita "Caminhada" na busca para filtrar a tabela.
5. Clica em "Novo Plano" para criar um plano ou em "Visualizar" para detalhes de "Caminhada".
6. Exclui um plano após confirmar no modal.

---

## Tela 4: Cadastro de Plano de Atividade

### Descrição
A Tela de Cadastro de Plano de Atividade permite criar planos personalizados para um animal, com um formulário que captura informações detalhadas sobre a atividade, frequência e duração. A interface é enriquecida com elementos visuais, como uma pré-visualização da barra de progresso inicial do plano, incentivando o usuário a configurar rotinas motivadoras. Com o dropdown de busca no topo, o contexto do animal é mantido, garantindo uma experiência fluida e personalizada.

### Componentes
- **Dropdown de Busca de Animais:** Pré-selecionado com o animal atual.
- **Formulário de Cadastro:**
  - **Atividade:** Dropdown com tipos de atividades (de `/api/v1/activities`, obrigatório).
  - **Frequência Semanal:** Campo numérico (ex: "3", obrigatório).
  - **Duração por Sessão:** Campo numérico em minutos (ex: "30", obrigatório).
  - **Observações:** Textarea para detalhes (opcional).
- **Botão "Salvar":** Envia o plano, em verde vibrante.
- **Botão "Cancelar":** Retorna à Listagem.
- **Pré-visualização de Progresso:** Mostra uma barra de progresso inicial (0%) para o plano.

### Funcionalidades
- **Envio de Dados:** POST para `/api/v1/animals/{animal_id}/activity-plans`.
- **Sucesso:** Redireciona para a Tela de Listagem com o novo plano.
- **Erro:** Exibe mensagens como "Frequência inválida".

### Fluxo de Uso do Usuário
1. Na Listagem de Planos, com "Rex" selecionado, o usuário clica em "Novo Plano".
2. Escolhe Atividade ("Caminhada"), Frequência ("3"), Duração ("30") e adiciona uma observação ("Após refeição").
3. Vê a barra de progresso inicial (0%) ao preencher.
4. Clica em "Salvar" e retorna à Listagem, onde o plano aparece.
5. Se deixa a Atividade vazia, vê um erro.
6. Clica em "Cancelar" para desistir.

---

## Tela 5: Registro de Atividades Realizadas

### Descrição
A Tela de Registro de Atividades Realizadas é uma página dedicada a marcar atividades como concluídas, essencial para atualizar o progresso dos planos. Com um formulário compacto e elementos visuais como ícones de check verde, ela incentiva o usuário a registrar atividades, reforçando a sensação de conquista. O dropdown de busca mantém o contexto do animal, permitindo registros rápidos e precisos.

### Componentes
- **Dropdown de Busca de Animais:** No topo, para selecionar o animal.
- **Formulário de Registro:**
  - **Plano:** Dropdown com planos ativos do animal (obrigatório).
  - **Data:** Date picker (obrigatório, padrão: hoje).
  - **Status:** Dropdown com "Concluído" ou "Não Realizado" (obrigatório).
- **Botão "Salvar":** Envia o registro.
- **Botão "Cancelar":** Volta à Listagem de Planos.
- **Ícone de Conquista:** Um check verde aparece ao salvar com "Concluído".

### Funcionalidades
- **Envio de Dados:** POST para `/api/v1/activity-plans/{plan_id}/activities`.
- **Sucesso:** Retorna à Listagem com a barra de progresso atualizada.
- **Erro:** Mensagens de validação aparecem.

### Fluxo de Uso do Usuário
1. Na Listagem de Planos, o usuário clica em "Registrar Atividade" para "Rex".
2. Seleciona o plano "Caminhada", Data ("26/10/2023") e Status ("Concluído").
3. Clica em "Salvar"; um ícone de check aparece, e o usuário volta à Listagem.
4. Se esquece a Data, vê um erro.
5. Clica em "Cancelar" para retornar sem salvar.

---

## Tela 6: Histórico de Atividades

### Descrição
A Tela de Histórico de Atividades exibe o registro completo de atividades realizadas por um animal, funcionando como um painel de acompanhamento detalhado. Com uma tabela interativa e filtros, ela permite ao usuário revisar o progresso ao longo do tempo, reforçado por uma linha do tempo visual que destaca marcos (ex: semanas com 100% de adesão). O dropdown de busca no topo facilita a troca entre animais, e o design motivacional mantém o usuário engajado.

### Componentes
- **Dropdown de Busca de Animais:** Atualiza o histórico dinamicamente.
- **Tabela de Histórico:** Colunas:
  - **Data:** Ex: "26/10/2023".
  - **Atividade:** Ex: "Caminhada".
  - **Status:** Ex: "Concluído".
  - **Observações:** Ex: "Feito com tutor".
- **Linha do Tempo Visual:** Mostra atividades concluídas com ícones de troféu para marcos.
- **Filtros:** Por data ou status.
- **Paginação:** Até 10 registros por página.

### Funcionalidades
- **Carregamento:** GET para `/api/v1/animals/{animal_id}/activity-history`.
- **Filtros:** Suporta GET `/api/v1/animals/{animal_id}/activity-history?date={range}`.
- **Linha do Tempo:** Calculada localmente com base nos dados retornados.

### Fluxo de Uso do Usuário
1. No menu, o usuário seleciona "Histórico de Atividades".
2. Escolhe "Luna" no dropdown; a tabela carrega com o histórico.
3. Vê a linha do tempo destacando "Semana 100% concluída" com um troféu.
4. Filtra por "Concluído" para ver apenas atividades realizadas.
5. Navega pelas páginas para revisar registros antigos.

---

## Estrutura e Navegação
As seis telas são **páginas distintas**, não seções dentro de uma "Tela de Resultados". Elas formam um fluxo lógico:
- **Listagem de Tipos → Cadastro de Tipo.**
- **Listagem de Planos → Cadastro de Plano → Registro de Atividades → Histórico.**
O dropdown de busca no topo permite alternar entre animais em todas as telas, mantendo o contexto e agilizando a navegação.

---

## Detalhes Técnicos
- **Rotas Backend:**
  - GET `/api/v1/activities` – Lista tipos de atividades.
  - POST `/api/v1/activities` – Cadastra um tipo.
  - DELETE `/api/v1/activities/{activity_id}` – Exclui um tipo.
  - GET `/api/v1/animals/{animal_id}/activity-plans` – Lista planos.
  - POST `/api/v1/animals/{animal_id}/activity-plans` – Cadastra plano.
  - DELETE `/api/v1/animals/{animal_id}/activity-plans/{plan_id}` – Exclui plano.
  - POST `/api/v1/activity-plans/{plan_id}/activities` – Registra atividade.
  - GET `/api/v1/animals/{animal_id}/activity-history` – Histórico.
  - GET `/api/v1/animals` – Lista animais para o dropdown.
- **Autenticação:** Token JWT em todas as requisições.
- **Frontend:** React, React Router, Tailwind CSS, com barras de progresso e ícones via bibliotecas como FontAwesome.

---

## Tarefas da Sprint
- Implementar dropdown de busca em todas as telas, integrado com `/api/v1/animals`.
- Criar tabelas e formulários com validações e elementos visuais incentivadores.
- Desenvolver a linha do tempo na Tela de Histórico com marcos visuais.
- Testar navegação, integração com backend e responsividade.

---

Esta versão revisada da Sprint 5 detalha as telas com descrições ricas, fluxos de uso claros e elementos visuais estratégicos, mantendo a feature do dropdown de busca. Para a Sprint 6 (Gamificação), introduzirei uma nova feature, como sugerido, além de intensificar os elementos de gamificação. O que achou? Podemos avançar?