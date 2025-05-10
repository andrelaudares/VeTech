import api from './api'; // Sua instância configurada do Axios ou similar

const getAnimals = () => {
  return api.get('/animals'); // Endpoint para listar animais da clínica logada
};

// Adicionar outros métodos conforme necessário (create, update, delete, getById)

const animalService = {
  getAnimals,
  // ...outros métodos
};

export default animalService;
