
# Sprint 2: Gestão de Animais - Detalhamento (Versão 2)

Esta sprint foca na implementação das funcionalidades principais para a gestão de animais em uma clínica veterinária. O objetivo é criar um sistema intuitivo e eficiente que permita aos usuários (funcionários da clínica) listar, cadastrar, visualizar, editar e gerenciar preferências alimentares dos animais. Abaixo, detalho cada uma das cinco **grupos de funcionalidades** que compõem a **Página de Animais**, que são áreas distintas interligadas por uma navegação clara dentro da mesma página.

---

## Página de Animais

A **Página de Animais** é composta por cinco grupos de funcionalidades principais, cada um com seu propósito específico, mas todos integrados em uma única página para facilitar a navegação e o uso intuitivo. Esses grupos são:

1. **Grupo 1: Listagem de Animais**
2. **Grupo 2: Cadastro de Animal**
3. **Grupo 3: Detalhes do Animal**
4. **Grupo 4: Edição de Animal**
5. **Grupo 5: Preferências Alimentares**

Esses grupos são organizados de forma atrativa e intuitiva, com algumas funcionalidades, como adicionar e editar, minimizadas em pop-ups para melhorar a experiência do usuário, mantendo o contexto da página sem redirecionamentos desnecessários.

---

## Integração com o Header

O componente `AppHeader` é essencial para a navegação e o controle de estado global da aplicação VeTech, especialmente por meio do dropdown de seleção de animal. No entanto, para a **Página de Animais**, a seleção de animal no header **não afeta** o comportamento desta página, conforme definido na documentação do header (arquivo `HEADER_DOCS-v2.md`). Isso implica que:

- **Visibilidade do Dropdown:** O dropdown de seleção de animal **não será exibido** enquanto o usuário estiver na Página de Animais, pois ela está classificada como uma "tela não afetada" pela seleção de animal (listada em `noAnimalSelectorPages`).
- **Impacto:** A Página de Animais sempre exibe informações gerais de todos os animais da clínica, independentemente de qualquer animal estar selecionado no header.
- **Navegação:** O header continua fornecendo acesso às outras telas do sistema (ex.: Tela Inicial, Tela de Agendamento, etc.), mas sua funcionalidade de estado global (`selectedAnimal`) é irrelevante para esta página.

Essa abordagem garante que a Página de Animais seja independente do estado do header, simplificando a lógica e evitando confusões durante o desenvolvimento e uso.

---

## Grupo 1: Listagem de Animais

### Descrição
O **Grupo de Listagem de Animais** é o ponto de entrada para a gestão de animais na página. Ele exibe uma lista completa de todos os animais cadastrados na clínica, funcionando como um painel de controle central. A interface é projetada para ser funcional, acessível e visualmente atrativa, permitindo ao usuário visualizar rapidamente informações-chave, buscar animais específicos e acessar ações relacionadas (como visualizar detalhes ou cadastrar um novo animal). Ideal para clínicas com grande volume de pacientes, o grupo inclui recursos como busca, filtragem e paginação.

### Componentes
- **Tabela de Animais:** Uma tabela organizada com colunas para Nome, Espécie, Raça, Idade, Peso e Ações (visualizar, editar, excluir).
- **Campo de Busca:** Um campo de texto para buscar animais por nome ou espécie, com filtragem em tempo real.
- **Filtros Avançados:** Dropdowns para filtrar por espécie (ex: "Cachorro", "Gato") ou faixa de idade.
- **Botão "Novo Animal":** Localizado no topo direito, abre o **Grupo de Cadastro** em um pop-up.
- **Paginação:** Exibe 10 animais por página, com controles para navegar entre páginas.
- **Indicador de Carregamento:** Um spinner exibido enquanto a lista é carregada da API.

### Funcionalidades
- **Carregamento Inicial:** Ao acessar a página, uma requisição GET é feita para a rota `/api/v1/animals`, retornando a lista de animais da clínica autenticada.
- **Busca e Filtro:** A busca é processada localmente na tabela ou via API (GET `/api/v1/animals?search={termo}`), dependendo da implementação.
- **Ações por Animal:**
  - **Visualizar:** Abre o **Grupo de Detalhes do Animal** em um pop-up ou expande uma seção na página.
  - **Editar:** Abre o **Grupo de Edição de Animal** em um pop-up.
  - **Excluir:** Abre um modal de confirmação; se confirmado, envia DELETE para `/api/v1/animals/{animal_id}`.
- **Autenticação:** Todas as requisições incluem o token JWT no header `Authorization`.

### Fluxo de Uso do Usuário
1. O usuário acessa a Página de Animais via navegação no header.
2. A listagem carrega, exibindo a tabela com todos os animais.
3. Para encontrar um animal, o usuário digita "Rex" no campo de busca; a tabela é filtrada.
4. Clica em "Visualizar" para abrir os detalhes de "Rex" em um pop-up.
5. Para adicionar um novo animal, clica em "Novo Animal" e o pop-up de cadastro é exibido.

---

## Grupo 2: Cadastro de Animal

### Descrição
O **Grupo de Cadastro de Animal** permite registrar um novo animal no sistema de forma ágil e estruturada. Implementado como um pop-up para minimizar a navegação e manter o contexto da Página de Animais, o formulário é simples, mas abrangente, capturando informações essenciais para o controle veterinário. A interface é intuitiva, com validações claras e feedback visual.

### Componentes
- **Formulário de Cadastro:**
  - Nome (texto, obrigatório)
  - Espécie (dropdown: "Cachorro", "Gato", "Ave", etc., obrigatório)
  - Raça (texto ou dropdown baseado na espécie, opcional)
  - Idade (número, opcional)
  - Peso (número em kg, opcional)
  - Histórico Médico (textarea, opcional)
- **Botão "Salvar":** Envia o formulário para a API.
- **Botão "Cancelar":** Fecha o pop-up sem salvar.
- **Mensagens de Erro:** Exibidas abaixo de cada campo em caso de validação falha.

### Funcionalidades
- **Envio de Dados:** Ao clicar em "Salvar", uma requisição POST é feita para `/api/v1/animals` com os dados preenchidos.
- **Sucesso:** Após o cadastro, o pop-up é fechado e a listagem é atualizada automaticamente.
- **Erro:** Se houver falhas (ex: campo obrigatório vazio), mensagens de erro são exibidas em tempo real.
- **Validação:** Implementada no frontend (ex: React Hook Form) e confirmada no backend.

### Fluxo de Uso do Usuário
1. Na listagem, o usuário clica em "Novo Animal".
2. O pop-up de cadastro é exibido.
3. O usuário preenche os dados (ex: Nome "Luna", Espécie "Gato") e clica em "Salvar".
4. Se bem-sucedido, o pop-up fecha e "Luna" aparece na listagem.
5. Se houver erro, mensagens de validação aparecem no pop-up.

---

## Grupo 3: Detalhes do Animal

### Descrição
O **Grupo de Detalhes do Animal** exibe todas as informações de um animal específico, funcionando como ponto de acesso para ações relacionadas. Implementado como um pop-up ou uma seção expansível na página, ele apresenta dados básicos, preferências alimentares e opções para gerenciar agendamentos, consultas e dietas. A interface é organizada de forma atrativa, com seções claras e botões intuitivos.

### Componentes
- **Card de Dados Básicos:** Exibe Nome, Espécie, Raça, Idade, Peso e Histórico Médico.
- **Seção de Preferências Alimentares:** Mostra listas "Gosta de" e "Não gosta de", com botão "Editar Preferências".
- **Botões de Ação:**
  - "Editar Animal" (abre **Grupo de Edição** em pop-up)
  - "Adicionar Agendamento"
  - "Ver Consultas"
  - "Gerenciar Dietas"
- **Abas de Navegação:** Separadas para "Agendamentos", "Consultas", "Dietas", etc.
- **Spinner de Carregamento:** Exibido ao buscar os dados.

### Funcionalidades
- **Carregamento:** Requisições GET para `/api/v1/animals/{animal_id}` (dados básicos) e `/api/v1/animals/{animal_id}/preferences` (preferências).
- **Navegação:** Botões abrem outros pop-ups ou redirecionam para telas específicas.
- **Feedback:** Mensagem de sucesso/erro ao carregar dados.

### Fluxo de Uso do Usuário
1. Na listagem, o usuário clica em "Visualizar" em "Rex".
2. O pop-up de detalhes abre, mostrando os dados de "Rex".
3. O usuário pode clicar em "Editar Preferências" ou navegar para outras ações.

---

## Grupo 4: Edição de Animal

### Descrição
O **Grupo de Edição de Animal** permite atualizar as informações de um animal já cadastrado. Implementado como um pop-up para manter a fluidez da experiência, ele é similar ao cadastro, mas com os campos pré-preenchidos, oferecendo uma edição rápida e intuitiva.

### Componentes
- **Formulário de Edição:** Campos iguais ao cadastro, preenchidos com os dados atuais.
- **Botão "Salvar":** Submete as alterações.
- **Botão "Cancelar":** Fecha o pop-up sem salvar.
- **Validações Visuais:** Mensagens de erro em tempo real.

### Funcionalidades
- **Atualização:** Requisição PATCH para `/api/v1/animals/{animal_id}` com os dados modificados.
- **Sucesso:** Fecha o pop-up e atualiza a listagem ou os detalhes.
- **Erro:** Exibe mensagens de validação.

### Fluxo de Uso do Usuário
1. Nos detalhes de "Luna", o usuário clica em "Editar Animal".
2. O pop-up de edição abre com os dados preenchidos.
3. O usuário atualiza o peso e clica em "Salvar".
4. O pop-up fecha e os dados são refletidos na página.

---

## Grupo 5: Preferências Alimentares

### Descrição
O **Grupo de Preferências Alimentares** permite gerenciar o que o animal gosta e não gosta de comer. Implementado como um pop-up acessado a partir dos detalhes do animal, ele é simples e focado, com uma interface clara e funcional.

### Componentes
- **Campo "Gosta de":** Lista ou texto para alimentos preferidos.
- **Campo "Não gosta de":** Lista ou texto para alimentos evitados.
- **Botão "Salvar":** Envia as preferências.
- **Botão "Cancelar":** Fecha o pop-up sem salvar.

### Funcionalidades
- **Carregamento:** GET em `/api/v1/animals/{animal_id}/preferences` para dados existentes.
- **Salvamento:** POST (se novo) ou PATCH (se existente) para `/api/v1/animals/{animal_id}/preferences`.
- **Retorno:** Após salvar, o pop-up fecha e os detalhes são atualizados.

### Fluxo de Uso do Usuário
1. Nos detalhes de "Rex", o usuário clica em "Editar Preferências".
2. O pop-up abre com as preferências atuais.
3. O usuário ajusta as preferências e clica em "Salvar".
4. O pop-up fecha e as mudanças aparecem nos detalhes.

---

## Estrutura e Navegação
A **Página de Animais** é uma única página que contém os cinco grupos de funcionalidades, organizados de forma intuitiva:
- **Listagem de Animais:** Área principal, sempre visível ao carregar a página.
- **Cadastro, Detalhes, Edição e Preferências:** Acessados via pop-ups para minimizar navegação e manter o usuário no contexto da gestão de animais.

Essa abordagem garante uma experiência fluida, com ações comuns realizadas sem sair da página, utilizando pop-ups para maximizar a usabilidade e a atratividade visual.

---

## Detalhes Técnicos
- **Rotas Backend:**
  - GET `/api/v1/animals`: Lista todos os animais.
  - POST `/api/v1/animals`: Cadastra um animal.
  - GET `/api/v1/animals/{animal_id}`: Detalhes de um animal.
  - PATCH `/api/v1/animals/{animal_id}`: Edita um animal.
  - DELETE `/api/v1/animals/{animal_id}`: Remove um animal.
  - GET/PATCH `/api/v1/animals/{animal_id}/preferences`: Gerencia preferências.
- **Autenticação:** Token JWT em todas as requisições.
- **Frontend:** React com React Router, componentes de pop-up (ex: Modals do Material UI).

---

## Tarefas da Sprint
- Implementar a Página de Animais com os cinco grupos de funcionalidades.
- Configurar pop-ups para Cadastro, Detalhes, Edição e Preferências.
- Garantir que o header não exiba o dropdown de seleção de animal na Página de Animais.
- Testar a navegação e a integração com o backend.