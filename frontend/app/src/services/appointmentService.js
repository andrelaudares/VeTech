import api from './api';

const appointmentService = {
  // Função para buscar todos os agendamentos, com filtro opcional por animal_id
  getAppointments: (animalId = null, status = null) => {
    const token = localStorage.getItem('token');
    let url = '/appointments';
    const params = [];
    if (animalId) params.push(`animal_id=${animalId}`);
    if (status) params.push(`status=${status}`);
    if (params.length > 0) url += `?${params.join('&')}`;
    return api.get(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // Função para buscar um agendamento específico pelo ID
  getAppointmentById: (appointmentId) => {
    const token = localStorage.getItem('token');
    return api.get(`/appointments/${appointmentId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // Função para criar um novo agendamento
  // appointmentData deve ser um objeto como:
  // { animal_id, date, start_time, end_time (opcional), description, status }
  createAppointment: (appointmentData) => {
    const token = localStorage.getItem('token');
    return api.post('/appointments', appointmentData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // Função para atualizar um agendamento existente
  // appointmentData deve conter apenas os campos a serem atualizados
  updateAppointment: (appointmentId, appointmentData) => {
    const token = localStorage.getItem('token');
    return api.patch(`/appointments/${appointmentId}`, appointmentData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // Função para excluir um agendamento
  deleteAppointment: (appointmentId) => {
    const token = localStorage.getItem('token');
    return api.delete(`/appointments/${appointmentId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
};

export default appointmentService; 