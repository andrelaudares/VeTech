# Sprint 4: Nutrição e Dietas - Detalhamento Revisado e Ampliado (Versão 2)

Esta sprint foca na construção de um módulo completo e robusto para a gestão de nutrição e dietas em uma clínica veterinária, oferecendo uma experiência fluida e intuitiva para os usuários (funcionários da clínica, como veterinários e nutricionistas). O objetivo é permitir o gerenciamento eficiente de planos de dieta, alimentos, restrições e snacks para os animais atendidos, com grupos de funcionalidades bem definidos que atendam a propósitos específicos. São implementados **oito grupos distintos**, todos integrados na **Página de Dietas** como áreas funcionais dentro de uma única página, interligadas por uma navegação lógica e acessível. Este design garante clareza, evita sobrecarga de informações e suporta o fluxo de trabalho da clínica de maneira organizada, utilizando pop-ups e layouts intuitivos para maximizar a usabilidade.

---

## Página de Dietas

A **Página de Dietas** é uma página única que agrega os oito grupos de funcionalidades descritos abaixo, organizados de forma atrativa e intuitiva. Esses grupos não são páginas separadas, mas sim seções distintas dentro da mesma interface, projetadas para oferecer uma experiência coesa e eficiente. Os grupos são:

1. **Grupo 1: Listagem de Dietas por Animal**
2. **Grupo 2: Cadastro de Dieta**
3. **Grupo 3: Detalhes da Dieta**
4. **Grupo 4: Cadastro de Opção de Dieta**
5. **Grupo 5: Listagem de Alimentos por Opção**
6. **Grupo 6: Cadastro de Alimento**
7. **Grupo 7: Gerenciamento de Alimentos Restritos**
8. **Grupo 8: Gerenciamento de Snacks**

Esses grupos são apresentados em uma estrutura visual que prioriza a navegabilidade e o apelo estético, com funcionalidades como adicionar e editar implementadas em pop-ups para manter o usuário no contexto da página, evitando redirecionamentos desnecessários.

---

## Integração com o Header

O componente Header, descrito em detalhes no arquivo `HEADER_DOCS.md`, é um elemento essencial da aplicação VeTech e desempenha um papel crítico na **Página de Dietas**. Ele não é apenas uma "nova feature" ou um detalhe secundário, mas sim uma funcionalidade central que controla o estado global da aplicação, especialmente por meio do **dropdown de seleção de animal**. Para esta página, a interação com o header é **obrigatória**, pois a seleção de um animal é um pré-requisito para o funcionamento adequado de todos os grupos de funcionalidades. Abaixo, detalho essa integração:

### Funcionalidade do Header na Página de Dietas
- **Dropdown de Seleção de Animal:** Localizado no header, este componente permite ao usuário escolher um animal específico da clínica (ex: "Rex", "Luna") antes de interagir com a página. Ele consome a API `GET /api/v1/animals` para listar os animais cadastrados, atualizando dinamicamente conforme a busca do usuário.
- **Estado Global (`selectedAnimal`):** O animal selecionado é armazenado no `AnimalContext`, um contexto global do React, e afeta diretamente o comportamento da Página de Dietas:
  - **Sem animal selecionado:** A página exibe uma mensagem bloqueante, como "Por favor, selecione um animal no header para gerenciar dietas", e desabilita ações como criar ou visualizar dietas.
  - **Com animal selecionado:** Todos os grupos de funcionalidades (listagem, cadastro, etc.) são ativados e exibem dados relativos ao animal escolhido, como suas dietas, alimentos restritos e snacks.
- **Visibilidade do Dropdown:** Conforme o documento `HEADER_DOCS.md`, a Página de Dietas é classificada como uma "tela que exige seleção de animal". Assim, o dropdown permanece visível e funcional enquanto o usuário estiver nesta página, garantindo que o contexto do animal esteja sempre claro.

### Impacto no Fluxo do Usuário
- Ao acessar a Página de Dietas pelo menu lateral (link "Dietas" no header), o usuário deve primeiro selecionar um animal no dropdown do header.
- Exemplo: Se o usuário escolhe "Rex", o estado `selectedAnimal` é atualizado, e a API `GET /api/v1/animals/{animal_id}/diets` é chamada para carregar as dietas de "Rex" no Grupo 1.
- Qualquer tentativa de cadastrar uma dieta ou interagir com outros grupos sem um animal selecionado resulta em feedback imediato (mensagem ou bloqueio), reforçando a dependência do header.

### Detalhes Técnicos do Header
- **Componente React:** O `AppHeader` é reutilizável e gerencia a navegação principal (ex: links para "Início", "Dietas", "Atividades") e o estado do animal.
- **Autenticação:** Todas as requisições disparadas pelo dropdown (como listar animais) incluem o token JWT no header `Authorization`.
- **Estilização:** Usa Material UI para um design consistente com o restante da aplicação, com um dropdown estilizado e responsivo.

Essa integração detalhada com o header assegura que a Página de Dietas funcione de forma contextualizada e segura, alinhada às necessidades da clínica veterinária.

---

## Design Intuitivo e Atratativo

A Página de Dietas é uma das mais importantes do sistema, pois incentiva os usuários a criar e gerenciar planos alimentares de forma eficiente e prazerosa. Por isso, o design não deve ser apenas funcional, mas também **extremamente atrativo**, com elementos visuais que motivem o uso contínuo. Aqui estão as diretrizes e sugestões para alcançar esse objetivo:

### Princípios de Design
- **Intuitividade:** A organização dos grupos deve seguir uma lógica natural (ex: listagem como ponto de entrada, cadastros em pop-ups acessíveis), com navegação clara e feedback visual constante.
- **Atratividade:** Componentes bonitos e chamativos são essenciais para engajar o usuário, transmitindo uma sensação de cuidado e profissionalismo.

### Elementos Visuais Sugeridos
- **Ícones Representativos:** Cada grupo pode ter um ícone associado (ex: prato para dietas, sinal de proibição para alimentos restritos, osso para snacks), tornando a interface mais visual e amigável.
- **Cores Vibrantes:** Uma paleta com tons de verde (saúde), azul (confiança) e amarelo (energia) para botões e destaques, combinada com fundos neutros para não sobrecarregar.
- **Layouts Modernos:** Uso de cards com sombras sutis, espaçamento generoso e tabelas responsivas para uma apresentação limpa e organizada.
- **Componentes Estilizados:** Botões com efeitos de hover (ex: leve aumento ou mudança de cor), pop-ups com animações suaves de entrada/saída, e gráficos simples (ex: barras de calorias).
- **Feedback Visual:** Spinners coloridos durante carregamentos, mensagens de sucesso com ícones (ex: check verde) e erros destacados em vermelho.

### Benefícios Esperados
Esses elementos não só facilitam a interação, mas também tornam a experiência mais agradável, motivando veterinários e nutricionistas a usar a página regularmente para planejar dietas criativas e bem estruturadas.

---

## Grupo 1: Listagem de Dietas por Animal

### Descrição
O **Grupo de Listagem de Dietas por Animal** é o ponto de entrada da Página de Dietas, exibindo uma visão geral das dietas associadas ao animal selecionado no header. Projetado como uma área principal e sempre visível ao carregar a página, ele permite monitoramento rápido e ações como cadastrar ou visualizar detalhes, tudo em uma interface interativa.

### Componentes
- **Tabela de Dietas:** Colunas configuráveis:
  - Tipo ("Caseira", "Industrializada")
  - Objetivo ("Emagrecimento", "Manutenção")
  - Data de Início (DD/MM/AAAA)
  - Data de Fim (DD/MM/AAAA ou "Em andamento")
  - Status ("Ativa" em verde, "Finalizada" em cinza)
  - Ações ("Visualizar", "Editar", "Excluir")
- **Campo de Busca:** Pesquisa em tempo real por tipo ou objetivo.
- **Filtros Avançados:** Dropdowns para status e datas.
- **Botão "Nova Dieta":** No canto superior direito, abre o Grupo 2 em um pop-up.
- **Paginação:** Até 10 dietas por página.
- **Indicador de Carregamento:** Spinner estilizado.

### Funcionalidades
- **Carregamento:** `GET /api/v1/animals/{animal_id}/diets` lista as dietas do animal selecionado.
- **Busca e Filtro:** Suporta filtragem via API (ex: `GET /api/v1/animals/{animal_id}/diets?status=ativa`).
- **Ações:**
  - Visualizar: Abre Grupo 3 em pop-up.
  - Editar: Abre Grupo 2 em pop-up com dados preenchidos.
  - Excluir: Modal de confirmação + `DELETE /api/v1/diets/{diet_id}`.

### Fluxo de Uso do Usuário
1. Usuário seleciona "Rex" no header.
2. Tabela carrega dietas de "Rex" (ex: "Dieta Caseira", Status: "Ativa").
3. Filtra por "Ativa" ou busca "Emagrecimento".
4. Clica em "Nova Dieta" para abrir pop-up de cadastro.

---

## Grupo 2: Cadastro de Dieta

### Descrição
O **Grupo de Cadastro de Dieta** permite criar novos planos alimentares em um pop-up intuitivo, mantendo o usuário no contexto da Página de Dietas. O formulário é simples e validado, ideal para registrar dietas rapidamente.

### Componentes
- **Formulário:**
  - Tipo: Dropdown ("Caseira", "Mista", obrigatório)
  - Objetivo: Dropdown ("Emagrecimento", "Ganho de Peso", obrigatório)
  - Data de Início: Seletor de data (obrigatório)
  - Data de Fim: Seletor opcional
  - Status: Dropdown ("Ativa", "Finalizada", padrão "Ativa")
- **Botões:** "Salvar" (envia dados) e "Cancelar" (fecha pop-up).
- **Mensagens de Erro:** Abaixo dos campos (ex: "Tipo é obrigatório").

### Funcionalidades
- **Envio:** `POST /api/v1/animals/{animal_id}/diets`.
- **Sucesso:** Fecha pop-up e atualiza Grupo 1.
- **Erro:** Exibe validações em tempo real.

### Fluxo de Uso do Usuário
1. No Grupo 1, clica em "Nova Dieta".
2. Preenche dados para "Rex" (ex: Tipo: "Caseira", Objetivo: "Emagrecimento").
3. Salva e vê a nova dieta na listagem.

---

## Grupo 3: Detalhes da Dieta

### Descrição
O **Grupo de Detalhes da Dieta** exibe informações completas de uma dieta em um pop-up, servindo como hub para ações relacionadas. Mostra dados básicos e opções associadas, com navegação para outros grupos.

### Componentes
- **Card de Dados:** Tipo, Objetivo, Datas, Status.
- **Tabela de Opções:** Nome, Valor Mensal, Calorias, Ações.
- **Botão "Adicionar Opção":** Abre Grupo 4 em pop-up.
- **Ações:** "Editar Dieta" e "Excluir Dieta".
- **Abas:** Links para Alimentos, Restrições, Snacks.

### Funcionalidades
- **Carregamento:** `GET /api/v1/diets/{diet_id}` e `GET /api/v1/diets/{diet_id}/options`.
- **Ações:** Editar abre pop-up, Excluir usa `DELETE /api/v1/diets/{diet_id}`.

### Fluxo de Uso do Usuário
1. No Grupo 1, clica em "Visualizar".
2. Vê detalhes de "Dieta Caseira" e opções como "Ração Light".
3. Adiciona ou edita opções via pop-up.

---

## Grupo 4: Cadastro de Opção de Dieta

### Descrição
O **Grupo de Cadastro de Opção de Dieta** adiciona opções específicas (ex: rações) em um pop-up, com um formulário detalhado e funcional.

### Componentes
- **Formulário:**
  - Nome (obrigatório)
  - Valor Mensal (opcional)
  - Calorias Totais (opcional)
  - Porção por Refeição (opcional)
  - Número de Refeições (opcional)
- **Botões:** "Salvar" e "Cancelar".

### Funcionalidades
- **Envio:** `POST /api/v1/diets/{diet_id}/options`.
- **Sucesso:** Atualiza Grupo 3.

### Fluxo de Uso do Usuário
1. No Grupo 3, clica em "Adicionar Opção".
2. Preenche "Ração Light" e salva.
3. Vê a opção na tabela de detalhes.

---

## Grupo 5: Listagem de Alimentos por Opção

### Descrição
O **Grupo de Listagem de Alimentos por Opção** mostra alimentos de uma opção em uma seção expansível ou pop-up, com opções de gerenciamento.

### Componentes
- **Tabela:** Nome, Tipo, Quantidade, Calorias, Horário, Ações.
- **Botão "Adicionar Alimento":** Abre Grupo 6 em pop-up.

### Funcionalidades
- **Carregamento:** `GET /api/v1/diet-options/{option_id}/foods`.
- **Ações:** Editar e Excluir (`DELETE /api/v1/diet-foods/{food_id}`).

### Fluxo de Uso do Usuário
1. No Grupo 3, acessa uma opção.
2. Vê alimentos como "Frango Cozido" e adiciona novos.

---

## Grupo 6: Cadastro de Alimento

### Descrição
O **Grupo de Cadastro de Alimento** registra alimentos em um pop-up, com campos detalhados para personalização.

### Componentes
- **Formulário:**
  - Nome (obrigatório)
  - Tipo (dropdown, obrigatório)
  - Quantidade (opcional)
  - Calorias (opcional)
  - Horário (opcional)
- **Botões:** "Salvar" e "Cancelar".

### Funcionalidades
- **Envio:** `POST /api/v1/diet-options/{option_id}/foods`.

### Fluxo de Uso do Usuário
1. No Grupo 5, clica em "Adicionar Alimento".
2. Cadastra "Frango Cozido" e salva.

---

## Grupo 7: Gerenciamento de Alimentos Restritos

### Descrição
O **Grupo de Gerenciamento de Alimentos Restritos** lista e gerencia alimentos a evitar, em uma seção integrada à página.

### Componentes
- **Tabela:** Nome, Motivo, Ações.
- **Botão "Adicionar":** Formulário inline ou pop-up.

### Funcionalidades
- **Rotas:** `GET`, `POST`, `PUT`, `DELETE` em `/api/v1/animals/{animal_id}/restricted-foods`.

### Fluxo de Uso do Usuário
1. Acessa a seção na página.
2. Adiciona "Chocolate" (Motivo: "Tóxico").

---

## Grupo 8: Gerenciamento de Snacks

### Descrição
O **Grupo de Gerenciamento de Snacks** controla snacks permitidos, em uma seção visualmente distinta.

### Componentes
- **Tabela:** Nome, Frequência, Quantidade, Observações, Ações.
- **Botão "Adicionar":** Formulário inline ou pop-up.

### Funcionalidades
- **Rotas:** `GET`, `POST`, `PUT`, `DELETE` em `/api/v1/animals/{animal_id}/snacks`.

### Fluxo de Uso do Usuário
1. Acessa a seção.
2. Adiciona "Bifinho" (3x/semana).

---

## Estrutura e Navegação
A Página de Dietas organiza os grupos em uma interface única:
- **Grupo 1:** Área principal, sempre visível.
- **Grupos 2-6:** Pop-ups para ações específicas.
- **Grupos 7-8:** Seções expansíveis ou abas.
Pop-ups minimizam navegação, mantendo o foco na página.

---

## Detalhes Técnicos
- **Rotas Backend:** Todas as rotas de `sprint4.md` foram incorporadas (ex: `POST /api/v1/animals/{animal_id}/diets`, `GET /api/v1/diet-options/{option_id}/foods`).
- **Autenticação:** Token JWT em todas as requisições.
- **Frontend:** React, React Router, Material UI, pop-ups com Material UI.

---

## Tarefas da Sprint
- Implementar a Página de Dietas com os oito grupos.
- Integrar o header com seleção obrigatória de animal.
- Desenvolver design atrativo com ícones, cores e pop-ups.
- Testar fluxos e integração com o backend.

-