import React, { useState, useEffect } from 'react';
import {
  Dialog, DialogActions, DialogContent, DialogTitle, Typography, Button, 
  Box, Grid, Paper, CircularProgress, IconButton, Divider, Tooltip, Chip
} from '@mui/material';
import {
  Edit as EditIcon, 
  RestaurantMenu as RestaurantMenuIcon, 
  Close as CloseIcon,
  Cake as CakeIcon,
  FitnessCenter as FitnessCenterIcon,
  Healing as HealingIcon,
  Pets as PetsIcon,
  LabelImportant as LabelImportantIcon
} from '@mui/icons-material';
import { useTheme } from '@mui/material/styles';
import animalService from '../services/animalService';

const DetailItem = ({ icon, label, value, fullWidth = false }) => {
  const theme = useTheme();
  return (
    <Grid item xs={12} sm={fullWidth ? 12 : 6} md={fullWidth ? 12 : 6} sx={{ display: 'flex', alignItems: 'center', mb: 1.5 }}>
      <Box sx={{ mr: 1.5, color: theme.palette.primary.main }}>{icon}</Box>
      <Box>
        <Typography variant="caption" sx={{ color: theme.palette.text.secondary, display: 'block' }}>{label}</Typography>
        <Typography variant="body1" sx={{ color: theme.palette.text.primary, fontWeight: 500 }}>{value || '-'}</Typography>
      </Box>
    </Grid>
  );
};

const AnimalDetailDialog = ({ open, onClose, animalId, onEditAnimal, onManagePreferences }) => {
  const theme = useTheme();
  const [animalDetails, setAnimalDetails] = useState(null);
  const [preferences, setPreferences] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (open && animalId) {
      const fetchDetails = async () => {
        setLoading(true);
        setError(null);
        setAnimalDetails(null);
        setPreferences(null);
        try {
          const [detailsData, preferencesData] = await Promise.allSettled([
            animalService.getAnimalById(animalId),
            animalService.getAnimalPreferences(animalId)
          ]);

          if (detailsData.status === 'fulfilled') {
            setAnimalDetails(detailsData.value);
          } else {
            setError(detailsData.reason?.message || 'Falha ao carregar dados do animal.');
          }

          if (preferencesData.status === 'fulfilled' && preferencesData.value) {
            setPreferences(preferencesData.value);
          } else {
            setPreferences({ gosta_de: 'Não informado', nao_gosta_de: 'Não informado' });
          }

        } catch (err) {
          setError(err.message || 'Falha ao carregar dados.');
        }
        setLoading(false);
      };
      fetchDetails();
    } else {
      setAnimalDetails(null);
      setPreferences(null);
      setLoading(false);
      setError(null);
    }
  }, [open, animalId]);

  const handleOpenPreferences = () => {
    if (animalDetails) onManagePreferences(animalDetails.id, preferences);
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth PaperProps={{ sx: { backgroundColor: theme.palette.background.paper, borderRadius: '12px' } }}>
      <DialogTitle sx={{ backgroundColor: theme.palette.primary.main, color: theme.palette.primary.contrastText, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <PetsIcon sx={{ mr: 1, fontSize: '2rem' }} />
          <Typography variant="h6">
            {animalDetails?.name ? `Detalhes de ${animalDetails.name}` : 'Detalhes do Animal'}
          </Typography>
        </Box>
        <Tooltip title="Fechar">
          <IconButton onClick={onClose} sx={{ color: theme.palette.primary.contrastText }}>
            <CloseIcon />
          </IconButton>
        </Tooltip>
      </DialogTitle>

      <DialogContent dividers sx={{ p: { xs: 2, md: 3 }, backgroundColor: theme.palette.background.default }}>
        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', my: 5, minHeight: '200px' }}>
            <CircularProgress color="primary" />
          </Box>
        )}

        {error && !loading && (
          <Typography color="error" sx={{ textAlign: 'center', my: 5 }}>{error}</Typography>
        )}

        {animalDetails && !loading && !error && (
          <Grid container spacing={3}>
            <Grid item xs={12} md={7}>
              <Paper elevation={1} sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Informações Gerais
                </Typography>
                <Grid container spacing={1}>
                  <DetailItem icon={<LabelImportantIcon />} label="Nome" value={animalDetails.name} />
                  <DetailItem icon={<PetsIcon />} label="Espécie" value={animalDetails.species} />
                  <DetailItem icon={<PetsIcon />} label="Raça" value={animalDetails.breed} />
                  <DetailItem icon={<CakeIcon />} label="Idade" value={animalDetails.age !== null ? `${animalDetails.age} anos` : '-'} />
                  <DetailItem icon={<FitnessCenterIcon />} label="Peso" value={animalDetails.weight !== null ? `${animalDetails.weight} kg` : '-'} />
                </Grid>

                <Divider sx={{ my: 2.5 }} />

                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1.5 }}>
                  <HealingIcon sx={{ mr: 1.5, color: theme.palette.primary.main }} />
                  <Typography variant="subtitle1" fontWeight="bold">Histórico Médico</Typography>
                </Box>
                <Typography variant="body2" paragraph sx={{ whiteSpace: 'pre-wrap', pl: 4 }}>
                  {animalDetails.medical_history || 'Nenhum histórico médico informado.'}
                </Typography>
              </Paper>
            </Grid>

            <Grid item xs={12} md={5}>
              <Paper elevation={1} sx={{ p: 3, height: '100%' }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1.5 }}>
                  <Typography variant="h6">Preferências</Typography>
                  <Button
                    startIcon={<RestaurantMenuIcon />}
                    onClick={handleOpenPreferences}
                    size="small"
                    variant="outlined"
                  >
                    Gerenciar
                  </Button>
                </Box>

                <Box sx={{ mb: 1 }}>
                  <Typography variant="caption" fontWeight="bold">Gosta de:</Typography>
                  <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', pl: 1 }}>{preferences?.gosta_de || '-'}</Typography>
                </Box>
                <Box>
                  <Typography variant="caption" fontWeight="bold">Não gosta de:</Typography>
                  <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', pl: 1 }}>{preferences?.nao_gosta_de || '-'}</Typography>
                </Box>

                <Divider sx={{ my: 2.5 }} />

                <Typography variant="caption">
                  Data de Cadastro: <Chip label={formatDate(animalDetails.created_at)} size="small" />
                </Typography>
                <Typography variant="caption" sx={{ mt: 0.5 }}>
                  Última Atualização: <Chip label={formatDate(animalDetails.updated_at)} size="small" />
                </Typography>
              </Paper>
            </Grid>
          </Grid>
        )}
      </DialogContent>

      <DialogActions sx={{ p: 2 }}>
        <Button onClick={onClose} variant="outlined">Fechar</Button>
        <Button
          startIcon={<EditIcon />}
          onClick={() => { if (animalDetails) onEditAnimal(animalDetails); onClose(); }}
          variant="contained"
          disabled={!animalDetails || loading}
        >
          Editar Animal
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default AnimalDetailDialog;
