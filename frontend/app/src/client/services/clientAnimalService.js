import api from '../../services/api';

const API_BASE_URL = '/client';

export const clientAnimalService = {
  /**
   * Obtém os dados do animal do cliente logado
   * Usa o token do cliente para identificar qual animal buscar
   */
  async getMyAnimal() {
    try {
      const response = await api.get(`${API_BASE_URL}/animal`);
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
      const response = await api.patch(`${API_BASE_URL}/animal`, animalData);
      return response.data;
    } catch (error) {
      console.error('Erro ao atualizar dados do animal:', error);
      throw new Error(error.response?.data?.detail || 'Erro ao atualizar dados do animal');
    }
  },

  /**
   * Altera a senha do cliente
   */
  async changePassword(passwordData) {
    try {
      const response = await api.patch(`${API_BASE_URL}/change-password`, passwordData);
      return response.data;
    } catch (error) {
      console.error('Erro ao alterar senha:', error);
      throw new Error(error.response?.data?.detail || 'Erro ao alterar senha');
    }
  }
};