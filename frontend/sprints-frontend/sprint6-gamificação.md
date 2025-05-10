# Sprint 6: Gamificação - Detalhamento Revisado e Ampliado 

Esta sprint foca na implementação de um módulo de gamificação robusto e envolvente para a clínica veterinária, projetado para incentivar os tutores a aderirem aos planos de saúde e atividades dos animais. A gamificação utiliza elementos de jogos — pontos, recompensas, rankings — para promover comportamentos positivos, como seguir dietas ou realizar exercícios. O módulo é composto por **nove telas distintas**, cada uma funcionando como uma página independente no sistema, interligadas por uma navegação fluida e intuitiva. Essas telas não são seções, cards ou grupos dentro de uma única "Tela de Resultados", mas sim páginas completas que formam um fluxo coeso, garantindo clareza e engajamento para os usuários (funcionários da clínica e, indiretamente, tutores).

**Nova Feature:** Todas as telas possuem um **dropdown de busca de animais** fixado no topo, permitindo que o usuário selecione rapidamente um animal para visualizar ou gerenciar suas informações de gamificação. Esse recurso é essencial para clínicas com muitos pacientes, atualizando dinamicamente o conteúdo da tela ao mudar de animal, sem recarregar a página.

**Usabilidade Estratégica para Gamificação:** A interface prioriza uma experiência motivadora com elementos visuais como barras de progresso, badges de conquistas, ícones animados de recompensas e paleta de cores vibrantes (ex.: tons de verde para sucesso, azul para progresso). Cada tela destaca o avanço do animal, celebra conquistas e incentiva ações futuras, alinhando-se aos objetivos da gamificação e tornando o uso do sistema recompensador tanto para funcionários quanto para tutores.

---

## Tela 1: Listagem de Metas

### Descrição
A Tela de Listagem de Metas é o hub administrativo da gamificação, uma página independente que centraliza a gestão de metas globais da clínica. Aqui, o usuário pode visualizar, editar ou criar metas aplicáveis a qualquer animal (ex.: "Caminhar 3x por semana", "Manter peso ideal por 15 dias"), com uma interface organizada e interativa. A tabela de metas é responsiva, com filtros e busca em tempo real, ideal para clínicas com alto volume de dados. Elementos visuais como ícones temáticos (pegadas, pratos) e badges de "meta ativa" tornam a navegação intuitiva e incentivadora, reforçando o engajamento.

### Componentes
- **Dropdown de Busca de Animais:** Fixado no topo, permite alternar entre animais, mas não filtra a listagem (metas são globais).
- **Tabela de Metas:** Colunas interativas:
  - **Descrição:** Ex.: "Caminhar 3x por semana".
  - **Tipo:** Ex.: "Atividade", "Dieta", "Peso".
  - **Pontos:** Ex.: "100".
  - **Status:** Ex.: "Ativa" (verde), "Inativa" (cinza).
  - **Ações:** Botões "Editar" (ícone de lápis) e "Excluir" (ícone de lixeira).
- **Campo de Busca:** Filtra metas por descrição ou tipo dinamicamente.
- **Botão "Nova Meta":** No canto superior direito, com ícone de estrela e cor amarela vibrante.
- **Paginação:** Limite de 10 metas por página, com botões "Anterior" e "Próximo".
- **Indicador de Carregamento:** Spinner circular durante carregamento ou busca.
- **Ícones Temáticos:** Cada meta exibe um ícone (ex.: pegada para "Atividade"), com tooltip ao passar o mouse.

### Funcionalidades
- **Carregamento Inicial:** Requisição GET para `/api/v1/gamification/goals` retorna todas as metas da clínica.
- **Busca Dinâmica:** Filtragem local ou via API com GET `/api/v1/gamification/goals?search={termo}`.
- **Ações por Meta:**
  - **Editar:** Redireciona para a Tela de Cadastro de Meta com dados preenchidos.
  - **Excluir:** Modal de confirmação ("Tem certeza?") antes de DELETE `/api/v1/gamification/goals/{goal_id}`.
- **Autenticação:** Token JWT no cabeçalho `Authorization` em todas as requisições.

### Fluxo de Uso do Usuário
1. O usuário acessa o sistema inserindo email (ex.: "funcionario@clinica.com") e senha na tela de login.
2. Se esqueceu a senha, clica em "Recuperar Senha", insere o email, recebe um link por email, clica no link e redefine a senha com validação (mínimo 8 caracteres).
3. Após login, no menu lateral, seleciona "Gamificação" > "Metas".
4. A tela carrega a tabela com metas como "Caminhar 3x por semana" (100 pontos, Ativa, ícone de pegada).
5. Digita "Caminhar" no campo de busca; a tabela filtra instantaneamente para essa meta.
6. Clica em "Nova Meta" para criar uma nova meta (redireciona à Tela 2).
7. Clica em "Editar" para ajustar os pontos de "Caminhar" ou "Excluir" para removê-la, confirmando no modal com "Sim" ou "Não".

---

## Tela 2: Cadastro de Meta

### Descrição
Esta página independente é o ambiente para criar ou editar metas de gamificação, oferecendo um formulário detalhado e visualmente atraente. O usuário define metas específicas com descrição, tipo, pontuação e status, recebendo feedback imediato sobre erros ou sucesso. A tela inclui uma pré-visualização animada do ícone escolhido (ex.: um osso girando para "Dieta"), reforçando a gamificação e tornando o cadastro mais interativo e motivador.

### Componentes
- **Dropdown de Busca de Animais:** No topo, informativo (não afeta o cadastro de metas globais).
- **Formulário de Cadastro:**
  - **Descrição:** Campo de texto (máx. 100 caracteres, ex.: "Seguir dieta por 7 dias", obrigatório).
  - **Tipo:** Dropdown com "Atividade", "Dieta", "Peso", "Consulta" (obrigatório).
  - **Pontos:** Campo numérico (1-1000, obrigatório).
  - **Status:** Dropdown "Ativa" ou "Inativa" (padrão: "Ativa", obrigatório).
  - **Ícone:** Dropdown com opções visuais (ex.: pegada, prato) ou upload customizado.
- **Botão "Salvar":** Verde, com ícone de check, envia os dados.
- **Botão "Cancelar":** Cinza, retorna à Tela 1.
- **Mensagens de Erro:** Em vermelho abaixo dos campos (ex.: "Pontos devem ser entre 1 e 1000").
- **Pré-visualização do Ícone:** À direita, exibe o ícone animado com tooltip (ex.: "Ícone da meta").

### Funcionalidades
- **Envio de Dados:** POST para `/api/v1/gamification/goals` com JSON do formulário.
- **Edição:** GET `/api/v1/gamification/goals/{goal_id}` pré-preenche o formulário.
- **Sucesso:** Redireciona à Tela 1 com a meta listada.
- **Erro:** Exibe validações como "Descrição obrigatória".
- **Validação Frontend:** React Hook Form verifica campos antes do envio.

### Fluxo de Uso do Usuário
1. Na Tela 1, clica em "Nova Meta" ou "Editar" em uma meta existente.
2. O formulário carrega vazio (novo) ou preenchido (edição).
3. Preenche Descrição ("Seguir dieta por 7 dias"), Tipo ("Dieta"), Pontos ("150"), Status ("Ativa"), seleciona ícone de prato.
4. Vê o ícone animado à direita ao escolhê-lo.
5. Clica em "Salvar"; spinner aparece, e, se OK, volta à Tela 1 com a meta atualizada.
6. Se deixa "Pontos" em branco, vê erro "Campo obrigatório".
7. Clica em "Cancelar" para voltar sem salvar.

---

## Tela 3: Atribuição de Pontuações

### Descrição
Esta página permite registrar pontos para um animal com base em metas cumpridas, sendo essencial para o progresso na gamificação. O formulário é simples, mas enriquecido com elementos visuais como um ícone de troféu animado ao salvar, celebrando a conquista. O dropdown de busca no topo assegura que o usuário atribua pontos ao animal correto, com contexto claro e usabilidade fluida.

### Componentes
- **Dropdown de Busca de Animais:** No topo, seleciona o animal (ex.: "Rex"), atualizando o formulário.
- **Formulário de Atribuição:**
  - **Meta:** Dropdown com metas ativas (ex.: "Caminhar 3x por semana", obrigatório).
  - **Pontos:** Numérico, pré-preenchido com os pontos da meta, editável.
  - **Data:** Date picker (padrão: hoje, obrigatório).
  - **Descrição:** Textarea (máx. 200 caracteres, opcional).
- **Botão "Salvar":** Verde, com ícone de troféu.
- **Botão "Cancelar":** Cinza, volta à Tela 1.
- **Feedback Visual:** Troféu animado aparece ao salvar com sucesso.

### Funcionalidades
- **Carregamento de Metas:** GET `/api/v1/gamification/goals?status=active` popula o dropdown.
- **Envio:** POST `/api/v1/gamification/points` com dados do formulário.
- **Sucesso:** Mensagem "Pontos atribuídos!" com animação.
- **Erro:** Validações como "Meta obrigatória".

### Fluxo de Uso do Usuário
1. Após login, no menu, seleciona "Gamificação" > "Atribuir Pontos".
2. Escolhe "Rex" no dropdown; o formulário ajusta-se a ele.
3. Seleciona "Caminhar 3x por semana" (100 pontos), ajusta para 120 se desejar, define a data e escreve "Caminhada concluída".
4. Clica em "Salvar"; troféu animado aparece, e volta à Tela 1.
5. Se esquece a meta, vê erro "Selecione uma meta".
6. Clica em "Cancelar" para desistir.

---

## Tela 4: Histórico de Pontuações

### Descrição
Esta página exibe o histórico detalhado de pontuações de um animal, funcionando como um painel de acompanhamento. Uma tabela interativa e uma linha do tempo visual (com ícones de medalhas para marcos) mostram o progresso, enquanto o dropdown de busca no topo permite alternar entre animais. O design é motivacional, com cores que destacam conquistas (ex.: dourado para marcos).

### Componentes
- **Dropdown de Busca de Animais:** No topo, atualiza o histórico ao selecionar.
- **Tabela de Histórico:** Colunas:
  - **Data:** Ex.: "26/10/2023".
  - **Meta:** Ex.: "Caminhar 3x por semana".
  - **Pontos:** Ex.: "100".
  - **Descrição:** Ex.: "Meta alcançada".
- **Linha do Tempo Visual:** Exibe pontuações com medalhas para marcos (ex.: 5 metas seguidas).
- **Filtros:** Por data (calendário) ou meta (dropdown).
- **Paginação:** 10 registros por página.

### Funcionalidades
- **Carregamento:** GET `/api/v1/animals/{animal_id}/gamification/points`.
- **Filtros:** GET `/api/v1/animals/{animal_id}/gamification/points?date={range}`.
- **Linha do Tempo:** Renderizada localmente com base nos dados.

### Fluxo de Uso do Usuário
1. Após login, seleciona "Gamificação" > "Histórico de Pontos".
2. Escolhe "Luna" no dropdown; tabela e linha do tempo carregam.
3. Vê marco "5 metas consecutivas" com medalha dourada.
4. Filtra por "Dieta" no dropdown de metas.
5. Navega entre páginas para ver registros antigos.

---

## Tela 5: Listagem de Recompensas

### Descrição
Esta página exibe todas as recompensas disponíveis (ex.: descontos, brindes) que tutores podem resgatar com pontos. A tabela interativa e ícones de presentes animados tornam a gestão de recompensas atrativa e incentivadora, enquanto o dropdown de busca no topo mantém o contexto, embora não filtre a listagem (recompensas são globais).

### Componentes
- **Dropdown de Busca de Animais:** Informativo, no topo.
- **Tabela de Recompensas:** Colunas:
  - **Nome:** Ex.: "Desconto de 10% em consulta".
  - **Pontos Necessários:** Ex.: "500".
  - **Tipo:** Ex.: "Desconto", "Brinde".
  - **Ações:** "Editar" e "Excluir".
- **Campo de Busca:** Filtra por nome ou tipo.
- **Botão "Nova Recompensa":** Com ícone de presente, no topo.
- **Paginação:** 10 recompensas por página.
- **Ícones Animados:** Presentes giram ao passar o mouse.

### Funcionalidades
- **Carregamento:** GET `/api/v1/gamification/rewards`.
- **Ações:**
  - **Editar:** Redireciona à Tela 6 com dados.
  - **Excluir:** Modal antes de DELETE `/api/v1/gamification/rewards/{reward_id}`.

### Fluxo de Uso do Usuário
1. Após login, seleciona "Gamificação" > "Recompensas".
2. Tabela carrega com "Desconto de 10%" (500 pontos).
3. Busca "Desconto" para filtrar.
4. Clica em "Nova Recompensa" para criar uma.
5. Edita ou exclui recompensas, confirmando exclusão.

---

## Tela 6: Cadastro de Recompensa

### Descrição
Página para criar ou editar recompensas, com um formulário que define nome, pontos, tipo e descrição. A pré-visualização do ícone (ex.: caixa de presente abrindo) e feedback visual tornam o cadastro envolvente, alinhado à gamificação.

### Componentes
- **Dropdown de Busca de Animais:** Informativo, no topo.
- **Formulário:**
  - **Nome:** Texto (ex.: "Brinde Especial", obrigatório).
  - **Pontos Necessários:** Numérico (ex.: "1000", obrigatório).
  - **Tipo:** Dropdown ("Desconto", "Brinde", etc.).
  - **Descrição:** Textarea (opcional).
  - **Ícone:** Seleção visual.
- **Botão "Salvar":** Verde.
- **Botão "Cancelar":** Cinza.
- **Pré-visualização:** Ícone animado à direita.

### Funcionalidades
- **Envio:** POST `/api/v1/gamification/rewards`.
- **Edição:** GET `/api/v1/gamification/rewards/{reward_id}`.
- **Sucesso:** Volta à Tela 5.

### Fluxo de Uso do Usuário
1. Na Tela 5, clica em "Nova Recompensa".
2. Preenche Nome ("Brinde Especial"), Pontos ("1000"), Tipo ("Brinde"), Descrição ("Exclusivo").
3. Seleciona ícone de presente; vê animação.
4. Clica em "Salvar" e volta à Tela 5.
5. Se esquece Nome, vê erro.

---

## Tela 7: Atribuição de Recompensas

### Descrição
Página para atribuir recompensas a animais com pontos suficientes. O formulário verifica automaticamente a elegibilidade, e uma animação de confetes ao salvar celebra a conquista, reforçando a gamificação.

### Componentes
- **Dropdown de Busca de Animais:** No topo, atualiza os dados.
- **Formulário:**
  - **Recompensa:** Dropdown com recompensas disponíveis.
  - **Pontos do Animal:** Ex.: "600".
  - **Pontos Necessários:** Ex.: "500".
- **Botão "Atribuir":** Verde, desativado se pontos insuficientes.
- **Animação:** Confetes ao salvar.

### Funcionalidades
- **Verificação:** GET `/api/v1/animals/{animal_id}/gamification/points` compara pontos.
- **Envio:** POST `/api/v1/animals/{animal_id}/gamification/rewards`.
- **Sucesso:** Animação e mensagem.

### Fluxo de Uso do Usuário
1. Após login, seleciona "Gamificação" > "Atribuir Recompensas".
2. Escolhe "Rex" (600 pontos).
3. Seleciona "Desconto de 10%" (500 pontos).
4. Clica em "Atribuir"; confetes aparecem.
5. Se pontos insuficientes, botão fica cinza.

---

## Tela 8: Ranking de Pets

### Descrição
Página que exibe o ranking dos animais por pontos, promovendo competição saudável. Uma tabela estilizada e um pódio visual (top 3 com medalhas) motivam os tutores, com o dropdown permitindo visualizar o contexto.

### Componentes
- **Dropdown de Busca de Animais:** Informativo.
- **Tabela de Ranking:**
  - **Posição:** Ex.: "1º".
  - **Animal:** Ex.: "Rex".
  - **Pontos:** Ex.: "1000".
- **Pódio Visual:** Top 3 com medalhas (ouro, prata, bronze).
- **Filtros:** Período (semanal, mensal).

### Funcionalidades
- **Carregamento:** GET `/api/v1/gamification/ranking`.
- **Filtros:** GET `/api/v1/gamification/ranking?period={period}`.

### Fluxo de Uso do Usuário
1. Após login, seleciona "Gamificação" > "Ranking".
2. Vê "Rex" em 1º (1000 pontos) com medalha de ouro.
3. Filtra por "Mensal" para ajustar o ranking.

---

## Tela 9: Relatórios de Progresso

### Descrição
Página para gerar relatórios detalhados do progresso de um animal, com gráficos interativos (ex.: linha de pontos) e estatísticas. O dropdown no topo foca em um animal, e o design visual motiva com cores e ícones.

### Componentes
- **Dropdown de Busca de Animais:** Atualiza o relatório.
- **Gráficos:** Linha de pontos, barras de metas.
- **Estatísticas:** Total de pontos, metas concluídas.
- **Botão "Gerar PDF":** Exporta o relatório.

### Funcionalidades
- **Carregamento:** GET `/api/v1/animals/{animal_id}/gamification/reports`.
- **Exportação:** Gera PDF com dados.

### Fluxo de Uso do Usuário
1. Após login, seleciona "Gamificação" > "Relatórios".
2. Escolhe "Luna"; vê gráficos e estatísticas.
3. Clica em "Gerar PDF" para baixar.

---

## Estrutura e Navegação
As 9 telas são **páginas distintas**, interligadas assim:
- Tela 1 → Tela 2 (metas).
- Tela 3 → Tela 4 (pontuações).
- Tela 5 → Tela 6 → Tela 7 (recompensas).
- Tela 8 (ranking).
- Tela 9 (relatórios).
O dropdown de busca no topo mantém o contexto em todas as telas.

---

## Detalhes Técnicos
- **Rotas Backend:** Mesmas da versão anterior, com GET `/api/v1/animals` para o dropdown.
- **Frontend:** React, Tailwind CSS, Chart.js (gráficos), Confetti (animações).
- **Autenticação:** JWT em todas as requisições.

---

## Tarefas da Sprint
- Implementar dropdown de busca integrado com `/api/v1/animals`.
- Adicionar animações e ícones motivacionais.
- Testar fluxos, integração e responsividade.