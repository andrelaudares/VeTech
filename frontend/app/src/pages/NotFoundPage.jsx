import React from 'react';
import { Box, Button, Container, Typography, Paper } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import ReportProblemIcon from '@mui/icons-material/ReportProblem'; // Ícone de erro

// Paleta de cores para consistência (pode ajustar se necessário)
const colors = {
  primaryAction: '#9DB8B2',
  primaryActionHover: '#82a8a0',
  paperBackground: '#FFFFFF',
  textPrimary: '#333',
  textSecondary: '#555',
  background: '#F9F9F9',
  errorColor: '#d32f2f' // Tom de vermelho para erro
};

const NotFoundPage = () => {
  return (
    <Container 
      component="main" 
      maxWidth="sm" 
      sx={{ 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center', 
        justifyContent: 'center', 
        minHeight: 'calc(100vh - 64px)', // Ajustar altura considerando o header (64px é o padrão do AppBar)
        textAlign: 'center',
        backgroundColor: colors.background,
        py: 6 
      }}
    >
      <Paper 
        elevation={3} 
        sx={{ 
          p: { xs: 3, sm: 5 }, 
          borderRadius: 2, 
          backgroundColor: colors.paperBackground,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          boxShadow: '0px 6px 20px rgba(0,0,0,0.1)' // Sombra mais pronunciada
        }}
      >
        <ReportProblemIcon sx={{ fontSize: 80, color: colors.errorColor, mb: 2 }} />
        <Typography 
          variant="h4" 
          component="h1" 
          gutterBottom 
          sx={{ color: colors.textPrimary, fontWeight: 'bold' }}
        >
          Oops! Página Não Encontrada
        </Typography>
        <Typography 
          variant="h6" 
          sx={{ color: colors.textSecondary, mb: 4, fontWeight: 'normal' }}
        >
          A página que você está procurando não existe ou foi movida.
        </Typography>
        <Button 
          component={RouterLink} 
          to="/inicio" 
          variant="contained" 
          sx={{ 
            backgroundColor: colors.primaryAction, 
            '&:hover': { backgroundColor: colors.primaryActionHover },
            color: colors.paperBackground, // Garantir contraste
            px: 4, // Padding horizontal
            py: 1.5 // Padding vertical
          }}
        >
          Voltar para o Início
        </Button>
      </Paper>
    </Container>
  );
};

export default NotFoundPage; 