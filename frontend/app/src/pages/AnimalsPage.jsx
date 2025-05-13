import React, { useState, useEffect } from 'react';
import { 
  Container, Typography, Button, Box, CircularProgress, Paper, TableContainer, 
  Table, TableHead, TableRow, TableCell, TableBody, TablePagination, TextField, Grid, IconButton
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon, Visibility as VisibilityIcon } from '@mui/icons-material';
import animalService from '../services/animalService';
import AnimalFormDialog from '../components/AnimalFormDialog';
import AnimalDetailDialog from '../components/AnimalDetailDialog';
import AnimalPreferencesDialog from '../components/AnimalPreferencesDialog';
// import AppHeader from '../components/AppHeader'; // Removido - Header vem do MainLayout
// import { useAuth } from '../contexts/AuthContext'; // Se necessário para obter clinic_id ou token diretamente

// TODO: Definir paleta de cores conforme especificado
const colors = {
  marromClaroSuave: '#D8CAB8',
  cremeClaro: '#F9F9F9',
  cinzaEsverdeado: '#9DB8B2',
  verdeOlivaSuave: '#CFE0C3',
  textPrimary: '#333', // Cor de texto principal
  textSecondary: '#555', // Cor de texto secundária
  // Adicionar mais cores se necessário
};

const AnimalsPage = () => {
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

  const [openNewAnimalDialog, setOpenNewAnimalDialog] = useState(false);
  // const { user } = useAuth(); // Exemplo se precisar do usuário logado

  const fetchAnimals = async () => {
    setLoading(true);
    try {
      // TODO: Adicionar filtro por clinic_id se o backend não fizer isso automaticamente baseado no token
      const data = await animalService.getAllAnimals();
      setAnimals(data || []);
      setError(null);
    } catch (err) {
      console.error("Erro ao buscar animais:", err);
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
    // TODO: Mostrar mensagem de sucesso (Snackbar)
  };

  const handleEditAnimal = (animalToEdit) => {
    setEditingAnimal(animalToEdit);
    setOpenFormDialog(true);
  };

  const handleDeleteAnimal = async (animalId) => {
    if (window.confirm('Tem certeza que deseja excluir este animal?')) {
      try {
        await animalService.deleteAnimal(animalId);
        setAnimals(prevAnimals => prevAnimals.filter(animal => animal.id !== animalId));
        // TODO: Mostrar notificação de sucesso
      } catch (err) {
        console.error('Erro ao excluir animal:', err);
        // TODO: Mostrar notificação de erro
      }
    }
  };

  const handleViewAnimalClick = (animalId) => {
    setViewingAnimalId(animalId);
    setOpenDetailDialog(true);
  };

  const handleCloseDetailDialog = () => {
    setOpenDetailDialog(false);
    setViewingAnimalId(null);
  };

  const handleOpenPreferencesDialog = async (animalIdForPrefs) => {
    setManagingPreferencesForAnimalId(animalIdForPrefs);
    try {
        // Busca as preferências atuais para popular o formulário
        const prefs = await animalService.getAnimalPreferences(animalIdForPrefs);
        setCurrentAnimalPreferences(prefs); 
    } catch (error) {
        console.error("Erro ao buscar preferências para o diálogo:", error);
        setCurrentAnimalPreferences(null); // Define como null se houver erro ou não existir
    }
    setOpenDetailDialog(false); // Fecha o dialog de detalhes para não sobrepor
    setOpenPreferencesDialog(true);
  };

  const handleClosePreferencesDialog = () => {
    setOpenPreferencesDialog(false);
    setManagingPreferencesForAnimalId(null);
    setCurrentAnimalPreferences(null);
    // Reabrir o dialog de detalhes se ele estava aberto para o mesmo animal
    if (viewingAnimalId) { // Se tinha um animal sendo visualizado antes de abrir prefs
        // Não reabre automaticamente para evitar loops, mas a lógica pode ser adicionada se necessário.
        // O ideal é que o AnimalDetailDialog recarregue suas prefs quando reaberto ou via prop.
    }
  };

  const handlePreferencesSuccess = () => {
    handleClosePreferencesDialog();
    // Se o dialog de detalhes estava aberto para o animal cujas prefs foram editadas, 
    // ele precisa ser atualizado. Uma forma é fechar e reabri-lo ou passar uma prop para refetch.
    // Por enquanto, apenas fechamos o dialog de preferências.
    // Para atualizar o AnimalDetailDialog, ele poderia ter um useEffect que busca preferências quando `open`.
    // Como o DetailDialog já busca prefs no seu useEffect quando aberto, fechar e reabrir o DetailDialog funcionaria.
    // Para simplificar: ao salvar prefs, fechamos o dialog de prefs.
    // Se o DetailDialog for aberto novamente, ele buscará as prefs atualizadas.
    if(viewingAnimalId) {
      // Para garantir que os detalhes sejam atualizados, podemos reabrir o dialog de detalhes
      // Isso fará com que o useEffect dentro de AnimalDetailDialog busque os dados novamente.
      setOpenDetailDialog(true); 
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
      <Paper sx={{ p: { xs: 2, md: 3 }, mb: 3, backgroundColor: 'white', borderRadius: 2, boxShadow: '0px 4px 20px rgba(0,0,0,0.05)' }}>
        <Grid container spacing={2} justifyContent="space-between" alignItems="center">
          <Grid item>
            <Typography variant="h4" component="h1" gutterBottom sx={{ color: colors.textPrimary }}>
              Gestão de Animais
            </Typography>
          </Grid>
          <Grid item>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={handleOpenNewAnimalDialog}
              sx={{ 
                backgroundColor: colors.verdeOlivaSuave, 
                color: colors.textPrimary, 
                '&:hover': { backgroundColor: colors.cinzaEsverdeado }
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
        <Typography sx={{ textAlign: 'center', mt: 4, color: colors.textSecondary }}>Nenhum animal encontrado.</Typography>
      ) : (
        <TableContainer component={Paper} sx={{ borderRadius: 2, boxShadow: '0px 4px 20px rgba(0,0,0,0.05)' }}>
          <Table sx={{ minWidth: 650 }} aria-label="tabela de animais">
            <TableHead sx={{ backgroundColor: colors.marromClaroSuave }}>
              <TableRow>
                <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }}>Nome</TableCell>
                <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }}>Espécie</TableCell>
                <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }}>Raça</TableCell>
                <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }}>Idade</TableCell>
                <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold' }}>Peso (kg)</TableCell>
                <TableCell align="center" sx={{ color: colors.textPrimary, fontWeight: 'bold' }}>Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {(rowsPerPage > 0
                ? filteredAnimals.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                : filteredAnimals
              ).map((animal) => (
                <TableRow key={animal.id} hover sx={{ '&:nth-of-type(odd)': { backgroundColor: colors.cremeClaro } }}>
                  <TableCell component="th" scope="row" sx={{ color: colors.textSecondary }}>{animal.name}</TableCell>
                  <TableCell sx={{ color: colors.textSecondary }}>{animal.species}</TableCell>
                  <TableCell sx={{ color: colors.textSecondary }}>{animal.breed || '-'}</TableCell>
                  <TableCell sx={{ color: colors.textSecondary }}>{animal.age !== null ? animal.age : '-'}</TableCell>
                  <TableCell sx={{ color: colors.textSecondary }}>{animal.weight !== null ? animal.weight : '-'}</TableCell>
                  <TableCell align="center">
                    <IconButton onClick={() => handleViewAnimalClick(animal.id)} size="small" sx={{ color: colors.cinzaEsverdeado }}><VisibilityIcon /></IconButton>
                    <IconButton onClick={() => handleEditAnimal(animal)} size="small" sx={{ color: colors.cinzaEsverdeado }}><EditIcon /></IconButton>
                    <IconButton onClick={() => handleDeleteAnimal(animal.id)} size="small" sx={{ color: '#c77777' }}><DeleteIcon /></IconButton>
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
            sx={{ backgroundColor: colors.marromClaroSuave, color: colors.textPrimary }}
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
          onManagePreferences={(animalIdForPrefs) => {
            handleOpenPreferencesDialog(animalIdForPrefs);
          }}
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
    </Container>
  );
};

export default AnimalsPage; 