import api from './api';

export const animalService = {
  // Operações básicas de animais
  async getAnimals() {
    const response = await api.get('/animals');
    return response.data;
  },

  async getAllAnimals(forceClinicToken = false) {
    let config = {};
    if (forceClinicToken) {
      const clinicToken = localStorage.getItem('viteToken');
      if (clinicToken) {
        config.headers = { Authorization: `Bearer ${clinicToken}` };
      }
    }
    const response = await api.get('/animals', config);
    return response.data;
  },

  async getAnimal(id) {
    const response = await api.get(`/animals/${id}`);
    return response.data;
  },

  async getAnimalById(id) {
    const response = await api.get(`/animals/${id}`);
    return response.data;
  },

  async createAnimal(animalData) {
    const response = await api.post('/animals', animalData);
    return response.data;
  },

  async updateAnimal(id, animalData) {
    const response = await api.put(`/animals/${id}`, animalData);
    return response.data;
  },

  async deleteAnimal(id) {
    const response = await api.delete(`/animals/${id}`);
    return response.data;
  },

  // Operações de preferências
  async createPreferences(animalId, preferences) {
    const response = await api.post(`/animals/${animalId}/preferences`, preferences);
    return response.data;
  },

  async getPreferences(animalId) {
    const response = await api.get(`/animals/${animalId}/preferences`);
    return response.data;
  },

  async getAnimalPreferences(animalId) {
    const response = await api.get(`/animals/${animalId}/preferences`);
    return response.data;
  },

  async updatePreferences(animalId, preferences) {
    const response = await api.put(`/animals/${animalId}/preferences`, preferences);
    return response.data;
  },

  // Operações de ativação de cliente/tutor
  async activateClientAccess(animalId, activationData) {
    const response = await api.post(`/animals/${animalId}/activate-client`, activationData);
    return response.data;
  },

  async updateClientInfo(animalId, clientData) {
    const response = await api.patch(`/animals/${animalId}/update-client`, clientData);
    return response.data;
  },

  async toggleClientStatus(animalId, active) {
    const response = await api.patch(`/animals/${animalId}/client-status`, { active });
    return response.data;
  },

  async getClientInfo(animalId) {
    const response = await api.get(`/animals/${animalId}/client-info`);
    return response.data;
  }
};

export default animalService;
