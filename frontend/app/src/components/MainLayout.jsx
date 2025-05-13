import React from 'react';
import { Outlet } from 'react-router-dom';
import AppHeader from './AppHeader';
import { Box } from '@mui/material';

const MainLayout = () => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppHeader />
      <Box component="main" sx={{ flexGrow: 1, p: 3 /* Adiciona padding ao conteúdo principal */ }}>
        <Outlet /> {/* Onde as páginas da rota aninhada serão renderizadas */}
      </Box>
      {/* Você pode adicionar um Footer aqui se desejar */}
    </Box>
  );
};

export default MainLayout; 