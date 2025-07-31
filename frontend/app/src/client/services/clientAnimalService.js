import api from '../../services/api';

const API_BASE_URL = '/client';

export const clientAnimalService = {
  /**
   * Obtém os dados do animal do cliente logado
   * Usa o token do cliente para identificar qual animal buscar
   */
  async getMyAnimal() {
    try {
      const token = localStorage.getItem('client_token');
      if (!token) {
        throw new Error('Token de autenticação não encontrado');
      }

      const response = await api.get(`${API_BASE_URL}/animal`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      return response.data;
    } catch (error) {
      console.error('Erro ao obter dados do animal:', error);
      throw new Error(error.response?.data?.detail || 'Erro ao obter dados do animal');
    }
  },

  /**
   * Atualiza os dados do animal do cliente
   * Inclui tanto dados do animal quanto dados do tutor
   */
  async updateMyAnimal(animalData) {
    try {
      const token = localStorage.getItem('client_token');
      if (!token) {
        throw new Error('Token de autenticação não encontrado');
      }

      const response = await api.patch(`${API_BASE_URL}/animal`, animalData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      return response.data;
    } catch (error) {
      console.error('Erro ao atualizar dados do animal:', error);
      throw new Error(error.response?.data?.detail || 'Erro ao atualizar dados do animal');
    }
  },

  /**
   * Altera a senha do tutor
   */
  async changePassword(currentPassword, newPassword) {
    try {
      const token = localStorage.getItem('client_token');
      if (!token) {
        throw new Error('Token de autenticação não encontrado');
      }

      // Atualizar apenas o campo senha
      const response = await api.patch(`${API_BASE_URL}/animal`, {
        senha: newPassword
      }, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      return response.data;
    } catch (error) {
      console.error('Erro ao alterar senha:', error);
      throw new Error(error.response?.data?.detail || 'Erro ao alterar senha');
    }
  }
};