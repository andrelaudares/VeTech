import { useClientAuth } from '../contexts/ClientAuthContext';
import { Navigate } from 'react-router-dom';

const ClientProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading, client, token } = useClientAuth();

  console.log("ClientProtectedRoute: Verificando autenticação...");
  console.log("- isAuthenticated:", isAuthenticated);
  console.log("- loading:", loading);
  console.log("- client:", client ? "Existe" : "Não existe");
  console.log("- token:", token ? "Existe" : "Não existe");

  // Verificar também o localStorage diretamente
  const storedToken = localStorage.getItem('client_token');
  const storedClientData = localStorage.getItem('clientData');
  
  console.log("ClientProtectedRoute: Verificação direta do localStorage:");
  console.log("- storedToken:", storedToken ? "Existe" : "Não existe");
  console.log("- storedClientData:", storedClientData ? "Existe" : "Não existe");

  if (loading) {
    console.log("ClientProtectedRoute: Carregando...");
    return <div>Carregando...</div>;
  }

  // Se temos dados no localStorage, considerar como autenticado
  if (storedToken && storedClientData) {
    console.log("ClientProtectedRoute: Dados encontrados no localStorage, permitindo acesso");
    return children;
  }

  if (!isAuthenticated) {
    console.log("ClientProtectedRoute: Usuário não autenticado, redirecionando para página principal de login");
    return <Navigate to="/login" replace />;
  }

  console.log("ClientProtectedRoute: Usuário autenticado, renderizando conteúdo");
  return children;
};

export default ClientProtectedRoute;