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
      console.log("ClientAuthContext: Inicializando autenticação...");
      
      const storedToken = localStorage.getItem('client_token');
      const storedClientData = localStorage.getItem('clientData');
      
      console.log("ClientAuthContext: Token armazenado:", storedToken ? "Existe" : "Não existe");
      console.log("ClientAuthContext: Dados do cliente armazenados:", storedClientData ? "Existem" : "Não existem");
      console.log("ClientAuthContext: Conteúdo do clientData:", storedClientData);
      
      if (storedToken && storedClientData && storedClientData !== 'undefined') {
        try {
          const clientData = JSON.parse(storedClientData);
          console.log("ClientAuthContext: Dados do cliente parseados:", clientData);
          
          setToken(storedToken);
          setClient(clientData);
          console.log("ClientAuthContext: Estado atualizado com dados armazenados");
        } catch (error) {
          console.error("ClientAuthContext: Erro ao parsear dados do cliente:", error);
          localStorage.removeItem('client_token');
          localStorage.removeItem('clientData');
        }
      } else {
        console.log("ClientAuthContext: Dados inválidos ou inexistentes no localStorage");
        // Limpar dados inválidos
        if (storedClientData === 'undefined' || storedClientData === 'null') {
          console.log("ClientAuthContext: Removendo dados inválidos do localStorage");
          localStorage.removeItem('client_token');
          localStorage.removeItem('clientData');
        }
      }
      
      setLoading(false);
      console.log("ClientAuthContext: Carregamento finalizado");
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
    localStorage.removeItem('clientData');
    setError(null);
  };

  const updateClient = (updatedClient) => {
    setClient(updatedClient);
  };

  const refreshAuth = () => {
    console.log("ClientAuthContext: Forçando atualização da autenticação...");
    const storedToken = localStorage.getItem('client_token');
    const storedClientData = localStorage.getItem('clientData');
    
    if (storedToken && storedClientData && storedClientData !== 'undefined') {
      try {
        const clientData = JSON.parse(storedClientData);
        setToken(storedToken);
        setClient(clientData);
        console.log("ClientAuthContext: Autenticação atualizada com sucesso");
      } catch (error) {
        console.error("ClientAuthContext: Erro ao atualizar autenticação:", error);
        logout();
      }
    } else {
      console.log("ClientAuthContext: Dados inválidos, fazendo logout");
      logout();
    }
  };

  const isAuthenticated = !!token && !!client;
  
  // Log para depuração
  useEffect(() => {
    console.log("ClientAuthContext: Estado atual:");
    console.log("- Token:", token ? "Existe" : "Não existe");
    console.log("- Client:", client ? "Existe" : "Não existe");
    console.log("- isAuthenticated:", isAuthenticated);
    console.log("- Loading:", loading);
    console.log("- Dados do client:", client);
  }, [token, client, isAuthenticated, loading]);

  const value = {
    client,
    token,
    loading,
    error,
    login,
    logout,
    updateClient,
    refreshAuth,
    isAuthenticated
  };

  return (
    <ClientAuthContext.Provider value={value}>
      {children}
    </ClientAuthContext.Provider>
  );
};