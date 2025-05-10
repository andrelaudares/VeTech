import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { AuthProvider } from './contexts/AuthContext.jsx'
import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { AnimalProvider } from './contexts/AnimalContext'

// Importações da fonte Roboto
import '@fontsource/roboto/300.css'
import '@fontsource/roboto/400.css'
import '@fontsource/roboto/500.css'
import '@fontsource/roboto/700.css'

// Nova paleta de cores VeTech
const vetechTheme = createTheme({
  palette: {
    primary: {
      main: '#A3C9A8', // Verde-matcha claro
    },
    secondary: {
      main: '#9DB8B2', // Cinza-esverdeado
    },
    background: {
      default: '#F9F9F9', // Creme
      paper: '#FFFFFF',   // Branco para Cards, Modais, etc.
    },
    text: {
      primary: '#333333', // Cinza escuro para texto principal
      secondary: '#555555', // Cinza um pouco mais claro para texto secundário
    },
    // Cores adicionais podem ser adicionadas aqui se necessário
    // Exemplo: accent: '#CFE0C3', // Verde-oliva suave
    //          divider: '#D8CAB8'
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 500,
    },
    h2: {
      fontWeight: 500,
    },
    h3: {
      fontWeight: 500,
    },
    h4: {
      fontWeight: 500,
    },
    h5: {
      fontWeight: 500,
    },
    h6: {
      fontWeight: 500,
    },
    // Você pode adicionar mais customizações de tipografia aqui
  },
  // Você pode adicionar customizações de componentes aqui
  // Exemplo:
  // components: {
  //   MuiButton: {
  //     styleOverrides: {
  //       root: {
  //         borderRadius: 8,
  //       },
  //     },
  //   },
  // },
})

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <AnimalProvider>
          <ThemeProvider theme={vetechTheme}>
            <CssBaseline /> {/* Normaliza o CSS e aplica o background.default do tema */}
            <App />
          </ThemeProvider>
        </AnimalProvider>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
