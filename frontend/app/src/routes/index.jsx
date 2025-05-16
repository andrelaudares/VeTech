import React from 'react';
import { Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import AppHeader from '../components/AppHeader';
import MainLayout from '../components/MainLayout';

// Importar páginas
import LandingPage from '../pages/LandingPage';
import LoginPage from '../pages/LoginPage';
import ProfilePage from '../pages/ProfilePage';
import DashboardPage from '../pages/DashboardPage';
import AnimalsPage from '../pages/AnimalsPage';
import AppointmentsPage from '../pages/AppointmentsPage';
import ConsultationsPage from '../pages/ConsultationsPage';
import DietsPage from '../pages/DietsPage';
import NotFoundPage from '../pages/NotFoundPage';

const ProtectedLayout = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="p-4">Carregando autenticação...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <MainLayout />;
};

const AppRoutes = () => {
  const { isAuthenticated, loading } = useAuth();
  console.log({ isAuthenticated, loading, path: window.location.pathname });

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Carregando...</div>;
  }

  return (
    <Routes>
      {/* Landing page é a raiz do sistema - verifica autenticação */}
      <Route 
        path="/" 
        element={isAuthenticated ? <Navigate to="/inicio" replace /> : <LandingPage />} 
      />

      <Route 
        path="/login" 
        element={isAuthenticated ? <Navigate to="/inicio" replace /> : <LoginPage />}
      />

      {/* Rotas protegidas */}
      <Route element={<ProtectedLayout />}>
        <Route path="/inicio" element={<DashboardPage />} />
        <Route path="/perfil" element={<ProfilePage />} />
        <Route path="/animais" element={<AnimalsPage />} />
        <Route path="/agendamentos" element={<AppointmentsPage />} />
        <Route path="/consultas" element={<ConsultationsPage />} />
        <Route path="/dietas" element={<DietsPage />} />
      </Route>

      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
};

export default AppRoutes;
