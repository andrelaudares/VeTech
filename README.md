# FinanceAI

O **FinanceAI** éum sistema com  **FastAPI** com **Supabase** no backend. Este projeto foi desenvolvido para fornecer uma interface de autenticação robusta e segura, permitindo o registro e login de usuários.

## Estrutura do Projeto~


   ```

 FinanceAI/
├── backend/ # API FastAPI
│ ├── app/
│ │ ├── api/ # Rotas da API
│ │ ├── core/ # Configurações e utilitários
│ │ ├── db/ # Conexão com banco de dados
│ │ └── models/ # Modelos de dados
│ ├── main.py # Ponto de entrada da API
│ └── requirements.txt # Dependências do backend
├── frontend/ # Interface React
│ ├── public/
│ ├── src/
│ │ ├── components/ # Componentes React
│ │ ├── pages/ # Páginas da aplicação
│ │ ├── services/ # Serviços de API
│ │ └── types/ # Tipos TypeScript
│ └── package.json # Dependências do frontend
└── .env # Variáveis de ambiente
  

   ```


## Tecnologias Utilizadas

- **Backend:**
  - **FastAPI**: Um framework moderno e rápido para construir APIs com Python.
  - **Supabase**: Uma plataforma de backend como serviço que fornece autenticação, banco de dados e armazenamento.
  - **Pydantic**: Para validação de dados e criação de modelos.
  - **httpx**: Para realizar requisições HTTP assíncronas.
  - **bcrypt**: Para hashing de senhas.

- **Frontend:**
  - **React**: Biblioteca JavaScript para construir interfaces de usuário.
  - **Axios**: Para realizar requisições HTTP ao backend.

## Funcionalidades

### Autenticação

- **Registro de Usuários**: Permite que novos usuários se registrem com validação de dados.
- **Login**: Usuários podem autenticar-se usando email e senha.
- **Proteção de Rotas**: Rotas autenticadas garantem que apenas usuários logados possam acessá-las.
- **Logout**: Usuários podem sair de suas contas.

### Estrutura do Backend

O backend é estruturado em várias pastas para melhor organização:

- **app/api**: Contém as rotas da API, incluindo autenticação.
- **app/core**: Configurações e utilitários, como variáveis de ambiente.
- **app/db**: Gerencia a conexão com o banco de dados Supabase.
- **app/models**: Define os modelos de dados utilizados na aplicação.

### Configuração do Banco de Dados (Supabase)

Antes de executar o projeto, certifique-se de:

1. Criar uma conta no Supabase e um projeto.
2. Configurar as credenciais no arquivo `.env`.
3. Criar a tabela `profiles` com os seguintes campos:
   - `id` (UUID, chave primária, referência para `auth.users`)
   - `email` (TEXT, único)
   - `name` (TEXT)
   - `phone` (TEXT)
   - `created_at` (TIMESTAMP)

### Configuração do Backend (FastAPI)

1. Navegue até a pasta do backend:
   ```bash
   cd backend
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o servidor:
   ```bash
   python main.py
   ```

   O backend estará disponível em `http://localhost:8000`.

### Configuração do Frontend (React)

1. Navegue até a pasta do frontend:
   ```bash
   cd frontend
   ```

2. Instale as dependências:
   ```bash
   npm install
   ```

3. Execute o servidor de desenvolvimento:
   ```bash
   npm start
   ```

   O frontend estará disponível em `http://localhost:3000`.

## Conclusão

O **FinanceAI** é uma aplicação que demonstra como integrar um frontend React com um backend FastAPI, utilizando Supabase para gerenciar autenticação e dados. Este projeto é uma base sólida para construir aplicações mais complexas e escaláveis.

## Contribuições

Sinta-se à vontade para contribuir com melhorias ou correções. Para isso, basta abrir um pull request ou issue.
