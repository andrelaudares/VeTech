# Sprint 3: Consultas e Agendamentos - Detalhamento Revisado

Esta sprint foca na implementação das funcionalidades principais para a gestão de consultas e agendamentos em uma clínica veterinária. O objetivo é criar um sistema intuitivo, eficiente e robusto que permita aos usuários (funcionários da clínica) listar, cadastrar, visualizar, editar e gerenciar consultas e agendamentos dos animais de forma fluida. Abaixo, detalho cada uma das oito telas propostas, que são páginas distintas interligadas por uma navegação clara e lógica, e não apenas seções, cards ou grupos dentro de uma única "Tela de agendamentos e consultas". Cada tela foi projetada com um propósito específico, garantindo uma experiência de uso otimizada e evitando sobrecarga de informações.

**Nova Feature:** A partir desta sprint, todas as telas incluem um **dropdown de busca de animais** posicionado no topo da página. Esse componente permite que o usuário selecione rapidamente um animal específico para visualizar ou gerenciar suas informações, um recurso essencial para clínicas com múltiplos pacientes cadastrados. A troca de animal no dropdown atualiza dinamicamente o conteúdo da tela, mantendo o contexto claro e agilizando o acesso às informações.

---

## Tela 0: Listagem de Dietas por Animal

### Descrição
A Tela de Listagem de Dietas por Animal é a porta de entrada para o módulo de consultas e agendamentos, funcionando como um painel de controle centralizado. Esta página independente apresenta uma visão geral dos agendamentos e consultas associadas a um animal específico, permitindo a clinica relate as consultas e faça agendamentos , aplicar filtros e realizar ações rápidas, como visualizar detalhes ou cadastrar novos agendamentos e consultas. Projetada para ser prática e eficiente, ela suporta o dia a dia de clínicas que precisam gerenciar múltiplas consultas e agendamentos com agilidade, oferecendo uma interface limpa e interativa.

### Componentes
- **Dropdown de Busca de Animais:** Localizado no topo da página, exibe uma lista de animais cadastrados e permite busca por nome em tempo real.
- **Tabela de Dietas:** Uma tabela responsiva com colunas configuráveis, incluindo:
  - **Tipo:** Exibe "Caseira", "Industrializada", etc.
  - **Objetivo:** Mostra "Emagrecimento", "Ganho de Peso", etc.
  - **Data de Início:** Formato DD/MM/AAAA.
  - **Data de Fim:** Formato DD/MM/AAAA ou "Em andamento" se não definida.
  - **Status:** Indicadores visuais como "Ativa" (verde) ou "Finalizada" (cinza).
  - **Ações:** Botões para "Visualizar", "Editar" e "Excluir".
- **Campo de Busca:** Pesquisa textual em tempo real por tipo ou objetivo.
- **Filtros Avançados:** Dropdowns para status (ex: "Ativa", "Finalizada") e intervalo de datas.
- **Botão "Nova Dieta":** Posicionado no canto superior direito, leva à Tela de Cadastro de Dieta.
- **Paginação:** Exibe até 10 dietas por página, com controles de navegação.
- **Indicador de Carregamento:** Um spinner aparece durante o carregamento de dados.

### Funcionalidades
- **Seleção de Animal:** O dropdown consome a API GET `/api/v1/animals` para listar animais e, ao selecionar um, carrega as dietas via GET `/api/v1/animals/{animal_id}/diets`.
- **Carregamento Inicial:** Exibe as dietas do animal selecionado automaticamente ao acessar a tela.
- **Busca e Filtro:** Suporta filtragem local ou via API (ex: GET `/api/v1/animals/{animal_id}/diets?status=ativa`).
- **Ações por Dieta:**
  - **Visualizar:** Redireciona para a Tela de Detalhes da Dieta.
  - **Editar:** Abre a Tela de Edição de Dieta (reutiliza o formulário de cadastro com dados preenchidos).
  - **Excluir:** Exibe um modal de confirmação antes de enviar DELETE para `/api/v1/diets/{diet_id}`.
- **Autenticação:** Todas as requisições incluem um token JWT no cabeçalho.

### Fluxo de Uso do Usuário
1. O usuário acessa o sistema digitando email e senha na tela de login.
2. Caso tenha esquecido a senha, clica em "Recuperar Senha", insere o email, recebe um link por email e redefine a senha.
3. Após o login, no menu lateral, clica em "Dietas" para carregar a Tela de Listagem de Dietas por Animal.
4. No dropdown de busca, digita "Rex" e seleciona o animal na lista suspensa.
5. A tabela carrega automaticamente as dietas associadas a "Rex", como "Dieta Caseira" (Objetivo: "Emagrecimento", Status: "Ativa").
6. O usuário aplica o filtro "Ativa" no dropdown de status para listar apenas dietas em andamento.
7. Clica em "Visualizar" em uma dieta para acessar seus detalhes ou em "Nova Dieta" para criar um novo plano.


---

## Tela 1: Listagem de Agendamentos

### Descrição
A Tela de Listagem de Agendamentos é o ponto de partida para a gestão de agendamentos no sistema. Trata-se de uma página independente que funciona como um painel de controle central, exibindo uma visão geral de todos os agendamentos registrados na clínica. Projetada para atender clínicas com alto volume de pacientes, esta tela oferece uma interface limpa e funcional, permitindo ao usuário visualizar rapidamente informações essenciais, realizar buscas, aplicar filtros e acessar ações relacionadas (como visualizar detalhes ou cadastrar novos agendamentos). A ênfase está na usabilidade, com uma tabela interativa e ferramentas de navegação que tornam a gestão diária mais eficiente.

### Componentes
- **Tabela de Agendamentos:** Uma tabela estruturada com colunas para Data, Hora, Animal, Descrição, Status (ex: "Agendado", "Concluído", "Cancelado") e Ações (visualizar, editar, excluir).
- **Campo de Busca:** Um campo de texto no topo da tabela para buscar agendamentos por nome do animal ou descrição, com filtragem dinâmica em tempo real.
- **Filtros Avançados:** Dropdowns para filtrar por status (ex: "Agendado") ou intervalo de datas, com opção de reset.
- **Botão "Novo Agendamento":** Posicionado no canto superior direito, destacado visualmente, redireciona para a Tela de Cadastro.
- **Paginação:** Exibe 10 agendamentos por página, com botões de navegação (anterior/próximo) e indicação da página atual (ex: "Página 1 de 5").
- **Indicador de Carregamento:** Um spinner centralizado exibido durante o carregamento inicial ou ao aplicar filtros/buscas.

### Funcionalidades
- **Carregamento Inicial:** Ao acessar a tela, uma requisição GET é enviada para `/api/v1/appointments`, retornando a lista completa de agendamentos associados à clínica autenticada.
- **Busca e Filtro:** A busca pode ser processada localmente na tabela (para respostas rápidas) ou via API com parâmetros (ex: GET `/api/v1/appointments?search={termo}`), dependendo do volume de dados.
- **Ações por Agendamento:**
  - **Visualizar:** Redireciona para a Tela de Detalhes do Agendamento.
  - **Editar:** Abre a Tela de Edição de Agendamento.
  - **Excluir:** Exibe um modal de confirmação; se confirmado, envia DELETE para `/api/v1/appointments/{appointment_id}` e atualiza a tabela.
- **Autenticação:** Todas as requisições incluem o token JWT no header `Authorization` para garantir segurança e acesso restrito.

### Fluxo de Uso do Usuário
1. O usuário acessa o sistema pela tela de login, inserindo email e senha válidos.
2. Se esqueceu a senha, clica em "Recuperar Senha", insere o email, recebe um link de redefinição por email e redefine a senha.
3. Após login, no menu lateral, seleciona "Agendamentos", carregando a Tela de Listagem de Agendamentos.
4. A tabela exibe todos os agendamentos cadastrados; o usuário digita "Rex" no campo de busca, e a tabela filtra para mostrar apenas os agendamentos de "Rex".
5. Alternativamente, seleciona "Agendado" no filtro de status para ver apenas agendamentos pendentes.
6. Clica em "Visualizar" na linha de um agendamento para acessar seus detalhes.
7. Para adicionar um novo agendamento, clica em "Novo Agendamento" e é levado à Tela de Cadastro.
8. Se a API demora a responder, o spinner mantém o usuário informado do carregamento.

---

## Tela 2: Cadastro de Agendamento

### Descrição
A Tela de Cadastro de Agendamento é uma página dedicada ao registro de novos agendamentos, projetada para ser rápida, intuitiva e confiável. O formulário é estruturado para capturar informações essenciais de maneira clara, com campos bem definidos e validações visíveis que orientam o usuário durante o preenchimento. Esta tela é ideal para recepcionistas ou veterinários que precisam agendar consultas ou procedimentos com agilidade, oferecendo feedback imediato e uma experiência sem frustrações.

### Componentes
- **Formulário de Cadastro:**
  - **Animal:** Dropdown com lista de animais cadastrados (obrigatório), com busca incremental por nome.
  - **Data:** Date picker com calendário interativo (obrigatório), restringindo datas passadas.
  - **Hora:** Time picker com intervalos de 15 minutos (obrigatório).
  - **Descrição:** Textarea para detalhes do agendamento (opcional), com limite de 500 caracteres.
  - **Status:** Dropdown com opções "Agendado", "Concluído" ou "Cancelado" (obrigatório, padrão "Agendado").
- **Botão "Salvar":** No canto inferior direito, envia o formulário à API.
- **Botão "Cancelar":** Ao lado de "Salvar", retorna à Tela de Listagem sem salvar.
- **Mensagens de Erro:** Exibidas em vermelho abaixo de cada campo em caso de validação falha (ex: "Campo obrigatório").

### Funcionalidades
- **Envio de Dados:** Ao clicar em "Salvar", uma requisição POST é enviada para `/api/v1/appointments` com os dados do formulário em formato JSON.
- **Sucesso:** Após confirmação do backend, o usuário é redirecionado para a Tela de Detalhes do novo agendamento.
- **Erro:** Se houver falhas (ex: data inválida ou animal não selecionado), mensagens de erro aparecem instantaneamente.
- **Validação:** Validações no frontend (ex: React Hook Form) e no backend garantem consistência dos dados.

### Fluxo de Uso do Usuário
1. Na Tela de Listagem, o usuário clica em "Novo Agendamento".
2. A Tela de Cadastro carrega com o formulário vazio.
3. Seleciona "Luna" no dropdown de animais, escolhe "2023-10-26" no date picker, define "10:00" no time picker, adiciona "Consulta de rotina" na descrição e mantém "Agendado" no status.
4. Clica em "Salvar"; um spinner aparece durante o processamento.
5. Se bem-sucedido, é redirecionado para a Tela de Detalhes do agendamento de "Luna".
6. Se deixa o campo "Animal" vazio e tenta salvar, vê "Campo obrigatório" em vermelho.
7. Caso desista, clica em "Cancelar" e volta à Listagem.

---

## Tela 3: Detalhes do Agendamento

### Descrição
A Tela de Detalhes do Agendamento é uma página central que exibe todas as informações de um agendamento específico, funcionando como um hub para ações relacionadas. Projetada para oferecer uma visão completa e organizada, ela apresenta os dados em seções visuais distintas (como cards ou abas), permitindo ao usuário consultar informações rapidamente e decidir os próximos passos (editar, excluir ou navegar para outras áreas). É ideal para revisões detalhadas ou tomadas de decisão baseadas no histórico do animal.

### Componentes
- **Card de Dados Básicos:** Exibe Animal, Data, Hora, Descrição e Status em um layout claro e legível.
- **Botões de Ação:**
  - "Editar Agendamento": Abre a Tela de Edição.
  - "Excluir Agendamento": Aciona um modal de confirmação.
- **Abas de Navegação:** Separadas para "Consultas", "Dietas" e outras áreas relacionadas ao animal.
- **Spinner de Carregamento:** Aparece enquanto os dados são buscados.

### Funcionalidades
- **Carregamento:** Requisição GET para `/api/v1/appointments/{appointment_id}` carrega os dados do agendamento.
- **Navegação:** Botões redirecionam para telas específicas (ex: "Editar" para Tela de Edição).
- **Feedback:** Exibe mensagens como "Agendamento não encontrado" em caso de erro.

### Fluxo de Uso do Usuário
1. Na Tela de Listagem, o usuário clica em "Visualizar" no agendamento de "Rex".
2. A Tela de Detalhes carrega, exibindo o card com Animal ("Rex"), Data ("2023-10-26"), Hora ("14:00"), etc.
3. Clica em "Editar Agendamento" para ajustar a hora.
4. Clica em "Excluir Agendamento", confirma no modal e o agendamento é removido.
5. Navega para a aba "Consultas" para verificar o histórico de "Rex".
6. Se a API falhar, uma mensagem de erro aparece, sugerindo tentar novamente.

---

## Tela 4: Edição de Agendamento

### Descrição
A Tela de Edição de Agendamento é uma página dedicada à atualização de agendamentos existentes, oferecendo uma interface familiar e consistente com a Tela de Cadastro. Os campos são pré-preenchidos com os dados atuais, permitindo ajustes rápidos e precisos. A tela é otimizada para correções ou mudanças de última hora, com validações que asseguram a integridade dos dados antes de salvar.

### Componentes
- **Formulário de Edição:** Mesmos campos do cadastro (Animal, Data, Hora, Descrição, Status), pré-preenchidos.
- **Botão "Salvar":** Submete as alterações à API.
- **Botão "Cancelar":** Retorna à Tela de Detalhes sem salvar.
- **Validações Visuais:** Mensagens de erro em tempo real (ex: "Hora inválida").

### Funcionalidades
- **Atualização:** Requisição PATCH para `/api/v1/appointments/{appointment_id}` com os dados modificados.
- **Sucesso:** Redireciona para a Tela de Detalhes com as alterações refletidas.
- **Erro:** Exibe mensagens como "Data inválida" se houver problemas.

### Fluxo de Uso do Usuário
1. Na Tela de Detalhes de "Luna", o usuário clica em "Editar Agendamento".
2. A Tela de Edição carrega com os dados atuais (ex: Data = "2023-10-26", Hora = "10:00").
3. Altera a hora para "11:00" e a descrição para "Consulta de emergência".
4. Clica em "Salvar"; após sucesso, volta à Tela de Detalhes atualizada.
5. Se insere uma data passada inválida, vê "Data deve ser futura".
6. Clica em "Cancelar" para descartar as mudanças.

---

## Tela 5: Listagem de Consultas

### Descrição
A Tela de Listagem de Consultas é uma página independente que serve como o núcleo da gestão de consultas, exibindo uma visão geral de todas as consultas registradas. Similar à Listagem de Agendamentos, mas focada em consultas, ela oferece uma tabela interativa com busca, filtros e ações, sendo essencial para o acompanhamento do histórico clínico dos animais. A interface é projetada para facilitar a identificação de consultas específicas e o acesso a detalhes ou edições.

### Componentes
- **Tabela de Consultas:** Colunas para Data, Animal, Descrição e Ações (visualizar, editar, excluir).
- **Campo de Busca:** Filtra consultas por animal ou descrição em tempo real.
- **Filtros Avançados:** Dropdowns para filtrar por data ou animal.
- **Botão "Nova Consulta":** No topo direito, leva à Tela de Cadastro.
- **Paginação:** 10 consultas por página, com navegação.
- **Indicador de Carregamento:** Spinner durante o carregamento.

### Funcionalidades
- **Carregamento Inicial:** Requisição GET para `/api/v1/consultations` retorna a lista de consultas.
- **Busca e Filtro:** GET `/api/v1/consultations?search={termo}` ou filtragem local.
- **Ações por Consulta:**
  - **Visualizar:** Abre a Tela de Detalhes da Consulta.
  - **Editar:** Abre a Tela de Edição de Consulta.
  - **Excluir:** Modal de confirmação seguido de DELETE para `/api/v1/consultations/{consultation_id}`.

### Fluxo de Uso do Usuário
1. Após login, o usuário seleciona "Consultas" no menu lateral.
2. A Tela de Listagem carrega com todas as consultas.
3. Digita "Luna" no campo de busca; a tabela mostra apenas consultas de "Luna".
4. Filtra por "2023-10" para ver consultas do mês.
5. Clica em "Visualizar" na linha de "Luna" para ver detalhes.
6. Clica em "Nova Consulta" para adicionar uma nova entrada.

---

## Tela 6: Cadastro de Consulta

### Descrição
A Tela de Cadastro de Consulta é uma página focada no registro de novas consultas, projetada para ser simples e eficaz. O formulário captura informações cruciais para o histórico veterinário, com uma interface que guia o usuário e minimiza erros. É perfeita para veterinários que precisam documentar atendimentos rapidamente após uma consulta.

### Componentes
- **Formulário de Cadastro:**
  - **Animal:** Dropdown com busca (obrigatório).
  - **Data:** Date picker (obrigatório).
  - **Descrição:** Textarea (opcional).
- **Botão "Salvar":** Envia os dados.
- **Botão "Cancelar":** Volta à Listagem.
- **Mensagens de Erro:** Abaixo dos campos.

### Funcionalidades
- **Envio de Dados:** POST para `/api/v1/consultations`.
- **Sucesso:** Redireciona para a Tela de Detalhes da Consulta.
- **Erro:** Exibe validações como "Data obrigatória".

### Fluxo de Uso do Usuário
1. Na Listagem, clica em "Nova Consulta".
2. Preenche: Animal ("Rex"), Data ("2023-10-26"), Descrição ("Vacinação").
3. Clica em "Salvar" e vai para os Detalhes.
4. Se esquece a data, vê um erro ao tentar salvar.
5. Clica em "Cancelar" para desistir.

---

## Tela 7: Detalhes da Consulta

### Descrição
A Tela de Detalhes da Consulta é uma página que exibe informações completas de uma consulta específica, servindo como ponto de referência para revisões ou ações adicionais. Organizada em seções visuais, ela facilita a consulta de dados e a navegação para áreas relacionadas, como agendamentos do mesmo animal.

### Componentes
- **Card de Dados Básicos:** Animal, Data, Descrição.
- **Botões de Ação:** "Editar Consulta", "Excluir Consulta".
- **Abas de Navegação:** "Agendamentos", "Dietas", etc.
- **Spinner de Carregamento:** Durante a busca.

### Funcionalidades
- **Carregamento:** GET para `/api/v1/consultations/{consultation_id}`.
- **Navegação:** Botões levam a telas específicas.
- **Feedback:** Mensagens de erro se aplicável.

### Fluxo de Uso do Usuário
1. Na Listagem, clica em "Visualizar" na consulta de "Rex".
2. Vê os detalhes: Animal ("Rex"), Data ("2023-10-26").
3. Clica em "Editar Consulta" para ajustar a descrição.
4. Exclui a consulta após confirmação no modal.
5. Navega para "Agendamentos" na aba.

---

## Tela 8: Edição de Consulta

### Descrição
A Tela de Edição de Consulta permite atualizar informações de consultas existentes, com uma interface consistente e prática. Pré-preenchida, ela suporta edições rápidas com validações que garantem dados corretos.

### Componentes
- **Formulário de Edição:** Animal, Data, Descrição (pré-preenchidos).
- **Botão "Salvar":** Submete alterações.
- **Botão "Cancelar":** Volta aos Detalhes.
- **Validações Visuais:** Erros em tempo real.

### Funcionalidades
- **Atualização:** PATCH para `/api/v1/consultations/{consultation_id}`.
- **Sucesso:** Volta aos Detalhes atualizados.
- **Erro:** Mensagens de validação.

### Fluxo de Uso do Usuário
1. Nos Detalhes de "Luna", clica em "Editar Consulta".
2. Altera a descrição para "Check-up atualizado".
3. Salva e retorna aos Detalhes.
4. Se insere data inválida, vê erro.
5. Cancela para descartar mudanças.

---

## Estrutura e Navegação
As oito telas são páginas distintas, não seções dentro de uma única "Tela de Animais". Elas formam um fluxo intuitivo:
- **Listagem de Agendamentos → Cadastro → Detalhes → Edição.**
- **Listagem de Consultas → Cadastro → Detalhes → Edição.**
A navegação ocorre via menu lateral e botões contextuais, mantendo cada funcionalidade separada e clara.

---

## Detalhes Técnicos
- **Rotas Backend:**
  - GET `/api/v1/appointments`
  - POST `/api/v1/appointments`
  - GET `/api/v1/appointments/{appointment_id}`
  - PATCH `/api/v1/appointments/{appointment_id}`
  - DELETE `/api/v1/appointments/{appointment_id}`
  - GET `/api/v1/consultations`
  - POST `/api/v1/consultations`
  - GET `/api/v1/consultations/{consultation_id}`
  - PATCH `/api/v1/consultations/{consultation_id}`
  - DELETE `/api/v1/consultations/{consultation_id}`
- **Autenticação:** Token JWT em todas as requisições.
- **Frontend:** React, React Router, Tailwind CSS.

---

## Tarefas da Sprint
- Criar tabelas reutilizáveis para Listagem.
- Desenvolver formulários validados para Cadastro/Edição.
- Implementar Telas de Detalhes com abas.
- Testar integração com backend e navegação.
