import React from 'react';
import { Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

// Importar páginas
import LoginPage from '../pages/LoginPage';
import ProfilePage from '../pages/ProfilePage';
import DashboardPage from '../pages/DashboardPage';
import AnimalsPage from '../pages/AnimalsPage';

const ProtectedRoute = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    // Pode mostrar um spinner/loading aqui enquanto verifica a autenticação
    return <div className="p-4">Carregando autenticação...</div>;
  }

  if (!isAuthenticated) {
    // Se não estiver autenticado, redireciona para a página de login
    // Pode passar o local atual para redirecionar de volta após o login, se desejar
    return <Navigate to="/login" replace />;
  }

  return <Outlet />; // Renderiza o componente da rota filha se autenticado
};

const AppRoutes = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Carregando...</div>; // Ou um spinner global
  }

  return (
    <Routes>
      {/* Rota pública para login - se já autenticado, redireciona para dashboard */}
      <Route 
        path="/login" 
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <LoginPage />}
      />

      {/* Rotas protegidas */}
      <Route element={<ProtectedRoute />}>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/perfil" element={<ProfilePage />} />
        <Route path="/animais" element={<AnimalsPage />} />
        {/* Adicionar outras rotas protegidas aqui */}
      </Route>

      {/* Rota padrão (raiz) */}
      {/* Se autenticado, vai para /dashboard, senão para /login */}
      <Route 
        path="/" 
        element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />} 
      />

      {/* Rota para Not Found (404) - opcional */}
      <Route path="*" element={<div className="p-4">Página não encontrada (404)</div>} />
    </Routes>
  );
};

export default AppRoutes; 