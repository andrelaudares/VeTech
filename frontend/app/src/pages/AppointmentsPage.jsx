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
import appointmentService from '../services/appointmentService';
import { animalService } from '../services/animalService';
import { useAnimal } from '../contexts/AnimalContext';
import { useAuth } from '../contexts/AuthContext';
import AppointmentFormModal from '../components/appointments/AppointmentFormModal';
import AppointmentDetailsModal from '../components/appointments/AppointmentDetailsModal';

const AppointmentsPage = () => {
  // Estados principais
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [allAnimals, setAllAnimals] = useState([]); // Estado local para todos os animais
  const { selectedAnimal } = useAnimal();
  const { isAuthenticated, loading: authLoading } = useAuth();

  // Estados para filtros e paginação
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  // Estados para modais
  const [openFormModal, setOpenFormModal] = useState(false);
  const [openDetailsModal, setOpenDetailsModal] = useState(false);
  const [selectedAppointment, setSelectedAppointment] = useState(null);
  const [isEditing, setIsEditing] = useState(false);

  // Estados para solicitações pendentes
  const [pendingRequests, setPendingRequests] = useState([]);
  const [openNotificationsModal, setOpenNotificationsModal] = useState(false);
  const [loadingRequests, setLoadingRequests] = useState(false);

  // Estado para snackbar
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success'
  });

  // Estados para estatísticas do dashboard
  const [stats, setStats] = useState({
    total_agendamentos: 0,
    agendamentos_hoje: 0,
    solicitacoes_pendentes: 0,
    animais_atendidos: 0
  });

  // Buscar todos os animais ao carregar a página
  useEffect(() => {
    const loadAnimals = async () => {
      if (!isAuthenticated) return;
      try {
        // Forçar uso do token de clínica
        const animals = await animalService.getAllAnimals(true);
        setAllAnimals(animals);
      } catch (err) {
        console.error('Erro ao carregar animais:', err);
      }
    };
    loadAnimals();
  }, [isAuthenticated]);

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
      const animalIdFilter = selectedAnimal ? selectedAnimal.id : null;
      const response = await appointmentService.getAppointments(animalIdFilter);
      console.log('API Response for Appointments (Animal ID: ' + animalIdFilter + '):', response.data);
      
      const appointmentsData = response.data || [];
      setAppointments(appointmentsData);
      
      // Calcular estatísticas
      const today = new Date().toISOString().split('T')[0];
      const todayAppointments = appointmentsData.filter(apt => apt.date === today);
      const uniqueAnimals = new Set(appointmentsData.map(apt => apt.animal_id));
      
      setStats({
        total_agendamentos: appointmentsData.length,
        agendamentos_hoje: todayAppointments.length,
        solicitacoes_pendentes: pendingRequests.length,
        animais_atendidos: uniqueAnimals.size
      });
      
    } catch (err) {
      console.error("Erro ao buscar agendamentos:", err);
      setError(err.response?.data?.detail || "Não foi possível carregar os agendamentos.");
      setAppointments([]);
    }
    setLoading(false);
  }, [selectedAnimal, isAuthenticated, authLoading, pendingRequests.length]);

  // Função para buscar solicitações pendentes (mockado por enquanto)
  const fetchPendingRequests = useCallback(async () => {
    if (!isAuthenticated) return;
    
    setLoadingRequests(true);
    try {
      // Simulação de dados mockados para solicitações pendentes
      const mockRequests = [
        {
          id: 1,
          tutor_name: "Maria Silva",
          phone: "(11) 99999-1234",
          animal_name: "Rex",
          requested_date: "2024-01-15",
          requested_time: "14:00",
          service_type: "Consulta Veterinária",
          notes: "Rex está com tosse há alguns dias",
          created_at: "2024-01-10T10:30:00"
        },
        {
          id: 2,
          tutor_name: "João Santos",
          phone: "(11) 88888-5678",
          animal_name: "Luna",
          requested_date: "2024-01-16",
          requested_time: "09:00",
          service_type: "Vacinação",
          notes: "Vacinação anual da Luna",
          created_at: "2024-01-11T15:45:00"
        },
        {
          id: 3,
          tutor_name: "Ana Costa",
          phone: "(11) 77777-9012",
          animal_name: "Mimi",
          requested_date: "2024-01-17",
          requested_time: "16:00",
          service_type: "Banho e Tosa",
          notes: "",
          created_at: "2024-01-12T09:15:00"
        }
      ];
      
      setPendingRequests(mockRequests);
      
      // Atualizar estatísticas
      setStats(prev => ({
        ...prev,
        solicitacoes_pendentes: mockRequests.length
      }));
      
    } catch (err) {
      console.error("Erro ao buscar solicitações pendentes:", err);
    }
    setLoadingRequests(false);
  }, [isAuthenticated]);

  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      fetchAppointments();
      fetchPendingRequests();
    } else if (!authLoading && !isAuthenticated) {
      setAppointments([]);
      setError("Você precisa estar logado para ver os agendamentos.");
    }
  }, [fetchAppointments, fetchPendingRequests, authLoading, isAuthenticated]);

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
  const getStatusChip = (status) => {
    const statusLower = status?.toLowerCase() || '';
    
    switch (statusLower) {
      case 'agendado':
        return <Chip label="Agendado" color="primary" size="small" />;
      case 'concluido':
      case 'concluído':
        return <Chip label="Concluído" color="success" size="small" />;
      case 'cancelado':
        return <Chip label="Cancelado" color="error" size="small" />;
      default:
        return <Chip label={status || 'Agendado'} color="default" size="small" />;
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
      label: 'Agendamentos Hoje', 
      value: stats.agendamentos_hoje || 0, 
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
      label: 'Animais Atendidos', 
      value: stats.animais_atendidos || 0, 
      icon: <PetsIcon />,
      color: '#9c27b0'
    }
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', color: '#333' }}>
          Agendamentos
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <IconButton 
            onClick={fetchAppointments}
            color="primary"
            title="Atualizar"
          >
            <RefreshIcon />
          </IconButton>
          <IconButton 
            onClick={() => setOpenNotificationsModal(true)}
            color="warning"
            title="Solicitações Pendentes"
          >
            <Badge badgeContent={pendingRequests.length} color="error">
              <NotificationsIcon />
            </Badge>
          </IconButton>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setOpenFormModal(true)}
            sx={{ backgroundColor: '#4caf50', '&:hover': { backgroundColor: '#45a049' } }}
          >
            Novo Agendamento
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
              label="Buscar por tutor ou animal"
              variant="outlined"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              size="small"
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <FormControl fullWidth size="small" sx={{ minWidth: 200 }}>
              <InputLabel>Status</InputLabel>
              <Select
                value={statusFilter}
                label="Status"
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <MenuItem value="">Todos</MenuItem>
                <MenuItem value="agendado">Agendado</MenuItem>
                <MenuItem value="concluido">Concluído</MenuItem>
                <MenuItem value="cancelado">Cancelado</MenuItem>
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
                <TableCell>Serviço</TableCell>
                <TableCell>Status</TableCell>
                <TableCell align="center">Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {appointments.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} align="center" sx={{ py: 4 }}>
                    <Typography color="textSecondary">
                      Nenhum agendamento encontrado
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : (
                appointments
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((appointment) => (
                    <TableRow key={appointment.id} hover>
                      <TableCell>{formatDate(appointment.date)}</TableCell>
                      <TableCell>{appointment.start_time || appointment.time || '-'}</TableCell>
                      <TableCell>{appointment.service_type || appointment.description || '-'}</TableCell>
                      <TableCell>{getStatusChip(appointment.status)}</TableCell>
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
                        <Tooltip title="Editar">
                          <IconButton
                            size="small"
                            onClick={() => {
                              setSelectedAppointment(appointment);
                              setIsEditing(true);
                              setOpenFormModal(true);
                            }}
                          >
                            <EditIcon />
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
          count={appointments.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={(event, newPage) => setPage(newPage)}
          onRowsPerPageChange={(event) => {
            setRowsPerPage(parseInt(event.target.value, 10));
            setPage(0);
          }}
        />
      </Paper>

      {/* Modais */}
      {openFormModal && (
        <AppointmentFormModal
          open={openFormModal}
          onClose={() => {
            setOpenFormModal(false);
            setSelectedAppointment(null);
            setIsEditing(false);
          }}
          appointment={selectedAppointment}
          isEditing={isEditing}
          allAnimals={allAnimals}
          selectedAnimalContext={selectedAnimal}
        />
      )}
      
      {openDetailsModal && (
        <AppointmentDetailsModal
          open={openDetailsModal}
          onClose={() => {
            setOpenDetailsModal(false);
            setSelectedAppointment(null);
          }}
          appointment={selectedAppointment}
          getAnimalNameById={(id) => allAnimals.find(a => a.id === id)?.name || 'Animal não encontrado'}
          onEdit={() => {
            setIsEditing(true);
            setOpenFormModal(true);
            setOpenDetailsModal(false);
          }}
        />
      )}

      {/* Modal de Notificações */}
      <Dialog
        open={openNotificationsModal}
        onClose={() => setOpenNotificationsModal(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle sx={{ 
          backgroundColor: '#4caf50', 
          color: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          gap: 1
        }}>
          <NotificationsIcon />
          Solicitações de Agendamento Pendentes
          {pendingRequests.length > 0 && (
            <Chip 
              label={pendingRequests.length} 
              size="small" 
              sx={{ 
                backgroundColor: '#ff9800', 
                color: 'white',
                fontWeight: 'bold'
              }} 
            />
          )}
        </DialogTitle>
        
        <DialogContent sx={{ p: 3 }}>
          {loadingRequests ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 4 }}>
              <CircularProgress />
              <Typography sx={{ ml: 2 }}>Carregando solicitações...</Typography>
            </Box>
          ) : pendingRequests.length === 0 ? (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <NotificationsIcon sx={{ fontSize: 48, color: '#666', mb: 2 }} />
              <Typography variant="h6" color="textSecondary">
                Nenhuma solicitação pendente
              </Typography>
              <Typography color="textSecondary">
                Quando os tutores enviarem solicitações de agendamento, elas aparecerão aqui.
              </Typography>
            </Box>
          ) : (
            <Grid container spacing={2}>
              {pendingRequests.map((request) => (
                <Grid item xs={12} key={request.id}>
                  <Card sx={{ 
                    border: '1px solid #e0e0e0',
                    borderRadius: 2,
                    '&:hover': { boxShadow: 3 }
                  }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                        <Box>
                          <Typography variant="h6" sx={{ color: '#333', fontWeight: 'bold' }}>
                            {request.tutor_name}
                          </Typography>
                          <Typography variant="body2" color="textSecondary" sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                            <PhoneIcon fontSize="small" />
                            {request.phone}
                          </Typography>
                        </Box>
                        <Chip 
                          label="Pendente" 
                          color="warning" 
                          size="small"
                          sx={{ fontWeight: 'bold' }}
                        />
                      </Box>
                      
                      <Divider sx={{ my: 2 }} />
                      
                      <Grid container spacing={2}>
                        <Grid item xs={12} sm={6}>
                          <Typography variant="body2" color="textSecondary">
                            <strong>Animal:</strong> {request.animal_name}
                          </Typography>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                          <Typography variant="body2" color="textSecondary">
                            <strong>Serviço:</strong> {request.service_type}
                          </Typography>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                          <Typography variant="body2" color="textSecondary">
                            <strong>Data Solicitada:</strong> {formatDate(request.requested_date)}
                          </Typography>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                          <Typography variant="body2" color="textSecondary">
                            <strong>Horário:</strong> {request.requested_time}
                          </Typography>
                        </Grid>
                        {request.notes && (
                          <Grid item xs={12}>
                            <Typography variant="body2" color="textSecondary">
                              <strong>Observações:</strong> {request.notes}
                            </Typography>
                          </Grid>
                        )}
                      </Grid>
                      
                      <Box sx={{ 
                        mt: 2, 
                        p: 2, 
                        backgroundColor: '#fff3e0', 
                        borderRadius: 1,
                        border: '1px solid #ffcc02'
                      }}>
                        <Typography variant="body2" color="textSecondary">
                          <strong>Atenção:</strong> Caso o horário sugerido não seja adequado, 
                          entre em contato com o tutor no número <strong>{request.phone}</strong> para decidir um horário.
                        </Typography>
                      </Box>
                      
                      <Box sx={{ display: 'flex', gap: 1, mt: 3, justifyContent: 'flex-end' }}>
                        <Button
                          variant="outlined"
                          color="error"
                          startIcon={<CloseIcon />}
                          size="small"
                        >
                          Recusar
                        </Button>
                        <Button
                          variant="contained"
                          color="success"
                          startIcon={<CheckIcon />}
                          size="small"
                        >
                          Confirmar
                        </Button>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          )}
        </DialogContent>
        
        <DialogActions sx={{ p: 2 }}>
          <Button 
            onClick={() => setOpenNotificationsModal(false)}
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

export default AppointmentsPage;