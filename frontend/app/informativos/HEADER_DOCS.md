# Documentação do AppHeader e AnimalContext: Guia de Desenvolvimento Frontend

## 1. Introdução

O `AppHeader.jsx` é um componente React central e reutilizável na aplicação VeTech. Ele desempenha um papel fundamental na navegação principal, na identidade visual da plataforma e, crucialmente, no gerenciamento do estado global do **animal selecionado** através do `AnimalContext`.

Este documento serve como um guia para desenvolvedores frontend, detalhando a estrutura do header, o funcionamento do `AnimalContext`, e como as diversas telas da aplicação devem se integrar com a seleção de animal. A correta compreensão e implementação dessas diretrizes são essenciais para a consistência funcional e a experiência do usuário, especialmente para o desenvolvimento de novas features e sprints.

**Objetivos Principais do Header e Contexto:**
*   Fornecer navegação clara e acessível entre as principais seções da aplicação.
*   Permitir a seleção de um animal específico, cujo contexto influenciará o conteúdo e as funcionalidades de diversas telas.
*   Manter a consistência da interface do usuário, garantindo que o dropdown de seleção de animal esteja presente e funcional conforme esperado em cada tela.

---

## 2. Estrutura do Componente `AppHeader.jsx`

O header é composto por:

### 2.1. Logotipo e Identidade Visual
*   Exibe o logotipo da VeTech.

### 2.2. Navegação Principal (Links do Menu)
*   Facilita o acesso às telas chave do sistema. Os links devem ser atualizados conforme novas seções são adicionadas:
    *   **Início (Dashboard)** (`/inicio`)
    *   **Animais** (`/animais`)
    *   **Agendamentos** (`/agendamentos`)
    *   **Dietas** (`/dietas`)
    *   **Atividades** (Agrupador para telas da Sprint 5, e.g., `/tipos-atividades`, `/planos-atividades`)
    *   **Gamificação** (Agrupador para telas da Sprint 6, e.g., `/metas-gamificacao`, `/ranking-pets`)
    *   **Consultas** (`/consultas`) - *implementar*
    *   **Resultados** (`/resultados`) - *implementar*
    *   **Perfil do Usuário** (`/perfil`)

### 2.3. Dropdown de Seleção de Animal
*   Este é o componente mais dinâmico do header, permitindo ao usuário selecionar um animal da lista associada à clínica.
*   A seleção (ou ausência de seleção) de um animal é gerenciada pelo `AnimalContext`.
*   A lista de animais no dropdown é populada pelos dados obtidos através do `AnimalContext`, que por sua vez busca os animais da clínica logada.

---

## 3. Contexto do Animal (`AnimalContext`)

O `AnimalContext` é o mecanismo central para compartilhar o estado do animal selecionado em toda a aplicação.

### 3.1. Funcionamento
*   **Provedor:** O `AnimalProvider` envolve os componentes que precisam de acesso ao contexto do animal (normalmente, em um nível superior da árvore de componentes, como no `App.jsx` ou `MainLayout.jsx`).
*   **Consumidores:** Componentes e páginas utilizam o hook `useAnimal()` para acessar os seguintes valores e funções:
    *   `selectedAnimal`: Objeto contendo os dados do animal atualmente selecionado (ou `null` se nenhum animal estiver selecionado).
    *   `animals`: Array com a lista de todos os animais da clínica, usados para popular o dropdown no header.
    *   `selectAnimal(animal)`: Função para atualizar o `selectedAnimal`. É chamada pelo dropdown no `AppHeader`.
    *   `loadingAnimals`: Booleano que indica se a lista de animais está sendo carregada.
    *   `animalError`: Possíveis erros ao carregar a lista de animais.

### 3.2. Como é Utilizado
1.  O `AppHeader.jsx` usa `useAnimal()` para exibir o dropdown com a `animals` e para chamar `selectAnimal()` quando o usuário escolhe um pet.
2.  As páginas individuais (como `DietsPage.jsx`, `AppointmentsPage.jsx`, etc.) usam `useAnimal()` para obter o `selectedAnimal`.
3.  Com base no `selectedAnimal`, a página decide:
    *   Se pode renderizar seu conteúdo principal (para telas de dependência obrigatória).
    *   Como filtrar os dados a serem exibidos (para telas de dependência opcional).
    *   Quais parâmetros enviar para as chamadas de API (e.g., `animal_id`).

---

## 4. Integração do Header e `AnimalContext` com as Telas da Aplicação

As telas da aplicação são categorizadas com base em como interagem com a seleção de animal no header. É crucial que todas as novas telas sejam projetadas considerando uma destas categorias. O dropdown de seleção de animal deve estar presente em *todas* as telas após o login, para consistência da UI e para permitir que o usuário mude o contexto do animal a qualquer momento. A diferença reside em como cada tela *reage* a essa seleção.

### 4.1. Telas que **Exigem** Seleção de Animal

*   **Descrição:** Estas telas não podem funcionar ou exibir seu conteúdo principal sem que um animal específico esteja selecionado no header.
*   **Comportamento Esperado:**
    *   **Com animal selecionado:** A tela busca e exibe dados específicos do `selectedAnimal.id`. Todas as operações (CRUD) são realizadas no contexto deste animal.
    *   **Sem animal selecionado (`selectedAnimal` é `null`):**
        *   A funcionalidade principal da tela deve ser bloqueada.
        *   Uma mensagem clara deve ser exibida ao usuário, instruindo-o a selecionar um animal no header (ex: \"Por favor, selecione um animal no header para visualizar as dietas.\").
        *   Não devem ser feitas chamadas de API que dependam de um `animal_id`.


### 4.2. Telas com Seleção de Animal **Opcional**

*   **Descrição:** Estas telas podem funcionar com ou sem um animal selecionado. A seleção de um animal geralmente filtra os dados exibidos ou altera o escopo das operações.
*   **Comportamento Esperado:**
    *   **Com animal selecionado:** A tela filtra os dados para mostrar apenas informações relevantes ao `selectedAnimal.id`. As chamadas de API incluem o `animal_id` como filtro.
    *   **Sem animal selecionado (`selectedAnimal` é `null`):** A tela exibe informações mais gerais ou agregadas (ex: dados de todos os animais da clínica). As chamadas de API não incluem `animal_id` ou o backend lida com a ausência desse filtro para retornar dados globais da clínica.
*   **Exemplos de Telas:**
    *   `AppointmentsPage.jsx` (Sprint 3): Mostra agendamentos do animal selecionado ou todos da clínica.
    *   `ConsultasPage.jsx` (a ser desenvolvida): Similar aos agendamentos.

---

## 5. Diretrizes para Desenvolvimento de Novas Telas

Ao desenvolver novas telas ou funcionalidades, siga estas diretrizes:

1.  **Determinar a Categoria da Tela:** Classifique a nova tela em uma das três categorias acima (Obrigatória, Opcional, Não Afetada).

2.  **Chamadas de API:**
    *   Para telas Obrigatórias e Opcionais (com animal selecionado), passe o `selectedAnimal.id` para os serviços e, subsequentemente, para as rotas do backend que esperam um `animal_id`.
    *   Garanta que os serviços (ex: `dietService.js`, `activityService.js`) possam aceitar `animal_id` como parâmetro em suas funções.

3.  **Interface do Usuário (UI):**
    *   O dropdown de seleção de animal no `AppHeader` deve estar sempre visível e funcional após o login.
    *   Se a tela for da categoria \"Obrigatória\" e nenhum animal estiver selecionado, forneça feedback claro ao usuário.
    *   Use indicadores de carregamento (`loading`, `loadingAnimals`) para melhorar a UX durante a busca de dados.


