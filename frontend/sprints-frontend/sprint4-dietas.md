# Sprint 4: Nutrição e Dietas - Detalhamento Revisado e Ampliado

Esta sprint foca na construção de um módulo completo e robusto para a gestão de nutrição e dietas em uma clínica veterinária, oferecendo uma experiência fluida e intuitiva para os usuários (funcionários da clínica, como veterinários e nutricionistas). O objetivo é permitir o gerenciamento eficiente de planos de dieta, alimentos, restrições e snacks para os animais atendidos, com telas bem definidas que atendam a propósitos específicos. São implementadas **oito telas distintas**, cada uma como uma página independente no sistema, interligadas por uma navegação lógica e acessível, e não como seções, cards ou grupos dentro de uma única "Tela de Dieta". Este design garante clareza, evita sobrecarga de informações e suporta o fluxo de trabalho da clínica de maneira organizada.

**Nova Feature:** A partir desta sprint, todas as telas incluem um **dropdown de busca de animais** posicionado no topo da página. Esse componente permite que o usuário selecione rapidamente um animal específico para visualizar ou gerenciar suas informações, um recurso essencial para clínicas com múltiplos pacientes cadastrados. A troca de animal no dropdown atualiza dinamicamente o conteúdo da tela, mantendo o contexto claro e agilizando o acesso às informações.

---

## Tela 0.1: Listagem de Dietas por Animal

### Descrição
A Tela de Listagem de Dietas por Animal é a porta de entrada para o módulo de nutrição, funcionando como um painel de controle centralizado. Esta página independente apresenta uma visão geral das dietas associadas a um animal específico, permitindo ao usuário monitorar planos alimentares ativos ou finalizados, aplicar filtros e realizar ações rápidas, como visualizar detalhes ou cadastrar novas dietas. Projetada para ser prática e eficiente, ela suporta o dia a dia de clínicas que precisam gerenciar múltiplas dietas com agilidade, oferecendo uma interface limpa e interativa.

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

## Tela 2: Cadastro de Dieta

### Descrição
A Tela de Cadastro de Dieta é uma página dedicada à criação de novos planos alimentares para um animal, projetada para ser intuitiva e guiar o usuário no preenchimento de informações essenciais. Com um formulário estruturado e validações claras, ela permite que veterinários ou nutricionistas registrem dietas personalizadas de forma rápida e precisa, minimizando erros e oferecendo feedback imediato. Esta tela é ideal para iniciar um novo acompanhamento nutricional, com foco na usabilidade e na captura de dados relevantes.

### Componentes
- **Dropdown de Busca de Animais:** No topo, pré-selecionado se o usuário veio da Listagem com um animal já escolhido.
- **Formulário de Cadastro:**
  - **Tipo:** Dropdown com opções como "Caseira", "Industrializada", "Mista" (campo obrigatório).
  - **Objetivo:** Dropdown com "Emagrecimento", "Ganho de Peso", "Manutenção" (obrigatório).
  - **Data de Início:** Campo de data com seletor (formato DD/MM/AAAA, obrigatório).
  - **Data de Fim:** Campo de data opcional (formato DD/MM/AAAA).
  - **Status:** Dropdown com "Ativa" ou "Finalizada" (obrigatório, padrão "Ativa").
- **Botão "Salvar":** Envia o formulário para o backend.
- **Botão "Cancelar":** Retorna à Tela de Listagem sem salvar.
- **Mensagens de Erro:** Exibidas abaixo dos campos em vermelho (ex: "Campo Tipo é obrigatório").

### Funcionalidades
- **Envio de Dados:** Envia um POST para `/api/v1/animals/{animal_id}/diets` com os dados preenchidos.
- **Sucesso:** Após o cadastro, redireciona para a Tela de Detalhes da Dieta recém-criada.
- **Erro:** Exibe mensagens de validação, como "Campo obrigatório" ou "Data inválida".
- **Validação no Frontend:** Verifica campos obrigatórios antes do envio.

### Fluxo de Uso do Usuário
1. Na Tela de Listagem, o usuário seleciona "Rex" no dropdown e clica em "Nova Dieta".
2. A tela de cadastro carrega com "Rex" pré-selecionado no dropdown.
3. O usuário escolhe Tipo ("Caseira"), Objetivo ("Emagrecimento"), Data de Início ("26/10/2023"), deixa Data de Fim em branco e define Status como "Ativa".
4. Clica em "Salvar"; o sistema valida os dados e, se bem-sucedido, redireciona para os Detalhes da Dieta.
5. Se esquece de preencher o Tipo, uma mensagem de erro aparece: "Campo Tipo é obrigatório".
6. Clica em "Cancelar" para voltar à Listagem sem salvar alterações.

---

## Tela 3: Detalhes da Dieta

### Descrição
A Tela de Detalhes da Dieta é uma página central que exibe todas as informações de um plano alimentar específico, funcionando como um hub para ações relacionadas. Com uma interface dividida em seções visuais claras, ela oferece uma visão detalhada da dieta (como tipo, objetivo e datas) e lista suas opções associadas, permitindo ao usuário consultar rapidamente o plano e decidir os próximos passos, como editar ou adicionar componentes. Esta tela é essencial para revisões aprofundadas e ajustes, proporcionando uma experiência rica e organizada.

### Componentes
- **Dropdown de Busca de Animais:** No topo, permite alternar entre animais sem sair da tela.
- **Card de Dados da Dieta:** Exibe Tipo, Objetivo, Data de Início, Data de Fim e Status em um layout destacado.
- **Lista de Opções de Dieta:** Uma tabela com colunas como Nome, Valor Mensal, Calorias Totais e ações (ex: "Editar", "Excluir"), com um botão "Adicionar Opção" acima.
- **Botões de Ação:** "Editar Dieta" (leva à edição) e "Excluir Dieta" (modal de confirmação).
- **Abas de Navegação:** Links para "Alimentos", "Restrições" e "Snacks", integrados ao contexto da dieta.
- **Spinner de Carregamento:** Aparece enquanto os dados são buscados.

### Funcionalidades
- **Carregamento:** Consome GET `/api/v1/diets/{diet_id}` para os dados da dieta e GET `/api/v1/diets/{diet_id}/options` para as opções.
- **Navegação:** Os botões e abas redirecionam para telas específicas.
- **Feedback:** Mensagens de erro ou sucesso após ações (ex: "Dieta excluída com sucesso").

### Fluxo de Uso do Usuário
1. Na Listagem, o usuário clica em "Visualizar" na dieta "Caseira" de "Rex".
2. A tela carrega com os detalhes: Tipo ("Caseira"), Objetivo ("Emagrecimento"), Status ("Ativa").
3. Na tabela de opções, vê "Ração Premium" (Valor: R$150, Calorias: 2000) e clica para acessar mais detalhes.
4. Clica em "Adicionar Opção" para incluir uma nova opção ao plano.
5. Usa a aba "Alimentos" para gerenciar os itens da dieta ou "Excluir Dieta" para remover o plano, confirmando no modal.

---

## Tela 4: Cadastro de Opção de Dieta

### Descrição
A Tela de Cadastro de Opção de Dieta é uma página focada na adição de opções específicas ao plano alimentar, como rações ou receitas personalizadas. Com um formulário simples e funcional, ela permite ao usuário detalhar aspectos como custo, calorias e porções, garantindo que cada opção seja bem documentada e integrada à dieta. Esta tela é prática para personalizar planos de forma granular, oferecendo flexibilidade e controle.

### Componentes
- **Dropdown de Busca de Animais:** No topo, mantendo o contexto do animal.
- **Formulário de Cadastro:**
  - **Nome:** Campo de texto (ex: "Ração Light", obrigatório).
  - **Valor Mensal:** Campo numérico (ex: "150.00", opcional).
  - **Calorias Totais:** Campo numérico (ex: "2000", opcional).
  - **Porção por Refeição:** Texto (ex: "250g", opcional).
  - **Número de Refeições:** Campo numérico (ex: "2", opcional).
- **Botão "Salvar":** Submete os dados.
- **Botão "Cancelar":** Retorna aos Detalhes da Dieta.

### Funcionalidades
- **Envio de Dados:** POST para `/api/v1/diets/{diet_id}/options` com os dados inseridos.
- **Sucesso:** Retorna à Tela de Detalhes com a nova opção listada.
- **Erro:** Exibe mensagens como "Nome é obrigatório" se a validação falhar.

### Fluxo de Uso do Usuário
1. Na Tela de Detalhes da Dieta, o usuário clica em "Adicionar Opção".
2. Preenche Nome ("Ração Light"), Valor Mensal ("150"), Calorias Totais ("2000"), Porção ("250g") e Refeições ("2").
3. Clica em "Salvar" e volta aos Detalhes, onde "Ração Light" aparece na lista.
4. Se deixa o Nome em branco, vê uma mensagem de erro ao tentar salvar.
5. Clica em "Cancelar" para desistir e retornar sem alterações.

---

## Tela 5: Listagem de Alimentos por Opção

### Descrição
A Tela de Listagem de Alimentos por Opção exibe todos os alimentos associados a uma opção específica de dieta, funcionando como um painel de gerenciamento detalhado. Com uma tabela interativa, o usuário pode visualizar, adicionar, editar ou remover alimentos, garantindo que cada opção seja composta por itens bem definidos. Esta página é crucial para ajustar os componentes de uma dieta, oferecendo clareza e controle sobre o que o animal consome.

### Componentes
- **Dropdown de Busca de Animais:** No topo, para manter o contexto.
- **Tabela de Alimentos:** Colunas incluem:
  - **Nome:** Ex: "Frango Cozido".
  - **Tipo:** Ex: "Proteína".
  - **Quantidade:** Ex: "200g".
  - **Calorias:** Ex: "150".
  - **Horário:** Ex: "Almoço".
  - **Ações:** Botões "Editar" e "Excluir".
- **Botão "Adicionar Alimento":** Acima da tabela, leva ao cadastro.
- **Paginação:** Exibe até 10 alimentos por página.

### Funcionalidades
- **Carregamento:** GET para `/api/v1/diet-options/{option_id}/foods` lista os alimentos.
- **Ações:** "Editar" abre a Tela de Edição de Alimento; "Excluir" remove via DELETE `/api/v1/diet-options/{option_id}/foods/{food_id}`.

### Fluxo de Uso do Usuário
1. Na Tela de Detalhes, o usuário clica em uma opção como "Ração Premium".
2. A tabela lista alimentos associados: "Ração Seca" (200g, Manhã), "Frango" (100g, Almoço).
3. Clica em "Adicionar Alimento" para incluir um novo item.
4. Seleciona "Editar" em "Frango" para ajustar a quantidade ou "Excluir" para removê-lo, confirmando no modal.

---

## Tela 6: Cadastro de Alimento

### Descrição
A Tela de Cadastro de Alimento permite adicionar alimentos a uma opção de dieta, com um formulário detalhado que captura informações específicas sobre o consumo. Projetada para ser rápida e precisa, ela assegura que cada alimento seja registrado com clareza, contribuindo para um plano alimentar completo e adaptado às necessidades do animal.

### Componentes
- **Dropdown de Busca de Animais:** No topo, para consistência.
- **Formulário de Cadastro:**
  - **Nome:** Texto (ex: "Frango Cozido", obrigatório).
  - **Tipo:** Dropdown ("Ração", "Proteína", "Vegetal", obrigatório).
  - **Quantidade:** Texto (ex: "200g", opcional).
  - **Calorias:** Número (ex: "150", opcional).
  - **Horário:** Dropdown ("Manhã", "Tarde", "Noite", opcional).
- **Botão "Salvar":** Envia os dados.
- **Botão "Cancelar":** Volta à Listagem de Alimentos.

### Funcionalidades
- **Envio de Dados:** POST para `/api/v1/diet-options/{option_id}/foods`.
- **Sucesso:** Retorna à Listagem com o novo alimento exibido.
- **Erro:** Mensagens de validação aparecem se campos obrigatórios estiverem vazios.

### Fluxo de Uso do Usuário
1. Na Listagem de Alimentos, o usuário clica em "Adicionar Alimento".
2. Preenche Nome ("Frango Cozido"), Tipo ("Proteína"), Quantidade ("100g"), Calorias ("150"), Horário ("Almoço").
3. Clica em "Salvar" e vê o alimento na lista ao retornar.
4. Se esquece o Nome, uma mensagem de erro impede o envio.
5. Clica em "Cancelar" para voltar sem salvar.

---

## Tela 7: Gerenciamento de Alimentos Restritos

### Descrição
A Tela de Gerenciamento de Alimentos Restritos é uma página dedicada a listar e adicionar alimentos que o animal deve evitar, essencial para garantir a segurança alimentar. Com uma interface simples e funcional, ela permite ao usuário registrar restrições com seus motivos, como alergias ou toxicidade, oferecendo uma visão clara das limitações nutricionais de cada paciente.

### Componentes
- **Dropdown de Busca de Animais:** No topo, para selecionar o animal.
- **Lista de Alimentos Restritos:** Tabela com:
  - **Nome:** Ex: "Chocolate".
  - **Motivo:** Ex: "Tóxico".
  - **Ações:** "Editar" e "Excluir".
- **Botão "Adicionar Alimento":** Abre um formulário inline ou redireciona para cadastro.
- **Paginação:** Se a lista for longa.

### Funcionalidades
- **Carregamento:** GET para `/api/v1/animals/{animal_id}/restricted-foods`.
- **Adicionar:** POST para `/api/v1/animals/{animal_id}/restricted-foods`.
- **Editar:** PUT para `/api/v1/animals/{animal_id}/restricted-foods/{food_id}`.
- **Excluir:** DELETE para `/api/v1/animals/{animal_id}/restricted-foods/{food_id}`.

### Fluxo de Uso do Usuário
1. No menu lateral, o usuário seleciona "Alimentos Restritos".
2. Escolhe "Rex" no dropdown de busca.
3. Vê a lista: "Chocolate" (Motivo: "Tóxico"), "Uva" (Motivo: "Tóxico").
4. Clica em "Adicionar Alimento", insere "Cebola" com Motivo "Tóxico" e salva.
5. Edita "Chocolate" para ajustar o motivo ou exclui "Uva", confirmando a ação.

---

## Tela 8: Gerenciamento de Snacks

### Descrição
A Tela de Gerenciamento de Snacks permite listar e adicionar petiscos permitidos entre as refeições, com controle detalhado sobre frequência e quantidade. Esta página é fundamental para equilibrar a dieta, oferecendo uma interface prática que ajuda a clínica a gerenciar o consumo de snacks de forma responsável e alinhada ao plano alimentar.

### Componentes
- **Dropdown de Busca de Animais:** No topo, para selecionar o animal.
- **Lista de Snacks:** Tabela com:
  - **Nome:** Ex: "Bifinho".
  - **Frequência Semanal:** Ex: "3x/semana".
  - **Quantidade:** Ex: "1 unidade".
  - **Observações:** Ex: "Após caminhada".
  - **Ações:** "Editar" e "Excluir".
- **Botão "Adicionar Snack":** Abre um formulário para inclusão.
- **Paginação:** Para listas extensas.

### Funcionalidades
- **Carregamento:** GET para `/api/v1/animals/{animal_id}/snacks`.
- **Adicionar:** POST para `/api/v1/animals/{animal_id}/snacks`.
- **Editar:** PUT para `/api/v1/animals/{animal_id}/snacks/{snack_id}`.
- **Excluir:** DELETE para `/api/v1/animals/{animal_id}/snacks/{snack_id}`.

### Fluxo de Uso do Usuário
1. No menu lateral, o usuário seleciona "Snacks".
2. Escolhe "Luna" no dropdown de busca.
3. Vê a lista: "Bifinho" (3x/semana, 1 unidade, "Após caminhada").
4. Clica em "Adicionar Snack", insere "Petisco Dental" (2x/semana, 1 unidade) e salva.
5. Edita "Bifinho" para mudar a frequência ou exclui outro snack, confirmando no modal.

---

## Estrutura e Navegação
As oito telas são **páginas distintas**, não seções ou cards dentro de uma única "Tela de Dieta". Elas seguem um fluxo intuitivo:
- **Listagem de Dietas por Animal → Cadastro de Dieta → Detalhes da Dieta → Cadastro de Opção → Listagem de Alimentos → Cadastro de Alimento.**
- **Gerenciamento de Alimentos Restritos e Snacks:** Acessíveis diretamente pelo menu lateral ou abas contextuais.
O dropdown de busca de animais no topo de cada tela permite alternar entre pacientes rapidamente, atualizando o conteúdo exibido sem necessidade de voltar ao menu principal.

---

## Detalhes Técnicos
- **Rotas Backend:**
  - GET `/api/v1/animals` – Lista todos os animais.
  - GET `/api/v1/animals/{animal_id}/diets` – Lista dietas de um animal.
  - POST `/api/v1/animals/{animal_id}/diets` – Cadastra uma dieta.
  - GET `/api/v1/diets/{diet_id}` – Detalhes de uma dieta.
  - PATCH `/api/v1/diets/{diet_id}` – Edita uma dieta.
  - DELETE `/api/v1/diets/{diet_id}` – Exclui uma dieta.
  - POST `/api/v1/diets/{diet_id}/options` – Adiciona uma opção à dieta.
  - GET `/api/v1/diet-options/{option_id}/foods` – Lista alimentos de uma opção.
  - POST `/api/v1/diet-options/{option_id}/foods` – Cadastra um alimento.
  - GET `/api/v1/animals/{animal_id}/restricted-foods` – Lista alimentos restritos.
  - POST `/api/v1/animals/{animal_id}/restricted-foods` – Adiciona alimento restrito.
  - GET `/api/v1/animals/{animal_id}/snacks` – Lista snacks.
  - POST `/api/v1/animals/{animal_id}/snacks` – Adiciona um snack.
- **Autenticação:** Token JWT em todas as requisições.
- **Frontend:** Desenvolvido com React, React Router e Tailwind CSS para estilização.

---

## Tarefas da Sprint
- Implementar o dropdown de busca de animais em todas as telas, integrando-o com a API.
- Desenvolver telas de listagem com filtros dinâmicos e paginação.
- Criar formulários validados para cadastros e edições.
- Garantir navegação fluida entre telas de dietas, opções e alimentos.
- Realizar testes de fluxo de uso e integração com o backend.

---

Esta versão ampliada da Sprint 4 reflete uma exploração mais profunda das telas, com descrições detalhadas e fluxos de uso claros, mantendo a nova feature do dropdown de busca de animais. Se estiver satisfeito, podemos avançar para a Sprint 5, detalhando o próximo módulo (ex: Atividades Físicas) com a mesma estrutura e uma nova feature. O que acha?