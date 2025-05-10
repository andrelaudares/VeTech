import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import api from '../services/api';
import authService from '../services/authService';
import clinicService from '../services/clinicService'; // Importar clinicService

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('viteToken'));
  const [loading, setLoading] = useState(true); // Começa true para indicar que estamos carregando/verificando

  const logout = useCallback(async () => {
    try {
      await authService.logout(); // Chamar a API de logout
    } catch (error) {
      console.error("Erro na API de logout:", error);
      // Mesmo se a API de logout falhar, continuamos com o logout no cliente
    }
    localStorage.removeItem('viteToken');
    api.defaults.headers.Authorization = null;
    setUser(null);
    setToken(null);
  }, []);

  const fetchProfileAndSetUser = useCallback(async (currentToken) => {
    if (currentToken) {
      api.defaults.headers.Authorization = `Bearer ${currentToken}`;
      try {
        const response = await clinicService.getProfile();
        setUser(response.data); // Supõe que response.data é o objeto do usuário/clínica
        setToken(currentToken);
      } catch (error) {
        console.error("Falha ao buscar perfil ou token inválido:", error);
        await logout(); // Faz logout se não conseguir buscar o perfil
      }
    }
    setLoading(false);
  }, [logout]);

  useEffect(() => {
    const storedToken = localStorage.getItem('viteToken');
    if (storedToken) {
      fetchProfileAndSetUser(storedToken);
    } else {
      setLoading(false); // Se não há token, não estamos autenticados e não estamos carregando
    }
  }, [fetchProfileAndSetUser]);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const response = await authService.login(email, password);
      const { access_token, clinic } = response.data;

      localStorage.setItem('viteToken', access_token);
      api.defaults.headers.Authorization = `Bearer ${access_token}`;
      setUser(clinic); // A API de login já retorna os dados da clínica
      setToken(access_token);
      setLoading(false);
      return clinic;
    } catch (error) {
      console.error('Falha no login:', error);
      await logout(); // Garante que o estado seja limpo em caso de falha no login
      setLoading(false);
      throw error;
    }
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated: !!token, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined || context === null) { // Adicionado cheque para null
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
}; 