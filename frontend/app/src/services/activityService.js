import api from './api';
// Presumindo que getAuthHeaders está em utils/auth.js ou similar
// Se não estiver, precisaremos ajustar o caminho ou criar a função.
// Por agora, vamos simular sua existência ou adaptar de outros serviços.

const getAuthHeaders = () => {
  const token = localStorage.getItem('authToken'); // Ou de onde quer que você pegue o token
  if (token) {
    return { Authorization: `Bearer ${token}` };
  }
  return {};
};


const API_URL = ''; // Base URL da API

// --- Seção 1: Tipos de Atividades (Grupos 1 e 2) ---

// POST /api/v1/atividades
export const createActivityType = async (activityTypeData) => {
  try {
    const response = await api.post(`${API_URL}/atividades`, activityTypeData, { headers: getAuthHeaders() });
    return response.data;
  } catch (error) {
    console.error("Erro ao criar tipo de atividade:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao criar tipo de atividade.');
  }
};

// GET /api/v1/atividades
export const getActivityTypes = async (params = {}) => {
  try {
    const response = await api.get(`${API_URL}/atividades`, { headers: getAuthHeaders(), params });
    return response.data;
  } catch (error) {
    console.error("Erro ao listar tipos de atividade:", error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao listar tipos de atividade.');
  }
};

// GET /api/v1/atividades/{atividade_id}
export const getActivityTypeById = async (activityTypeId) => {
  try {
    const response = await api.get(`${API_URL}/atividades/${activityTypeId}`, { headers: getAuthHeaders() });
    return response.data;
  } catch (error) {
    console.error(`Erro ao buscar tipo de atividade ${activityTypeId}:`, error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao buscar tipo de atividade.');
  }
};

// PUT /api/v1/atividades/{atividade_id}
export const updateActivityType = async (activityTypeId, activityTypeData) => {
  try {
    const response = await api.put(`${API_URL}/atividades/${activityTypeId}`, activityTypeData, { headers: getAuthHeaders() });
    return response.data;
  } catch (error) {
    console.error(`Erro ao atualizar tipo de atividade ${activityTypeId}:`, error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao atualizar tipo de atividade.');
  }
};

// DELETE /api/v1/atividades/{atividade_id}
export const deleteActivityType = async (activityTypeId) => {
  try {
    // O backend retorna 204 No Content, então response.data pode não existir.
    await api.delete(`${API_URL}/atividades/${activityTypeId}`, { headers: getAuthHeaders() });
    return { message: 'Tipo de atividade excluído com sucesso.' }; 
  } catch (error) {
    console.error(`Erro ao excluir tipo de atividade ${activityTypeId}:`, error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao excluir tipo de atividade.');
  }
};

// --- Seção 2: Planos de Atividade (Grupos 3 e 4) ---

// POST /api/v1/animals/{animal_id}/planos-atividade
export const createActivityPlan = async (animalId, planData) => {
  try {
    // animal_id está na URL. clinic_id é pego pelo backend do token.
    // atividade_id deve estar em planData.
    const response = await api.post(`${API_URL}/animals/${animalId}/planos-atividade`, planData, { headers: getAuthHeaders() });
    return response.data;
  } catch (error) {
    console.error(`Erro ao criar plano de atividade para o animal ${animalId}:`, error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao criar plano de atividade.');
  }
};

// GET /api/v1/animals/{animal_id}/planos-atividade
export const getActivityPlansByAnimal = async (animalId, params = {}) => {
  try {
    const response = await api.get(`${API_URL}/animals/${animalId}/planos-atividade`, { headers: getAuthHeaders(), params });
    return response.data;
  } catch (error) {
    console.error(`Erro ao listar planos de atividade para o animal ${animalId}:`, error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao listar planos de atividade.');
  }
};

// GET /api/v1/planos-atividade/{plano_id}
export const getActivityPlanById = async (planId) => {
  try {
    const response = await api.get(`${API_URL}/planos-atividade/${planId}`, { headers: getAuthHeaders() });
    return response.data;
  } catch (error) {
    console.error(`Erro ao buscar plano de atividade ${planId}:`, error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao buscar plano de atividade.');
  }
};

// PUT /api/v1/planos-atividade/{plano_id}
export const updateActivityPlan = async (planId, planData) => {
  try {
    const response = await api.put(`${API_URL}/planos-atividade/${planId}`, planData, { headers: getAuthHeaders() });
    return response.data;
  } catch (error) {
    console.error(`Erro ao atualizar plano de atividade ${planId}:`, error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao atualizar plano de atividade.');
  }
};

// DELETE /api/v1/planos-atividade/{plano_id}
export const deleteActivityPlan = async (planId) => {
  try {
    await api.delete(`${API_URL}/planos-atividade/${planId}`, { headers: getAuthHeaders() });
    return { message: 'Plano de atividade excluído com sucesso.' };
  } catch (error) {
    console.error(`Erro ao excluir plano de atividade ${planId}:`, error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao excluir plano de atividade.');
  }
};

// --- Seção 3: Atividades Realizadas (Grupos 5 e 6) ---

// POST /api/v1/planos-atividade/{plano_id}/atividades-realizadas
export const logActivityExecution = async (planId, logData) => {
  try {
    // logData deve conter animal_id e os outros campos de ActivityLogCreate.
    // O backend python `activities.py` em `create_activity_log` usa `plan_info['animal_id']` se `log_data.animal_id` não corresponder,
    // mas `ActivityLogCreate` model espera `animal_id`.
    // É mais seguro que o frontend envie `animal_id` em `logData`.
    const response = await api.post(`${API_URL}/planos-atividade/${planId}/atividades-realizadas`, logData, { headers: getAuthHeaders() });
    return response.data;
  } catch (error) {
    console.error(`Erro ao registrar atividade realizada para o plano ${planId}:`, error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao registrar atividade realizada.');
  }
};

// GET /api/v1/animals/{animal_id}/atividades-realizadas (Histórico do Animal)
export const getActivityHistoryByAnimal = async (animalId, params = {}) => {
  try {
    const response = await api.get(`${API_URL}/animals/${animalId}/atividades-realizadas`, { headers: getAuthHeaders(), params });
    return response.data;
  } catch (error) {
    console.error(`Erro ao buscar histórico de atividades para o animal ${animalId}:`, error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao buscar histórico de atividades.');
  }
};

// GET /api/v1/planos-atividade/{plano_id}/atividades-realizadas (Logs de um Plano)
// Esta rota não está explicitamente no sprint5.md (backend), mas é útil e o backend a implementa.
export const getActivityLogsByPlan = async (planId, params = {}) => {
  try {
    const response = await api.get(`${API_URL}/planos-atividade/${planId}/atividades-realizadas`, { headers: getAuthHeaders(), params });
    return response.data;
  } catch (error) {
    console.error(`Erro ao listar logs de atividade para o plano ${planId}:`, error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao listar logs de atividade do plano.');
  }
};

// PUT /api/v1/atividades-realizadas/{realizacao_id}
export const updateActivityLog = async (logId, logUpdateData) => {
  try {
    const response = await api.put(`${API_URL}/atividades-realizadas/${logId}`, logUpdateData, { headers: getAuthHeaders() });
    return response.data;
  } catch (error) {
    console.error(`Erro ao atualizar registro de atividade realizada ${logId}:`, error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao atualizar registro de atividade.');
  }
};

// DELETE /api/v1/atividades-realizadas/{realizacao_id}
export const deleteActivityLog = async (logId) => {
  try {
    await api.delete(`${API_URL}/atividades-realizadas/${logId}`, { headers: getAuthHeaders() });
    return { message: 'Registro de atividade excluído com sucesso.' };
  } catch (error) {
    console.error(`Erro ao excluir registro de atividade realizada ${logId}:`, error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao excluir registro de atividade.');
  }
};

// --- Seção 4: Métricas de Atividade ---

// GET /api/v1/animals/{animal_id}/activity-metrics
export const getActivityMetrics = async (animalId, params = {}) => {
  try {
    const response = await api.get(`${API_URL}/animals/${animalId}/activity-metrics`, { headers: getAuthHeaders(), params });
    return response.data;
  } catch (error) {
    console.error(`Erro ao buscar métricas de atividade para o animal ${animalId}:`, error.response?.data || error.message);
    throw error.response?.data || new Error('Erro no servidor ao buscar métricas de atividade.');
  }
};

const activityService = {
  createActivityType,
  getActivityTypes,
  getActivityTypeById,
  updateActivityType,
  deleteActivityType,
  createActivityPlan,
  getActivityPlansByAnimal,
  getActivityPlanById,
  updateActivityPlan,
  deleteActivityPlan,
  logActivityExecution,
  getActivityHistoryByAnimal,
  getActivityLogsByPlan,
  updateActivityLog,
  deleteActivityLog,
  getActivityMetrics,
};

export default activityService; 