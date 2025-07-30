import { Navigate } from 'react-router-dom';
import { useClientAuth } from '../contexts/ClientAuthContext';

const ClientProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useClientAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/client/login" replace />;
  }

  return children;
};

export default ClientProtectedRoute;