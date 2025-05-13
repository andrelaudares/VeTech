# Sprint 3: Consultas e Agendamentos - Detalhamento (Versão 2)

Esta sprint foca na implementação das funcionalidades principais para a gestão de consultas e agendamentos em uma clínica veterinária. O objetivo é criar um sistema intuitivo, eficiente e robusto que permita aos usuários (funcionários da clínica) listar, cadastrar, visualizar, editar e gerenciar consultas e agendamentos dos animais de forma fluida. Abaixo, detalho cada uma das **grupos de funcionalidades** que compõem as **Páginas de Consultas** e **Páginas de Agendamentos**, que são áreas distintas interligadas por uma navegação clara dentro da mesma página.

---

## Páginas de Consultas e Agendamentos

As **Páginas de Consultas** e **Páginas de Agendamentos** são compostas por grupos de funcionalidades principais, cada um com seu propósito específico, mas todos integrados em uma única página para facilitar a navegação e o uso intuitivo. Esses grupos são:

- **Página de Agendamentos:**
  1. **Grupo 1: Listagem de Agendamentos**
  2. **Grupo 2: Cadastro de Agendamento**
  3. **Grupo 3: Detalhes do Agendamento**
  4. **Grupo 4: Edição de Agendamento**

- **Página de Consultas:**
  1. **Grupo 1: Listagem de Consultas**
  2. **Grupo 2: Cadastro de Consulta**
  3. **Grupo 3: Detalhes da Consulta**
  4. **Grupo 4: Edição de Consulta**

Esses grupos são organizados de forma atrativa e intuitiva, com algumas funcionalidades, como adicionar e editar, minimizadas em pop-ups para melhorar a experiência do usuário, mantendo o contexto da página sem redirecionamentos desnecessários.

---

## Integração com o Header

O componente `AppHeader` é essencial para a navegação e o controle de estado global da aplicação VeTech, especialmente por meio do dropdown de seleção de animal. Para as **Páginas de Consultas** e **Páginas de Agendamentos**, a seleção de animal no header **afeta diretamente** o comportamento dessas páginas, pois elas estão classificadas como "telas com seleção opcional" (conforme `HEADER_DOCS-v2.md`). Isso implica que:

- **Visibilidade do Dropdown:** O dropdown de seleção de animal **será exibido** enquanto o usuário estiver nas Páginas de Consultas ou Agendamentos.
- **Impacto da Seleção:**
  - **Sem animal selecionado:** A página exibe uma visão geral, mostrando todos os agendamentos ou consultas da clínica.
  - **Com animal selecionado:** A página aplica um filtro automático, exibindo apenas os agendamentos ou consultas do animal escolhido no header.
- **Estado Global:** O estado `selectedAnimal` no `AnimalContext` é utilizado para determinar o filtro aplicado nas requisições e na exibição dos dados.

Essa abordagem permite que o usuário alterne facilmente entre uma visão geral e uma visão específica de um animal, sem precisar navegar para outra página, melhorando a usabilidade e a eficiência.

---

## Página de Agendamentos

### Grupo 1: Listagem de Agendamentos

#### Descrição
O **Grupo de Listagem de Agendamentos** é o ponto de entrada para a gestão de agendamentos na página. Ele exibe uma lista de agendamentos, que pode ser geral (todos os agendamentos da clínica) ou filtrada pelo animal selecionado no header. A interface é projetada para ser funcional, acessível e visualmente atrativa, permitindo ao usuário visualizar rapidamente informações-chave, buscar agendamentos específicos e acessar ações relacionadas.

#### Componentes
- **Tabela de Agendamentos:** Uma tabela organizada com colunas para Data, Hora, Animal, Descrição, Status e Ações (visualizar, editar, excluir).
- **Campo de Busca:** Um campo de texto para buscar agendamentos por nome do animal ou descrição, com filtragem em tempo real.
- **Filtros Avançados:** Dropdowns para filtrar por status (ex: "Agendado") ou intervalo de datas.
- **Botão "Novo Agendamento":** Localizado no topo direito, abre o **Grupo de Cadastro** em um pop-up.
- **Paginação:** Exibe 10 agendamentos por página, com controles para navegar entre páginas.
- **Indicador de Carregamento:** Um spinner exibido enquanto a lista é carregada da API.

#### Funcionalidades
- **Carregamento Inicial:**
  - Se **nenhum animal estiver selecionado** no header, faz uma requisição GET para `/api/v1/appointments` para listar todos os agendamentos da clínica.
  - Se **um animal estiver selecionado**, faz uma requisição GET para `/api/v1/appointments?animal_id={selectedAnimal.id}` para listar apenas os agendamentos do animal selecionado.
- **Busca e Filtro:** A busca é processada localmente na tabela ou via API, dependendo da implementação.
- **Ações por Agendamento:**
  - **Visualizar:** Abre o **Grupo de Detalhes do Agendamento** em um pop-up.
  - **Editar:** Abre o **Grupo de Edição de Agendamento** em um pop-up.
  - **Excluir:** Abre um modal de confirmação; se confirmado, envia DELETE para `/api/v1/appointments/{appointment_id}`.
- **Autenticação:** Todas as requisições incluem o token JWT no header `Authorization`.

#### Fluxo de Uso do Usuário
1. O usuário acessa a Página de Agendamentos via navegação no header.
2. Se nenhum animal estiver selecionado no header, a listagem carrega todos os agendamentos da clínica.
3. Se um animal for selecionado no header (ex: "Rex"), a listagem filtra automaticamente para mostrar apenas os agendamentos de "Rex".
4. O usuário pode buscar ou filtrar dentro da lista exibida.
5. Para adicionar um novo agendamento, clica em "Novo Agendamento" e o pop-up de cadastro é exibido.

---

### Grupo 2: Cadastro de Agendamento

#### Descrição
O **Grupo de Cadastro de Agendamento** permite registrar um novo agendamento no sistema de forma ágil e estruturada. Implementado como um pop-up para manter o contexto da Página de Agendamentos, o formulário é simples, mas abrangente, capturando informações essenciais para o agendamento.

#### Componentes
- **Formulário de Cadastro:**
  - **Animal:** Dropdown com lista de animais (obrigatório), pré-selecionado se um animal estiver selecionado no header.
  - **Data:** Date picker (obrigatório).
  - **Hora:** Time picker (obrigatório).
  - **Descrição:** Textarea (opcional).
  - **Status:** Dropdown com opções "Agendado", "Concluído", "Cancelado" (obrigatório, padrão "Agendado").
- **Botão "Salvar":** Envia o formulário para a API.
- **Botão "Cancelar":** Fecha o pop-up sem salvar.
- **Mensagens de Erro:** Exibidas abaixo de cada campo em caso de validação falha.

#### Funcionalidades
- **Pré-seleção de Animal:** Se um animal estiver selecionado no header, o campo "Animal" no formulário é pré-preenchido com esse animal.
- **Envio de Dados:** Ao clicar em "Salvar", uma requisição POST é feita para `/api/v1/appointments` com os dados preenchidos.
- **Sucesso:** Após o cadastro, o pop-up é fechado e a listagem é atualizada automaticamente.
- **Erro:** Se houver falhas, mensagens de erro são exibidas em tempo real.
- **Validação:** Implementada no frontend e confirmada no backend.

#### Fluxo de Uso do Usuário
1. Na listagem, o usuário clica em "Novo Agendamento".
2. O pop-up de cadastro é exibido.
3. Se um animal estiver selecionado no header, o campo "Animal" já está preenchido.
4. O usuário preenche os demais dados e clica em "Salvar".
5. Se bem-sucedido, o pop-up fecha e o novo agendamento aparece na listagem.

---

### Grupo 3: Detalhes do Agendamento

#### Descrição
O **Grupo de Detalhes do Agendamento** exibe todas as informações de um agendamento específico, funcionando como ponto de acesso para ações relacionadas. Implementado como um pop-up, ele apresenta dados básicos e opções para editar ou excluir o agendamento.

#### Componentes
- **Card de Dados Básicos:** Exibe Animal, Data, Hora, Descrição e Status.
- **Botões de Ação:**
  - "Editar Agendamento" (abre **Grupo de Edição** em pop-up)
  - "Excluir Agendamento" (abre modal de confirmação)
- **Spinner de Carregamento:** Exibido ao buscar os dados.

#### Funcionalidades
- **Carregamento:** Requisição GET para `/api/v1/appointments/{appointment_id}`.
- **Navegação:** Botões abrem outros pop-ups ou executam ações.
- **Feedback:** Mensagem de sucesso/erro ao carregar dados.

#### Fluxo de Uso do Usuário
1. Na listagem, o usuário clica em "Visualizar" em um agendamento.
2. O pop-up de detalhes abre, mostrando os dados do agendamento.
3. O usuário pode clicar em "Editar Agendamento" ou "Excluir Agendamento".

---

### Grupo 4: Edição de Agendamento

#### Descrição
O **Grupo de Edição de Agendamento** permite atualizar as informações de um agendamento já cadastrado. Implementado como um pop-up, ele é similar ao cadastro, mas com os campos pré-preenchidos, oferecendo uma edição rápida e intuitiva.

#### Componentes
- **Formulário de Edição:** Campos iguais ao cadastro, preenchidos com os dados atuais.
- **Botão "Salvar":** Submete as alterações.
- **Botão "Cancelar":** Fecha o pop-up sem salvar.
- **Validações Visuais:** Mensagens de erro em tempo real.

#### Funcionalidades
- **Atualização:** Requisição PATCH para `/api/v1/appointments/{appointment_id}`.
- **Sucesso:** Fecha o pop-up e atualiza a listagem ou os detalhes.
- **Erro:** Exibe mensagens de validação.

#### Fluxo de Uso do Usuário
1. Nos detalhes de um agendamento, o usuário clica em "Editar Agendamento".
2. O pop-up de edição abre com os dados preenchidos.
3. O usuário atualiza os dados e clica em "Salvar".
4. O pop-up fecha e os dados são refletidos na página.

---

## Página de Consultas

### Grupo 1: Listagem de Consultas

#### Descrição
O **Grupo de Listagem de Consultas** é o ponto de entrada para a gestão de consultas na página. Ele exibe uma lista de consultas, que pode ser geral (todas as consultas da clínica) ou filtrada pelo animal selecionado no header. A interface é projetada para ser funcional, acessível e visualmente atrativa.

#### Componentes
- **Tabela de Consultas:** Uma tabela organizada com colunas para Data, Animal, Descrição e Ações (visualizar, editar, excluir).
- **Campo de Busca:** Um campo de texto para buscar consultas por nome do animal ou descrição.
- **Filtros Avançados:** Dropdowns para filtrar por data ou animal.
- **Botão "Nova Consulta":** Localizado no topo direito, abre o **Grupo de Cadastro** em um pop-up.
- **Paginação:** Exibe 10 consultas por página.
- **Indicador de Carregamento:** Spinner durante o carregamento.

#### Funcionalidades
- **Carregamento Inicial:**
  - Se **nenhum animal estiver selecionado** no header, faz uma requisição GET para `/api/v1/consultations` para listar todas as consultas da clínica.
  - Se **um animal estiver selecionado**, faz uma requisição GET para `/api/v1/consultations?animal_id={selectedAnimal.id}` para listar apenas as consultas do animal selecionado.
- **Busca e Filtro:** Filtragem local ou via API.
- **Ações por Consulta:**
  - **Visualizar:** Abre o **Grupo de Detalhes da Consulta** em um pop-up.
  - **Editar:** Abre o **Grupo de Edição de Consulta** em um pop-up.
  - **Excluir:** Abre um modal de confirmação e envia DELETE para `/api/v1/consultations/{consultation_id}`.

#### Fluxo de Uso do Usuário
1. O usuário acessa a Página de Consultas via navegação no header.
2. Se nenhum animal estiver selecionado, a listagem carrega todas as consultas da clínica.
3. Se um animal for selecionado, a listagem filtra automaticamente para mostrar apenas as consultas desse animal.
4. O usuário pode buscar ou filtrar dentro da lista exibida.
5. Para adicionar uma nova consulta, clica em "Nova Consulta" e o pop-up de cadastro é exibido.

---

### Grupo 2: Cadastro de Consulta

#### Descrição
O **Grupo de Cadastro de Consulta** permite registrar uma nova consulta no sistema. Implementado como um pop-up, o formulário é simples e captura informações essenciais para o histórico veterinário.

#### Componentes
- **Formulário de Cadastro:**
  - **Animal:** Dropdown com lista de animais (obrigatório), pré-selecionado se um animal estiver selecionado no header.
  - **Data:** Date picker (obrigatório).
  - **Descrição:** Textarea (opcional).
- **Botão "Salvar":** Envia o formulário para a API.
- **Botão "Cancelar":** Fecha o pop-up sem salvar.
- **Mensagens de Erro:** Exibidas em caso de validação falha.

#### Funcionalidades
- **Pré-seleção de Animal:** Se um animal estiver selecionado no header, o campo "Animal" é pré-preenchido.
- **Envio de Dados:** POST para `/api/v1/consultations`.
- **Sucesso:** Fecha o pop-up e atualiza a listagem.
- **Erro:** Exibe mensagens de validação.

#### Fluxo de Uso do Usuário
1. Na listagem, o usuário clica em "Nova Consulta".
2. O pop-up de cadastro é exibido, com o animal pré-selecionado se aplicável.
3. O usuário preenche os dados e clica em "Salvar".
4. O pop-up fecha e a nova consulta aparece na listagem.

---

### Grupo 3: Detalhes da Consulta

#### Descrição
O **Grupo de Detalhes da Consulta** exibe todas as informações de uma consulta específica. Implementado como um pop-up, ele apresenta dados básicos e opções para editar ou excluir a consulta.

#### Componentes
- **Card de Dados Básicos:** Exibe Animal, Data e Descrição.
- **Botões de Ação:**
  - "Editar Consulta" (abre **Grupo de Edição** em pop-up)
  - "Excluir Consulta" (abre modal de confirmação)
- **Spinner de Carregamento:** Exibido ao buscar os dados.

#### Funcionalidades
- **Carregamento:** GET para `/api/v1/consultations/{consultation_id}`.
- **Navegação:** Botões abrem outros pop-ups ou executam ações.
- **Feedback:** Mensagem de sucesso/erro ao carregar dados.

#### Fluxo de Uso do Usuário
1. Na listagem, o usuário clica em "Visualizar" em uma consulta.
2. O pop-up de detalhes abre, mostrando os dados da consulta.
3. O usuário pode clicar em "Editar Consulta" ou "Excluir Consulta".

---

### Grupo 4: Edição de Consulta

#### Descrição
O **Grupo de Edição de Consulta** permite atualizar as informações de uma consulta já cadastrada. Implementado como um pop-up, ele é similar ao cadastro, mas com os campos pré-preenchidos.

#### Componentes
- **Formulário de Edição:** Campos iguais ao cadastro, preenchidos com os dados atuais.
- **Botão "Salvar":** Submete as alterações.
- **Botão "Cancelar":** Fecha o pop-up sem salvar.
- **Validações Visuais:** Mensagens de erro em tempo real.

#### Funcionalidades
- **Atualização:** PATCH para `/api/v1/consultations/{consultation_id}`.
- **Sucesso:** Fecha o pop-up e atualiza a listagem ou os detalhes.
- **Erro:** Exibe mensagens de validação.

#### Fluxo de Uso do Usuário
1. Nos detalhes de uma consulta, o usuário clica em "Editar Consulta".
2. O pop-up de edição abre com os dados preenchidos.
3. O usuário atualiza os dados e clica em "Salvar".
4. O pop-up fecha e os dados são refletidos na página.

---

## Estrutura e Navegação
Cada página (Consultas e Agendamentos) é uma página única que contém seus respectivos grupos de funcionalidades, organizados de forma intuitiva:
- **Listagem:** Área principal, sempre visível ao carregar a página.
- **Cadastro, Detalhes, Edição:** Acessados via pop-ups para minimizar navegação e manter o usuário no contexto da gestão de consultas ou agendamentos.

Essa abordagem garante uma experiência fluida, com ações comuns realizadas sem sair da página, utilizando pop-ups para maximizar a usabilidade e a atratividade visual.

---

## Detalhes Técnicos
- **Rotas Backend:**
  - **Agendamentos:**
    - GET `/api/v1/appointments`
    - POST `/api/v1/appointments`
    - GET `/api/v1/appointments/{appointment_id}`
    - PATCH `/api/v1/appointments/{appointment_id}`
    - DELETE `/api/v1/appointments/{appointment_id}`
  - **Consultas:**
    - GET `/api/v1/consultations`
    - POST `/api/v1/consultations`
    - GET `/api/v1/consultations/{consultation_id}`
    - PATCH `/api/v1/consultations/{consultation_id}`
    - DELETE `/api/v1/consultations/{consultation_id}`
- **Autenticação:** Token JWT em todas as requisições.
- **Frontend:** React com React Router, Tailwind CSS para estilização e componentes de pop-up (ex: Modals do Material UI).

---

## Tarefas da Sprint
- Implementar as Páginas de Consultas e Agendamentos com os grupos de funcionalidades.
- Configurar pop-ups para Cadastro, Detalhes e Edição.
- Integrar o estado do header (`selectedAnimal`) para filtrar automaticamente as listagens.
- Testar a navegação, a integração com o backend e a consistência dos estados.