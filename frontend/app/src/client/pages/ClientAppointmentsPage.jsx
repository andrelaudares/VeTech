import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Typography,
  Container,
  Button,
  Paper,
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  CircularProgress,
  TextField,
  TablePagination,
  IconButton,
  Tooltip,
  Grid,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Card,
  CardContent,
  Chip,
  Divider,
  Snackbar,
  Alert,
  Badge
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import VisibilityIcon from '@mui/icons-material/Visibility';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import NotificationsIcon from '@mui/icons-material/Notifications';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
import PhoneIcon from '@mui/icons-material/Phone';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import PetsIcon from '@mui/icons-material/Pets';
import RefreshIcon from '@mui/icons-material/Refresh';
import { useClientAuth } from '../contexts/ClientAuthContext';
import { clientAuthService } from '../services/clientAuthService';

const ClientAppointmentsPage = () => {
  // Estados principais
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { client, isAuthenticated, loading: authLoading } = useClientAuth();

  // Estados para filtros e paginação
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  // Estados para modais
  const [openRequestModal, setOpenRequestModal] = useState(false);
  const [openDetailsModal, setOpenDetailsModal] = useState(false);
  const [selectedAppointment, setSelectedAppointment] = useState(null);

  // Estados para formulário de solicitação
  const [requestForm, setRequestForm] = useState({
    date: '',
    time: '',
    description: '',
    notes: ''
  });

  // Estado para snackbar
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success'
  });

  // Estados para estatísticas do dashboard
  const [stats, setStats] = useState({
    total_agendamentos: 0,
    agendamentos_proximos: 0,
    solicitacoes_pendentes: 0,
    consultas_concluidas: 0
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

  const fetchAppointments = useCallback(async () => {
    if (authLoading || !isAuthenticated) {
      if (!authLoading && !isAuthenticated) {
        setError("Você precisa estar logado para ver os agendamentos.");
        setAppointments([]);
      }
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      // Simulando carregamento da API
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setAppointments(mockAppointments);
      
      // Calcular estatísticas
      const today = new Date().toISOString().split('T')[0];
      const futureAppointments = mockAppointments.filter(apt => apt.date >= today && apt.status !== 'completed');
      const pendingRequests = mockAppointments.filter(apt => apt.solicitado_por_cliente && apt.status_solicitacao === 'aguardando_aprovacao');
      const completedAppointments = mockAppointments.filter(apt => apt.status === 'completed');
      
      setStats({
        total_agendamentos: mockAppointments.length,
        agendamentos_proximos: futureAppointments.length,
        solicitacoes_pendentes: pendingRequests.length,
        consultas_concluidas: completedAppointments.length
      });
      
    } catch (err) {
      console.error("Erro ao buscar agendamentos:", err);
      setError("Não foi possível carregar os agendamentos.");
      setAppointments([]);
    }
    setLoading(false);
  }, [isAuthenticated, authLoading]);

  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      fetchAppointments();
    } else if (!authLoading && !isAuthenticated) {
      setAppointments([]);
      setError("Você precisa estar logado para ver os agendamentos.");
    }
  }, [fetchAppointments, authLoading, isAuthenticated]);

  // Formatar data para exibição
  const formatDate = (dateString) => {
    if (!dateString) return '-';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('pt-BR');
    } catch (error) {
      return dateString;
    }
  };

  // Formatar status para exibição
  const getStatusChip = (appointment) => {
    // Se foi solicitado pelo cliente, usar status da solicitação
    if (appointment.solicitado_por_cliente) {
      switch (appointment.status_solicitacao) {
        case 'aguardando_aprovacao':
          return <Chip label="Aguardando Aprovação" color="warning" size="small" />;
        case 'pendente':
          return <Chip label="Solicitação Pendente" color="info" size="small" />;
        case 'aprovado':
          return <Chip label="Solicitação Aprovada" color="success" size="small" />;
        case 'rejeitado':
          return <Chip label="Solicitação Rejeitada" color="error" size="small" />;
        default:
          return <Chip label="Solicitação" color="default" size="small" />;
      }
    }
    
    // Status normal do agendamento
    switch (appointment.status) {
      case 'confirmed':
        return <Chip label="Confirmado" color="success" size="small" />;
      case 'pending':
        return <Chip label="Pendente" color="warning" size="small" />;
      case 'cancelled':
        return <Chip label="Cancelado" color="error" size="small" />;
      case 'completed':
        return <Chip label="Concluído" color="primary" size="small" />;
      default:
        return <Chip label={appointment.status || 'Agendado'} color="default" size="small" />;
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
        setSnackbar({
          open: true,
          message: 'Por favor, preencha todos os campos obrigatórios.',
          severity: 'error'
        });
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
      setOpenRequestModal(false);
      setRequestForm({ date: '', time: '', description: '', notes: '' });
      
      setSnackbar({
        open: true,
        message: 'Solicitação enviada com sucesso! A clínica analisará sua solicitação.',
        severity: 'success'
      });
      
    } catch (error) {
      console.error('Erro ao enviar solicitação:', error);
      setSnackbar({
        open: true,
        message: 'Erro ao enviar solicitação. Tente novamente.',
        severity: 'error'
      });
    }
  };

  // Estados de carregamento e erro
  if (authLoading || loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <CircularProgress />
        <Typography sx={{ ml: 2 }}>Carregando agendamentos...</Typography>
      </Container>
    );
  }

  if (!isAuthenticated) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="warning">Você precisa estar logado para acessar os agendamentos.</Alert>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="error" action={
          <Button color="inherit" size="small" onClick={fetchAppointments}>
            Tentar Novamente
          </Button>
        }>
          {error}
        </Alert>
      </Container>
    );
  }

  // Definir cards de estatísticas
  const statCards = [
    { 
      label: 'Total de Agendamentos', 
      value: stats.total_agendamentos || 0, 
      icon: <CalendarTodayIcon />,
      color: '#2196f3'
    },
    { 
      label: 'Próximos Agendamentos', 
      value: stats.agendamentos_proximos || 0, 
      icon: <CalendarTodayIcon />,
      color: '#4caf50'
    },
    { 
      label: 'Solicitações Pendentes', 
      value: stats.solicitacoes_pendentes || 0, 
      icon: <NotificationsIcon />,
      color: '#ff9800'
    },
    { 
      label: 'Consultas Concluídas', 
      value: stats.consultas_concluidas || 0, 
      icon: <PetsIcon />,
      color: '#9c27b0'
    }
  ];

  // Filtrar agendamentos
  const filteredAppointments = appointments.filter(appointment => {
    const matchesSearch = !searchTerm || 
      appointment.service_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
      appointment.animal_name.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = !statusFilter || appointment.status === statusFilter;
    
    return matchesSearch && matchesStatus;
  });

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', color: '#333' }}>
            Meus Agendamentos
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Acompanhe suas consultas e procedimentos
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <IconButton 
            onClick={fetchAppointments}
            color="primary"
            title="Atualizar"
          >
            <RefreshIcon />
          </IconButton>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setOpenRequestModal(true)}
            sx={{ backgroundColor: '#4caf50', '&:hover': { backgroundColor: '#45a049' } }}
          >
            Solicitar Agendamento
          </Button>
        </Box>
      </Box>

      {/* Cards de Estatísticas */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {statCards.map((card, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card sx={{ 
              height: '100%',
              background: `linear-gradient(135deg, ${card.color}20, ${card.color}10)`,
              border: `1px solid ${card.color}30`,
              '&:hover': { 
                transform: 'translateY(-2px)',
                boxShadow: 3,
                transition: 'all 0.3s ease'
              }
            }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box>
                    <Typography color="textSecondary" gutterBottom variant="body2">
                      {card.label}
                    </Typography>
                    <Typography variant="h4" component="div" sx={{ fontWeight: 'bold', color: card.color }}>
                      {card.value}
                    </Typography>
                  </Box>
                  <Box sx={{ color: card.color, opacity: 0.7 }}>
                    {card.icon}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Filtros */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Buscar por serviço ou animal"
              variant="outlined"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              size="small"
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <FormControl fullWidth size="small">
              <InputLabel>Status</InputLabel>
              <Select
                value={statusFilter}
                label="Status"
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <MenuItem value="">Todos</MenuItem>
                <MenuItem value="confirmed">Confirmado</MenuItem>
                <MenuItem value="pending">Pendente</MenuItem>
                <MenuItem value="completed">Concluído</MenuItem>
                <MenuItem value="cancelled">Cancelado</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={2}>
            <Button
              fullWidth
              variant="outlined"
              onClick={() => {
                setSearchTerm('');
                setStatusFilter('');
              }}
            >
              Limpar Filtros
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* Tabela de Agendamentos */}
      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        <TableContainer>
          <Table stickyHeader>
            <TableHead>
              <TableRow>
                <TableCell>Data</TableCell>
                <TableCell>Horário</TableCell>
                <TableCell>Animal</TableCell>
                <TableCell>Serviço</TableCell>
                <TableCell>Status</TableCell>
                <TableCell align="center">Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredAppointments.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} align="center" sx={{ py: 4 }}>
                    <Typography color="textSecondary">
                      Nenhum agendamento encontrado
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : (
                filteredAppointments
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((appointment) => (
                    <TableRow key={appointment.id} hover>
                      <TableCell>{formatDate(appointment.date)}</TableCell>
                      <TableCell>{appointment.time}</TableCell>
                      <TableCell>{appointment.animal_name}</TableCell>
                      <TableCell>{appointment.service_type}</TableCell>
                      <TableCell>{getStatusChip(appointment)}</TableCell>
                      <TableCell align="center">
                        <Tooltip title="Ver detalhes">
                          <IconButton
                            size="small"
                            onClick={() => {
                              setSelectedAppointment(appointment);
                              setOpenDetailsModal(true);
                            }}
                          >
                            <VisibilityIcon />
                          </IconButton>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={filteredAppointments.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={(event, newPage) => setPage(newPage)}
          onRowsPerPageChange={(event) => {
            setRowsPerPage(parseInt(event.target.value, 10));
            setPage(0);
          }}
        />
      </Paper>

      {/* Modal de Solicitação de Agendamento */}
      <Dialog
        open={openRequestModal}
        onClose={() => setOpenRequestModal(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle sx={{ 
          backgroundColor: '#4caf50', 
          color: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          gap: 1
        }}>
          <AddIcon />
          Solicitar Agendamento
        </DialogTitle>
        
        <DialogContent sx={{ p: 3 }}>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Data Preferida"
                type="date"
                value={requestForm.date}
                onChange={(e) => handleRequestFormChange('date', e.target.value)}
                InputLabelProps={{ shrink: true }}
                inputProps={{ min: new Date().toISOString().split('T')[0] }}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth required>
                <InputLabel>Horário Preferido</InputLabel>
                <Select
                  value={requestForm.time}
                  label="Horário Preferido"
                  onChange={(e) => handleRequestFormChange('time', e.target.value)}
                >
                  <MenuItem value="08:00">08:00</MenuItem>
                  <MenuItem value="09:00">09:00</MenuItem>
                  <MenuItem value="10:00">10:00</MenuItem>
                  <MenuItem value="11:00">11:00</MenuItem>
                  <MenuItem value="14:00">14:00</MenuItem>
                  <MenuItem value="15:00">15:00</MenuItem>
                  <MenuItem value="16:00">16:00</MenuItem>
                  <MenuItem value="17:00">17:00</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth required>
                <InputLabel>Tipo de Serviço</InputLabel>
                <Select
                  value={requestForm.description}
                  label="Tipo de Serviço"
                  onChange={(e) => handleRequestFormChange('description', e.target.value)}
                >
                  <MenuItem value="Consulta Veterinária">Consulta Veterinária</MenuItem>
                  <MenuItem value="Vacinação">Vacinação</MenuItem>
                  <MenuItem value="Exame de Rotina">Exame de Rotina</MenuItem>
                  <MenuItem value="Cirurgia">Cirurgia</MenuItem>
                  <MenuItem value="Emergência">Emergência</MenuItem>
                  <MenuItem value="Banho e Tosa">Banho e Tosa</MenuItem>
                  <MenuItem value="Outros">Outros</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Observações"
                multiline
                rows={3}
                value={requestForm.notes}
                onChange={(e) => handleRequestFormChange('notes', e.target.value)}
                placeholder="Descreva detalhes sobre o atendimento ou observações importantes..."
              />
            </Grid>
            <Grid item xs={12}>
              <Alert severity="info">
                Esta é uma solicitação de agendamento. A clínica analisará sua solicitação e entrará em contato para confirmar.
              </Alert>
            </Grid>
          </Grid>
        </DialogContent>
        
        <DialogActions sx={{ p: 2 }}>
          <Button 
            onClick={() => setOpenRequestModal(false)}
            sx={{ color: '#666' }}
          >
            Cancelar
          </Button>
          <Button
            onClick={handleSubmitRequest}
            variant="contained"
            sx={{ backgroundColor: '#4caf50', '&:hover': { backgroundColor: '#45a049' } }}
          >
            Enviar Solicitação
          </Button>
        </DialogActions>
      </Dialog>

      {/* Modal de Detalhes do Agendamento */}
      <Dialog
        open={openDetailsModal}
        onClose={() => setOpenDetailsModal(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle sx={{ 
          backgroundColor: '#2196f3', 
          color: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          gap: 1
        }}>
          <VisibilityIcon />
          Detalhes do Agendamento
        </DialogTitle>
        
        <DialogContent sx={{ p: 3 }}>
          {selectedAppointment && (
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="textSecondary">
                  <strong>Data:</strong> {formatDate(selectedAppointment.date)}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="textSecondary">
                  <strong>Horário:</strong> {selectedAppointment.time}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="textSecondary">
                  <strong>Animal:</strong> {selectedAppointment.animal_name}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="textSecondary">
                  <strong>Serviço:</strong> {selectedAppointment.service_type}
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="body2" color="textSecondary">
                  <strong>Status:</strong> {getStatusChip(selectedAppointment)}
                </Typography>
              </Grid>
              {selectedAppointment.notes && (
                <Grid item xs={12}>
                  <Typography variant="body2" color="textSecondary">
                    <strong>Observações:</strong> {selectedAppointment.notes}
                  </Typography>
                </Grid>
              )}
            </Grid>
          )}
        </DialogContent>
        
        <DialogActions sx={{ p: 2 }}>
          <Button 
            onClick={() => setOpenDetailsModal(false)}
            sx={{ color: '#666' }}
          >
            Fechar
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert 
          onClose={() => setSnackbar({ ...snackbar, open: false })} 
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default ClientAppointmentsPage;