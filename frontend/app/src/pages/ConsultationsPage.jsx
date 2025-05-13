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
  Grid
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import VisibilityIcon from '@mui/icons-material/Visibility';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import consultationService from '../services/consultationService';
import { useAnimal } from '../contexts/AnimalContext';
import { useAuth } from '../contexts/AuthContext';
import ConsultationFormModal from '../components/consultations/ConsultationFormModal';
import ConsultationDetailsModal from '../components/consultations/ConsultationDetailsModal';

// Paleta de cores definida:
// Marrom-claro suave – #D8CAB8
// Creme claro – #F9F9F9
// Cinza-esverdeado – #9DB8B2
// Verde-oliva suave – #CFE0C3

const colors = {
  background: '#F9F9F9',
  tableHeader: '#D8CAB8',
  buttonPrimary: '#9DB8B2',
  buttonPrimaryHover: '#82a8a0',
  buttonSecondary: '#CFE0C3',
  buttonSecondaryHover: '#b8d4a8',
  textPrimary: '#333',
  textSecondary: '#555',
  paperBackground: '#FFFFFF',
  borderColor: '#E0E0E0'
};

const ConsultationsPage = () => {
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

  const fetchConsultations = useCallback(async () => {
    if (authLoading || !isAuthenticated) {
      if (!authLoading && !isAuthenticated) {
        setError("Você precisa estar logado para ver as consultas.");
        setConsultations([]);
      }
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const animalIdFilter = selectedAnimal ? selectedAnimal.id : null;
      const response = await consultationService.getConsultations(animalIdFilter);
      setConsultations(response.data || []);
    } catch (err) {
      console.error("Erro ao buscar consultas:", err);
      setError(err.response?.data?.detail || "Não foi possível carregar as consultas.");
      setConsultations([]);
    }
    setLoading(false);
  }, [selectedAnimal, isAuthenticated, authLoading]);

  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      fetchConsultations();
    } else if (!authLoading && !isAuthenticated) {
      setConsultations([]);
      setError("Você precisa estar logado para ver as consultas.");
      setLoading(false);
    }
  }, [fetchConsultations, isAuthenticated, authLoading]);

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

  const handleOpenCreateModal = () => {
    setSelectedConsultation(null);
    setIsEditing(false);
    setOpenFormModal(true);
  };

  const handleOpenEditModal = (consultation) => {
    setSelectedConsultation(consultation);
    setIsEditing(true);
    setOpenFormModal(true);
  };

  const handleOpenDetailsModal = (consultation) => {
    setSelectedConsultation(consultation);
    setOpenDetailsModal(true);
  };

  const handleCloseModals = () => {
    setOpenFormModal(false);
    setOpenDetailsModal(false);
    setSelectedConsultation(null);
    setIsEditing(false);
    fetchConsultations(); 
  };

  const handleDeleteConsultation = async (consultationId) => {
    if (window.confirm("Tem certeza que deseja excluir esta consulta?")) {
      setLoading(true);
      try {
        await consultationService.deleteConsultation(consultationId);
        fetchConsultations();
      } catch (err) {
        console.error("Erro ao excluir consulta:", err);
        setError(err.response?.data?.detail || "Erro ao excluir consulta.");
      } finally {
        setLoading(false);
      }
    }
  };

  const filteredConsultations = consultations.filter(consultation => {
    const searchTermLower = searchTerm.toLowerCase();
    const description = consultation.description?.toLowerCase() || '';
    return description.includes(searchTermLower);
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
          Consultas
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
          Nova Consulta
        </Button>
      </Box>

      <Paper sx={{ p: 2.5, mb: 3, backgroundColor: colors.paperBackground, borderRadius: 2, boxShadow: '0px 4px 12px rgba(0,0,0,0.05)' }}>
        <Grid container spacing={2} alignItems="center">
            <Grid item xs={12}>
                <TextField 
                  fullWidth 
                  label="Buscar por Descrição"
                  variant="outlined" 
                  value={searchTerm}
                  onChange={handleSearchChange}
                  size="small"
                />
            </Grid>
        </Grid>
      </Paper>

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', my: 5, color: colors.buttonPrimary }}>
          <CircularProgress color="inherit" />
          <Typography sx={{ ml: 2 }}>Carregando consultas...</Typography>
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
            <Table sx={{ minWidth: 700 }} aria-label="tabela de consultas">
              <TableHead sx={{ backgroundColor: colors.tableHeader }}>
                <TableRow>
                  <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold', py: 1.5 }}>Data</TableCell>
                  { !selectedAnimal && <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold', py: 1.5 }}>Animal</TableCell> }
                  <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold', py: 1.5, width: '50%' }}>Descrição</TableCell>
                  <TableCell align="right" sx={{ color: colors.textPrimary, fontWeight: 'bold', py: 1.5, pr: 2.5 }}>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredConsultations.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((consultation) => (
                  <TableRow key={consultation.id} hover sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                    <TableCell sx={{ py: 1 }}>{new Date(consultation.date).toLocaleDateString()}</TableCell>
                    { !selectedAnimal && <TableCell sx={{ py: 1 }}>{getAnimalNameById(consultation.animal_id)}</TableCell> }
                    <TableCell sx={{ py: 1, maxWidth: 350, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      <Tooltip title={consultation.description} placement="bottom-start">
                        <span>{consultation.description || '-'}</span>
                      </Tooltip>
                    </TableCell>
                    <TableCell align="right" sx={{ py: 0.5, pr: 1.5 }}>
                      <Tooltip title="Visualizar">
                        <IconButton size="small" sx={{ color: colors.buttonPrimary, mr: 0.5 }} onClick={() => handleOpenDetailsModal(consultation)}>
                          <VisibilityIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Editar">
                        <IconButton size="small" sx={{ color: colors.buttonSecondary, '&:hover': {color: colors.buttonSecondaryHover}, mr: 0.5 }} onClick={() => handleOpenEditModal(consultation)}>
                          <EditIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Excluir">
                        <IconButton size="small" sx={{ color: '#e57373', '&:hover': {color: '#d32f2f'} }} onClick={() => handleDeleteConsultation(consultation.id)}>
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
                {filteredConsultations.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={4} sx={{ textAlign: 'center', py: 4, color: colors.textSecondary }}>
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
              sx={{ borderTop: `1px solid ${colors.borderColor}` }}
            />
          </TableContainer>
        </Paper>
      )}
      {openFormModal && (
        <ConsultationFormModal 
          open={openFormModal} 
          onClose={handleCloseModals} 
          consultation={selectedConsultation} 
          isEditing={isEditing} 
          allAnimals={allAnimals} 
          selectedAnimalContext={selectedAnimal} 
        />
      )}
      {openDetailsModal && (
        <ConsultationDetailsModal 
          open={openDetailsModal} 
          onClose={handleCloseModals} 
          consultation={selectedConsultation} 
          getAnimalNameById={getAnimalNameById}
          onEdit={() => handleOpenEditModal(selectedConsultation)}
        />
      )}
    </Container>
  );
};

export default ConsultationsPage; 