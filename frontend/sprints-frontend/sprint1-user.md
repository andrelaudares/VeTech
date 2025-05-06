# Sprint 1: Autenticação e Perfil

**Objetivo:** Criar a base de autenticação e gerenciamento de perfil da clínica, permitindo que os usuários façam login de forma segura e gerenciem suas informações básicas no sistema.

---

## Telas

### 1. Tela de Login

- **Descrição:**  
  Esta é a tela inicial do sistema, projetada para autenticar os usuários (representantes da clínica) de maneira simples e segura. A interface é minimalista, destacando o formulário de login e o branding da VeTech, para transmitir confiança e profissionalismo. O objetivo é garantir que o acesso ao sistema seja rápido e intuitivo, com feedback claro em caso de sucesso ou erro.

- **Componentes:**  
  - Campo de texto para email (com placeholder "Digite seu email").  
  - Campo de senha (com opção de ocultar/mostrar a senha).  
  - Botão "Entrar" (estilizado em azul, destacado visualmente).  
  - Link "Esqueci minha senha" (em texto menor, clicável, mas sem funcionalidade nesta sprint).  
  - Logo da VeTech no topo da tela.  

- **Funcionalidade:**  
  - O formulário coleta email e senha do usuário.  
  - Ao clicar em "Entrar", o sistema envia uma requisição POST para o endpoint `/api/v1/auth/login` com os dados inseridos.  
  - Se as credenciais forem válidas, a API retorna um token JWT, que é armazenado no `localStorage` para autenticação futura.  
  - O usuário é redirecionado automaticamente para a rota `/dashboard`.  
  - Em caso de erro (credenciais inválidas ou falha na API), uma mensagem de erro é exibida abaixo do formulário (ex: "Email ou senha incorretos").  

- **Fluxo de Uso do Usuário:**  
  1. O usuário acessa o sistema pela URL base (ex: `https://vetech-app.com/`).  
  2. Visualiza a tela de login com o logo da VeTech e o formulário centralizado.  
  3. Insere seu email cadastrado (ex: `clinica@example.com`) no campo correspondente.  
  4. Digita sua senha no campo de senha, podendo clicar em um ícone para visualizar os caracteres, se desejar.  
  5. Clica no botão "Entrar".  
  6. Durante o processamento, um ícone de carregamento (loader) aparece no botão.  
  7. Se as credenciais estiverem corretas, o usuário é redirecionado para o dashboard da clínica.  
  8. Se as credenciais estiverem incorretas, uma mensagem de erro aparece, e o usuário pode tentar novamente.  
  9. Caso tenha esquecido a senha, o usuário pode clicar em "Esqueci minha senha" (nesta sprint, o link apenas exibe um alerta informando que a funcionalidade estará disponível em breve).  

---

### 2. Tela de Perfil da Clínica

- **Descrição:**  
  Esta tela permite que a clínica visualize e edite suas informações cadastrais de forma organizada e prática. Ela foi desenhada para ser uma interface clara, onde os dados são apresentados em um formato visualmente acessível, com a opção de edição disponível para ajustes rápidos. O foco é oferecer uma experiência fluida, com feedback imediato após alterações, reforçando a confiabilidade do sistema.

- **Componentes:**  
  - Card ou seção estilizada contendo os dados da clínica:  
    - Nome da clínica (ex: "Clínica Vet Amigo").  
    - Email (ex: "clinica@example.com", não editável).  
    - Telefone (ex: "(11) 98765-4321").  
    - Plano de assinatura (ex: "Básico", não editável).  
  - Botão "Editar" (ao lado do card, em destaque).  
  - Modal de edição (aberto ao clicar em "Editar"), contendo:  
    - Campo de texto para nome da clínica (pré-preenchido).  
    - Campo de texto para telefone (pré-preenchido, com máscara para formato).  
    - Botão "Salvar" (em azul).  
    - Botão "Cancelar" (em cinza, para fechar o modal sem salvar).  

- **Funcionalidade:**  
  - Ao carregar a tela, uma requisição GET é enviada para `/api/v1/clinic/profile` para buscar os dados atuais da clínica autenticada.  
  - Os dados retornados são exibidos no card de perfil.  
  - Ao clicar em "Editar", um modal aparece com os campos nome e telefone preenchidos com os valores atuais.  
  - Após alterações, o botão "Salvar" envia uma requisição PUT para `/api/v1/clinic/profile` com os novos dados.  
  - Se a atualização for bem-sucedida, o modal é fechado, e o card reflete os dados atualizados.  
  - Em caso de erro (ex: telefone inválido), uma mensagem de erro aparece no modal.  

- **Fluxo de Uso do Usuário:**  
  1. Após o login, o usuário navega até a tela de perfil via menu (ex: clicando em "Perfil" na barra lateral).  
  2. Visualiza os dados atuais da clínica exibidos em um card (nome, email, telefone, plano).  
  3. Decide alterar informações e clica no botão "Editar".  
  4. Um modal é aberto, mostrando os campos editáveis (nome e telefone) já preenchidos com os valores atuais.  
  5. O usuário modifica o nome (ex: de "Clínica Vet Amigo" para "Vet Amigo SP") e/ou o telefone (ex: de "(11) 98765-4321" para "(11) 91234-5678").  
  6. Clica em "Salvar" para enviar as alterações.  
  7. Durante o processamento, um loader aparece no botão "Salvar".  
  8. Se bem-sucedido, o modal fecha, e o card na tela principal exibe os novos dados.  
  9. Se houver erro (ex: telefone com formato inválido), uma mensagem aparece no modal (ex: "Telefone deve seguir o formato (XX) XXXXX-XXXX").  
  10. Caso desista das alterações, o usuário clica em "Cancelar", e o modal é fechado sem salvar nada.  

---

## Detalhes Técnicos

- **Autenticação:**  
  - Uso de Context API para gerenciar o estado global de autenticação.  
  - Token JWT armazenado no `localStorage` e enviado via header `Authorization: Bearer <token>` em todas as requisições autenticadas.  
  - Interceptor no Axios para adicionar o token automaticamente.  

- **Roteamento:**  
  - React Router configurado com:  
    - `/` para tela de login.  
    - `/dashboard` como destino pós-login.  
    - `/perfil` para a tela de perfil.  

- **UI/UX:**  
  - Login: Logo VeTech centralizado no topo, formulário em um card com bordas arredondadas.  
  - Perfil: Card com dados em fonte legível, botão "Editar" com ícone de lápis, modal com espaçamento confortável.  

- **Validação:**  
  - Login: Email e senha obrigatórios; email deve conter "@" e domínio válido.  
  - Perfil: Nome não vazio; telefone com máscara e validação de formato (ex: "(XX) XXXXX-XXXX").  

- **Feedback:**  
  - Loader durante requisições (login e salvar perfil).  
  - Mensagens de erro/sucesso (ex: "Login realizado com sucesso", "Dados salvos com sucesso").  

- **Segurança:**  
  - Rotas protegidas: sem token válido, redireciona para login.  
  - Senhas criptografadas pela API (não manipuladas no frontend).  

- **Responsividade:**  
  - Design otimizado para desktops e tablets (telas de 1024px ou mais), com ajustes para mobile em sprint futura.  

---

## Tarefas

- Configurar React Router com rotas definidas.  
- Implementar autenticação usando Context API e Axios.  
- Criar layout com Tailwind CSS (login e perfil).  
- Desenvolver telas de login e perfil com componentes React.  
- Adicionar validação de formulários e feedback visual ao usuário.