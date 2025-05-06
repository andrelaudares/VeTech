# Sprint 2: Gestão de Animais - Detalhamento

Esta sprint foca na implementação das funcionalidades principais para a gestão de animais em uma clínica veterinária. O objetivo é criar um sistema intuitivo e eficiente que permita aos usuários (funcionários da clínica) listar, cadastrar, visualizar, editar e gerenciar preferências alimentares dos animais. Abaixo, detalho cada uma das cinco telas propostas, que são páginas distintas interligadas por uma navegação clara, e não apenas seções ou cards dentro de uma única tela.

---

## Tela 1: Listagem de Animais

### Descrição
A Tela de Listagem de Animais é o ponto de entrada para a gestão de animais no sistema. Ela exibe uma lista completa de todos os animais cadastrados na clínica, funcionando como um painel de controle central. A interface é projetada para ser funcional e acessível, permitindo ao usuário visualizar rapidamente informações-chave, buscar animais específicos e acessar ações relacionadas (como visualizar detalhes ou cadastrar um novo animal). Ideal para clínicas com grande volume de pacientes, a tela inclui recursos como busca, filtragem e paginação.

### Componentes
- **Tabela de Animais:** Uma tabela organizada com colunas para Nome, Espécie, Raça, Idade, Peso e Ações (visualizar, editar, excluir).
- **Campo de Busca:** Um campo de texto para buscar animais por nome ou espécie, com filtragem em tempo real.
- **Filtros Avançados:** Dropdowns para filtrar por espécie (ex: "Cachorro", "Gato") ou faixa de idade.
- **Botão "Novo Animal":** Localizado no topo direito, abre a tela de cadastro.
- **Paginação:** Exibe 10 animais por página, com controles para navegar entre páginas.
- **Indicador de Carregamento:** Um spinner exibido enquanto a lista é carregada da API.

### Funcionalidades
- **Carregamento Inicial:** Ao acessar a tela, uma requisição GET é feita para a rota `/api/v1/animals`, retornando a lista de animais da clínica autenticada.
- **Busca e Filtro:** A busca é processada localmente na tabela ou via API (GET `/api/v1/animals?search={termo}`), dependendo da implementação.
- **Ações por Animal:**
  - **Visualizar:** Redireciona para a Tela de Detalhes do Animal.
  - **Editar:** Abre a Tela de Edição de Animal.
  - **Excluir:** Abre um modal de confirmação; se confirmado, envia DELETE para `/api/v1/animals/{animal_id}`.
- **Autenticação:** Todas as requisições incluem o token JWT no header `Authorization`.

### Fluxo de Uso do Usuário
1. O usuário acessa o sistema digitando suas credenciais (email e senha) na tela de login.
2. Caso tenha esquecido a senha, clica em "Recuperar Senha", insere o email e recebe um link de redefinição por email.
3. Após login bem-sucedido, navega até a seção "Animais" no menu lateral.
4. A Tela de Listagem de Animais carrega, exibindo a tabela com todos os animais cadastrados.
5. Para encontrar um animal, o usuário digita "Rex" no campo de busca; a tabela é filtrada para mostrar apenas animais correspondentes.
6. Alternativamente, usa os filtros avançados para listar apenas "Cachorros" com menos de 5 anos.
7. Clica em "Visualizar" na linha de "Rex" para ver mais detalhes.
8. Para adicionar um novo animal, clica em "Novo Animal" e é redirecionado para a Tela de Cadastro.

---

## Tela 2: Cadastro de Animal

### Descrição
A Tela de Cadastro de Animal permite registrar um novo animal no sistema de forma ágil e estruturada. O formulário é simples, mas abrangente, capturando informações essenciais para o controle veterinário. A interface prioriza usabilidade, com campos bem sinalizados, validações em tempo real e feedback claro, garantindo que o usuário insira dados consistentes.

### Componentes
- **Formulário de Cadastro:**
  - Nome (texto, obrigatório)
  - Espécie (dropdown: "Cachorro", "Gato", "Ave", etc., obrigatório)
  - Raça (texto ou dropdown baseado na espécie, opcional)
  - Idade (número, opcional)
  - Peso (número em kg, opcional)
  - Histórico Médico (textarea, opcional)
- **Botão "Salvar":** Envia o formulário para a API.
- **Botão "Cancelar":** Retorna à Tela de Listagem sem salvar.
- **Mensagens de Erro:** Exibidas abaixo de cada campo em caso de validação falha.

### Funcionalidades
- **Envio de Dados:** Ao clicar em "Salvar", uma requisição POST é feita para `/api/v1/animals` com os dados preenchidos.
- **Sucesso:** Após o cadastro, o usuário é redirecionado para a Tela de Detalhes do novo animal.
- **Erro:** Se houver falhas (ex: campo obrigatório vazio), mensagens de erro são exibidas em tempo real.
- **Validação:** Implementada no frontend (ex: React Hook Form) e confirmada no backend.

### Fluxo de Uso do Usuário
1. Na Tela de Listagem, o usuário clica em "Novo Animal".
2. A Tela de Cadastro é exibida, com o formulário vazio.
3. O usuário preenche: Nome ("Luna"), Espécie ("Gato"), Raça ("Siamês"), Idade (2), Peso (4.5), Histórico Médico ("Vacinas em dia").
4. Clica em "Salvar"; um spinner aparece enquanto a requisição é processada.
5. Se bem-sucedido, é redirecionado para a Tela de Detalhes de "Luna".
6. Se digitar uma idade inválida (ex: "abc"), uma mensagem de erro aparece: "Idade deve ser um número".
7. Caso desista, clica em "Cancelar" e retorna à Listagem.

---

## Tela 3: Detalhes do Animal

### Descrição
A Tela de Detalhes do Animal é um hub centralizado que exibe todas as informações de um animal específico, funcionando como ponto de acesso para ações relacionadas. Ela apresenta dados básicos, preferências alimentares e opções para gerenciar agendamentos, consultas e dietas. A interface é dividida em seções visuais (cards ou abas), oferecendo clareza e facilidade de navegação.

### Componentes
- **Card de Dados Básicos:** Exibe Nome, Espécie, Raça, Idade, Peso e Histórico Médico.
- **Seção de Preferências Alimentares:** Mostra listas "Gosta de" e "Não gosta de", com botão "Editar Preferências".
- **Botões de Ação:**
  - "Editar Animal" (abre Tela de Edição)
  - "Adicionar Agendamento"
  - "Ver Consultas"
  - "Gerenciar Dietas"
- **Abas de Navegação:** Separadas para "Agendamentos", "Consultas", "Dietas", etc.
- **Spinner de Carregamento:** Exibido ao buscar os dados.

### Funcionalidades
- **Carregamento:** Requisições GET para `/api/v1/animals/{animal_id}` (dados básicos) e `/api/v1/animals/{animal_id}/preferences` (preferências).
- **Navegação:** Botões redirecionam para telas específicas (ex: "Editar Animal" para Tela de Edição).
- **Feedback:** Mensagem de sucesso/erro ao carregar dados (ex: "Animal não encontrado").

### Fluxo de Uso do Usuário
1. Na Tela de Listagem, o usuário clica em "Visualizar" no animal "Rex".
2. A Tela de Detalhes carrega, mostrando o card com Nome ("Rex"), Espécie ("Cachorro"), etc.
3. Na seção de preferências, vê "Gosta de: Ração Premium" e "Não gosta de: Vegetais".
4. Clica em "Editar Preferências" para ajustar as preferências alimentares.
5. Clica em "Editar Animal" para atualizar o peso de "Rex".
6. Navega para a aba "Consultas" para ver o histórico de visitas.
7. Clica em "Adicionar Agendamento" para marcar uma consulta futura.

---

## Tela 4: Edição de Animal

### Descrição
A Tela de Edição de Animal permite atualizar as informações de um animal já cadastrado. Similar à Tela de Cadastro, mas com os campos pré-preenchidos, ela é otimizada para edições rápidas e precisas. A interface mantém consistência visual com o cadastro, facilitando o aprendizado do usuário.

### Componentes
- **Formulário de Edição:** Campos iguais ao cadastro, mas preenchidos com os dados atuais.
- **Botão "Salvar":** Submete as alterações.
- **Botão "Cancelar":** Retorna à Tela de Detalhes sem salvar.
- **Validações Visuais:** Mensagens de erro em tempo real.

### Funcionalidades
- **Atualização:** Requisição PATCH para `/api/v1/animals/{animal_id}` com os dados modificados.
- **Sucesso:** Redireciona para a Tela de Detalhes com os dados atualizados.
- **Erro:** Exibe mensagens de validação (ex: "Peso inválido").

### Fluxo de Uso do Usuário
1. Na Tela de Detalhes de "Luna", o usuário clica em "Editar Animal".
2. A Tela de Edição aparece com os campos preenchidos (ex: Peso = 4.5).
3. Atualiza o peso para 5.0 e adiciona "Castrada" ao Histórico Médico.
4. Clica em "Salvar"; após sucesso, volta à Tela de Detalhes com as mudanças refletidas.
5. Se tentar salvar com erro (ex: peso negativo), vê uma mensagem de validação.
6. Clica em "Cancelar" para descartar as alterações.

---

## Tela 5: Preferências Alimentares

### Descrição
A Tela de Preferências Alimentares (ou modal) permite gerenciar o que o animal gosta e não gosta de comer. É uma interface simples e focada, acessada a partir da Tela de Detalhes, com campos editáveis para personalizar as preferências. Pode ser implementada como tela separada ou modal, dependendo do design final.

### Componentes
- **Campo "Gosta de":** Lista ou texto para alimentos preferidos.
- **Campo "Não gosta de":** Lista ou texto para alimentos evitados.
- **Botão "Salvar":** Envia as preferências.
- **Botão "Cancelar":** Fecha a tela/modal sem salvar.

### Funcionalidades
- **Carregamento:** GET em `/api/v1/animals/{animal_id}/preferences` para dados existentes.
- **Salvamento:** POST (se novo) ou PATCH (se existente) para `/api/v1/animals/{animal_id}/preferences`.
- **Retorno:** Após salvar, volta à Tela de Detalhes com as preferências atualizadas.

### Fluxo de Uso do Usuário
1. Na Tela de Detalhes de "Rex", o usuário clica em "Editar Preferências".
2. A tela (ou modal) abre, mostrando "Gosta de: Ração Premium" e "Não gosta de: Vegetais".
3. Adiciona "Frango" a "Gosta de" e remove "Vegetais" de "Não gosta de".
4. Clica em "Salvar"; as preferências são atualizadas e exibidas na Tela de Detalhes.
5. Se desistir, clica em "Cancelar" para voltar sem alterações.

---

## Estrutura e Navegação
As cinco telas são páginas distintas, não apenas seções dentro de uma única "Tela de Animais". Elas se conectam por uma navegação intuitiva:
- **Listagem de Animais:** Tela inicial, acessa Cadastro e Detalhes.
- **Cadastro de Animal:** Acessada via "Novo Animal" na Listagem.
- **Detalhes do Animal:** Acessada via "Visualizar" na Listagem, conecta a Edição e Preferências.
- **Edição de Animal:** Acessada via "Editar Animal" nos Detalhes.
- **Preferências Alimentares:** Acessada via "Editar Preferências" nos Detalhes.

Essa separação garante clareza e evita sobrecarga de informações, com cada tela tendo um propósito específico.

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
- **Frontend:** React com React Router para navegação e Tailwind CSS para estilização.

---

## Tarefas da Sprint
- Implementar tabela reutilizável para Listagem.
- Criar formulários validados para Cadastro e Edição.
- Desenvolver Tela de Detalhes com abas e ações.
- Configurar gerenciamento de Preferências (tela ou modal).
- Testar navegação e integração com backend.

---

Essa versão detalhada da Sprint 2 reflete as melhorias solicitadas. Para avançar para a Sprint 3, podemos incluir funcionalidades como agendamentos ou consultas. O que acha?