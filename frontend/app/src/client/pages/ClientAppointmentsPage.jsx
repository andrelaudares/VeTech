import { useState, useEffect } from 'react';
import { useClientAuth } from '../contexts/ClientAuthContext';
import { clientAuthService } from '../services/clientAuthService';

const ClientAppointmentsPage = () => {
  const { client } = useClientAuth();
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showRequestModal, setShowRequestModal] = useState(false);
  const [requestForm, setRequestForm] = useState({
    date: '',
    time: '',
    description: '',
    notes: ''
  });

  // Dados mockados para demonstração
  const mockAppointments = [
    {
      id: '1',
      date: '2024-01-15',
      time: '14:30',
      service_type: 'Consulta de Rotina',
      status: 'confirmed',
      animal_name: 'Rex',
      notes: 'Vacinação em dia',
      solicitado_por_cliente: false,
      status_solicitacao: null
    },
    {
      id: '2',
      date: '2024-01-20',
      time: '10:00',
      service_type: 'Exame de Sangue',
      status: 'pending',
      animal_name: 'Rex',
      notes: 'Jejum de 12 horas',
      solicitado_por_cliente: true,
      status_solicitacao: 'pendente'
    },
    {
      id: '3',
      date: '2024-01-10',
      time: '16:00',
      service_type: 'Castração',
      status: 'completed',
      animal_name: 'Rex',
      notes: 'Procedimento realizado com sucesso',
      solicitado_por_cliente: false,
      status_solicitacao: null
    },
    {
      id: '4',
      date: '2024-01-25',
      time: '09:30',
      service_type: 'Consulta Dermatológica',
      status: 'pending',
      animal_name: 'Rex',
      notes: 'Verificar alergia na pele',
      solicitado_por_cliente: true,
      status_solicitacao: 'aguardando_aprovacao'
    }
  ];

  useEffect(() => {
    const loadAppointments = async () => {
      try {
        // Simulando carregamento da API
        setTimeout(() => {
          setAppointments(mockAppointments);
          setLoading(false);
        }, 1000);
        
        // Código real da API (comentado para usar dados mockados)
        // const appointmentsData = await clientAuthService.getAppointments();
        // setAppointments(appointmentsData);
      } catch (error) {
        console.error('Erro ao carregar agendamentos:', error);
        setLoading(false);
      }
    };

    loadAppointments();
  }, []);

  const getStatusColor = (appointment) => {
    // Se foi solicitado pelo cliente, usar status da solicitação
    if (appointment.solicitado_por_cliente) {
      switch (appointment.status_solicitacao) {
        case 'aguardando_aprovacao':
          return 'bg-orange-100 text-orange-800';
        case 'pendente':
          return 'bg-yellow-100 text-yellow-800';
        case 'aprovado':
          return 'bg-green-100 text-green-800';
        case 'rejeitado':
          return 'bg-red-100 text-red-800';
        default:
          return 'bg-gray-100 text-gray-800';
      }
    }
    
    // Status normal do agendamento
    switch (appointment.status) {
      case 'confirmed':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      case 'completed':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (appointment) => {
    // Se foi solicitado pelo cliente, usar status da solicitação
    if (appointment.solicitado_por_cliente) {
      switch (appointment.status_solicitacao) {
        case 'aguardando_aprovacao':
          return 'Aguardando Aprovação';
        case 'pendente':
          return 'Solicitação Pendente';
        case 'aprovado':
          return 'Solicitação Aprovada';
        case 'rejeitado':
          return 'Solicitação Rejeitada';
        default:
          return 'Solicitação';
      }
    }
    
    // Status normal do agendamento
    switch (appointment.status) {
      case 'confirmed':
        return 'Confirmado';
      case 'pending':
        return 'Pendente';
      case 'cancelled':
        return 'Cancelado';
      case 'completed':
        return 'Concluído';
      default:
        return appointment.status;
    }
  };

  const handleRequestFormChange = (field, value) => {
    setRequestForm(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmitRequest = async () => {
    try {
      // Validação básica
      if (!requestForm.date || !requestForm.time || !requestForm.description) {
        alert('Por favor, preencha todos os campos obrigatórios.');
        return;
      }

      // Simulação de envio da solicitação
      const newRequest = {
        id: Date.now().toString(),
        date: requestForm.date,
        time: requestForm.time,
        service_type: requestForm.description,
        status: 'pending',
        animal_name: 'Rex',
        notes: requestForm.notes,
        solicitado_por_cliente: true,
        status_solicitacao: 'aguardando_aprovacao'
      };

      setAppointments(prev => [...prev, newRequest]);
      setShowRequestModal(false);
      setRequestForm({ date: '', time: '', description: '', notes: '' });
      
      alert('Solicitação enviada com sucesso! A clínica analisará sua solicitação.');
      
      // Aqui seria feita a chamada real para a API
      // await clientAuthService.requestAppointment(requestForm);
    } catch (error) {
      console.error('Erro ao enviar solicitação:', error);
      alert('Erro ao enviar solicitação. Tente novamente.');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Meus Agendamentos</h1>
              <p className="text-gray-600">Acompanhe suas consultas e procedimentos</p>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setShowRequestModal(true)}
                className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <svg className="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Solicitar Agendamento
              </button>
              <span className="text-sm text-gray-500">{client?.name || 'Tutor'}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {appointments.length > 0 ? (
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <ul className="divide-y divide-gray-200">
              {appointments.map((appointment) => (
                <li key={appointment.id}>
                  <div className="px-4 py-4 sm:px-6 hover:bg-gray-50">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className="flex-shrink-0">
                          <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                            <svg className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="flex items-center">
                            <p className="text-sm font-medium text-gray-900">
                              {appointment.service_type}
                            </p>
                            <span className={`ml-2 inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(appointment)}`}>
                              {getStatusText(appointment)}
                            </span>
                          </div>
                          <div className="mt-1 flex items-center text-sm text-gray-500">
                            <svg className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            <p>
                              {formatDate(appointment.date)} às {appointment.time}
                            </p>
                          </div>
                          {appointment.animal_name && (
                            <div className="mt-1 flex items-center text-sm text-gray-500">
                              <svg className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                              </svg>
                              <p>Pet: {appointment.animal_name}</p>
                            </div>
                          )}
                        </div>
                      </div>
                      <div className="flex items-center">
                        {appointment.status === 'pending' && (
                          <button className="ml-2 inline-flex items-center px-3 py-1 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                            Confirmar
                          </button>
                        )}
                        <svg className="ml-2 h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </div>
                    </div>
                    {appointment.notes && (
                      <div className="mt-3">
                        <p className="text-sm text-gray-600 bg-gray-50 p-3 rounded">
                          <strong>Observações:</strong> {appointment.notes}
                        </p>
                      </div>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="mx-auto h-24 w-24 text-gray-400">
              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="mt-4 text-lg font-medium text-gray-900">Nenhum agendamento encontrado</h3>
            <p className="mt-2 text-gray-500">
              Você ainda não possui agendamentos no sistema.
            </p>
            <div className="mt-6">
              <button className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                <svg className="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Agendar Consulta
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Modal de Solicitação de Agendamento */}
      {showRequestModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-medium text-gray-900">Solicitar Agendamento</h3>
                <button
                  onClick={() => setShowRequestModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              <form className="space-y-4">
                <div>
                  <label htmlFor="date" className="block text-sm font-medium text-gray-700">
                    Data Preferida *
                  </label>
                  <input
                    type="date"
                    id="date"
                    value={requestForm.date}
                    onChange={(e) => handleRequestFormChange('date', e.target.value)}
                    min={new Date().toISOString().split('T')[0]}
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="time" className="block text-sm font-medium text-gray-700">
                    Horário Preferido *
                  </label>
                  <select
                    id="time"
                    value={requestForm.time}
                    onChange={(e) => handleRequestFormChange('time', e.target.value)}
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    required
                  >
                    <option value="">Selecione um horário</option>
                    <option value="08:00">08:00</option>
                    <option value="09:00">09:00</option>
                    <option value="10:00">10:00</option>
                    <option value="11:00">11:00</option>
                    <option value="14:00">14:00</option>
                    <option value="15:00">15:00</option>
                    <option value="16:00">16:00</option>
                    <option value="17:00">17:00</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                    Tipo de Serviço *
                  </label>
                  <select
                    id="description"
                    value={requestForm.description}
                    onChange={(e) => handleRequestFormChange('description', e.target.value)}
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    required
                  >
                    <option value="">Selecione o serviço</option>
                    <option value="Consulta Veterinária">Consulta Veterinária</option>
                    <option value="Vacinação">Vacinação</option>
                    <option value="Exame de Rotina">Exame de Rotina</option>
                    <option value="Cirurgia">Cirurgia</option>
                    <option value="Emergência">Emergência</option>
                    <option value="Banho e Tosa">Banho e Tosa</option>
                    <option value="Outros">Outros</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="notes" className="block text-sm font-medium text-gray-700">
                    Observações
                  </label>
                  <textarea
                    id="notes"
                    rows={3}
                    value={requestForm.notes}
                    onChange={(e) => handleRequestFormChange('notes', e.target.value)}
                    placeholder="Descreva detalhes sobre o atendimento ou observações importantes..."
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  />
                </div>

                <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm text-yellow-700">
                        Esta é uma solicitação de agendamento. A clínica analisará sua solicitação e entrará em contato para confirmar.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="flex justify-end space-x-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowRequestModal(false)}
                    className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    Cancelar
                  </button>
                  <button
                    type="button"
                    onClick={handleSubmitRequest}
                    className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    Enviar Solicitação
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClientAppointmentsPage;