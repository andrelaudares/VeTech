import api from './api';

const dashboardService = {
  // Buscar estatísticas gerais do dashboard
  async getStats() {
    try {
      const response = await api.get('/dashboard/stats');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar estatísticas do dashboard:', error);
      throw error;
    }
  },

  // Buscar agendamentos de hoje
  async getAppointmentsToday() {
    try {
      const response = await api.get('/dashboard/appointments-today');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar agendamentos de hoje:', error);
      throw error;
    }
  },

  // Buscar alertas do dashboard
  async getAlerts() {
    try {
      const response = await api.get('/dashboard/alerts');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar alertas do dashboard:', error);
      throw error;
    }
  }
};

export default dashboardService; 