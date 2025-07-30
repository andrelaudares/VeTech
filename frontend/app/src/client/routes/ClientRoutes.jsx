import { Routes, Route, Navigate } from 'react-router-dom';
import { ClientAuthProvider } from '../contexts/ClientAuthContext';
import ClientProtectedRoute from '../components/ClientProtectedRoute';
import ClientLayout from '../components/ClientLayout';
import ClientDashboardPage from '../pages/ClientDashboardPage';
import ClientAnimalsPage from '../pages/ClientAnimalsPage';
import ClientAppointmentsPage from '../pages/ClientAppointmentsPage';
import ClientProfilePage from '../pages/ClientProfilePage';

const ClientRoutes = () => {
  return (
    <ClientAuthProvider>
      <Routes>
        {/* Redirecionar /client/login para a página principal de login */}
        <Route path="/login" element={<Navigate to="/login" replace />} />
        <Route 
          path="/" 
          element={
            <ClientProtectedRoute>
              <ClientLayout />
            </ClientProtectedRoute>
          }
        >
          <Route index element={<ClientDashboardPage />} />
          <Route path="dashboard" element={<ClientDashboardPage />} />
          <Route path="animals" element={<ClientAnimalsPage />} />
          <Route path="appointments" element={<ClientAppointmentsPage />} />
          <Route path="profile" element={<ClientProfilePage />} />
        </Route>
      </Routes>
    </ClientAuthProvider>
  );
};

export default ClientRoutes;