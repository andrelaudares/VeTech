import React, { useState, useEffect } from 'react';
import {
  Dialog, DialogActions, DialogContent, DialogTitle, TextField, Button, 
  Grid, CircularProgress, Typography
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import animalService from '../services/animalService';

// Paleta de cores
const colors = {
  marromClaroSuave: '#D8CAB8',
  cremeClaro: '#F9F9F9',
  cinzaEsverdeado: '#9DB8B2',
  verdeOlivaSuave: '#CFE0C3',
  textPrimary: '#333',
  errorRed: '#d32f2f'
};

const AnimalPreferencesDialog = ({ open, onClose, animalId, currentPreferences, onSuccess }) => {
  const { control, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm({
    defaultValues: {
      gosta_de: '',
      nao_gosta_de: ''
    }
  });

  // Determina se já existem preferências para decidir entre POST e PATCH
  const [hasExistingPreferences, setHasExistingPreferences] = useState(false);

  useEffect(() => {
    if (open && currentPreferences) {
        reset({
            gosta_de: currentPreferences.gosta_de || '',
            nao_gosta_de: currentPreferences.nao_gosta_de || ''
        });
        // Se currentPreferences tem um 'id', significa que elas existem no backend
        setHasExistingPreferences(Boolean(currentPreferences.id)); 
    } else if (open) { // Se abrir sem currentPreferences, assume que não existem
        reset({ gosta_de: '', nao_gosta_de: '' });
        setHasExistingPreferences(false);
    }
  }, [currentPreferences, open, reset]);

  const onSubmit = async (data) => {
    if (!animalId) {
      console.error("ID do animal não fornecido para salvar preferências.");
      alert("Erro: ID do animal não encontrado.");
      return;
    }
    try {
      if (hasExistingPreferences) {
        await animalService.updateAnimalPreferences(animalId, data);
      } else {
        await animalService.createAnimalPreferences(animalId, data);
      }
      onSuccess(); // Callback para fechar o dialog e atualizar os detalhes
    } catch (error) {
      console.error('Erro ao salvar preferências:', error);
      alert(`Erro ao salvar preferências: ${error.message || 'Verifique os dados e tente novamente.'}`);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} PaperProps={{ sx: { backgroundColor: colors.cremeClaro } }}>
      <DialogTitle sx={{ backgroundColor: colors.marromClaroSuave, color: colors.textPrimary }}>
        Gerenciar Preferências Alimentares
      </DialogTitle>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <DialogContent sx={{ pt: 2 }}>
          <Typography sx={{ mb: 2, color: colors.textSecondary }}>
            Atualize as preferências alimentares do animal.
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Controller
                name="gosta_de"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Gosta de (alimentos, petiscos)"
                    multiline
                    rows={3}
                    fullWidth
                    sx={{ backgroundColor: 'white' }}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12}>
              <Controller
                name="nao_gosta_de"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Não gosta de (alimentos, texturas)"
                    multiline
                    rows={3}
                    fullWidth
                    sx={{ backgroundColor: 'white' }}
                  />
                )}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions sx={{ padding: '16px 24px', backgroundColor: colors.marromClaroSuave }}>
          <Button onClick={onClose} sx={{ color: colors.textPrimary }} disabled={isSubmitting}>
            Cancelar
          </Button>
          <Button 
            type="submit" 
            variant="contained" 
            sx={{ 
              backgroundColor: colors.verdeOlivaSuave, 
              color: colors.textPrimary, 
              '&:hover': { backgroundColor: colors.cinzaEsverdeado }
            }}
            disabled={isSubmitting}
          >
            {isSubmitting ? <CircularProgress size={24} color="inherit" /> : 'Salvar Preferências'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};

export default AnimalPreferencesDialog; 