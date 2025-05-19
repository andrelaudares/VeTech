# Sprint 5: Atividades Físicas - Detalhamento Revisado e Ampliado (Versão 2)

Esta sprint foca na construção de um módulo robusto e intuitivo para a gestão de atividades físicas em uma clínica veterinária, permitindo que os usuários (funcionários da clínica, como veterinários ou cuidadores) gerenciem planos de atividades, registrem exercícios realizados e acompanhem o progresso dos animais. O objetivo é oferecer uma interface fluida, visualmente atraente e funcional, que facilite o planejamento e monitoramento de rotinas físicas personalizadas. São implementados **seis grupos de funcionalidades distintos**, todos integrados na **Página de Atividades** como áreas funcionais dentro de uma única página, interligadas por uma navegação clara e lógica. Este design assegura clareza, evita sobrecarga de informações e suporta o fluxo de trabalho da clínica, utilizando pop-ups para ações específicas e layouts intuitivos para maximizar a usabilidade.

---

## Página de Atividades

A **Página de Atividades** é uma página única que agrega os seis grupos de funcionalidades descritos abaixo, organizados de forma atrativa e intuitiva. Esses grupos não são páginas separadas, mas sim seções distintas dentro da mesma interface, projetadas para oferecer uma experiência coesa e eficiente. Os grupos são:

1. **Grupo 1: Listagem de Tipos de Atividades**
2. **Grupo 2: Cadastro de Tipo de Atividade**
3. **Grupo 3: Listagem de Planos de Atividade**
4. **Grupo 4: Cadastro de Plano de Atividade**
5. **Grupo 5: Registro de Atividades Realizadas**
6. **Grupo 6: Histórico de Atividades**

Esses grupos são apresentados em uma estrutura visual que prioriza a navegabilidade e o apelo estético, com funcionalidades como adicionar e editar implementadas em pop-ups para manter o usuário no contexto da página, evitando redirecionamentos desnecessários.

---

## Integração com o Header

O componente `AppHeader`, detalhado no arquivo `HEADER_DOCS.md`, é um elemento essencial da aplicação VeTech e desempenha um papel crítico na **Página de Atividades**. Ele não é apenas uma "feature contínua", mas sim uma funcionalidade central que controla o estado global da aplicação, especialmente por meio do **dropdown de seleção de animal**. Para esta página, a interação com o header é **obrigatória**, pois a seleção de um animal é um pré-requisito para o funcionamento adequado de todos os grupos de funcionalidades. Abaixo, detalho essa integração:

### Funcionalidade do Header na Página de Atividades
- **Dropdown de Seleção de Animal:** Localizado no header, este componente permite ao usuário escolher um animal específico da clínica (ex: "Rex", "Luna") antes de interagir com a página. Ele consome a API `GET /api/v1/animals` para listar os animais cadastrados, atualizando dinamicamente conforme a busca do usuário.
- **Estado Global (`selectedAnimal`):** O animal selecionado é armazenado no `AnimalContext`, um contexto global do React, e afeta diretamente o comportamento da Página de Atividades:
  - **Sem animal selecionado:** A página exibe uma mensagem bloqueante, como "Por favor, selecione um animal no header para gerenciar atividades físicas", e desabilita ações como criar ou visualizar planos.
  - **Com animal selecionado:** Todos os grupos de funcionalidades (listagem, cadastro, etc.) são ativados e exibem dados relativos ao animal escolhido, como seus planos de atividades e histórico.
- **Visibilidade do Dropdown:** Conforme o documento `HEADER_DOCS.md`, a Página de Atividades é classificada como uma "tela que exige seleção de animal". Assim, o dropdown permanece visível e funcional enquanto o usuário estiver nesta página, garantindo que o contexto do animal esteja sempre claro.

### Impacto no Fluxo do Usuário
- Ao acessar a Página de Atividades pelo menu lateral (link "Atividades" no header), o usuário deve primeiro selecionar um animal no dropdown do header.
- Exemplo: Se o usuário escolhe "Rex", o estado `selectedAnimal` é atualizado, e a API `GET /api/v1/animals/{animal_id}/activity-plans` é chamada para carregar os planos de atividades de "Rex" no Grupo 3.
- Qualquer tentativa de cadastrar um plano ou interagir com outros grupos sem um animal selecionado resulta em feedback imediato (mensagem ou bloqueio), reforçando a dependência do header.

### Detalhes Técnicos do Header
- **Componente React:** O `AppHeader` é reutilizável e gerencia a navegação principal (ex: links para "Início", "Atividades", "Dietas") e o estado do animal.
- **Autenticação:** Todas as requisições disparadas pelo dropdown (como listar animais) incluem o token JWT no header `Authorization`.
- **Estilização:** Usa Tailwind CSS para um design consistente com o restante da aplicação, com um dropdown estilizado e responsivo.

Essa integração detalhada com o header assegura que a Página de Atividades funcione de forma contextualizada e segura, alinhada às necessidades da clínica veterinária.

---

## Design Intuitivo e Atratativo

A Página de Atividades é uma das mais importantes do sistema, pois incentiva os usuários a criar e gerenciar planos de atividades físicas de forma eficiente e prazerosa. Por isso, o design não deve ser apenas funcional, mas também **extremamente atrativo**, com elementos visuais que motivem o uso contínuo. Aqui estão as diretrizes e sugestões para alcançar esse objetivo:

### Princípios de Design
- **Intuitividade:** A organização dos grupos deve seguir uma lógica natural (ex: listagem de tipos como ponto de entrada administrativo, listagem de planos como foco principal para o animal), com navegação clara e feedback visual constante.
- **Atratividade:** Componentes bonitos e chamativos são essenciais para engajar o usuário, transmitindo uma sensação de cuidado e profissionalismo.

### Elementos Visuais Sugeridos
- **Ícones Representativos:** Cada grupo pode ter um ícone associado (ex: tênis para atividades, gráfico para histórico), tornando a interface mais visual e amigável.
- **Barras de Progresso:** Em planos e histórico, barras coloridas (verde para concluído, amarelo para parcial) incentivam o usuário a acompanhar o progresso.
- **Cores Vibrantes:** Uma paleta com tons de azul (confiança), verde (saúde) e laranja (energia) para botões e destaques, combinada com fundos neutros.
- **Layouts Modernos:** Uso de cards com sombras sutis, espaçamento generoso e tabelas responsivas para uma apresentação limpa e organizada.
- **Componentes Estilizados:** Botões com efeitos de hover (ex: leve aumento ou mudança de cor), pop-ups com animações suaves de entrada/saída, e gráficos simples (ex: linha do tempo no histórico).
- **Feedback Visual:** Spinners coloridos durante carregamentos, mensagens de sucesso com ícones (ex: check verde) e erros destacados em vermelho.

### Benefícios Esperados
Esses elementos não só facilitam a interação, mas também tornam a experiência mais agradável, motivando veterinários e cuidadores a usar a página regularmente para planejar atividades criativas e bem estruturadas.

---

## Grupo 1: Listagem de Tipos de Atividades

### Descrição
O **Grupo de Listagem de Tipos de Atividades** é o ponto de entrada administrativo para o gerenciamento de atividades físicas globais da clínica, exibindo todos os tipos de atividades disponíveis no sistema (ex: caminhada, corrida, natação). Projetado como uma área principal e sempre visível ao carregar a página, ele permite visualização, edição e adição de novos tipos que podem ser usados em planos personalizados. A interface incorpora elementos visuais motivacionais, como ícones representando cada tipo de atividade, para tornar a experiência mais dinâmica.

### Componentes
- **Tabela de Tipos de Atividades:** Colunas configuráveis:
  - Nome (ex: "Caminhada")
  - Tipo (ex: "Aeróbico")
  - Calorias por Hora (ex: "200 kcal/h")
  - Ações ("Editar", "Excluir")
- **Ícones Visuais:** Cada tipo de atividade tem um ícone correspondente (ex: pegada para "Caminhada").
- **Campo de Busca:** Pesquisa em tempo real por nome ou tipo.
- **Botão "Novo Tipo":** No canto superior direito, abre o Grupo 2 em um pop-up.
- **Paginação:** Até 10 tipos por página.
- **Indicador de Carregamento:** Spinner estilizado.

### Funcionalidades
- **Carregamento:** `GET /api/v1/activities` lista os tipos de atividades globais da clínica.
- **Busca:** Filtragem via API (ex: `GET /api/v1/activities?search={termo}`).
- **Ações:**
  - Editar: Abre Grupo 2 em pop-up com dados preenchidos.
  - Excluir: Modal de confirmação + `DELETE /api/v1/activities/{activity_id}`.

### Fluxo de Uso do Usuário
1. Usuário acessa a Página de Atividades e vê a listagem de tipos.
2. Busca "Caminhada" e vê tipos filtrados.
3. Clica em "Novo Tipo" para abrir pop-up de cadastro.
4. Edita ou exclui tipos existentes via pop-up ou modal.

---

## Grupo 2: Cadastro de Tipo de Atividade

### Descrição
O **Grupo de Cadastro de Tipo de Atividade** permite criar novos tipos de atividades em um pop-up intuitivo, mantendo o usuário no contexto da Página de Atividades. O formulário é simples e validado, ideal para registrar atividades rapidamente.

### Componentes
- **Formulário:**
  - Nome (obrigatório)
  - Tipo (dropdown: "Aeróbico", "Força", etc., obrigatório)
  - Calorias por Hora (opcional)
  - Ícone (opcional, dropdown ou upload)
- **Pré-visualização do Ícone:** Mostra o ícone selecionado.
- **Botões:** "Salvar" (envia dados) e "Cancelar" (fecha pop-up).
- **Mensagens de Erro:** Abaixo dos campos.

### Funcionalidades
- **Envio:** `POST /api/v1/activities`.
- **Sucesso:** Fecha pop-up e atualiza Grupo 1.
- **Erro:** Exibe validações em tempo real.

### Fluxo de Uso do Usuário
1. No Grupo 1, clica em "Novo Tipo".
2. Preenche dados (ex: Nome: "Natação", Tipo: "Aeróbico").
3. Salva e vê o novo tipo na listagem.

---

## Grupo 3: Listagem de Planos de Atividade

### Descrição
O **Grupo de Listagem de Planos de Atividade** exibe os planos de atividades associados ao animal selecionado no header, funcionando como um painel de monitoramento personalizado. Com barras de progresso e ícones, ele motiva o usuário a acompanhar o progresso.

### Componentes
- **Tabela de Planos:** Colunas:
  - Atividade (ex: "Caminhada")
  - Frequência Semanal (ex: "3x/semana")
  - Duração por Sessão (ex: "30 min")
  - Progresso (barra de progresso, ex: 75%)
  - Ações ("Visualizar", "Editar", "Excluir")
- **Campo de Busca:** Filtra por nome da atividade.
- **Botão "Novo Plano":** Abre Grupo 4 em pop-up.
- **Paginação:** Até 10 planos por página.

### Funcionalidades
- **Carregamento:** `GET /api/v1/animals/{animal_id}/activity-plans`.
- **Ações:**
  - Visualizar: Abre detalhes em pop-up.
  - Editar: Abre Grupo 4 em pop-up com dados.
  - Excluir: Modal + `DELETE /api/v1/animals/{animal_id}/activity-plans/{plan_id}`.

### Fluxo de Uso do Usuário
1. Usuário seleciona "Rex" no header.
2. Tabela carrega planos de "Rex" com barras de progresso.
3. Clica em "Novo Plano" para criar um plano via pop-up.

---

## Grupo 4: Cadastro de Plano de Atividade

### Descrição
O **Grupo de Cadastro de Plano de Atividade** permite criar planos personalizados em um pop-up, com pré-visualização de progresso inicial.

### Componentes
- **Formulário:**
  - Atividade (dropdown de `/api/v1/activities`, obrigatório)
  - Frequência Semanal (obrigatório)
  - Duração por Sessão (obrigatório)
  - Observações (opcional)
- **Pré-visualização de Progresso:** Barra a 0%.
- **Botões:** "Salvar" e "Cancelar".

### Funcionalidades
- **Envio:** `POST /api/v1/animals/{animal_id}/activity-plans`.
- **Sucesso:** Atualiza Grupo 3.

### Fluxo de Uso do Usuário
1. No Grupo 3, clica em "Novo Plano".
2. Preenche dados para "Rex" (ex: Atividade: "Caminhada").
3. Salva e vê o plano na listagem.

---

## Grupo 5: Registro de Atividades Realizadas

### Descrição
O **Grupo de Registro de Atividades Realizadas** marca atividades como concluídas em um pop-up, com ícones de check para feedback visual.

### Componentes
- **Formulário:**
  - Plano (dropdown de planos ativos, obrigatório)
  - Data (date picker, obrigatório)
  - Status ("Concluído", "Não Realizado", obrigatório)
- **Ícone de Conquista:** Check verde ao salvar "Concluído".
- **Botões:** "Salvar" e "Cancelar".

### Funcionalidades
- **Envio:** `POST /api/v1/activity-plans/{plan_id}/activities`.
- **Sucesso:** Atualiza progresso no Grupo 3.

### Fluxo de Uso do Usuário
1. No Grupo 3, clica em "Registrar Atividade".
2. Seleciona plano, data e status.
3. Salva e vê ícone de check.

---

## Grupo 6: Histórico de Atividades

### Descrição
O **Grupo de Histórico de Atividades** exibe o registro completo de atividades em uma seção com linha do tempo visual e filtros.

### Componentes
- **Tabela:** Data, Atividade, Status, Observações.
- **Linha do Tempo:** Ícones de troféu para marcos.
- **Filtros:** Por data ou status.
- **Paginação:** Até 10 registros.

### Funcionalidades
- **Carregamento:** `GET /api/v1/animals/{animal_id}/activity-history`.
- **Filtros:** `GET /api/v1/animals/{animal_id}/activity-history?date={range}`.

### Fluxo de Uso do Usuário
1. Acessa a seção de histórico.
2. Vê atividades de "Luna" com troféus para semanas 100% concluídas.
3. Filtra por "Concluído".

---

## Estrutura e Navegação
A Página de Atividades organiza os grupos em uma interface única:
- **Grupo 1 e 3:** Áreas principais, visíveis ao carregar.
- **Grupos 2, 4, 5:** Pop-ups para ações.
- **Grupo 6:** Seção expansível ou aba.
Pop-ups minimizam navegação, mantendo o foco na página.

---

## Detalhes Técnicos
- **Rotas Backend:** Todas as rotas de `sprint5.md` foram incorporadas (ex: `GET /api/v1/activities`, `POST /api/v1/animals/{animal_id}/activity-plans`).
- **Autenticação:** Token JWT em todas as requisições.
- **Frontend:** React, React Router, Tailwind CSS, pop-ups com Material UI, ícones via FontAwesome.

---

## Tarefas da Sprint
- Implementar a Página de Atividades com os seis grupos.
- Integrar o header com seleção obrigatória de animal.
- Desenvolver design atrativo com barras de progresso, ícones e pop-ups.
- Testar fluxos e integração com o backend.

---