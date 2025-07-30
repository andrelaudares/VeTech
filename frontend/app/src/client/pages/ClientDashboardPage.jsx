import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Container,
  Grid,
  Paper,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  CardActions
} from '@mui/material';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import PetsIcon from '@mui/icons-material/Pets';
import FavoriteIcon from '@mui/icons-material/Favorite';
import NotificationsIcon from '@mui/icons-material/Notifications';
import RefreshIcon from '@mui/icons-material/Refresh';
import AddIcon from '@mui/icons-material/Add';
import VisibilityIcon from '@mui/icons-material/Visibility';
import { useNavigate } from 'react-router-dom';
import { useClientAuth } from '../contexts/ClientAuthContext';

const ClientDashboardPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated, loading: authLoading } = useClientAuth();
  
  // Estados para dados do dashboard (mockup)
  const [stats, setStats] = useState({
    pets_ativos: 2,
    consultas_agendadas: 1,
    saude_geral: 'Boa',
    lembretes_pendentes: 3
  });
  const [upcomingAppointments, setUpcomingAppointments] = useState([]);
  const [healthAlerts, setHealthAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Função para buscar dados do dashboard (mockup)
  const fetchDashboardData = async () => {
    if (!isAuthenticated) return;
    
    try {
      setLoading(true);
      setError(null);

      // Simular carregamento
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Dados mockados para demonstração
      const mockAppointments = [
        {
          id: 1,
          pet_name: 'Rex',
          clinic_name: 'Clínica VetCare',
          date: '2024-01-15',
          time: '14:30',
          type: 'Consulta de Rotina',
          status: 'agendado'
        },
        {
          id: 2,
          pet_name: 'Luna',
          clinic_name: 'Clínica VetCare',
          date: '2024-01-20',
          time: '10:00',
          type: 'Vacinação',
          status: 'agendado'
        }
      ];

      const mockAlerts = [
        {
          id: 1,
          type: 'vaccination',
          message: 'Rex precisa da vacina antirrábica em 5 dias',
          priority: 'high',
          icon: '💉'
        },
        {
          id: 2,
          type: 'checkup',
          message: 'Luna está com consulta de rotina agendada',
          priority: 'medium',
          icon: '🩺'
        },
        {
          id: 3,
          type: 'medication',
          message: 'Lembrete: Dar medicação para Rex às 18h',
          priority: 'medium',
          icon: '💊'
        }
      ];

      setUpcomingAppointments(mockAppointments);
      setHealthAlerts(mockAlerts);

    } catch (err) {
      console.error('Erro ao buscar dados do dashboard:', err);
      setError('Erro ao carregar dados do dashboard. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  // Buscar dados quando a autenticação estiver pronta
  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      fetchDashboardData();
    } else if (!authLoading && !isAuthenticated) {
      setLoading(false);
    }
  }, [isAuthenticated, authLoading]);

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
        <Typography sx={{ ml: 2 }}>Carregando dashboard...</Typography>
      </Container>
    );
  }

  if (!isAuthenticated) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="warning">Você precisa estar logado para acessar o dashboard.</Alert>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="error" action={
          <Button color="inherit" size="small" onClick={fetchDashboardData}>
            Tentar Novamente
          </Button>
        }>
          {error}
        </Alert>
      </Container>
    );
  }

  // Definir cards de estatísticas com dados mockados
  const statCards = [
    { 
      label: 'Meus Pets', 
      value: stats.pets_ativos || 0, 
      icon: <PetsIcon />,
      action: () => navigate('/client/animals')
    },
    { 
      label: 'Consultas Agendadas', 
      value: stats.consultas_agendadas || 0, 
      icon: <CalendarTodayIcon />,
      action: () => navigate('/client/appointments')
    },
    { 
      label: 'Saúde Geral', 
      value: stats.saude_geral || 'N/A', 
      icon: <FavoriteIcon />,
      action: () => navigate('/client/animals')
    },
    { 
      label: 'Lembretes', 
      value: stats.lembretes_pendentes || 0, 
      icon: <NotificationsIcon />,
      action: () => {}
    },
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h4" fontWeight="bold">Dashboard do Tutor</Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
            Bem-vindo! Aqui você pode acompanhar a saúde dos seus pets.
          </Typography>
        </Box>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={fetchDashboardData}
          disabled={loading}
          size="small"
        >
          Atualizar
        </Button>
      </Box>

      {/* Cards de Resumo */}
      <Grid container spacing={3}>
        {statCards.map((item, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Paper 
              sx={{ 
                p: 3, 
                display: 'flex', 
                alignItems: 'center', 
                gap: 2, 
                borderRadius: 2,
                cursor: item.action ? 'pointer' : 'default',
                '&:hover': item.action ? {
                  transform: 'translateY(-2px)',
                  boxShadow: 4
                } : {}
              }} 
              elevation={3}
              onClick={item.action}
            >
              <Box sx={{ fontSize: 32, color: '#23e865' }}>{item.icon}</Box>
              <Box>
                <Typography variant="h6" fontWeight="bold">{item.value}</Typography>
                <Typography variant="body2" color="text.secondary">{item.label}</Typography>
              </Box>
            </Paper>
          </Grid>
        ))}
      </Grid>

      {/* Próximas Consultas */}
      <Box mt={6}>
        <Typography variant="h6" fontWeight="bold" mb={2}>Próximas Consultas</Typography>
        <Paper elevation={2}>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow style={{backgroundColor: '#23e865'}}>
                  <TableCell>Pet</TableCell>
                  <TableCell>Clínica</TableCell>
                  <TableCell>Data</TableCell>
                  <TableCell>Horário</TableCell>
                  <TableCell>Tipo</TableCell>
                  <TableCell>Status</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {upcomingAppointments.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} align="center">
                      <Typography variant="body2" color="text.secondary" sx={{ py: 2 }}>
                        Nenhuma consulta agendada
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  upcomingAppointments.map((appointment, index) => (
                    <TableRow key={appointment.id || index}>
                      <TableCell>{appointment.pet_name || '-'}</TableCell>
                      <TableCell>{appointment.clinic_name || '-'}</TableCell>
                      <TableCell>{formatDate(appointment.date)}</TableCell>
                      <TableCell>{appointment.time || '-'}</TableCell>
                      <TableCell>{appointment.type || '-'}</TableCell>
                      <TableCell>
                        {getStatusChip(appointment.status)}
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </Box>

      {/* Alertas de Saúde e Ações Rápidas */}
      <Grid container spacing={3} mt={4}>
        {/* Alertas de Saúde */}
        <Grid item xs={12} md={8}>
          <Typography variant="h6" fontWeight="bold" mb={2}>Alertas de Saúde</Typography>
          {healthAlerts.length === 0 ? (
            <Paper sx={{ p: 3, backgroundColor: '#d4edda' }} elevation={1}>
              <Typography variant="body2" sx={{ color: '#155724' }}>
                ✅ Tudo em ordem! Nenhum alerta no momento.
              </Typography>
            </Paper>
          ) : (
            <Grid container spacing={2}>
              {healthAlerts.map((alert, index) => (
                <Grid item xs={12} key={index}>
                  <Paper sx={{ p: 2, backgroundColor: alert.priority === 'high' ? '#fff3cd' : '#e7f3ff' }} elevation={1}>
                    <Typography variant="body2" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <span>{alert.icon}</span>
                      {alert.message}
                    </Typography>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          )}
        </Grid>

        {/* Ações Rápidas */}
        <Grid item xs={12} md={4}>
          <Typography variant="h6" fontWeight="bold" mb={2}>Ações Rápidas</Typography>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Card elevation={2}>
                <CardContent sx={{ pb: 1 }}>
                  <Typography variant="h6" component="div" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <PetsIcon color="primary" />
                    Meus Pets
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Visualize e gerencie informações dos seus pets
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button 
                    size="small" 
                    startIcon={<VisibilityIcon />}
                    onClick={() => navigate('/client/animals')}
                  >
                    Ver Pets
                  </Button>
                </CardActions>
              </Card>
            </Grid>
            
            <Grid item xs={12}>
              <Card elevation={2}>
                <CardContent sx={{ pb: 1 }}>
                  <Typography variant="h6" component="div" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <CalendarTodayIcon color="primary" />
                    Agendamentos
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Veja seus agendamentos e histórico
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button 
                    size="small" 
                    startIcon={<VisibilityIcon />}
                    onClick={() => navigate('/client/appointments')}
                  >
                    Ver Agendamentos
                  </Button>
                </CardActions>
              </Card>
            </Grid>

            <Grid item xs={12}>
              <Card elevation={2}>
                <CardContent sx={{ pb: 1 }}>
                  <Typography variant="h6" component="div" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <NotificationsIcon color="primary" />
                    Lembretes
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Configure lembretes para medicações e cuidados
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button 
                    size="small" 
                    startIcon={<AddIcon />}
                    disabled
                    sx={{ color: 'text.secondary' }}
                  >
                    Em Breve
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Container>
  );
};

export default ClientDashboardPage;