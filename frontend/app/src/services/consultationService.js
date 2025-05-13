import api from './api';

const consultationService = {
  // Função para buscar todas as consultas, com filtro opcional por animal_id
  getConsultations: (animalId = null) => {
    const token = localStorage.getItem('userToken');
    console.log('ConsultationService: Token lido do localStorage para getConsultations:', token);
    let url = '/consultations';
    if (animalId) {
      url += `?animal_id=${animalId}`;
    }
    return api.get(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // Função para buscar uma consulta específica pelo ID
  getConsultationById: (consultationId) => {
    const token = localStorage.getItem('userToken');
    return api.get(`/consultations/${consultationId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // Função para criar uma nova consulta
  // consultationData deve ser um objeto como:
  // { animal_id, description, date (opcional, YYYY-MM-DDTHH:mm:ssZ) }
  createConsultation: (consultationData) => {
    const token = localStorage.getItem('userToken');
    return api.post('/consultations', consultationData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // Função para atualizar uma consulta existente
  // consultationData deve conter apenas os campos a serem atualizados
  updateConsultation: (consultationId, consultationData) => {
    const token = localStorage.getItem('userToken');
    return api.patch(`/consultations/${consultationId}`, consultationData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // Função para excluir uma consulta
  deleteConsultation: (consultationId) => {
    const token = localStorage.getItem('userToken');
    return api.delete(`/consultations/${consultationId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
};

export default consultationService; 