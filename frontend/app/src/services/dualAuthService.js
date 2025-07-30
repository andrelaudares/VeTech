import api from './api';

const dualAuthService = {
  // Verificar tipo de usuário (clínica ou tutor)
  async checkUserType(email) {
    try {
      const response = await api.post('/auth/check-user-type', { email });
      return response.data;
    } catch (error) {
      console.error('Erro ao verificar tipo de usuário:', error);
      throw error;
    }
  },

  // Login dual (clínica ou tutor)
  async dualLogin(email, password) {
    try {
      const response = await api.post('/auth/dual-login', { email, password });
      return response.data;
    } catch (error) {
      console.error('Erro no login dual:', error);
      throw error;
    }
  }
};

export default dualAuthService;