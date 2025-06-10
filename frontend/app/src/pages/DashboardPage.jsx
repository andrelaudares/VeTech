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
  Alert
} from '@mui/material';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import PetsIcon from '@mui/icons-material/Pets';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import DirectionsRunIcon from '@mui/icons-material/DirectionsRun';
import RefreshIcon from '@mui/icons-material/Refresh';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import dashboardService from '../services/dashboardService';

const DashboardPage = () => {

  const navigate = useNavigate();
  const { isAuthenticated, loading: authLoading } = useAuth();
  
  // Estados para dados do dashboard
  const [stats, setStats] = useState({
    consultas_hoje: 0,
    animais_ativos: 0,
    animais_sem_dietas: 0,
    animais_sem_atividades: 0
  });
  const [appointmentsToday, setAppointmentsToday] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Função para buscar dados do dashboard
  const fetchDashboardData = async () => {
    if (!isAuthenticated) return;
    
    try {
      setLoading(true);
      setError(null);

      // Buscar todas as informações em paralelo
      const [statsData, appointmentsData, alertsData] = await Promise.all([
        dashboardService.getStats(),
        dashboardService.getAppointmentsToday(),
        dashboardService.getAlerts()
      ]);

      setStats(statsData);
      setAppointmentsToday(appointmentsData);
      setAlerts(alertsData);

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

  // Formatar hora para exibição
  const formatTime = (timeString) => {
    if (!timeString) return '-';
    try {
      // Se for apenas hora (HH:MM:SS), usar diretamente
      if (timeString.includes(':') && !timeString.includes('T')) {
        return timeString.substring(0, 5); // Retorna HH:MM
      }
      // Se for datetime completo, extrair apenas a hora
      const date = new Date(timeString);
      return date.toLocaleTimeString('pt-BR', { 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    } catch (error) {
      return timeString;
    }
  };

  // Formatar status para exibição
  const getStatusChip = (status) => {
    const statusLower = status?.toLowerCase() || '';
    
    switch (statusLower) {
      case 'confirmado':
      case 'agendado':
        return <Chip label="Agendado" color="primary" size="small" />;
      case 'concluido':
      case 'concluído':
        return <Chip label="Concluído" color="success" size="small" />;
      case 'cancelado':
        return <Chip label="Cancelado" color="error" size="small" />;
      case 'em_andamento':
        return <Chip label="Em Andamento" color="warning" size="small" />;
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

  // Definir cards de estatísticas com dados reais
  const statCards = [
    { 
      label: 'Consultas Hoje', 
      value: stats.consultas_hoje || 0, 
      icon: <CalendarTodayIcon /> 
    },
    { 
      label: 'Animais Ativos', 
      value: stats.animais_ativos || 0, 
      icon: <PetsIcon /> 
    },
    { 
      label: 'Sem Dietas', 
      value: stats.animais_sem_dietas || 0, 
      icon: <RestaurantIcon /> 
    },
    { 
      label: 'Sem Atividades', 
      value: stats.animais_sem_atividades || 0, 
      icon: <DirectionsRunIcon /> 
    },
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" fontWeight="bold">Dashboard</Typography>
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
            <Paper sx={{ p: 3, display: 'flex', alignItems: 'center', gap: 2, borderRadius: 2 }} elevation={3}>
              <Box sx={{ fontSize: 32, color: '#23e865' }}>{item.icon}</Box>
              <Box>
                <Typography variant="h6" fontWeight="bold">{item.value}</Typography>
                <Typography variant="body2" color="text.secondary">{item.label}</Typography>
              </Box>
            </Paper>
          </Grid>
        ))}
      </Grid>

      {/* Tabela de Consultas */}
      <Box mt={6}>
        <Typography variant="h6" fontWeight="bold" mb={2}>Consultas de Hoje</Typography>
        <Paper elevation={2}>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow style={{backgroundColor: '#23e865'}}>
                  <TableCell>Animal</TableCell>
                  <TableCell>Dono</TableCell>
                  <TableCell>Horário</TableCell>
                  <TableCell>Status</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {appointmentsToday.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={4} align="center">
                      <Typography variant="body2" color="text.secondary" sx={{ py: 2 }}>
                        Nenhuma consulta agendada para hoje
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  appointmentsToday.map((appointment, index) => (
                    <TableRow key={appointment.id || index}>
                      <TableCell>{appointment.animal_name || '-'}</TableCell>
                      <TableCell>{appointment.owner_name || '-'}</TableCell>
                      <TableCell>{formatTime(appointment.time_scheduled)}</TableCell>
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

      {/* Avisos e Ações Rápidas */}
      <Box mt={6}>
        <Typography variant="h6" fontWeight="bold" mb={2}>Avisos</Typography>
        {alerts.length === 0 ? (
          <Paper sx={{ p: 3, backgroundColor: '#d4edda' }} elevation={1}>
            <Typography variant="body2" sx={{ color: '#155724' }}>
              ✅ Tudo em ordem! Nenhum alerta no momento.
            </Typography>
          </Paper>
        ) : (
          <Paper sx={{ p: 3, backgroundColor: '#fff3cd' }} elevation={1}>
            {alerts.map((alert, index) => (
              <Typography key={index} variant="body2" sx={{ mb: index < alerts.length - 1 ? 1 : 0 }}>
                {alert.icon} {alert.message}
              </Typography>
            ))}
          </Paper>
        )}

        <Box display="flex" gap={2} mt={3}>
          <Button variant="contained" color="primary" onClick={() => navigate('/agendamentos')}>+ Novo Agendamento</Button>
          <Button variant="outlined" color="primary" onClick={() => {navigate('/animais')}}>+ Novo Animal</Button>
        </Box>
      </Box>
    </Container>
  );
};

export default DashboardPage;
