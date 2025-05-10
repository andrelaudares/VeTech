# Documentação do Componente AppHeader

## Visão Geral

O `AppHeader.jsx` é um componente React reutilizável responsável por renderizar o cabeçalho principal da aplicação VeTech após o login do usuário. Ele fornece navegação consistente, identidade visual e funcionalidades globais como seleção de animal e acesso ao perfil do usuário.

## Localização

`frontend/app/src/components/AppHeader.jsx`

## Funcionalidades Principais

1.  **Identidade Visual:**
    *   Exibe o logo da VeTech.
    *   Exibe o título "VeTech Painel". Clicar no logo ou no título navega para a página inicial (`/inicio`).

2.  **Navegação Principal:**
    *   Contém links/botões para as seções principais da aplicação.
    *   Atualmente implementado: Botão "Início" (leva para `/inicio`).
    *   *Ponto de Extensão:* Novos links para seções como "Animais", "Agendamentos", "Consultas", "Dietas", etc., podem ser adicionados aqui.

3.  **Seleção Global de Animal:**
    *   Apresenta um dropdown (`Select` do Material UI) que permite ao usuário selecionar um animal específico da sua clínica.
    *   A lista de animais é carregada dinamicamente através do `AnimalContext` (`fetchAnimals`).
    *   Quando um animal é selecionado, o estado `selectedAnimal` no `AnimalContext` é atualizado.
    *   **Exibição Condicional:** O seletor de animal não é exibido em certas páginas (configurado na variável `noAnimalSelectorPages`), como "/perfil" e "/inicio".
    *   Este animal selecionado fica disponível globalmente para outras páginas e componentes através do hook `useAnimal()`.

4.  **Menu do Usuário:**
    *   Exibe o nome do usuário logado (obtido do `AuthContext`).
    *   Apresenta um ícone de avatar/perfil.
    *   Ao clicar no ícone, um menu (`Menu` do Material UI) é aberto com as seguintes opções:
        *   **Perfil:** Navega para a página de perfil do usuário (`/perfil`).
        *   **Sair:** Executa a função `logout` do `AuthContext` e redireciona para a página de login (`/login`).

## Dependências de Contexto

*   **`AuthContext` (`useAuth()`):**
    *   Para obter informações do `user` logado (como nome).
    *   Para acessar a função `logout`.
*   **`AnimalContext` (`useAnimal()`):**
    *   Para obter a lista de `animals` da clínica.
    *   Para obter e definir o `selectedAnimal`.
    *   Para acessar a função `fetchAnimals` para carregar os animais.

## Uso nas Páginas

As páginas que necessitam deste cabeçalho devem simplesmente renderizar o componente `<AppHeader />` no topo de sua estrutura JSX. O `AnimalProvider` e `AuthProvider` devem estar configurados em um nível superior na árvore de componentes (geralmente em `main.jsx` ou `App.jsx`).

## Lógica de Exibição do Seletor de Animal

A variável `noAnimalSelectorPages` (uma array de strings de rotas) dentro do `AppHeader.jsx` controla em quais páginas o dropdown de seleção de animal *não* deve ser exibido. A visibilidade é determinada comparando `location.pathname` (da rota atual) com esta lista.

## Como as Páginas Utilizam o Animal Selecionado

As páginas que precisam reagir à seleção de um animal (ex: Tela de Dietas, Tela de Atividades) devem:
1.  Importar o hook `useAnimal` do `AnimalContext`.
2.  Chamar `const { selectedAnimal } = useAnimal();` para obter o animal atualmente selecionado.
3.  Usar o objeto `selectedAnimal` (que pode ser o objeto do animal ou `null`) para filtrar dados, fazer requisições específicas ou adaptar a UI.

## Futuras Extensões Possíveis

*   Adicionar mais itens de navegação principal (links diretos ou um menu dropdown de navegação).
*   Integrar notificações.
*   Alterar dinamicamente o título "VeTech Painel" para refletir a seção atual, se desejado.
*   Melhorar a interface do seletor de animais (ex: pesquisa/autocomplete se a lista for muito grande). 