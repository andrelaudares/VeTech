import api from '../../services/api';

const API_BASE_URL = '/api/v1';

export const clientAuthService = {
  async login(email, password) {
    try {
      const response = await api.post(`${API_BASE_URL}/auth/dual-login`, {
        email,
        password
      });
      
      // Verificar se é um cliente
      if (response.data.user_type !== 'client') {
        throw new Error('Este login é específico para clientes');
      }
      
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Erro ao fazer login');
    }
  },

  async getCurrentClient() {
    try {
      const response = await api.get(`${API_BASE_URL}/client/profile`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Erro ao obter dados do cliente');
    }
  },

  async getProfile() {
    try {
      const response = await api.get(`${API_BASE_URL}/client/profile`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Erro ao obter perfil do cliente');
    }
  },

  async updateProfile(profileData) {
    try {
      const response = await api.put(`${API_BASE_URL}/client/profile`, profileData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Erro ao atualizar perfil');
    }
  },

  async getAnimals() {
    try {
      const response = await api.get(`${API_BASE_URL}/client/animals`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Erro ao obter animais');
    }
  },

  async getAnimalDetails(animalId) {
    try {
      const response = await api.get(`${API_BASE_URL}/client/animals/${animalId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Erro ao obter detalhes do animal');
    }
  },

  async updateAnimal(animalId, animalData) {
    try {
      const response = await api.put(`${API_BASE_URL}/client/animals/${animalId}`, animalData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Erro ao atualizar animal');
    }
  },

  async getAppointments() {
    try {
      const response = await api.get(`${API_BASE_URL}/client/appointments`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Erro ao obter agendamentos');
    }
  }
};