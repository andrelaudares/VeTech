import api from './api';

const appointmentService = {
  // Função para buscar todos os agendamentos, com filtro opcional por animal_id
  getAppointments: (animalId = null) => {
    const token = localStorage.getItem('userToken');
    console.log('AppointmentService: Token lido do localStorage para getAppointments:', token);
    let url = '/appointments';
    if (animalId) {
      url += `?animal_id=${animalId}`;
    }
    return api.get(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // Função para buscar um agendamento específico pelo ID
  getAppointmentById: (appointmentId) => {
    const token = localStorage.getItem('userToken');
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
    const token = localStorage.getItem('userToken');
    return api.post('/appointments', appointmentData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // Função para atualizar um agendamento existente
  // appointmentData deve conter apenas os campos a serem atualizados
  updateAppointment: (appointmentId, appointmentData) => {
    const token = localStorage.getItem('userToken');
    return api.patch(`/appointments/${appointmentId}`, appointmentData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // Função para excluir um agendamento
  deleteAppointment: (appointmentId) => {
    const token = localStorage.getItem('userToken');
    return api.delete(`/appointments/${appointmentId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
};

export default appointmentService; 