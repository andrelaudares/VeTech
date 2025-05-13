# Documentação do Componente AppHeader

## 1. Introdução

O Header é um componente essencial na aplicação VeTech, desenvolvido em React como um elemento reutilizável. Ele serve como o principal ponto de navegação entre as telas do sistema e controla estados globais que afetam o comportamento de várias páginas, especialmente através da funcionalidade de escolha de animal. Sua correta implementação e integração são fundamentais para o funcionamento consistente da aplicação, e os desenvolvedores devem estar atentos à sua influência ao criar cada tela individualmente.


- **Objetivo:** Fornecer navegação, identidade visual e controle de estado global (como o animal selecionado).

---

## 2. Estrutura do Header

O header é composto por três elementos principais:

### 2.1. Navegação Principal
O header oferece acesso às seguintes telas do sistema:

- **Tela Inicial (Dashboard)** - Já desenvolvida
- **Tela de Animais**
- **Tela de Agendamento**
- **Tela de Consulta**
- **Tela de Dietas**
- **Tela de Atividades**
- **Tela de Resultados**
- **Tela de Perfil do Usuário** - Já desenvolvida

Atualmente, apenas o botão "Início" está implementado, redirecionando para `/inicio`. Os links para as demais telas serão adicionados conforme o desenvolvimento avança.

---

## 3. Integração com as Telas

O header influencia diretamente o comportamento das telas, especialmente por meio da seleção de animal. As telas podem ser classificadas em três categorias:

### 3.1. Telas que Exigem Seleção de Animal
- **Tela de Dietas**
- **Tela de Atividades**
- **Tela de Resultados**

Nessas telas, a seleção de um animal é obrigatória. Se nenhum animal for selecionado, a tela deve bloquear ações ou exibir uma mensagem como "Por favor, selecione um animal no header".

### 3.2. Telas com Seleção Opcional

- **Tela de Agendamento**
- **Tela de Consulta**

Nessas telas, a seleção de um animal é opcional:
- **Sem animal selecionado:** Mostra informações gerais ou de todos os animais da clínica.
- **Com animal selecionado:** Filtra os dados para exibir apenas informações do animal escolhido.

### 3.3. Telas Não Afetadas
- **Tela de Animais**
- **Tela Inicial**
- **Tela de Perfil do Usuário**

Essas telas não mudam de estado com a seleção de animal e não dependem do dropdown.
