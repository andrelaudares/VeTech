import api from './api';

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

// 1. Dietas
export const createDiet = async (animalId, dietData) => {
  try {
    const response = await api.post(`/animals/${animalId}/diets`, dietData, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao criar dieta:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao criar dieta.');
  }
};

export const getDietsByAnimal = async (animalId) => {
  try {
    const response = await api.get(`/animals/${animalId}/diets`, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar dietas do animal:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao buscar dietas do animal.');
  }
};

export const getDietById = async (dietId) => {
  try {
    const response = await api.get(`/diets/${dietId}`, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar detalhes da dieta:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao buscar detalhes da dieta.');
  }
};

export const updateDiet = async (dietId, dietData) => {
  try {
    const response = await api.put(`/diets/${dietId}`, dietData, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao atualizar dieta:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao atualizar dieta.');
  }
};

export const deleteDiet = async (dietId) => {
  try {
    const response = await api.delete(`/diets/${dietId}`, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao excluir dieta:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao excluir dieta.');
  }
};

// 2. Opções de Dieta
export const createDietOption = async (dietId, optionData) => {
  try {
    const response = await api.post(`/diets/${dietId}/options`, optionData, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao criar opção de dieta:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao criar opção de dieta.');
  }
};

// GET /diets/{diet_id}/options - Não é necessário, pois os detalhes da dieta já incluem as opções.

export const updateDietOption = async (optionId, optionData) => {
  try {
    const response = await api.put(`/diet-options/${optionId}`, optionData, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao atualizar opção de dieta:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao atualizar opção de dieta.');
  }
};

export const deleteDietOption = async (optionId) => {
  try {
    const response = await api.delete(`/diet-options/${optionId}`, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao excluir opção de dieta:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao excluir opção de dieta.');
  }
};

// 3. Alimentos da Dieta
export const addFoodToOption = async (optionId, foodData) => {
  try {
    const response = await api.post(`/diet-options/${optionId}/foods`, foodData, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao adicionar alimento à opção:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao adicionar alimento à opção.');
  }
};

export const getFoodsByOption = async (optionId) => {
  try {
    const response = await api.get(`/diet-options/${optionId}/foods`, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar alimentos da opção:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao buscar alimentos da opção.');
  }
};

export const updateDietFood = async (foodId, foodData) => {
  try {
    const response = await api.put(`/diet-foods/${foodId}`, foodData, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao atualizar alimento da dieta:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao atualizar alimento da dieta.');
  }
};

export const deleteDietFood = async (foodId) => {
  try {
    const response = await api.delete(`/diet-foods/${foodId}`, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao excluir alimento da dieta:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao excluir alimento da dieta.');
  }
};

// 4. Alimentos Restritos
export const addRestrictedFood = async (animalId, foodData) => {
  try {
    const response = await api.post(`/animals/${animalId}/restricted-foods`, foodData, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao adicionar alimento restrito:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao adicionar alimento restrito.');
  }
};

export const getRestrictedFoods = async (animalId) => {
  try {
    const response = await api.get(`/animals/${animalId}/restricted-foods`, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar alimentos restritos:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao buscar alimentos restritos.');
  }
};

export const updateRestrictedFood = async (animalId, foodId, foodData) => {
  try {
    const response = await api.put(`/animals/${animalId}/restricted-foods/${foodId}`, foodData, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao atualizar alimento restrito:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao atualizar alimento restrito.');
  }
};

export const deleteRestrictedFood = async (animalId, foodId) => {
  try {
    const response = await api.delete(`/animals/${animalId}/restricted-foods/${foodId}`, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao excluir alimento restrito:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao excluir alimento restrito.');
  }
};

// 5. Snacks
export const addSnack = async (animalId, snackData) => {
  try {
    const response = await api.post(`/animals/${animalId}/snacks`, snackData, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao adicionar snack:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao adicionar snack.');
  }
};

export const getSnacks = async (animalId) => {
  try {
    const response = await api.get(`/animals/${animalId}/snacks`, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar snacks:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao buscar snacks.');
  }
};

export const updateSnack = async (animalId, snackId, snackData) => {
  try {
    const response = await api.put(`/animals/${animalId}/snacks/${snackId}`, snackData, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao atualizar snack:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao atualizar snack.');
  }
};

export const deleteSnack = async (animalId, snackId) => {
  try {
    const response = await api.delete(`/animals/${animalId}/snacks/${snackId}`, {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao excluir snack:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao excluir snack.');
  }
};

const dietService = {
  createDiet,
  getDietsByAnimal,
  getDietById,
  updateDiet,
  deleteDiet,
  createDietOption,
  updateDietOption,
  deleteDietOption,
  addFoodToOption,
  getFoodsByOption,
  updateDietFood,
  deleteDietFood,
  addRestrictedFood,
  getRestrictedFoods,
  updateRestrictedFood,
  deleteRestrictedFood,
  addSnack,
  getSnacks,
  updateSnack,
  deleteSnack,
};

export default dietService; 