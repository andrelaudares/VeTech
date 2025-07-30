import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Button, Table, TableBody, TableCell, TableContainer, 
  TableHead, TableRow, Paper, IconButton, TextField, TablePagination,
  CircularProgress, Snackbar, Alert, Dialog, DialogActions, DialogContent,
  DialogContentText, DialogTitle, Chip, useTheme, Container, Grid, Tooltip
} from '@mui/material';
import {
  Add as AddIcon,
  Visibility as VisibilityIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  PersonAdd as PersonAddIcon,
  ToggleOff as ToggleOffIcon,
  ToggleOn as ToggleOnIcon
} from '@mui/icons-material';
import { Plus, Eye, Edit, Trash2, Settings, ToggleLeft, ToggleRight } from 'lucide-react';
import { animalService } from '../services/animalService';
import AnimalFormDialog from '../components/AnimalFormDialog';
import AnimalDetailDialog from '../components/AnimalDetailDialog';
import AnimalPreferencesDialog from '../components/AnimalPreferencesDialog';
import ClientActivationDialog from '../components/ClientActivationDialog';

const AnimalsPage = () => {
  const theme = useTheme();

  const [animals, setAnimals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');

  const [openFormDialog, setOpenFormDialog] = useState(false);
  const [editingAnimal, setEditingAnimal] = useState(null);
  const [openDetailDialog, setOpenDetailDialog] = useState(false);
  const [viewingAnimalId, setViewingAnimalId] = useState(null);

  const [openPreferencesDialog, setOpenPreferencesDialog] = useState(false);
  const [managingPreferencesForAnimalId, setManagingPreferencesForAnimalId] = useState(null);
  const [currentAnimalPreferences, setCurrentAnimalPreferences] = useState(null);

  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState('success');

  const [confirmDeleteOpen, setConfirmDeleteOpen] = useState(false);
  const [animalToDelete, setAnimalToDelete] = useState(null);

  // Estados para ativação de cliente
  const [openActivationDialog, setOpenActivationDialog] = useState(false);
  const [activatingAnimal, setActivatingAnimal] = useState(null);

  const showSnackbar = (message, severity = 'success') => {
    setSnackbarMessage(message);
    setSnackbarSeverity(severity);
    setSnackbarOpen(true);
  };

  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };

  const fetchAnimals = async () => {
    setLoading(true);
    try {
      const data = await animalService.getAllAnimals();
      setAnimals(data || []);
      setError(null);
    } catch (err) {
      setError(err.message || 'Falha ao carregar animais.');
      setAnimals([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnimals();
  }, []);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value.toLowerCase());
  };

  const filteredAnimals = animals.filter(animal => 
    animal.name.toLowerCase().includes(searchTerm) || 
    animal.species.toLowerCase().includes(searchTerm)
  );

  const handleOpenNewAnimalDialog = () => {
    setEditingAnimal(null);
    setOpenFormDialog(true);
  };

  const handleCloseFormDialog = () => {
    setOpenFormDialog(false);
    setEditingAnimal(null);
  };

  const handleAnimalSubmitSuccess = () => {
    handleCloseFormDialog();
    fetchAnimals();
    showSnackbar('Animal salvo com sucesso!', 'success');
  };

  const handleEditAnimal = (animalToEdit) => {
    setEditingAnimal(animalToEdit);
    setOpenFormDialog(true);
  };

  const handleDeleteRequest = (animalId) => {
    setAnimalToDelete(animalId);
    setConfirmDeleteOpen(true);
  };

  const handleConfirmDelete = async () => {
    try {
      await animalService.deleteAnimal(animalToDelete);
      setAnimals(prev => prev.filter(a => a.id !== animalToDelete));
      showSnackbar('Animal excluído com sucesso!', 'success');
    } catch (err) {
      showSnackbar('Erro ao excluir animal.', 'error');
    }
    setConfirmDeleteOpen(false);
    setAnimalToDelete(null);
  };

  const handleViewAnimalClick = (id) => {
    setViewingAnimalId(id);
    setOpenDetailDialog(true);
  };

  const handleCloseDetailDialog = () => {
    setOpenDetailDialog(false);
    setViewingAnimalId(null);
  };

  const handleOpenPreferencesDialog = async (animalIdForPrefs) => {
    setManagingPreferencesForAnimalId(animalIdForPrefs);
    try {
      const prefs = await animalService.getAnimalPreferences(animalIdForPrefs);
      setCurrentAnimalPreferences(prefs);
    } catch {
      setCurrentAnimalPreferences(null);
    }
    setOpenDetailDialog(false);
    setOpenPreferencesDialog(true);
  };

  const handleClosePreferencesDialog = () => {
    setOpenPreferencesDialog(false);
    setManagingPreferencesForAnimalId(null);
    setCurrentAnimalPreferences(null);
    if (viewingAnimalId) {
      setOpenDetailDialog(true);
    }
  };

  const handlePreferencesSuccess = () => {
    handleClosePreferencesDialog();
    showSnackbar('Preferências atualizadas com sucesso!', 'success');
    if (viewingAnimalId) {
      setOpenDetailDialog(true);
    }
  };

  // Funções para ativação de cliente
  const handleOpenActivationDialog = (animal) => {
    setActivatingAnimal(animal);
    setOpenActivationDialog(true);
  };

  const handleCloseActivationDialog = () => {
    setOpenActivationDialog(false);
    setActivatingAnimal(null);
  };

  const handleActivationSuccess = () => {
    handleCloseActivationDialog();
    fetchAnimals(); // Recarregar a lista para atualizar o status
    showSnackbar('Cliente ativado com sucesso!', 'success');
  };

  const handleToggleClientStatus = async (animalId, currentStatus) => {
    try {
      await animalService.toggleClientStatus(animalId, !currentStatus);
      fetchAnimals(); // Recarregar a lista
      showSnackbar(
        `Acesso do cliente ${!currentStatus ? 'ativado' : 'desativado'} com sucesso!`, 
        'success'
      );
    } catch (err) {
      showSnackbar('Erro ao alterar status do cliente.', 'error');
    }
  };

  const getClientStatusChip = (animal) => {
    if (!animal.tutor_name || !animal.email) {
      return (
        <Chip 
          label="Não Configurado" 
          size="small" 
          color="default"
          variant="outlined"
        />
      );
    }
    
    if (animal.client_active) {
      return (
        <Chip 
          label="Ativo" 
          size="small" 
          color="success"
          variant="filled"
        />
      );
    } else {
      return (
        <Chip 
          label="Inativo" 
          size="small" 
          color="warning"
          variant="outlined"
        />
      );
    }
  };

  if (loading && !openFormDialog && !openDetailDialog && !openPreferencesDialog) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 'calc(100vh - 64px)' }}> 
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container sx={{mt: 2}}>
        <Typography color="error" sx={{ textAlign: 'center', mt: 4 }}>Erro: {error}</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
      <Paper sx={{ p: { xs: 2, md: 3 }, mb: 3, borderRadius: 2 }}>
        <Grid container spacing={2} justifyContent="space-between" alignItems="center">
          <Grid item>
            <Typography variant="h4" gutterBottom color="text.primary">
              Gestão de Animais
            </Typography>
          </Grid>
          <Grid item>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={handleOpenNewAnimalDialog}
              sx={{
                backgroundColor: theme.palette.primary.main,
                color: theme.palette.text.primary,
                '&:hover': { backgroundColor: theme.palette.secondary.main, color: 'white' }
              }}
            >
              Novo Animal
            </Button>
          </Grid>
        </Grid>
        <TextField 
          fullWidth
          label="Buscar por Nome ou Espécie"
          variant="outlined"
          margin="normal"
          onChange={handleSearchChange}
          sx={{ backgroundColor: 'white' }}
        />
      </Paper>

      {filteredAnimals.length === 0 && !loading ? (
        <Typography sx={{ textAlign: 'center', mt: 4 }} color="text.secondary">Nenhum animal encontrado.</Typography>
      ) : (
        <TableContainer component={Paper} sx={{ borderRadius: 2 }}>
          <Table>
            <TableHead sx={{ backgroundColor: theme.palette.primary.main }}>
              <TableRow>
                <TableCell sx={{ color: theme.palette.primary.contrastText, fontWeight: 'bold' }}>Nome</TableCell>
                <TableCell sx={{ color: theme.palette.primary.contrastText, fontWeight: 'bold' }}>Espécie</TableCell>
                <TableCell sx={{ color: theme.palette.primary.contrastText, fontWeight: 'bold' }}>Raça</TableCell>
                <TableCell sx={{ color: theme.palette.primary.contrastText, fontWeight: 'bold' }}>Idade</TableCell>
                <TableCell sx={{ color: theme.palette.primary.contrastText, fontWeight: 'bold' }}>Peso (kg)</TableCell>
                <TableCell sx={{ color: theme.palette.primary.contrastText, fontWeight: 'bold' }}>Status Cliente</TableCell>
                <TableCell align="center" sx={{ color: theme.palette.primary.contrastText, fontWeight: 'bold' }}>Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {(rowsPerPage > 0
                ? filteredAnimals.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                : filteredAnimals
              ).map((animal) => (
                <TableRow key={animal.id} hover>
                  <TableCell>{animal.name}</TableCell>
                  <TableCell>{animal.species}</TableCell>
                  <TableCell>{animal.breed || '-'}</TableCell>
                  <TableCell>{animal.age !== null ? animal.age : '-'}</TableCell>
                  <TableCell>{animal.weight !== null ? animal.weight : '-'}</TableCell>
                  <TableCell>{getClientStatusChip(animal)}</TableCell>
                  <TableCell align="center">
                    <Tooltip title="Visualizar">
                      <IconButton onClick={() => handleViewAnimalClick(animal.id)} size="small" sx={{ color: '#169c44' }}>
                        <VisibilityIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Editar">
                      <IconButton onClick={() => handleEditAnimal(animal)} size="small" color="primary">
                        <EditIcon />
                      </IconButton>
                    </Tooltip>
                    
                    {/* Botões de ativação de cliente */}
                    {!animal.tutor_name || !animal.email ? (
                      <Tooltip title="Ativar Cliente">
                        <IconButton 
                          onClick={() => handleOpenActivationDialog(animal)} 
                          size="small" 
                          sx={{ color: '#2196f3' }}
                        >
                          <PersonAddIcon />
                        </IconButton>
                      </Tooltip>
                    ) : (
                      <Tooltip title={animal.client_active ? "Desativar Cliente" : "Ativar Cliente"}>
                        <IconButton 
                          onClick={() => handleToggleClientStatus(animal.id, animal.client_active)} 
                          size="small" 
                          sx={{ color: animal.client_active ? '#ff9800' : '#4caf50' }}
                        >
                          {animal.client_active ? <ToggleOffIcon /> : <ToggleOnIcon />}
                        </IconButton>
                      </Tooltip>
                    )}
                    
                    <Tooltip title="Excluir">
                      <IconButton onClick={() => handleDeleteRequest(animal.id)} size="small" sx={{ color: theme.palette.error.main }}>
                        <DeleteIcon />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <TablePagination
            rowsPerPageOptions={[5, 10, 25, { label: 'Todos', value: -1 }]}
            component="div"
            count={filteredAnimals.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
            labelRowsPerPage="Animais por página:"
            labelDisplayedRows={({ from, to, count }) => `${from}–${to} de ${count !== -1 ? count : `mais de ${to}`}`}
            sx={{ backgroundColor: theme.palette.primary.main, color: theme.palette.primary.contrastText }}
          />
        </TableContainer>
      )}

      <AnimalFormDialog 
        open={openFormDialog}
        onClose={handleCloseFormDialog}
        onSuccess={handleAnimalSubmitSuccess}
        animal={editingAnimal}
      />

      {viewingAnimalId && (
        <AnimalDetailDialog
          open={openDetailDialog}
          onClose={handleCloseDetailDialog}
          animalId={viewingAnimalId}
          onEditAnimal={(animalToEdit) => {
            handleCloseDetailDialog();
            handleEditAnimal(animalToEdit);
          }}
          onManagePreferences={handleOpenPreferencesDialog}
        />
      )}

      {managingPreferencesForAnimalId && (
        <AnimalPreferencesDialog
          open={openPreferencesDialog}
          onClose={handleClosePreferencesDialog}
          animalId={managingPreferencesForAnimalId}
          currentPreferences={currentAnimalPreferences}
          onSuccess={handlePreferencesSuccess}
        />
      )}

      {activatingAnimal && (
        <ClientActivationDialog
          open={openActivationDialog}
          onClose={handleCloseActivationDialog}
          animal={activatingAnimal}
          onSuccess={handleActivationSuccess}
        />
      )}

      <Dialog
        open={confirmDeleteOpen}
        onClose={() => setConfirmDeleteOpen(false)}
      >
        <DialogTitle>Confirmar Exclusão</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Tem certeza que deseja excluir este animal? Esta ação não pode ser desfeita.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConfirmDeleteOpen(false)} color="inherit">
            Cancelar
          </Button>
          <Button
            onClick={handleConfirmDelete}
            color="error"
            variant="contained"
          >
            Excluir
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar open={snackbarOpen} autoHideDuration={4000} onClose={handleCloseSnackbar} anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}>
        <Alert onClose={handleCloseSnackbar} severity={snackbarSeverity} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default AnimalsPage;
