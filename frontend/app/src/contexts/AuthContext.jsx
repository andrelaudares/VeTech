// AuthContext.js

import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import api from '../services/api';
import authService from '../services/authService';
import clinicService from '../services/clinicService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('viteToken'));
  const [loading, setLoading] = useState(true);
  const [authError, setAuthError] = useState(null); // ESTADO PARA ERROS DE AUTENTICAÇÃO

  const logout = useCallback(async () => {
    console.log("AuthContext: Iniciando logout...");
    try {
      await authService.logout();
      console.log("AuthContext: Logout na API bem-sucedido.");
    } catch (error) {
      console.error("AuthContext: Erro na API de logout:", error);
    }
    localStorage.removeItem('viteToken');
    api.defaults.headers.Authorization = null;
    setUser(null);
    setToken(null);
    setAuthError(null);
    console.log("AuthContext: Logout concluído, estado limpo.");
  }, []);

  const fetchProfileAndSetUser = useCallback(async (currentToken) => {
    console.log("AuthContext: Tentando buscar perfil com token...");
    if (currentToken) {
      api.defaults.headers.Authorization = `Bearer ${currentToken}`;
      try {
        const response = await clinicService.getProfile();
        setUser(response.data);
        setToken(currentToken);
        setAuthError(null);
        console.log("AuthContext: Perfil carregado com sucesso.");
      } catch (error) {
        console.error("AuthContext: Falha ao buscar perfil ou token inválido:", error);
        await logout();
        setAuthError('Sua sessão expirou ou é inválida. Faça login novamente.');
      }
    }
    setLoading(false);
    console.log("AuthContext: Fim do carregamento inicial.");
  }, [logout]);

  useEffect(() => {
    console.log("AuthContext: useEffect de carregamento inicial.");
    const storedToken = localStorage.getItem('viteToken');
    if (storedToken) {
      fetchProfileAndSetUser(storedToken);
    } else {
      setLoading(false);
      console.log("AuthContext: Nenhum token armazenado, carregamento inicial concluído.");
    }
  }, [fetchProfileAndSetUser]);

  const login = async (email, password) => {
    console.log("AuthContext: Tentando login para:", email);
    setLoading(true);
    setAuthError(null); // Limpa qualquer erro anterior

    try {
      const response = await authService.login(email, password);
      const { access_token, clinic } = response.data;

      localStorage.setItem('viteToken', access_token);
      api.defaults.headers.Authorization = `Bearer ${access_token}`;
      setUser(clinic);
      setToken(access_token);
      setLoading(false);
      console.log("AuthContext: Login bem-sucedido. Usuário:", clinic);
      return clinic;
    } catch (error) {
      console.error('AuthContext: Erro capturado na função login:', error);
      
      let errorMessage = 'Ocorreu um erro ao tentar fazer login. Por favor, tente novamente.';
      if (error.response) {
        console.log("AuthContext: Erro de resposta da API. Status:", error.response.status, "Dados:", error.response.data);
        if (error.response.status === 401) {
          errorMessage = 'Email ou senha incorretos.';
        } else if (error.response.data && error.response.data.detail) {
          errorMessage = error.response.data.detail;
        } else {
          errorMessage = `Erro do servidor: ${error.response.status}`;
        }
      } else if (error.request) {
        console.log("AuthContext: Erro de requisição (sem resposta do servidor).");
        errorMessage = 'Não foi possível conectar ao servidor. Verifique sua conexão com a internet.';
      } else {
        console.log("AuthContext: Outro tipo de erro na requisição.");
        errorMessage = `Erro inesperado: ${error.message}`;
      }
      
      setAuthError(errorMessage); // DEFINE A MENSAGEM DE ERRO
      console.log("AuthContext: authError definido como:", errorMessage);

      // Limpeza em caso de falha no login
      localStorage.removeItem('viteToken'); 
      api.defaults.headers.Authorization = null;
      setUser(null);
      setToken(null);
      
      setLoading(false);
      console.log("AuthContext: Login falhou, token e usuário limpos.");
      throw error; // RELANÇA O ERRO
    }
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated: !!token, loading, authError }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined || context === null) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
};