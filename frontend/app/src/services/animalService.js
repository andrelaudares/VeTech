import api from './api'; // Sua instância configurada do Axios ou similar

const getAnimals = () => {
  return api.get('/animals'); // Endpoint para listar animais da clínica logada
};

// Adicionar outros métodos conforme necessário (create, update, delete, getById)

const animalService = {
  getAnimals,
  getAllAnimals: async () => {
    const token = localStorage.getItem('userToken'); // Adicionado para debug
    console.log('AnimalService: Token lido do localStorage para getAllAnimals:', token); // Adicionado para debug
    const response = await api.get('/animals');
    return response.data;
  },
  createAnimal: async (animalData) => {
    const response = await api.post('/animals', animalData);
    return response.data;
  },
  getAnimalById: async (animalId) => {
    const response = await api.get(`/animals/${animalId}`);
    return response.data;
  },
  updateAnimal: async (animalId, animalData) => {
    const response = await api.patch(`/animals/${animalId}`, animalData);
    return response.data;
  },
  deleteAnimal: async (animalId) => {
    const response = await api.delete(`/animals/${animalId}`);
    return response.data; // Ou response.status se não houver corpo na resposta
  },
  getAnimalPreferences: async (animalId) => {
    const response = await api.get(`/animals/${animalId}/preferences`);
    return response.data;
  },
  createAnimalPreferences: async (animalId, preferencesData) => {
    const response = await api.post(`/animals/${animalId}/preferences`, preferencesData);
    return response.data;
  },
  updateAnimalPreferences: async (animalId, preferencesData) => {
    const response = await api.patch(`/animals/${animalId}/preferences`, preferencesData);
    return response.data;
  }
};

export default animalService;
