// routes/index.jsx

import React from 'react';
import { Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import AppHeader from '../components/AppHeader';
import MainLayout from '../components/MainLayout';
import { Box, CircularProgress, Typography } from '@mui/material';

// Importar páginas
import LandingPage from '../pages/LandingPage';
import LoginPage from '../pages/LoginPage';
import ProfilePage from '../pages/ProfilePage';
import DashboardPage from '../pages/DashboardPage';
import AnimalsPage from '../pages/AnimalsPage';
import AppointmentsPage from '../pages/AppointmentsPage';
import ConsultationsPage from '../pages/ConsultationsPage';
import DietsPage from '../pages/DietsPage';
import ActivitiesPage from '../pages/ActivitiesPage';
import NotFoundPage from '../pages/NotFoundPage';

// Importar rotas do cliente
import ClientRoutes from '../client/routes/ClientRoutes';

const ProtectedLayout = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  // console.log("ProtectedLayout: isAuthenticated:", isAuthenticated, "loading:", loading); // Log aqui

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
        <Typography sx={{ ml: 2 }}>Carregando autenticação...</Typography>
      </Box>
    );
  }

  // Se não está autenticado, sempre redireciona para o login
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <MainLayout>{children}</MainLayout>;
};

const AppRoutes = () => {
  const { isAuthenticated, loading } = useAuth();
  console.log("AppRoutes Global Log:", { isAuthenticated, loading, path: window.location.pathname });

  // Exibir um spinner de carregamento global enquanto a autenticação está sendo verificada
  // if (loading) {
  //   return (
  //     <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
  //       <CircularProgress />
  //       <Typography sx={{ ml: 2 }}>Verificando sessão...</Typography>
  //     </Box>
  //   );
  // }

  return (
    <Routes>
      {/* Rota da raiz: Se autenticado, vai para /inicio. Caso contrário, para a LandingPage */}
      <Route
        path="/"
        element={isAuthenticated ? <Navigate to="/inicio" replace /> : <LandingPage />}
      />

      {/* Rota de Login: Se autenticado, vai para /inicio. Caso contrário, exibe o LoginPage */}
      <Route
        path="/login"
        element={isAuthenticated ? <Navigate to="/inicio" replace /> : <LoginPage />}
      />

      {/* Rotas da área do cliente (tutor) */}
      <Route path="/client/*" element={<ClientRoutes />} />

      {/* Rotas protegidas (exigem autenticação) */}
      {/* O ProtectedLayout já lida com o redirecionamento para /login se não autenticado */}
      <Route element={<ProtectedLayout />}>
        <Route path="/inicio" element={<DashboardPage />} />
        <Route path="/perfil" element={<ProfilePage />} />
        <Route path="/animais" element={<AnimalsPage />} />
        <Route path="/agendamentos" element={<AppointmentsPage />} />
        <Route path="/consultas" element={<ConsultationsPage />} />
        <Route path="/dietas" element={<DietsPage />} />
        <Route path="/atividades" element={<ActivitiesPage />} />
      </Route>

      {/* Rota para páginas não encontradas */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
};

export default AppRoutes;