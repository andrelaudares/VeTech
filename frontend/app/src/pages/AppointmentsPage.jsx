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
  InputLabel
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import VisibilityIcon from '@mui/icons-material/Visibility';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import appointmentService from '../services/appointmentService';
import { useAnimal } from '../contexts/AnimalContext';
import { useAuth } from '../contexts/AuthContext';
import AppointmentFormModal from '../components/appointments/AppointmentFormModal';
import AppointmentDetailsModal from '../components/appointments/AppointmentDetailsModal';

// Componentes dos Modais (serão criados depois)
// import AppointmentDetailsModal from '../components/appointments/AppointmentDetailsModal';

// Paleta de cores
const colors = {
  background: '#F9F9F9', // Creme claro
  tableHeader: '#D8CAB8', // Marrom-claro suave
  buttonPrimary: '#9DB8B2', // Cinza-esverdeado
  buttonPrimaryHover: '#82a8a0',
  buttonSecondary: '#CFE0C3', // Verde-oliva suave
  buttonSecondaryHover: '#b8d4a8',
  textPrimary: '#333',
  textSecondary: '#555',
  paperBackground: '#FFFFFF', // Branco para cards e paper
  borderColor: '#E0E0E0' // Cor suave para bordas
};

const AppointmentsPage = () => {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { selectedAnimal, animals: allAnimals } = useAnimal(); // `animals` do contexto são todos os animais da clínica
  const { isAuthenticated, loading: authLoading } = useAuth();
  
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  const [openFormModal, setOpenFormModal] = useState(false);
  const [openDetailsModal, setOpenDetailsModal] = useState(false);
  const [selectedAppointment, setSelectedAppointment] = useState(null);
  const [isEditing, setIsEditing] = useState(false);

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
      // O endpoint de agendamentos já pode ser filtrado por animal_id, conforme sprint3.md e appointmentService
      const response = await appointmentService.getAppointments(animalIdFilter);
      setAppointments(response.data || []);
    } catch (err) {
      console.error("Erro ao buscar agendamentos:", err);
      setError(err.response?.data?.detail || "Não foi possível carregar os agendamentos.");
      setAppointments([]);
    }
    setLoading(false);
  }, [selectedAnimal, isAuthenticated, authLoading]);

  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      fetchAppointments();
    } else if (!authLoading && !isAuthenticated) {
      setAppointments([]);
      setError("Você precisa estar logado para ver os agendamentos.");
      setLoading(false);
    }
  }, [fetchAppointments, isAuthenticated, authLoading]);

  const getAnimalNameById = useCallback((animalId) => {
    const animal = allAnimals.find(a => a.id === animalId);
    return animal ? animal.name : 'Desconhecido';
  }, [allAnimals]);

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value.toLowerCase());
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleStatusFilterChange = (event) => {
    setStatusFilter(event.target.value);
    setPage(0); // Resetar para a primeira página ao mudar filtro
  };

  const handleOpenCreateModal = () => {
    setSelectedAppointment(null);
    setIsEditing(false);
    setOpenFormModal(true);
  };

  const handleOpenEditModal = (appointment) => {
    setSelectedAppointment(appointment);
    setIsEditing(true);
    setOpenFormModal(true);
  };

  const handleOpenDetailsModal = (appointment) => {
    setSelectedAppointment(appointment);
    setOpenDetailsModal(true);
  };

  const handleCloseModals = () => {
    setOpenFormModal(false);
    setOpenDetailsModal(false);
    setSelectedAppointment(null);
    setIsEditing(false);
    fetchAppointments(); // Rebuscar os dados após fechar modal de formulário
  };

  const handleDeleteAppointment = async (appointmentId) => {
    if (window.confirm("Tem certeza que deseja excluir este agendamento?")) {
      try {
        setLoading(true); // Poderia ter um loading específico para a ação
        await appointmentService.deleteAppointment(appointmentId);
        fetchAppointments(); // Rebuscar após a exclusão
      } catch (err) {
        console.error("Erro ao excluir agendamento:", err);
        setError(err.response?.data?.detail || "Erro ao excluir agendamento.");
      } finally {
        setLoading(false);
      }
    }
  };

  const filteredAppointments = appointments.filter(appointment => {
    const searchTermLower = searchTerm.toLowerCase();
    const description = appointment.description?.toLowerCase() || '';
    const status = appointment.status?.toLowerCase() || '';

    const matchesSearch = description.includes(searchTermLower) || status.includes(searchTermLower);

    const matchesStatusFilter = statusFilter ? appointment.status === statusFilter : true;

    return matchesSearch && matchesStatusFilter;
  });

  if (authLoading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <CircularProgress />
        <Typography sx={{ ml: 2 }}>Verificando autenticação...</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4, backgroundColor: colors.background, p: { xs: 2, md: 3 }, borderRadius: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3, flexWrap: 'wrap' }}>
        <Typography variant="h4" component="h1" sx={{ color: colors.textPrimary, fontWeight: '500', mb: { xs: 2, sm: 0 } }}>
          Agendamentos
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          sx={{
            backgroundColor: colors.buttonPrimary, 
            color: colors.paperBackground, 
            '&:hover': { backgroundColor: colors.buttonPrimaryHover },
            padding: '8px 16px',
            fontSize: '0.9rem'
          }}
          onClick={handleOpenCreateModal} 
        >
          Novo Agendamento
        </Button>
      </Box>

      <Paper sx={{ p: 2.5, mb: 3, backgroundColor: colors.paperBackground, borderRadius: 2, boxShadow: '0px 4px 12px rgba(0,0,0,0.05)' }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={8}>
            <TextField 
              fullWidth 
              label="Buscar por Descrição ou Status"
              variant="outlined" 
              value={searchTerm}
              onChange={handleSearchChange}
              size="small"
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth variant="outlined" size="small">
              <InputLabel id="status-filter-label">Filtrar por Status</InputLabel>
              <Select
                labelId="status-filter-label"
                value={statusFilter}
                onChange={handleStatusFilterChange}
                label="Filtrar por Status"
              >
                <MenuItem value="">
                  <em>Todos os Status</em>
                </MenuItem>
                <MenuItem value="scheduled">Agendado</MenuItem>
                <MenuItem value="completed">Concluído</MenuItem>
                <MenuItem value="cancelled">Cancelado</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
        {/* TODO: Adicionar Filtro de intervalo de datas */}
      </Paper>

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', my: 5, color: colors.buttonPrimary }}>
          <CircularProgress color="inherit" />
          <Typography sx={{ ml: 2 }}>Carregando agendamentos...</Typography>
        </Box>
      )}
      {error && (
        <Paper sx={{ p:2, textAlign: 'center', my:3, backgroundColor: '#ffebee', color: '#c62828', borderRadius: 2}} elevation={3}>
          <Typography variant="h6">Oops!</Typography>
          <Typography>{error}</Typography>
        </Paper>
      )}
      {!loading && !error && (
        <Paper elevation={2} sx={{ borderRadius: 2, overflow: 'hidden', backgroundColor: colors.paperBackground }}>
          <TableContainer>
            <Table sx={{ minWidth: 700 }} aria-label="tabela de agendamentos">
              <TableHead sx={{ backgroundColor: colors.tableHeader }}>
                <TableRow>
                  <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold', py: 1.5 }}>Data</TableCell>
                  <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold', py: 1.5 }}>Hora</TableCell>
                  {/* Removido temporariamente até que o filtro do header seja o único */}
                  { !selectedAnimal && <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold', py: 1.5 }}>Animal</TableCell> }
                  <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold', py: 1.5 }}>Descrição</TableCell>
                  <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold', py: 1.5 }}>Status</TableCell>
                  <TableCell align="right" sx={{ color: colors.textPrimary, fontWeight: 'bold', py: 1.5, pr: 2.5 }}>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredAppointments.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((appointment) => (
                  <TableRow key={appointment.id} hover sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                    <TableCell sx={{ py: 1 }}>{new Date(appointment.date).toLocaleDateString()}</TableCell>
                    <TableCell sx={{ py: 1 }}>{appointment.start_time ? appointment.start_time.substring(0,5) : '--'}</TableCell>
                    {/* Exibir o nome do animal apenas se nenhum animal estiver selecionado no header */}
                    { !selectedAnimal && <TableCell sx={{ py: 1 }}>{getAnimalNameById(appointment.animal_id)}</TableCell> }
                    <TableCell sx={{ py: 1, maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                       <Tooltip title={appointment.description} placement="bottom-start">
                           <span>{appointment.description || '-'}</span>
                       </Tooltip>
                    </TableCell>
                    <TableCell sx={{ py: 1 }}>
                        <Box component="span" sx={{
                            p: '4px 8px', 
                            borderRadius: '12px', 
                            color: colors.paperBackground,
                            backgroundColor: appointment.status === 'scheduled' ? colors.buttonPrimary : 
                                             appointment.status === 'completed' ? colors.buttonSecondary : 
                                             appointment.status === 'cancelled' ? '#f44336' : colors.textSecondary,
                            fontSize: '0.75rem',
                            fontWeight: '500'
                        }}>
                            {appointment.status === 'scheduled' ? 'Agendado' :
                             appointment.status === 'completed' ? 'Concluído' :
                             appointment.status === 'cancelled' ? 'Cancelado' : appointment.status}
                        </Box>
                    </TableCell>
                    <TableCell align="right" sx={{ py: 0.5, pr: 1.5 }}>
                      <Tooltip title="Visualizar">
                        <IconButton size="small" sx={{ color: colors.buttonPrimary, mr: 0.5 }} onClick={() => handleOpenDetailsModal(appointment)}>
                          <VisibilityIcon fontSize="small"/>
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Editar">
                        <IconButton size="small" sx={{ color: colors.buttonSecondary, '&:hover': {color: colors.buttonSecondaryHover}, mr: 0.5 }} onClick={() => handleOpenEditModal(appointment)}>
                          <EditIcon fontSize="small"/>
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Excluir">
                        <IconButton size="small" sx={{ color: '#e57373', '&:hover': {color: '#d32f2f'} }} onClick={() => handleDeleteAppointment(appointment.id)}>
                          <DeleteIcon fontSize="small"/>
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
                {filteredAppointments.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={6} sx={{ textAlign: 'center', py: 4, color: colors.textSecondary }}>
                      Nenhum agendamento encontrado com os filtros atuais.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
            <TablePagination
              rowsPerPageOptions={[5, 10, 25]}
              component="div"
              count={filteredAppointments.length}
              rowsPerPage={rowsPerPage}
              page={page}
              onPageChange={handleChangePage}
              onRowsPerPageChange={handleChangeRowsPerPage}
              labelRowsPerPage="Itens por página:"
              labelDisplayedRows={({ from, to, count }) => `${from}–${to} de ${count}`}
              sx={{ borderTop: `1px solid ${colors.borderColor}` }}
            />
          </TableContainer>
        </Paper>
      )}
      {/* TODO: Implementar AppointmentFormModal e AppointmentDetailsModal */}
      {openFormModal && (
        <AppointmentFormModal 
          open={openFormModal} 
          onClose={handleCloseModals} 
          appointment={selectedAppointment} 
          isEditing={isEditing} 
          allAnimals={allAnimals} 
          selectedAnimalContext={selectedAnimal} 
        />
      )}
      {openDetailsModal && (
        <AppointmentDetailsModal 
          open={openDetailsModal} 
          onClose={handleCloseModals} 
          appointment={selectedAppointment} 
          getAnimalNameById={getAnimalNameById} 
          onEdit={() => handleOpenEditModal(selectedAppointment)}
        />
      )}
    </Container>
  );
};

export default AppointmentsPage; 