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
    mode: 'light', // se quiser um dark mode, troque para 'dark'
    primary: {
      main: '#23e865', // Verde vivo
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#1cba52', // Tom complementar para botões secundários
    },
    background: {
      default: '#f4fff6', // Fundo com leve tom esverdeado
      paper: '#ffffff',   // Cards e modais brancos
    },
    text: {
      primary: '#1b1b1b',
      secondary: '#4f4f4f',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h5: { fontWeight: 600 },
    h6: { fontWeight: 600 },
    body1: { fontSize: 16 },
    body2: { fontSize: 14 },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
      },
    },
  },
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
