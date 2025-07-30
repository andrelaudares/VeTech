import { createContext, useContext, useState, useEffect } from 'react';
import { clientAuthService } from '../services/clientAuthService';

const ClientAuthContext = createContext();

export const useClientAuth = () => {
  const context = useContext(ClientAuthContext);
  if (!context) {
    throw new Error('useClientAuth deve ser usado dentro de um ClientAuthProvider');
  }
  return context;
};

export const ClientAuthProvider = ({ children }) => {
  const [client, setClient] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('client_token'));
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const initializeAuth = async () => {
      const storedToken = localStorage.getItem('client_token');
      if (storedToken) {
        try {
          const clientData = await clientAuthService.getCurrentClient();
          setClient(clientData);
          setToken(storedToken);
        } catch (error) {
          console.error('Erro ao verificar autenticação:', error);
          localStorage.removeItem('client_token');
          setToken(null);
          setClient(null);
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (email, password) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await clientAuthService.login(email, password);
      
      setToken(response.access_token);
      setClient(response.client);
      localStorage.setItem('client_token', response.access_token);
      
      return response;
    } catch (error) {
      setError(error.message || 'Erro ao fazer login');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setClient(null);
    setToken(null);
    localStorage.removeItem('client_token');
    setError(null);
  };

  const updateClient = (updatedClient) => {
    setClient(updatedClient);
  };

  const value = {
    client,
    token,
    loading,
    error,
    login,
    logout,
    updateClient,
    isAuthenticated: !!token && !!client
  };

  return (
    <ClientAuthContext.Provider value={value}>
      {children}
    </ClientAuthContext.Provider>
  );
};