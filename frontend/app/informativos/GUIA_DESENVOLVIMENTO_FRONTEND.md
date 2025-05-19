# Guia de Desenvolvimento Frontend VeTech

## 1. Introdução

Este guia tem como objetivo fornecer um passo a passo detalhado e boas práticas para a criação de novas páginas e funcionalidades no frontend da aplicação VeTech. A ideia é padronizar o desenvolvimento, facilitar a integração de novos membros à equipe e minimizar a ocorrência de erros comuns.

## 2. Pré-requisitos

Antes de começar, espera-se que você tenha um conhecimento básico de:

*   React (Hooks, Componentes funcionais)
*   JavaScript (ES6+)
*   Material UI (Componentes, Sistema de Grid, Estilização)
*   Gerenciamento de dependências com npm ou yarn
*   Consumo de APIs REST

## 3. Estrutura de Pastas Relevantes (`frontend/app/src`)

Entender a organização das pastas é crucial:

*   `assets/`: Imagens, fontes e outros arquivos estáticos.
*   `components/`: Componentes React reutilizáveis em várias partes da aplicação (ex: `AppHeader.jsx`, modais genéricos).
*   `contexts/`: Context API do React para gerenciamento de estado global (ex: `AuthContext.jsx`, `AnimalContext.jsx`).
*   `hooks/`: Hooks customizados reutilizáveis.
*   `pages/`: Componentes React que representam páginas completas da aplicação (ex: `LoginPage.jsx`, `AppointmentsPage.jsx`).
*   `routes/`: Configuração das rotas da aplicação (`index.jsx`).
*   `services/`: Funções para interagir com a API backend (ex: `authService.js`, `animalService.js`).
*   `styles/`: Arquivos de estilização globais ou temas.
*   `utils/`: Funções utilitárias diversas.
*   `main.jsx`: Ponto de entrada principal da aplicação React, onde Providers de contexto e rotas são geralmente configurados.

## 4. Passo a Passo para Criar uma Nova Página

Vamos supor que você precise criar uma nova página chamada "HistoricoTratamentos".

### 4.1. Criação do Arquivo da Página

1.  Crie um novo arquivo JSX em `frontend/app/src/pages/`.
    *   Exemplo: `HistoricoTratamentosPage.jsx`

2.  Estruture o componente básico da página:

    ```jsx
    import React, { useState, useEffect, useCallback } from 'react';
    import { Box, Typography, Container, CircularProgress, Alert } from '@mui/material';
    // Outros imports necessários (Material UI, serviços, componentes, etc.)

    // Hooks de contexto (se necessário)
    // import { useAuth } from '../contexts/AuthContext';
    // import { useAnimal } from '../contexts/AnimalContext';

    // Serviços (se necessário)
    // import { getHistorico } from '../services/historicoService'; // Exemplo

    const HistoricoTratamentosPage = () => {
        const [historico, setHistorico] = useState([]);
        const [loading, setLoading] = useState(false);
        const [error, setError] = useState(null);

        // const { token } = useAuth(); // Se a rota for protegida
        // const { selectedAnimal } = useAnimal(); // Se a página depender do animal selecionado

        // Função para buscar dados
        const fetchHistorico = useCallback(async () => {
            // if (!selectedAnimal || !token) return; // Condições para buscar
            setLoading(true);
            setError(null);
            try {
                // const data = await getHistorico(selectedAnimal.id, token);
                // setHistorico(data);
                console.log("Buscando histórico..."); // Placeholder
                setHistorico([]); // Placeholder
            } catch (err) {
                setError(err.message || 'Erro ao buscar histórico de tratamentos.');
                console.error(err);
            } finally {
                setLoading(false);
            }
        }, [/* selectedAnimal, token */]); // Dependências do useCallback

        useEffect(() => {
            fetchHistorico();
        }, [fetchHistorico]);

        if (loading) {
            return (
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 'calc(100vh - 64px)' }}>
                    <CircularProgress />
                    <Typography sx={{ ml: 2 }}>Carregando histórico...</Typography>
                </Box>
            );
        }

        if (error) {
            return (
                <Container sx={{ py: 3 }}>
                    <Alert severity="error">{error}</Alert>
                </Container>
            );
        }

        return (
            <Container maxWidth="lg" sx={{ py: 3, backgroundColor: '#F9F9F9' }}>
                <Typography variant="h4" component="h1" gutterBottom sx={{ color: '#4A4A4A' }}>
                    Histórico de Tratamentos
                </Typography>
                {/* Conteúdo da página aqui: Tabela, Cards, etc. */}
                {historico.length === 0 && !loading && (
                    <Typography>Nenhum histórico de tratamento encontrado.</Typography>
                )}
                {/* Exemplo: {historico.map(item => <div key={item.id}>{item.descricao}</div>)} */}
            </Container>
        );
    };

    export default HistoricoTratamentosPage;
    ```

### 4.2. Criação do Serviço (se necessário)

Se a nova página precisar buscar ou enviar dados para a API:

1.  Crie (ou adicione a um existente) um arquivo de serviço em `frontend/app/src/services/`.
    *   Exemplo: `historicoService.js`

2.  Defina as funções para interagir com os endpoints da API:

    ```javascript
    import api from './api'; // Instância configurada do Axios

    export const getHistorico = async (animalId, token) => {
        try {
            const response = await api.get(`/historico/animal/${animalId}`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            return response.data;
        } catch (error) {
            console.error("Erro ao buscar histórico:", error.response?.data || error.message);
            throw error.response?.data || new Error('Erro no servidor ao buscar histórico.');
        }
    };

    export const addTratamento = async (dadosTratamento, token) => {
        try {
            const response = await api.post('/historico', dadosTratamento, {
                headers: { Authorization: `Bearer ${token}` }
            });
            return response.data;
        } catch (error) {
            console.error("Erro ao adicionar tratamento:", error.response?.data || error.message);
            throw error.response?.data || new Error('Erro no servidor ao adicionar tratamento.');
        }
    };
    // Adicionar outras funções (update, delete) conforme necessário
    ```
    *   **Nota sobre `api.js`**: Geralmente, existe um arquivo `src/services/api.js` que configura a instância base do Axios, definindo a `baseURL` da API e, possivelmente, interceptadores para lidar com JWT.

### 4.3. Configuração de Rotas

1.  Abra o arquivo `frontend/app/src/routes/index.jsx`.
2.  Importe o novo componente da página:

    ```jsx
    // ... outros imports
    import HistoricoTratamentosPage from '../pages/HistoricoTratamentosPage';
    ```

3.  Adicione a nova rota à lista de rotas. Se a página exigir autenticação, envolva-a com `ProtectedRoute`:

    ```jsx
    // ...
    {
        path: '/historico-tratamentos',
        element: (
            <ProtectedRoute>
                <HistoricoTratamentosPage />
            </ProtectedRoute>
        )
    },
    // ...
    ```
    *   `ProtectedRoute` é um componente customizado que verifica se o usuário está autenticado (usando o `AuthContext`). Se não estiver, redireciona para a página de login.

### 4.4. Integração com o Header (`AppHeader.jsx`)

Se a nova página deve ser acessível diretamente pelo menu principal no cabeçalho:

1.  Abra `frontend/app/src/components/AppHeader.jsx`.
2.  Adicione um novo item de navegação. Isso pode ser um `Button` ou um `MenuItem` dentro de um menu existente.

    ```jsx
    // ... dentro do return do AppHeader, na seção de navegação
    <Button
        color="inherit"
        component={RouterLink}
        to="/historico-tratamentos"
        sx={{ my: 2, color: 'white', display: 'block', marginX: 1 }}
    >
        Histórico
    </Button>
    // ...
    ```

3.  **Considerações sobre o Seletor Global de Animal (Conteúdo de `HEADER_DOCS.md` integrado):**
    *   O `AppHeader.jsx` contém um seletor de animal global que utiliza o `AnimalContext`.
    *   A lista de animais é carregada pelo `fetchAnimals` do `AnimalContext`.
    *   Quando um animal é selecionado, `selectedAnimal` no `AnimalContext` é atualizado.
    *   **Exibição Condicional do Seletor:** O seletor de animal NÃO é exibido em certas páginas, configuradas na variável `noAnimalSelectorPages` dentro de `AppHeader.jsx` (ex: `/perfil`, `/inicio`). Se sua nova página não deve exibir o seletor, adicione a rota a esta array.
    *   Páginas que precisam dos dados do animal selecionado devem usar o hook `useAnimal()`: `const { selectedAnimal } = useAnimal();`.

### 4.5. Uso de Contextos

#### 4.5.1. `AuthContext` (Autenticação e JWT)

*   **Localização**: `frontend/app/src/contexts/AuthContext.jsx`
*   **Providencia**: `user` (dados do usuário logado), `token` (JWT), `login()`, `logout()`, `loading`, `isAuthenticated`.
*   **JWT**:
    *   Após o login bem-sucedido (via `authService.js`), o token JWT retornado pela API é armazenado, geralmente no `localStorage`.
    *   O `AuthContext` lê o token do `localStorage` ao inicializar para manter o usuário logado entre sessões.
    *   Para requisições autenticadas, o token JWT deve ser incluído no header `Authorization` como `Bearer <token>`. Isso é tipicamente gerenciado no arquivo `src/services/api.js` ou diretamente nas funções de serviço, como mostrado no exemplo `historicoService.js`.
*   **Uso**:
    ```jsx
    import { useAuth } from '../contexts/AuthContext';
    // ...
    const { user, token, logout } = useAuth();
    ```

#### 4.5.2. `AnimalContext` (Seleção Global de Animal)

*   **Localização**: `frontend/app/src/contexts/AnimalContext.jsx`
*   **Providencia**: `animals` (lista de animais do usuário), `selectedAnimal` (animal atualmente selecionado no header), `selectAnimal()` (função para mudar o animal selecionado), `fetchAnimals()`, `loading`, `error`.
*   **Uso**:
    ```jsx
    import { useAnimal } from '../contexts/AnimalContext';
    // ...
    const { animals, selectedAnimal, fetchAnimals } = useAnimal();

    useEffect(() => {
        // Se sua página depende do animal, você pode querer buscar dados quando o selectedAnimal mudar.
        if (selectedAnimal) {
            // fetchDataForAnimal(selectedAnimal.id);
        }
    }, [selectedAnimal]);
    ```
    *   A lógica de carregar os animais (`fetchAnimals`) geralmente é chamada uma vez quando o `AnimalProvider` monta ou quando o usuário loga. O `AppHeader` utiliza este contexto para popular o dropdown de seleção.

### 4.6. Estilização

*   Utilize componentes do Material UI sempre que possível.
*   Siga a paleta de cores do projeto:
    *   Marrom-claro suave: `#D8CAB8`
    *   Creme claro: `#F9F9F9` (bom para backgrounds de página/container)
    *   Cinza-esverdeado: `#9DB8B2`
    *   Verde-oliva suave: `#CFE0C3`
    *   Considere cores neutras adicionais para texto e bordas (ex: `#4A4A4A` para texto principal, `#E0E0E0` para divisórias).
*   Use a prop `sx` para estilizações pontuais e o hook `makeStyles` ou `styled` do `@mui/system` (ou `styled-components` se preferir) para estilizações mais complexas e reutilizáveis.
*   Mantenha a consistência visual com o restante da aplicação.

### 4.7. Criação de Componentes Reutilizáveis

*   Se partes da sua nova página puderem ser reutilizadas em outros lugares (ex: um formulário customizado, um card de exibição de dados específico), crie-os como componentes separados em `frontend/app/src/components/`.
*   **Modais**: Para formulários de criação/edição (`XxxFormModal.jsx`) ou exibição de detalhes (`XxxDetailsModal.jsx`), crie componentes de modal separados. Eles geralmente recebem props como `open`, `onClose`, `data` (para edição/detalhes), e `onSave`.

## 5. Tratamento de Erros e Feedback ao Usuário

*   **Carregamento (`loading`)**:
    *   Use um estado `loading` (booleano).
    *   Exiba um indicador de carregamento (`<CircularProgress />` do Material UI) enquanto os dados estão sendo buscados.
    *   Desabilite botões de ação durante o carregamento para evitar múltiplas submissões.
*   **Erros (`error`)**:
    *   Use um estado `error` (string ou objeto de erro).
    *   Exiba mensagens de erro claras para o usuário usando o componente `<Alert severity="error">` do Material UI.
    *   Logue erros detalhados no console para depuração.

## 6. Boas Práticas e Convenções

*   **Nomenclatura**:
    *   Componentes: `PascalCase` (ex: `HistoricoTratamentosPage.jsx`).
    *   Funções e variáveis: `camelCase` (ex: `fetchHistorico`).
    *   Arquivos de serviço: `camelCase` (ex: `historicoService.js`).
*   **Comentários**: Comente partes complexas do código ou lógica não óbvia. Evite comentários excessivos para código autoexplicativo.
*   **DRY (Don't Repeat Yourself)**: Evite duplicação de código criando funções utilitárias e componentes reutilizáveis.
*   **Imports**: Organize os imports (ex: React, bibliotecas externas, componentes locais, contextos, serviços, estilos).
*   **Responsividade**: Pense em como a página se comportará em diferentes tamanhos de tela. Use o sistema de grid do Material UI.

## 7. Dependências Importantes e Configurações

### 7.1. Date Pickers (`@mui/x-date-pickers`)

Para campos de data e hora, a biblioteca `@mui/x-date-pickers` é utilizada.

1.  **Instalação (IMPORTANTE: no diretório `frontend/app/`):**
    ```bash
    cd frontend/app
    npm install @mui/x-date-pickers date-fns
    ```
    *   `date-fns` é uma biblioteca de manipulação de datas popular e é uma das opções de adaptador.

2.  **Configuração do Adaptador**:
    Em `main.jsx` (ou no componente raiz da sua aplicação), configure o `LocalizationProvider` com o adaptador apropriado:

    ```jsx
    // frontend/app/src/main.jsx
    import React from 'react';
    import ReactDOM from 'react-dom/client';
    import App from './App';
    import { BrowserRouter } from 'react-router-dom';
    import { AuthProvider } from './contexts/AuthContext';
    import { AnimalProvider } from './contexts/AnimalContext';
    import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
    import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFnsV3'; // Caminho corrigido se usar V3
    // OU, se você instalou a versão padrão que pode não ser V3:
    // import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
    import { ptBR } from 'date-fns/locale'; // Para localização em Português

    ReactDOM.createRoot(document.getElementById('root')).render(
      <React.StrictMode>
        <BrowserRouter>
          <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ptBR}>
            <AuthProvider>
              <AnimalProvider>
                <App />
              </AnimalProvider>
            </AuthProvider>
          </LocalizationProvider>
        </BrowserRouter>
      </React.StrictMode>
    );
    ```
    *   **Atenção ao caminho do import do Adapter**: O erro `Failed to resolve import "@mui/x-date-pickers/AdapterDateFnsV3"` indica que o Vite não consegue encontrar o arquivo nesse caminho específico. Verifique sua instalação e a versão do `@mui/x-date-pickers`. Se você instalou a versão mais recente sem especificar v6 ou v7 para os pickers, o caminho pode ser apenas `@mui/x-date-pickers/AdapterDateFns`. Se estiver usando a v5 dos pickers, o caminho seria `@date-io/date-fns` e a instalação seria `npm install @date-io/date-fns date-fns`. **Verifique a documentação oficial da versão do `@mui/x-date-pickers` que você está usando para o caminho correto do adaptador.**

3.  **Uso nos Componentes**:
    ```jsx
    import { DatePicker } from '@mui/x-date-pickers/DatePicker';
    import { TimePicker } from '@mui/x-date-pickers/TimePicker';
    // ...
    <DatePicker
      label="Data do Tratamento"
      value={dataSelecionada}
      onChange={(novaData) => setDataSelecionada(novaData)}
      renderInput={(params) => <TextField {...params} fullWidth margin="normal" />}
    />
    ```

## 8. Comandos Úteis do Terminal (a partir da raiz do projeto)

*   **Instalar dependências do frontend**:
    ```bash
    cd frontend/app
    npm install
    ```
*   **Iniciar servidor de desenvolvimento do frontend**:
    ```bash
    cd frontend/app
    npm run dev
    ```
*   **Instalar uma nova dependência no frontend**:
    ```bash
    cd frontend/app
    npm install nome-do-pacote
    ```

## 9. Resolução de Problemas Comuns

*   **`Failed to resolve import ...`**:
    1.  Verifique se a dependência está listada no `frontend/app/package.json`.
    2.  Certifique-se de que você executou `npm install` dentro do diretório `frontend/app/`.
    3.  Verifique se o caminho do import no seu código está correto (sensível a maiúsculas/minúsculas e estrutura de pastas).
    4.  Tente deletar a pasta `node_modules` e o arquivo `package-lock.json` (ou `yarn.lock`) dentro de `frontend/app/` e rodar `npm install` novamente.
    5.  Reinicie o servidor de desenvolvimento do Vite. Às vezes, o Vite pode precisar limpar seu cache (`npm run dev -- --force`).
*   **Problemas com `&&` no PowerShell**:
    *   Lembre-se que seu PowerShell tem problemas com `&&`. Se precisar executar múltiplos comandos sequencialmente, execute-os um por vez ou use um script `.ps1`.
*   **Dados não atualizam ou comportamento estranho**:
    *   Verifique as dependências dos seus `useEffect` e `useCallback`.
    *   Use as ferramentas de desenvolvedor do navegador (aba Network para verificar requisições, Console para erros, React DevTools para inspecionar componentes e estado).

## 10. Considerações sobre a API Backend

*   As definições das rotas da API, payloads esperados e respostas podem ser encontradas na documentação do backend (ex: arquivos `sprint5.md` na pasta do backend, ou diretamente nos arquivos Python como `activities.py`).
*   Certifique-se de que o servidor backend está rodando e acessível pela URL configurada no `src/services/api.js`.

---
