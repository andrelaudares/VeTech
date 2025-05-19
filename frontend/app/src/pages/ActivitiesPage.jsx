import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Typography,
  Container,
  CircularProgress,
  Alert,
  Paper,
  Button,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  IconButton,
  Tooltip,
  TextField,
  Grid,
  LinearProgress,
  Chip,
  Rating,
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { useAnimal } from '../contexts/AnimalContext';
import activityService from '../services/activityService';
import ActivityTypeFormModal from '../components/activities/ActivityTypeFormModal';
import ActivityPlanFormModal from '../components/activities/ActivityPlanFormModal';
import LogActivityFormModal from '../components/activities/LogActivityFormModal';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';

// Ícones (exemplo, adicionar mais conforme o design)
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter'; // Para Atividades
import ListAltIcon from '@mui/icons-material/ListAlt'; // Para Tipos de Atividade
import EventNoteIcon from '@mui/icons-material/EventNote'; // Para Planos
import HistoryIcon from '@mui/icons-material/History'; // Para Histórico
import AddIcon from '@mui/icons-material/Add';
import PetsIcon from '@mui/icons-material/Pets';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import SearchIcon from '@mui/icons-material/Search';
import VisibilityIcon from '@mui/icons-material/Visibility';
import PlaylistPlayIcon from '@mui/icons-material/PlaylistPlay';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import PlayCircleOutlineIcon from '@mui/icons-material/PlayCircleOutline';
import EventAvailableIcon from '@mui/icons-material/EventAvailable';
import TimelapseIcon from '@mui/icons-material/Timelapse';
import MoodIcon from '@mui/icons-material/Mood';
import FitnessTrackerIcon from '@mui/icons-material/FitnessCenter';

// Paleta de cores (conforme GUIA_DESENVOLVIMENTO_FRONTEND.md e DietsPage.jsx)
const colors = {
  background: '#F9F9F9',        // Creme claro
  tableHeader: '#D8CAB8',     // Marrom-claro suave
  primaryAction: '#9DB8B2',    // Cinza-esverdeado
  primaryActionHover: '#82a8a0',
  secondaryAction: '#CFE0C3',  // Verde-oliva suave
  secondaryActionHover: '#b8d4a8',
  textPrimary: '#333333', // Cor de texto principal (mais escura para contraste)
  textSecondary: '#555555',
  paperBackground: '#FFFFFF',
  borderColor: '#E0E0E0',
  tabIndicator: '#9DB8B2',
  deleteColor: '#e57373',
  deleteColorHover: '#d32f2f',
  progressColor: '#9DB8B2',
  statusActive: '#9DB8B2', // Cinza-esverdeado para ativo
  statusConcluido: '#CFE0C3', // Verde-oliva suave para concluído
  statusInativo: '#BDBDBD', // Cinza para inativo
};

const calculateProgress = (plan, history) => {
  if (!plan || !history) return 0;
  if (plan.status === 'concluido') return 100;
  if (plan.status === 'inativo') return 0;

  const relevantHistory = history.filter(log => log.plano_atividade_id === plan.id);
  if (!relevantHistory.length) {
    // Se não há histórico, e o plano não tem data de fim mas está ativo, simular um pequeno progresso.
    // Se tiver data de fim, o cálculo por data ainda se aplica.
    if(plan.status === 'ativo' && !plan.data_fim) return 10; 
  }

  // Cálculo de progresso baseado em datas se não houver registros ou se ainda for relevante
  let progressByDate = 0;
  if (plan.data_inicio && plan.data_fim) {
    const start = new Date(plan.data_inicio).getTime();
    const end = new Date(plan.data_fim).getTime();
    const now = new Date().getTime();
    if (now >= end) progressByDate = 100;
    else if (now < start) progressByDate = 0;
    else progressByDate = Math.min(100, Math.max(0, ((now - start) / (end - start)) * 100));
  } else if (plan.data_inicio && plan.status === 'ativo') {
    // Se ativo, sem data_fim, mas com data_inicio, um pequeno progresso base
    progressByDate = 10; 
  }

  // Se houver histórico, tentar calcular progresso com base nele
  // Esta é uma simplificação. Um cálculo mais robusto poderia considerar
  // a frequência semanal e a duração das atividades registradas em relação ao período.
  if (relevantHistory.length > 0 && plan.frequencia_semanal && plan.duracao_minutos) {
    // Exemplo muito simples: cada registro conta como uma fração do objetivo semanal
    // Poderia ser muito mais elaborado, considerando o período total do plano.
    // Por agora, vamos apenas dar um boost se tiver histórico
    return Math.max(progressByDate, 30 + Math.min(70, relevantHistory.length * 10)); // Exemplo
  }
  
  return progressByDate; // Fallback para progresso por data ou o base se ativo
};

const getStatusChip = (status) => {
  switch (status) {
    case 'ativo':
      return <Chip label="Ativo" size="small" icon={<PlayCircleOutlineIcon />} sx={{ backgroundColor: colors.statusActive, color: 'white' }} />;
    case 'concluido':
      return <Chip label="Concluído" size="small" icon={<CheckCircleOutlineIcon />} sx={{ backgroundColor: colors.statusConcluido, color: colors.textPrimary }} />;
    case 'inativo':
      return <Chip label="Inativo" size="small" icon={<HighlightOffIcon />} sx={{ backgroundColor: colors.statusInativo, color: 'white' }} />;
    default:
      return <Chip label={status || 'N/A'} size="small" />;
  }
};

const ActivitiesPage = () => {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const { selectedAnimal, loading: animalLoading } = useAnimal();

  const [currentTab, setCurrentTab] = useState(0); // 0: Tipos, 1: Planos, 2: Histórico
  const [loadingData, setLoadingData] = useState(false);
  const [error, setError] = useState(null);

  // Estados para Tipos de Atividades (Grupo 1 e 2)
  const [activityTypes, setActivityTypes] = useState([]);
  const [loadingTypes, setLoadingTypes] = useState(false);
  const [errorTypes, setErrorTypes] = useState(null);
  const [openActivityTypeModal, setOpenActivityTypeModal] = useState(false);
  const [isEditingActivityType, setIsEditingActivityType] = useState(false);
  const [selectedActivityType, setSelectedActivityType] = useState(null);
  const [searchTermActivityTypes, setSearchTermActivityTypes] = useState('');
  const [pageActivityTypes, setPageActivityTypes] = useState(0);
  const [rowsPerPageActivityTypes, setRowsPerPageActivityTypes] = useState(5);

  // Estados para Planos de Atividade (Grupo 3, 4 e 5)
  const [activityPlans, setActivityPlans] = useState([]);
  const [loadingPlans, setLoadingPlans] = useState(false);
  const [errorPlans, setErrorPlans] = useState(null);
  const [searchTermActivityPlans, setSearchTermActivityPlans] = useState('');
  const [pageActivityPlans, setPageActivityPlans] = useState(0);
  const [rowsPerPageActivityPlans, setRowsPerPageActivityPlans] = useState(5);
  const [openActivityPlanModal, setOpenActivityPlanModal] = useState(false);
  const [isEditingActivityPlan, setIsEditingActivityPlan] = useState(false);
  const [selectedActivityPlan, setSelectedActivityPlan] = useState(null);
  
  const [openLogActivityModal, setOpenLogActivityModal] = useState(false);
  const [planToLog, setPlanToLog] = useState(null);

  // Estados para Histórico de Atividades (Grupo 6)
  const [activityHistory, setActivityHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [errorHistory, setErrorHistory] = useState(null);
  const [searchTermHistory, setSearchTermHistory] = useState('');
  const [pageHistory, setPageHistory] = useState(0);
  const [rowsPerPageHistory, setRowsPerPageHistory] = useState(10);

  const fetchActivityTypes = useCallback(async () => {
    setLoadingTypes(true);
    setErrorTypes(null);
    try {
      const typesResponse = await activityService.getActivityTypes();
      setActivityTypes(typesResponse || []);
    } catch (err) {
      console.error("Erro ao buscar tipos de atividade:", err);
      setErrorTypes(err.message || err.detail || "Falha ao carregar tipos de atividade.");
    } finally {
      setLoadingTypes(false);
    }
  }, []);

  const fetchDataForSelectedAnimal = useCallback(async () => {
    if (!selectedAnimal?.id || !isAuthenticated) {
      setActivityPlans([]);
      setActivityHistory([]);
      return;
    }
    setLoadingPlans(true);
    setErrorPlans(null);
    let plans = [];
    let history = [];

    try {
      const plansResponse = await activityService.getActivityPlansByAnimal(selectedAnimal.id);
      plans = plansResponse || [];
    } catch (err) {
      console.error("Erro ao buscar planos de atividade:", err);
      setErrorPlans(err.message || err.detail || "Falha ao carregar planos de atividade.");
    }
    
    setLoadingHistory(true);
    setErrorHistory(null);
    try {
      const historyResponse = await activityService.getActivityHistoryByAnimal(selectedAnimal.id);
      history = historyResponse || [];
      setActivityHistory(history);
    } catch (err) {
      console.error("Erro ao buscar histórico de atividades:", err);
      setErrorHistory(err.message || err.detail || "Falha ao carregar histórico de atividades.");
    } finally {
      setLoadingHistory(false);
    }

    // Calcular progresso dos planos APÓS ter o histórico
    const plansWithDetails = plans.map(plan => ({
      ...plan,
      nome_atividade: plan.nome_atividade || 'N/A',
      progress: calculateProgress(plan, history) // Passar histórico para cálculo
    }));
    setActivityPlans(plansWithDetails);
    setLoadingPlans(false); // Mover para após o processamento dos planos
  }, [selectedAnimal, isAuthenticated]);

  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      fetchActivityTypes(); // Tipos de atividade são globais, carregam independente do animal
    }
  }, [fetchActivityTypes, isAuthenticated, authLoading]);

  useEffect(() => {
    if (!authLoading && isAuthenticated && selectedAnimal) {
        fetchDataForSelectedAnimal();
    }
  }, [fetchDataForSelectedAnimal, selectedAnimal, isAuthenticated, authLoading]);

  const handleTabChange = (event, newValue) => {
    setCurrentTab(newValue);
    setPageActivityTypes(0);
    setSearchTermActivityTypes('');
    setPageActivityPlans(0);
    setSearchTermActivityPlans('');
  };

  // --- Handlers para Tipos de Atividade (Grupo 1 e 2) ---
  const handleOpenCreateActivityTypeModal = () => {
    setSelectedActivityType(null);
    setIsEditingActivityType(false);
    setOpenActivityTypeModal(true);
  };

  const handleOpenEditActivityTypeModal = (type) => {
    setSelectedActivityType(type);
    setIsEditingActivityType(true);
    setOpenActivityTypeModal(true);
  };

  const handleCloseActivityTypeModal = () => {
    setOpenActivityTypeModal(false);
    setSelectedActivityType(null);
    setIsEditingActivityType(false);
  };

  const handleSaveActivityTypeSuccess = () => {
    handleCloseActivityTypeModal();
    fetchActivityTypes(); // Recarregar lista de tipos
  };

  const handleDeleteActivityType = async (typeId) => {
    if (window.confirm("Tem certeza que deseja excluir este tipo de atividade? Isso pode afetar planos existentes.")) {
      setLoadingTypes(true);
      try {
        await activityService.deleteActivityType(typeId);
        fetchActivityTypes();
      } catch (err) {
        console.error("Erro ao excluir tipo de atividade:", err);
        setErrorTypes(err.message || err.detail || "Erro ao excluir tipo de atividade. Verifique se não está em uso.");
      } finally {
        setLoadingTypes(false);
      }
    }
  };

  const handleChangePageActivityTypes = (event, newPage) => {
    setPageActivityTypes(newPage);
  };

  const handleChangeRowsPerPageActivityTypes = (event) => {
    setRowsPerPageActivityTypes(parseInt(event.target.value, 10));
    setPageActivityTypes(0);
  };

  const handleSearchActivityTypesChange = (event) => {
    setSearchTermActivityTypes(event.target.value.toLowerCase());
    setPageActivityTypes(0);
  };

  const filteredActivityTypes = activityTypes.filter(type => {
    const searchTermLower = searchTermActivityTypes.toLowerCase();
    return (type.nome?.toLowerCase() || '').includes(searchTermLower) || 
           (type.tipo?.toLowerCase() || '').includes(searchTermLower);
  });

  // --- Handlers para Planos de Atividade (Grupo 3, 4 e 5) ---
  const handleOpenCreateActivityPlanModal = () => {
    if (!selectedAnimal?.id) {
        alert("Selecione um animal primeiro.");
        return;
    }
    setSelectedActivityPlan(null);
    setIsEditingActivityPlan(false);
    setOpenActivityPlanModal(true);
  };

  const handleOpenEditActivityPlanModal = (plan) => {
    setSelectedActivityPlan(plan);
    setIsEditingActivityPlan(true);
    setOpenActivityPlanModal(true);
  };

  const handleCloseActivityPlanModal = () => {
    setOpenActivityPlanModal(false);
  };

  const handleSaveActivityPlanSuccess = () => {
    handleCloseActivityPlanModal();
    fetchDataForSelectedAnimal();
  };

  const handleDeleteActivityPlan = async (planId) => {
    if (window.confirm("Tem certeza que deseja excluir este plano de atividade?")) {
      setLoadingPlans(true);
      try {
        await activityService.deleteActivityPlan(planId);
        fetchDataForSelectedAnimal();
      } catch (err) {
        console.error("Erro ao excluir plano de atividade:", err);
        setErrorPlans(err.message || "Erro ao excluir plano.");
      } finally {
        setLoadingPlans(false);
      }
    }
  };

  // --- Log de Atividade Handlers ---
  const handleOpenLogActivityModal = (plan) => {
    setPlanToLog(plan);
    setOpenLogActivityModal(true);
  };

  const handleCloseLogActivityModal = () => {
    setOpenLogActivityModal(false);
    setPlanToLog(null);
  };

  const handleLogActivitySuccess = () => {
    handleCloseLogActivityModal();
    fetchDataForSelectedAnimal();
  };

  const handleChangePageActivityPlans = (event, newPage) => {
    setPageActivityPlans(newPage);
  };

  const handleChangeRowsPerPageActivityPlans = (event) => {
    setRowsPerPageActivityPlans(parseInt(event.target.value, 10));
    setPageActivityPlans(0);
  };

  const handleSearchActivityPlansChange = (event) => {
    setSearchTermActivityPlans(event.target.value.toLowerCase());
    setPageActivityPlans(0);
  };

  const filteredActivityPlans = activityPlans.filter(plan => {
    const searchTermLower = searchTermActivityPlans.toLowerCase();
    return (plan.nome_atividade?.toLowerCase() || '').includes(searchTermLower) || 
           (plan.orientacoes?.toLowerCase() || '').includes(searchTermLower);
  });

  // --- Handlers para Histórico de Atividades (Grupo 6) ---
  const handleChangePageHistory = (event, newPage) => setPageHistory(newPage);
  const handleChangeRowsPerPageHistory = (event) => {
    setRowsPerPageHistory(parseInt(event.target.value, 10));
    setPageHistory(0);
  };
  const handleSearchHistoryChange = (event) => {
    setSearchTermHistory(event.target.value.toLowerCase());
    setPageHistory(0);
  };

  const filteredActivityHistory = activityHistory.filter(log => {
    const searchTermLower = searchTermHistory.toLowerCase();
    const logDate = log.data_hora_inicio ? format(new Date(log.data_hora_inicio), 'dd/MM/yyyy HH:mm') : '';
    // Adicionar nome_atividade ao histórico se não vier do backend (precisaria de um join ou mapeamento)
    // Por agora, assumindo que o `log` pode ter `plano_atividade.tipo_atividade.nome` ou similar
    // ou que `planToLog.nome_atividade` foi adicionado ao log no backend.
    // Vamos assumir que `log.nome_atividade_plano` existe para simplificar.
    return (
      (log.nome_atividade_plano?.toLowerCase() || '').includes(searchTermLower) ||
      logDate.includes(searchTermLower) ||
      (log.observacoes?.toLowerCase() || '').includes(searchTermLower)
    );
  });

  // ---- Renderização Condicional Inicial ----
  if (authLoading || (isAuthenticated && animalLoading && currentTab !== 0 && !selectedAnimal)) {
    let message = 'Carregando...';
    if (authLoading) message = 'Verificando autenticação...';
    else if (animalLoading && !selectedAnimal) message = 'Carregando dados do animal...';
    
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <CircularProgress />
        <Typography sx={{ ml: 2 }}>{message}</Typography>
      </Container>
    );
  }

  if (!isAuthenticated) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="warning">Você precisa estar logado para acessar esta página.</Alert>
      </Container>
    );
  }

  // Conforme sprint5-atividades(v2).md e HEADER_DOCS.md, a seleção de animal é obrigatória.
  if (!selectedAnimal) {
    return (
      <Container maxWidth="sm" sx={{ mt: 8, mb: 4, textAlign: 'center' }}>
        <Paper elevation={3} sx={{ p: { xs: 3, sm: 5 }, borderRadius: 2, backgroundColor: colors.paperBackground }}>
          <PetsIcon sx={{ fontSize: 60, color: colors.primaryAction, mb: 2 }} />
          <Typography variant="h5" component="h1" gutterBottom sx={{ color: colors.textPrimary, fontWeight: '500' }}>
            Selecione um Animal
          </Typography>
          <Typography variant="body1" sx={{ color: colors.textSecondary }}>
            Por favor, selecione um animal no menu superior para gerenciar as atividades físicas.
          </Typography>
        </Paper>
      </Container>
    );
  }

  // ---- Layout Principal da Página de Atividades ----
  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4, backgroundColor: colors.background, p: { xs: 2, md: 3 }, borderRadius: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3, flexWrap: 'wrap', gap: 2 }}>
        <Typography variant="h4" component="h1" sx={{ color: colors.textPrimary, fontWeight: '500' }}>
          Atividades Físicas {selectedAnimal && currentTab !==0 ? <>de <span style={{ color: colors.primaryAction }}>{selectedAnimal.name}</span></> : 'Globais'}
        </Typography>
        {currentTab === 0 && (
           <Button 
            variant="contained" 
            startIcon={<AddIcon />} 
            onClick={handleOpenCreateActivityTypeModal}
            sx={{ backgroundColor: colors.primaryAction, color: colors.paperBackground, '&:hover': { backgroundColor: colors.primaryActionHover } }}
           >
            Novo Tipo de Atividade
           </Button>
        )}
        {currentTab === 1 && selectedAnimal && (
            <Button 
                variant="contained" 
                startIcon={<AddIcon />}
                onClick={handleOpenCreateActivityPlanModal}
                sx={{ backgroundColor: colors.primaryAction, color: colors.paperBackground, '&:hover': { backgroundColor: colors.primaryActionHover } }}
            >
                Novo Plano de Atividade
            </Button>
        )}
      </Box>

      <Paper elevation={1} sx={{ mb: 3, borderRadius: '8px 8px 0 0', overflow: 'hidden' }}>
        <Tabs
          value={currentTab}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          variant="fullWidth"
          aria-label="abas de atividades físicas"
          sx={{ borderBottom: 1, borderColor: 'divider', '& .MuiTabs-indicator': { backgroundColor: colors.tabIndicator } }}
        >
          <Tab icon={<ListAltIcon />} iconPosition="start" label="Tipos de Atividade" sx={{ fontWeight: currentTab === 0 ? '600' : 'normal' }} />
          <Tab icon={<EventNoteIcon />} iconPosition="start" label="Planos do Animal" sx={{ fontWeight: currentTab === 1 ? '600' : 'normal' }} disabled={!selectedAnimal} />
          <Tab icon={<HistoryIcon />} iconPosition="start" label="Histórico de Atividades" sx={{ fontWeight: currentTab === 2 ? '600' : 'normal' }} disabled={!selectedAnimal}/>
        </Tabs>
      </Paper>

      {loadingData && (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', my: 5, color: colors.primaryAction }}>
          <CircularProgress color="inherit" />
          <Typography sx={{ ml: 2 }}>Carregando dados de atividades...</Typography>
        </Box>
      )}
      {error && (
        <Alert severity="error" sx={{ my: 2 }}>{error}</Alert>
      )}

      {!loadingData && !error && (
        <Box>
          {/* Aba 0: Tipos de Atividade (Grupo 1 e 2) */} 
          {currentTab === 0 && (
            <Paper elevation={2} sx={{ p: { xs: 1.5, md: 2.5 }, borderRadius: 2, backgroundColor: colors.paperBackground }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2.5, flexWrap: 'wrap', gap: 1.5}}>
                <Typography variant="h6" sx={{ color: colors.textPrimary, fontWeight: '500' }}>
                  Gerenciar Tipos de Atividades Globais
                </Typography>
                <TextField
                  label="Buscar por Nome ou Tipo"
                  variant="outlined"
                  size="small"
                  value={searchTermActivityTypes}
                  onChange={handleSearchActivityTypesChange}
                  InputProps={{
                    startAdornment: (
                      <SearchIcon position="start" sx={{ color: colors.textSecondary, mr: 0.5}} />
                    ),
                  }}
                  sx={{ minWidth: '280px'}}
                />
              </Box>
              {loadingTypes && <Box sx={{ display: 'flex', justifyContent: 'center', my: 3}}><CircularProgress sx={{color: colors.primaryAction}}/></Box>}
              {!loadingTypes && errorTypes && <Alert severity="error" sx={{my:2}}>{errorTypes}</Alert>}
              {!loadingTypes && !errorTypes && (
                activityTypes.length === 0 && !searchTermActivityTypes ? (
                  <Typography sx={{ textAlign: 'center', color: colors.textSecondary, py: 4 }}>Nenhum tipo de atividade cadastrado no sistema.</Typography>
                ) : filteredActivityTypes.length === 0 && searchTermActivityTypes ? (
                  <Typography sx={{ textAlign: 'center', color: colors.textSecondary, py: 4 }}>Nenhum tipo de atividade encontrado com o termo "{searchTermActivityTypes}".</Typography>
                ) : (
                  <>
                    <TableContainer sx={{ borderRadius: 1.5, border: `1px solid ${colors.borderColor}`}}>
                      <Table sx={{ minWidth: 650 }} aria-label="tabela de tipos de atividade" size="small">
                        <TableHead sx={{ backgroundColor: colors.tableHeader }}>
                          <TableRow>
                            <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }}>Nome</TableCell>
                            <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }}>Tipo</TableCell>
                            <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }} align="right">Calorias/min</TableCell>
                            <TableCell align="right" sx={{ color: colors.textPrimary, fontWeight: 'bold', pr: 2.5 }}>Ações</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {filteredActivityTypes.slice(pageActivityTypes * rowsPerPageActivityTypes, pageActivityTypes * rowsPerPageActivityTypes + rowsPerPageActivityTypes).map((type) => (
                            <TableRow key={type.id} hover sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                              <TableCell>{type.nome}</TableCell>
                              <TableCell>{type.tipo}</TableCell>
                              <TableCell align="right">{type.calorias_estimadas_por_minuto ?? '-'}</TableCell>
                              <TableCell align="right" sx={{ py: 0.5, pr: 1.5 }}>
                                <Tooltip title="Editar Tipo">
                                  <IconButton size="small" sx={{ color: colors.secondaryAction, '&:hover': { color: colors.secondaryActionHover }, mr: 0.5 }} onClick={() => handleOpenEditActivityTypeModal(type)}>
                                    <EditIcon fontSize="small" />
                                  </IconButton>
                                </Tooltip>
                                <Tooltip title="Excluir Tipo">
                                  <IconButton size="small" sx={{ color: colors.deleteColor, '&:hover': {color: colors.deleteColorHover} }} onClick={() => handleDeleteActivityType(type.id)}>
                                    <DeleteIcon fontSize="small" />
                                  </IconButton>
                                </Tooltip>
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                    <TablePagination
                      rowsPerPageOptions={[5, 10, 25]}
                      component="div"
                      count={filteredActivityTypes.length}
                      rowsPerPage={rowsPerPageActivityTypes}
                      page={pageActivityTypes}
                      onPageChange={handleChangePageActivityTypes}
                      onRowsPerPageChange={handleChangeRowsPerPageActivityTypes}
                      labelRowsPerPage="Tipos por página:"
                      labelDisplayedRows={({ from, to, count }) => `${from}–${to} de ${count}`}
                      sx={{ borderTop: `1px solid ${colors.borderColor}`, mt:0, borderBottomLeftRadius: '8px', borderBottomRightRadius: '8px', backgroundColor: colors.paperBackground }}
                    />
                  </>
                )
              )}
            </Paper>
          )}

          {/* Aba 1: Planos de Atividade (Grupo 3, 4 e 5) */} 
          {currentTab === 1 && selectedAnimal && (
            <Paper elevation={2} sx={{ p: { xs: 1.5, md: 2.5 }, borderRadius: 2, backgroundColor: colors.paperBackground }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2.5, flexWrap: 'wrap', gap: 1.5}}>
                <Typography variant="h6" sx={{ color: colors.textPrimary, fontWeight: '500' }}>Planos de Atividade</Typography>
                <TextField
                  label="Buscar Planos"
                  variant="outlined"
                  size="small"
                  value={searchTermActivityPlans}
                  onChange={handleSearchActivityPlansChange}
                  InputProps={{
                    startAdornment: (
                      <SearchIcon position="start" sx={{ color: colors.textSecondary, mr: 0.5}} />
                    ),
                  }}
                  sx={{ minWidth: '280px'}}
                />
              </Box>
              {loadingPlans && <Box sx={{ display: 'flex', justifyContent: 'center', my: 3}}><CircularProgress sx={{color: colors.primaryAction}}/></Box>}
              {!loadingPlans && errorPlans && <Alert severity="error" sx={{my:2}}>{errorPlans}</Alert>}
              {!loadingPlans && !errorPlans && (
                !filteredActivityPlans.length ? (
                  <Typography sx={{ textAlign: 'center', color: colors.textSecondary, py: 4 }}>Nenhum plano para "{searchTermActivityPlans}"</Typography>
                ) : (
                  <>
                    <TableContainer sx={{ borderRadius: 1.5, border: `1px solid ${colors.borderColor}`}}>
                      <Table sx={{ minWidth: 700 }} aria-label="tabela de planos de atividade" size="small">
                        <TableHead sx={{ backgroundColor: colors.tableHeader }}>
                          <TableRow>
                            <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }}>Atividade</TableCell>
                            <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }}>Frequência</TableCell>
                            <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }}>Duração</TableCell>
                            <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold', width: '20%' }}>Progresso</TableCell>
                            <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }} align="center">Status</TableCell>
                            <TableCell align="right" sx={{ color: colors.textPrimary, fontWeight: 'bold', pr: 2.5 }}>Ações</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {filteredActivityPlans.slice(pageActivityPlans * rowsPerPageActivityPlans, pageActivityPlans * rowsPerPageActivityPlans + rowsPerPageActivityPlans).map((plan) => (
                            <TableRow key={plan.id} hover>
                              <TableCell>{plan.nome_atividade}</TableCell>
                              <TableCell>{plan.frequencia_semanal ? `${plan.frequencia_semanal}x/sem` : '-'}</TableCell>
                              <TableCell>{plan.duracao_minutos ? `${plan.duracao_minutos} min` : '-'}</TableCell>
                              <TableCell>
                                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                  <Box sx={{ width: '100%', mr: 1 }}>
                                    <LinearProgress variant="determinate" value={plan.progress} sx={{ height: 10, borderRadius: 5, backgroundColor: '#e0e0e0', '& .MuiLinearProgress-bar': { backgroundColor: colors.progressColor } }} />
                                  </Box>
                                  <Box sx={{ minWidth: 35 }}><Typography variant="body2" color="text.secondary">{`${Math.round(plan.progress)}%`}</Typography></Box>
                                </Box>
                              </TableCell>
                              <TableCell align="center">{getStatusChip(plan.status)}</TableCell>
                              <TableCell align="right" sx={{ py: 0.5, pr: 1.5, whiteSpace: 'nowrap' }}>
                                <Tooltip title="Registrar Atividade"><IconButton size="small" sx={{ color: colors.secondaryAction, '&:hover': { color: colors.secondaryActionHover }, mr: 0.5 }} onClick={() => handleOpenLogActivityModal(plan)}><PlaylistPlayIcon fontSize="small" /></IconButton></Tooltip>
                                <Tooltip title="Editar Plano"><IconButton size="small" sx={{ color: colors.secondaryAction, '&:hover': { color: colors.secondaryActionHover }, mr: 0.5 }} onClick={() => handleOpenEditActivityPlanModal(plan)}><EditIcon fontSize="small" /></IconButton></Tooltip>
                                <Tooltip title="Excluir Plano"><IconButton size="small" sx={{ color: colors.deleteColor, '&:hover': {color: colors.deleteColorHover} }} onClick={() => handleDeleteActivityPlan(plan.id)}><DeleteIcon fontSize="small" /></IconButton></Tooltip>
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                    <TablePagination
                      rowsPerPageOptions={[5, 10, 25]}
                      component="div"
                      count={filteredActivityPlans.length}
                      rowsPerPage={rowsPerPageActivityPlans}
                      page={pageActivityPlans}
                      onPageChange={handleChangePageActivityPlans}
                      onRowsPerPageChange={handleChangeRowsPerPageActivityPlans}
                      labelRowsPerPage="Planos por página:"
                      labelDisplayedRows={({ from, to, count }) => `${from}–${to} de ${count}`}
                      sx={{ borderTop: `1px solid ${colors.borderColor}`, mt:0, borderBottomLeftRadius: '8px', borderBottomRightRadius: '8px', backgroundColor: colors.paperBackground }}
                    />
                  </>
                )
              )}
            </Paper>
          )}

          {/* Aba 2: Histórico de Atividades (Grupo 6) */} 
          {currentTab === 2 && selectedAnimal && (
            <Paper elevation={2} sx={{ p: { xs: 1.5, md: 2.5 }, borderRadius: 2, backgroundColor: colors.paperBackground }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2.5, flexWrap: 'wrap', gap: 1.5}}>
                <Typography variant="h6" sx={{ color: colors.textPrimary, fontWeight: '500' }}>
                    Histórico de Atividades de <span style={{ color: colors.primaryAction }}>{selectedAnimal.name}</span>
                </Typography>
                <TextField 
                    label="Buscar no Histórico (Nome, Data, Obs.)"
                    variant="outlined" 
                    size="small" 
                    value={searchTermHistory}
                    onChange={handleSearchHistoryChange} 
                    InputProps={{startAdornment: (<SearchIcon position="start" sx={{ color: colors.textSecondary, mr: 0.5}} />)}}
                    sx={{ minWidth: '300px'}}
                />
              </Box>
              {loadingHistory && <Box sx={{ display: 'flex', justifyContent: 'center', my: 3}}><CircularProgress sx={{color: colors.primaryAction}}/></Box>}
              {!loadingHistory && errorHistory && <Alert severity="error" sx={{my:2}}>{errorHistory}</Alert>}
              {!loadingHistory && !errorHistory && (
                !filteredActivityHistory.length ? (
                    <Typography sx={{ textAlign: 'center', color: colors.textSecondary, py: 4 }}> 
                        {searchTermHistory 
                            ? `Nenhum registro encontrado para "${searchTermHistory}".` 
                            : `Nenhum histórico de atividades encontrado para ${selectedAnimal.name}.`}
                    </Typography>
                ) : (
                <>
                    <TableContainer sx={{ borderRadius: 1.5, border: `1px solid ${colors.borderColor}`}}>
                        <Table sx={{ minWidth: 750 }} aria-label="tabela de histórico de atividades" size="small">
                            <TableHead sx={{ backgroundColor: colors.tableHeader }}><TableRow>
                                <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }}>Data e Hora</TableCell>
                                <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }}>Atividade (Plano)</TableCell>
                                <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }} align="right">Duração</TableCell>
                                <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }} align="center">Esforço</TableCell>
                                <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }} align="center">Satisfação</TableCell>
                                <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }}>Observações</TableCell>
                                <TableCell align="right" sx={{ color: colors.textPrimary, fontWeight: 'bold', pr: 2.5 }}>Ações</TableCell>
                            </TableRow></TableHead>
                            <TableBody>
                            {filteredActivityHistory.slice(pageHistory * rowsPerPageHistory, pageHistory * rowsPerPageHistory + rowsPerPageHistory).map((log) => (
                                <TableRow key={log.id} hover>
                                    <TableCell component="th" scope="row">
                                        {log.data_hora_inicio ? format(new Date(log.data_hora_inicio), 'dd/MM/yy HH:mm', { locale: ptBR }) : 'N/A'}
                                    </TableCell>
                                    <TableCell>{log.nome_atividade_plano || 'N/A' /* TODO: Popular este campo */}</TableCell>
                                    <TableCell align="right">{log.duracao_realizada_minutos ? `${log.duracao_realizada_minutos} min` : '-'}</TableCell>
                                    <TableCell align="center">
                                        <Tooltip title={`${log.esforco_percebido}%` || 'N/A'}>
                                            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                                <FitnessTrackerIcon fontSize="small" sx={{ opacity: Math.max(0.2, (log.esforco_percebido || 0) / 100), color: colors.primaryAction }}/>
                                                <Typography variant="caption" sx={{ml:0.5}}>{log.esforco_percebido}%</Typography>
                                            </Box>
                                        </Tooltip>
                                    </TableCell>
                                    <TableCell align="center">
                                        <Tooltip title={`${log.satisfacao} de 5` || 'N/A'}>
                                        <Rating name="read-only-satisfaction" value={log.satisfacao} readOnly size="small" emptyIcon={<MoodIcon style={{ opacity: 0.55 }} fontSize="inherit" />}/>
                                        </Tooltip>
                                    </TableCell>
                                    <TableCell>
                                        <Tooltip title={log.observacoes || 'Sem observações'}>
                                            <Typography variant="body2" noWrap sx={{ maxWidth: 150, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                                                {log.observacoes || '-'}
                                            </Typography>
                                        </Tooltip>
                                    </TableCell>
                                    <TableCell align="right" sx={{ py: 0.5, pr: 1.5, whiteSpace: 'nowrap' }}>
                                        <Tooltip title="Ver Detalhes (Em breve)"><IconButton size="small" disabled><VisibilityIcon fontSize="small" /></IconButton></Tooltip>
                                        <Tooltip title="Editar Log (Em breve)"><IconButton size="small" disabled sx={{mx:0.5}}><EditIcon fontSize="small" /></IconButton></Tooltip>
                                        <Tooltip title="Excluir Log (Em breve)"><IconButton size="small" disabled><DeleteIcon fontSize="small" /></IconButton></Tooltip>
                                    </TableCell>
                                </TableRow>
                            ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                    <TablePagination 
                        rowsPerPageOptions={[5, 10, 20, 50]}
                        component="div" 
                        count={filteredActivityHistory.length} 
                        rowsPerPage={rowsPerPageHistory}
                        page={pageHistory}
                        onPageChange={handleChangePageHistory}
                        onRowsPerPageChange={handleChangeRowsPerPageHistory}
                        labelRowsPerPage="Registros por página:"
                        labelDisplayedRows={({ from, to, count }) => `${from}–${to} de ${count}`}
                        sx={{ borderTop: `1px solid ${colors.borderColor}`, mt:0, borderRadius: '0 0 8px 8px', backgroundColor: colors.paperBackground }}
                    />
                </>
                )
            )}
        </Paper>
      )}
        </Box>
      )}

      {openActivityTypeModal && (
        <ActivityTypeFormModal 
            open={openActivityTypeModal}
            onClose={handleCloseActivityTypeModal}
            activityTypeData={selectedActivityType}
            isEditing={isEditingActivityType}
            onSaveSuccess={handleSaveActivityTypeSuccess}
        />
      )}
      {openActivityPlanModal && selectedAnimal && (
        <ActivityPlanFormModal
            open={openActivityPlanModal}
            onClose={handleCloseActivityPlanModal}
            planData={selectedActivityPlan}
            isEditing={isEditingActivityPlan}
            onSaveSuccess={handleSaveActivityPlanSuccess}
            animalId={selectedAnimal.id}
            availableActivityTypes={activityTypes}
        />
      )}
      
      {openLogActivityModal && selectedAnimal && planToLog && (
        <LogActivityFormModal 
            open={openLogActivityModal}
            onClose={handleCloseLogActivityModal}
            onSaveSuccess={handleLogActivitySuccess}
            planToLog={planToLog}
            animalId={selectedAnimal.id}
        />
      )}

    </Container>
  );
};

export default ActivitiesPage; 