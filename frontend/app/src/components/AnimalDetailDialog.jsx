import React, { useState, useEffect } from 'react';
import {
  Dialog, DialogActions, DialogContent, DialogTitle, Typography, Button, 
  Box, Grid, Paper, CircularProgress, IconButton, Divider, Tooltip, Chip
} from '@mui/material';
import {
  Edit as EditIcon, 
  RestaurantMenu as RestaurantMenuIcon, 
  Close as CloseIcon,
  Cake as CakeIcon, // Idade
  FitnessCenter as FitnessCenterIcon, // Peso
  Healing as HealingIcon, // Histórico Médico
  Pets as PetsIcon, // Espécie/Raça
  LabelImportant as LabelImportantIcon // Nome
} from '@mui/icons-material';
import animalService from '../services/animalService';
// import AnimalPreferencesDialog from './AnimalPreferencesDialog'; // Será criado e importado depois

// Paleta de cores
const colors = {
  marromClaroSuave: '#D8CAB8',
  cremeClaro: '#F9F9F9',
  cinzaEsverdeado: '#9DB8B2',
  verdeOlivaSuave: '#CFE0C3',
  textPrimary: '#333',
  textSecondary: '#555',
  chipBackground: '#e0e0e0', // Um cinza claro para chips
};

const DetailItem = ({ icon, label, value, fullWidth = false }) => (
  <Grid item xs={12} sm={fullWidth ? 12 : 6} md={fullWidth ? 12 : 6} sx={{ display: 'flex', alignItems: 'center', mb: 1.5 }}>
    <Box sx={{ mr: 1.5, color: colors.cinzaEsverdeado }}>{icon}</Box>
    <Box>
      <Typography variant="caption" sx={{ color: colors.textSecondary, display: 'block' }}>
        {label}
      </Typography>
      <Typography variant="body1" sx={{ color: colors.textPrimary, fontWeight: '500' }}>
        {value || '-'}
      </Typography>
    </Box>
  </Grid>
);

const AnimalDetailDialog = ({ open, onClose, animalId, onEditAnimal, onManagePreferences }) => {
  const [animalDetails, setAnimalDetails] = useState(null);
  const [preferences, setPreferences] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // const [openPreferencesDialog, setOpenPreferencesDialog] = useState(false); // Para o dialog de preferências

  useEffect(() => {
    if (open && animalId) {
      const fetchDetails = async () => {
        setLoading(true);
        setError(null);
        setAnimalDetails(null); // Limpa dados antigos antes de buscar novos
        setPreferences(null);
        try {
          const [detailsData, preferencesData] = await Promise.allSettled([
            animalService.getAnimalById(animalId),
            animalService.getAnimalPreferences(animalId)
          ]);

          if (detailsData.status === 'fulfilled') {
            setAnimalDetails(detailsData.value);
          } else {
            console.error("Erro ao buscar detalhes do animal:", detailsData.reason);
            setError(detailsData.reason?.message || 'Falha ao carregar dados do animal.');
          }

          if (preferencesData.status === 'fulfilled' && preferencesData.value) {
            setPreferences(preferencesData.value);
          } else {
            // Não define erro se as preferências não existirem, apenas não as mostra ou mostra "Não informado"
            setPreferences({ gosta_de: 'Não informado', nao_gosta_de: 'Não informado' });
            if (preferencesData.status === 'rejected') {
                console.warn("Aviso ao buscar preferências:", preferencesData.reason);
            }
          }

        } catch (err) { // Este catch pode não ser atingido devido ao Promise.allSettled
          console.error("Erro geral ao buscar dados:", err);
          setError(err.message || 'Falha ao carregar dados.');
        }
        setLoading(false);
      };
      fetchDetails();
    } else {
      // Limpa os dados quando o dialog é fechado ou não há animalId
      setAnimalDetails(null);
      setPreferences(null);
      setLoading(false);
      setError(null);
    }
  }, [open, animalId]);

  const handleOpenPreferences = () => {
    if (animalDetails) {
      // setOpenPreferencesDialog(true);
      onManagePreferences(animalDetails.id, preferences); // Passa as preferências atuais também
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth PaperProps={{ sx: { backgroundColor: colors.cremeClaro, borderRadius: '12px' } }}>
      <DialogTitle sx={{ backgroundColor: colors.marromClaroSuave, color: colors.textPrimary, display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: `1px solid ${colors.cinzaEsverdeado}` }}>
        <Box sx={{display: 'flex', alignItems: 'center'}}>
            <PetsIcon sx={{mr:1, fontSize: '2rem'}}/>
            <Typography variant="h6" component="div"> 
                {animalDetails?.name ? `Detalhes de ${animalDetails.name}` : 'Detalhes do Animal'}
            </Typography>
        </Box>
        <Tooltip title="Fechar">
          <IconButton onClick={onClose} sx={{ color: colors.textPrimary }}><CloseIcon /></IconButton>
        </Tooltip>
      </DialogTitle>
      
      <DialogContent dividers sx={{ p: {xs: 2, md:3}, backgroundColor: 'white' }}>
        {loading && <Box sx={{ display: 'flex', justifyContent: 'center', alignItems:'center', my: 5, minHeight: '200px' }}><CircularProgress color="primary"/></Box>}
        {error && !loading && <Typography color="error" sx={{ textAlign: 'center', my: 5 }}>{error}</Typography>}
        
        {animalDetails && !loading && !error && (
          <Grid container spacing={3}>
            {/* Coluna Esquerda: Informações Básicas e Saúde */}
            <Grid item xs={12} md={7}>
              <Paper elevation={0} sx={{ p: {xs:1.5, md:2.5}, backgroundColor: colors.cremeClaro, borderRadius: '8px', border: `1px solid ${colors.marromClaroSuave}` }}>
                <Typography variant="h6" gutterBottom sx={{ color: colors.verdeOlivaSuave, fontWeight: 'bold', mb: 2 }}>
                  Informações Gerais
                </Typography>
                <Grid container spacing={1}>
                  <DetailItem icon={<LabelImportantIcon />} label="Nome" value={animalDetails.name} />
                  <DetailItem icon={<PetsIcon />} label="Espécie" value={animalDetails.species} />
                  <DetailItem icon={<PetsIcon />} label="Raça" value={animalDetails.breed} />
                  <DetailItem icon={<CakeIcon />} label="Idade" value={animalDetails.age !== null ? `${animalDetails.age} anos` : '-'} />
                  <DetailItem icon={<FitnessCenterIcon />} label="Peso" value={animalDetails.weight !== null ? `${animalDetails.weight} kg` : '-'} />
                </Grid>
                
                <Divider sx={{ my: 2.5, borderColor: colors.marromClaroSuave }} />
                
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1.5}}>
                    <HealingIcon sx={{ mr: 1.5, color: colors.cinzaEsverdeado }} />
                    <Typography variant="subtitle1" sx={{ color: colors.textSecondary, fontWeight: 'bold' }}>Histórico Médico</Typography>
                </Box>
                <Typography variant="body2" paragraph sx={{ color: colors.textPrimary, mt: 0.5, whiteSpace: 'pre-wrap', pl: 4 /* Alinhar com texto acima*/ }}>
                  {animalDetails.medical_history || 'Nenhum histórico médico informado.'}
                </Typography>
              </Paper>
            </Grid>

            {/* Coluna Direita: Preferências e Datas */}
            <Grid item xs={12} md={5}>
              <Paper elevation={0} sx={{ p: {xs:1.5, md:2.5}, backgroundColor: colors.cremeClaro, borderRadius: '8px', border: `1px solid ${colors.marromClaroSuave}`, height: '100%' }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1.5 }}>
                  <Typography variant="h6" sx={{ color: colors.verdeOlivaSuave, fontWeight: 'bold' }}>
                    Preferências
                  </Typography>
                  <Button 
                      startIcon={<RestaurantMenuIcon />} 
                      onClick={handleOpenPreferences}
                      size="small"
                      sx={{ 
                          color: colors.cinzaEsverdeado, 
                          borderColor: colors.cinzaEsverdeado, 
                          '&:hover': { backgroundColor: colors.verdeOlivaSuave, color: 'white', borderColor: colors.verdeOlivaSuave}
                      }}
                      variant="outlined"
                  >
                      Gerenciar
                  </Button>
                </Box>
                <Box sx={{mb:1}}>
                    <Typography variant="caption" display="block" sx={{ color: colors.textSecondary, fontWeight: 'bold' }}>Gosta de:</Typography>
                    <Typography variant="body2" sx={{ color: colors.textPrimary, whiteSpace: 'pre-wrap', pl:1 }}>{preferences?.gosta_de || '-'}</Typography>
                </Box>
                <Box>
                    <Typography variant="caption" display="block" sx={{ color: colors.textSecondary, fontWeight: 'bold' }}>Não gosta de:</Typography>
                    <Typography variant="body2" sx={{ color: colors.textPrimary, whiteSpace: 'pre-wrap', pl:1 }}>{preferences?.nao_gosta_de || '-'}</Typography>
                </Box>

                <Divider sx={{ my: 2.5, borderColor: colors.marromClaroSuave }} />

                 <Typography variant="caption" sx={{ color: colors.textSecondary, display: 'block', textAlign: 'left', mt:1}}>
                    Data de Cadastro: <Chip label={formatDate(animalDetails.created_at)} size="small" sx={{backgroundColor: colors.chipBackground, color: colors.textPrimary}}/>
                </Typography>
                <Typography variant="caption" sx={{ color: colors.textSecondary, display: 'block', textAlign: 'left', mt:0.5}}>
                    Última Atualização: <Chip label={formatDate(animalDetails.updated_at)} size="small" sx={{backgroundColor: colors.chipBackground, color: colors.textPrimary}}/>
                </Typography>
              </Paper>
            </Grid>
          </Grid>
        )}
      </DialogContent>
      
      <DialogActions sx={{ padding: '16px 24px', backgroundColor: colors.marromClaroSuave, borderTop: `1px solid ${colors.cinzaEsverdeado}` }}>
        <Button 
            onClick={onClose} 
            variant='outlined'
            sx={{ 
                color: colors.textPrimary, 
                borderColor: colors.cinzaEsverdeado,
                '&:hover': { backgroundColor: colors.cinzaEsverdeado, color: 'white', borderColor: colors.cinzaEsverdeado }
            }}
        >
          Fechar
        </Button>
        <Button 
            startIcon={<EditIcon />} 
            onClick={() => {
                if(animalDetails) onEditAnimal(animalDetails);
                onClose(); 
            }}
            variant="contained"
            sx={{ 
                backgroundColor: colors.verdeOlivaSuave, 
                color: colors.textPrimary, 
                '&:hover': { backgroundColor: colors.cinzaEsverdeado, color: 'white' }
            }}
            disabled={!animalDetails || loading}
        >
          Editar Animal
        </Button>
      </DialogActions>

      {/* 
      {animalDetails && (
        <AnimalPreferencesDialog 
          open={openPreferencesDialog}
          onClose={() => setOpenPreferencesDialog(false)}
          animalId={animalDetails.id}
          currentPreferences={preferences}
          onSuccess={() => {
            // Refetch preferences
            animalService.getAnimalPreferences(animalDetails.id)
              .then(data => setPreferences(data || { gosta_de: 'Não informado', nao_gosta_de: 'Não informado' }))
              .catch(err => console.error('Erro ao recarregar preferências', err));
            setOpenPreferencesDialog(false);
          }}
        />
      )}
      */}
    </Dialog>
  );
};

export default AnimalDetailDialog; 