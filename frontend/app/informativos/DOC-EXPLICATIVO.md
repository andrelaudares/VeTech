# Documentação - VeTech Frontend

## Estrutura do Projeto

O projeto frontend do VeTech foi construído utilizando React com Vite, uma ferramenta moderna de build que proporciona um ambiente de desenvolvimento mais rápido e eficiente. A estrutura organizacional do projeto foi pensada para facilitar a manutenção e escalabilidade, seguindo boas práticas de desenvolvimento React.

```
frontend/app/
├── node_modules/          # Dependências do projeto
├── public/                # Arquivos estáticos
├── src/                   # Código-fonte principal
│   ├── assets/            # Imagens, fontes e outros recursos
│   ├── components/        # Componentes React reutilizáveis
│   ├── contexts/          # Contextos da Context API
│   ├── hooks/             # Hooks personalizados
│   ├── pages/             # Componentes de páginas principais
│   ├── routes/            # Configuração de rotas
│   ├── services/          # Serviços de API e lógica de negócios
│   ├── styles/            # Estilos globais (se necessário)
│   ├── utils/             # Funções utilitárias
│   ├── App.jsx            # Componente principal da aplicação
│   ├── App.css            # Estilos do componente App
│   ├── main.jsx           # Ponto de entrada da aplicação
│   └── index.css          # Estilos globais (incluindo Tailwind)
├── .gitignore             # Arquivos e pastas ignorados pelo Git
├── index.html             # HTML principal
├── package.json           # Dependências e scripts do projeto
├── postcss.config.js      # Configuração do PostCSS
├── tailwind.config.js     # Configuração do Tailwind CSS
└── vite.config.js         # Configuração do Vite
```

## Tecnologias Utilizadas

- **React**: Biblioteca JavaScript para construção de interfaces de usuário
- **React Router**: Para navegação entre páginas
- **Context API**: Para gerenciamento de estado global (autenticação)
- **Axios**: Para requisições HTTP
- **React Hook Form**: Para gerenciamento e validação de formulários
- **Tailwind CSS**: Framework de CSS utilitário para estilização
- **Vite**: Ferramenta de build

## Principais Arquivos e Suas Funções

### 1. Context API (Autenticação)

**`src/contexts/AuthContext.jsx`**

Este arquivo é o coração do sistema de autenticação. Ele:

- Cria e exporta o `AuthContext` e `AuthProvider`
- Gerencia o estado do usuário logado e do token JWT
- Implementa funções de `login` e `logout`
- Verifica automaticamente a existência de um token salvo ao iniciar a aplicação
- Configura o Axios para enviar o token em todas as requisições
- Recupera o perfil do usuário quando existe um token válido

```jsx
// Exemplo simplificado
const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('viteToken'));
  // Implementação das funções de login, logout, etc.
  
  return (
    <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
};
```

### 2. Serviços de API

**`src/services/api.js`**
- Configura a instância base do Axios com a URL da API
- Ponto central para configurações como interceptors, headers padrão, etc.

**`src/services/authService.js`**
- Implementa funções para comunicação com endpoints de autenticação
- Métodos: `login`, `register`, `logout`

**`src/services/clinicService.js`**
- Implementa funções para comunicação com endpoints relacionados à clínica
- Métodos: `getProfile`, `updateProfile`

### 3. Configuração de Rotas

**`src/routes/index.jsx`**
- Define todas as rotas da aplicação
- Implementa proteção de rotas com `ProtectedRoute`
- Configura redirecionamentos baseados no estado de autenticação

### 4. Páginas Principais

**`src/pages/LoginPage.jsx`**
- Formulário de login com validação
- Interface atraente com gradiente e elementos estilizados
- Feedback visual para erros e estado de carregamento

**`src/pages/DashboardPage.jsx`**
- Página inicial após login
- Layout com menu lateral e cards informativos
- Implementa o botão de logout

**`src/pages/ProfilePage.jsx`**
- Exibe os dados da clínica
- Implementa o modal de edição do perfil
- Demonstra a integração completa com a API

### 5. Ponto de Entrada da Aplicação

**`src/main.jsx`**
- Configura o React Strict Mode
- Envolve a aplicação com o `BrowserRouter` e `AuthProvider`
- Renderiza o componente App

## Fluxo de Autenticação

1. **Inicialização**:
   - O `AuthProvider` verifica se existe um token JWT no `localStorage`
   - Se existir, configura o Axios e tenta buscar o perfil do usuário
   - Se o token for inválido, faz logout

2. **Login**:
   - Usuário submete o formulário de login
   - `authService.login()` é chamado
   - Se bem-sucedido, o token é armazenado no `localStorage`
   - O usuário é redirecionado para o Dashboard

3. **Requisições Autenticadas**:
   - O token é automaticamente incluído no header `Authorization` do Axios
   - Se uma requisição falhar por token inválido, o usuário é deslogado

4. **Logout**:
   - `authService.logout()` é chamado
   - O token é removido do `localStorage`
   - O estado de usuário e token são limpos
   - O usuário é redirecionado para login

## Proteção de Rotas

O componente `ProtectedRoute` garante que apenas usuários autenticados possam acessar determinadas páginas:

```jsx
const ProtectedRoute = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};
```

## Estilização

O projeto utiliza Tailwind CSS, configurado via `tailwind.config.js` e `postcss.config.js`. A abordagem de estilização é baseada em classes utilitárias, que oferecem:

- Desenvolvimento mais rápido
- Estilos consistentes
- Menos arquivos CSS
- Responsividade simplificada

## Como Executar o Projeto

```bash
# Navegar até a pasta do projeto
cd frontend/app

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev
```

## Próximos Passos

1. **Sprint 2 - Gestão de Animais**: Implementar as telas de listagem, cadastro, detalhes, edição e preferências alimentares de animais.

2. **Melhorias Potenciais**:
   - Adicionar testes unitários e de integração
   - Implementar sistema de refresh token
   - Adicionar animações e transições para melhor UX
   - Criar versão mobile responsiva
   - Implementar internacionalização
   - Adicionar tema escuro/claro

## Conclusão

O frontend do VeTech foi desenvolvido seguindo boas práticas de organização, segurança e experiência do usuário. A estrutura modular permite fácil manutenção e expansão futura, enquanto o sistema de autenticação robusto garante que apenas usuários autorizados acessem as funcionalidades protegidas.

A escolha de tecnologias modernas como React, Context API, React Router, Tailwind CSS e Vite proporciona uma base sólida para o crescimento do projeto, com foco em performance e experiência do desenvolvedor. 