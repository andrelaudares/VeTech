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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Snackbar,
  Alert
} from '@mui/material';
import { useTheme } from '@mui/material/styles';
import AddIcon from '@mui/icons-material/Add';
import VisibilityIcon from '@mui/icons-material/Visibility';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import consultationService from '../services/consultationService';
import { useAnimal } from '../contexts/AnimalContext';
import { useAuth } from '../contexts/AuthContext';
import ConsultationFormModal from '../components/consultations/ConsultationFormModal';
import ConsultationDetailsModal from '../components/consultations/ConsultationDetailsModal';

const ConsultationsPage = () => {
  const theme = useTheme();
  const [consultations, setConsultations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { selectedAnimal, animals: allAnimals } = useAnimal();
  const { isAuthenticated, loading: authLoading } = useAuth();

  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');

  const [openFormModal, setOpenFormModal] = useState(false);
  const [openDetailsModal, setOpenDetailsModal] = useState(false);
  const [selectedConsultation, setSelectedConsultation] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [confirmDeleteOpen, setConfirmDeleteOpen] = useState(false);
  const [consultationToDelete, setConsultationToDelete] = useState(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const handleSnackbarClose = () => setSnackbar({ ...snackbar, open: false });

  const fetchConsultations = useCallback(async () => {
    if (authLoading || !isAuthenticated) return;
    setLoading(true);
    try {
      const animalIdFilter = selectedAnimal?.id;
      const response = await consultationService.getConsultations(animalIdFilter);
      setConsultations(response.data || []);
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao carregar consultas.');
      setConsultations([]);
    }
    setLoading(false);
  }, [selectedAnimal, isAuthenticated, authLoading]);

  useEffect(() => {
    if (!authLoading && isAuthenticated) fetchConsultations();
  }, [fetchConsultations, isAuthenticated, authLoading, selectedAnimal]);

  const getAnimalNameById = useCallback((id) => {
    const animal = allAnimals.find(a => a.id === id);
    return animal ? animal.name : 'Desconhecido';
  }, [allAnimals]);

  const handleChangePage = (event, newPage) => setPage(newPage);
  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleDeleteRequest = (id) => {
    setConsultationToDelete(id);
    setConfirmDeleteOpen(true);
  };

  const handleConfirmDelete = async () => {
    try {
      await consultationService.deleteConsultation(consultationToDelete);
      setSnackbar({ open: true, message: 'Consulta excluída com sucesso!', severity: 'success' });
      fetchConsultations();
    } catch (err) {
      setSnackbar({ open: true, message: 'Erro ao excluir consulta.', severity: 'error' });
    }
    setConfirmDeleteOpen(false);
    setConsultationToDelete(null);
  };

  const handleCloseModals = (updated = false) => {
    setOpenFormModal(false);
    setOpenDetailsModal(false);
    setSelectedConsultation(null);
    setIsEditing(false);
    if (updated) fetchConsultations();
  };

  const filteredConsultations = consultations.filter(consultation => {
    const searchTermLower = searchTerm.toLowerCase();
    const description = consultation.description?.toLowerCase() || '';
    return description.includes(searchTermLower);
  });

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3, flexWrap: 'wrap' }}>
        <Typography variant="h4" fontWeight={600}>Consultas</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => { setOpenFormModal(true); setSelectedConsultation(null); setIsEditing(false); }}
          sx={{
            backgroundColor: theme.palette.primary.main,
            color: theme.palette.primary.contrastText,
            '&:hover': { backgroundColor: theme.palette.secondary.main }
          }}
        >
          Nova Consulta
        </Button>
      </Box>

      <Paper sx={{ p: 2.5, mb: 3, backgroundColor: theme.palette.background.paper }} elevation={3}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Buscar por Descrição"
              variant="outlined"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              size="small"
            />
          </Grid>
        </Grid>
      </Paper>

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', my: 5 }}>
          <CircularProgress color="primary" />
          <Typography sx={{ ml: 2 }}>Carregando consultas...</Typography>
        </Box>
      )}

      {error && (
        <Paper
          sx={{
            p: 2,
            textAlign: 'center',
            my: 3,
            backgroundColor: theme.palette.error.light,
            color: theme.palette.error.dark,
            borderRadius: 2
          }}
          elevation={3}
        >
          <Typography variant="h6">Oops!</Typography>
          <Typography>{error}</Typography>
        </Paper>
      )}

      {!loading && !error && (
        <Paper elevation={2} sx={{ borderRadius: 2, overflow: 'hidden', backgroundColor: theme.palette.background.paper }}>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow sx={{ backgroundColor: theme.palette.primary.main }}>
                  <TableCell sx={{ color: theme.palette.primary.contrastText }}><b>Data</b></TableCell>
                  {!selectedAnimal && <TableCell sx={{ color: theme.palette.primary.contrastText }}><b>Animal</b></TableCell>}
                  <TableCell sx={{ color: theme.palette.primary.contrastText }}><b>Descrição</b></TableCell>
                  <TableCell align="right" sx={{ color: theme.palette.primary.contrastText }}><b>Ações</b></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredConsultations.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((consultation) => (
                  <TableRow key={consultation.id} hover>
                    <TableCell>{new Date(consultation.date).toLocaleDateString()}</TableCell>
                    {!selectedAnimal && <TableCell>{getAnimalNameById(consultation.animal_id)}</TableCell>}
                    <TableCell>
                      <Tooltip title={consultation.description} placement="bottom-start">
                        <span>{consultation.description || '-'}</span>
                      </Tooltip>
                    </TableCell>
                    <TableCell align="right">
                      <Tooltip title="Visualizar">
                        <IconButton size="small" onClick={() => { setSelectedConsultation(consultation); setOpenDetailsModal(true); }}>
                          <VisibilityIcon fontSize="small" sx={{ color: theme.palette.secondary.main }} />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Editar">
                        <IconButton size="small" onClick={() => { setSelectedConsultation(consultation); setIsEditing(true); setOpenFormModal(true); }}>
                          <EditIcon fontSize="small" sx={{ color: theme.palette.primary.main }} />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Excluir">
                        <IconButton size="small" onClick={() => handleDeleteRequest(consultation.id)}>
                          <DeleteIcon fontSize="small" sx={{
                            color: theme.palette.error.main,
                            '&:hover': { color: theme.palette.error.dark }
                          }} />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
                {filteredConsultations.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={4} sx={{ textAlign: 'center', py: 4 }}>
                      Nenhuma consulta encontrada com os filtros atuais.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
            <TablePagination
              rowsPerPageOptions={[5, 10, 25]}
              component="div"
              count={filteredConsultations.length}
              rowsPerPage={rowsPerPage}
              page={page}
              onPageChange={handleChangePage}
              onRowsPerPageChange={handleChangeRowsPerPage}
              labelRowsPerPage="Itens por página:"
              labelDisplayedRows={({ from, to, count }) => `${from}–${to} de ${count}`}
              sx={{
                backgroundColor: theme.palette.primary.main,
                color: theme.palette.primary.contrastText,
                '& .MuiTablePagination-actions': { color: theme.palette.primary.contrastText }
              }}
            />
          </TableContainer>
        </Paper>
      )}

      <Dialog open={confirmDeleteOpen} onClose={() => setConfirmDeleteOpen(false)}>
        <DialogTitle>Confirmar Exclusão</DialogTitle>
        <DialogContent>
          <DialogContentText>Tem certeza que deseja excluir esta consulta? Esta ação não poderá ser desfeita.</DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConfirmDeleteOpen(false)}>Cancelar</Button>
          <Button onClick={handleConfirmDelete} variant="contained" color="error">Excluir</Button>
        </DialogActions>
      </Dialog>

      <Snackbar open={snackbar.open} autoHideDuration={4000} onClose={handleSnackbarClose} anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}>
        <Alert onClose={handleSnackbarClose} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>

      {openFormModal && (
        <ConsultationFormModal
          open={openFormModal}
          onClose={(success) => handleCloseModals(success)}
          consultation={selectedConsultation}
          isEditing={isEditing}
          allAnimals={allAnimals}
          selectedAnimalContext={selectedAnimal}
          setSnackbar={setSnackbar}
        />
      )}

      {openDetailsModal && (
        <ConsultationDetailsModal
          open={openDetailsModal}
          onClose={handleCloseModals}
          consultation={selectedConsultation}
          getAnimalNameById={getAnimalNameById}
          onEdit={() => { setIsEditing(true); setOpenDetailsModal(false); setOpenFormModal(true); }}
        />
      )}
    </Container>
  );
};

export default ConsultationsPage;
