import React, { useState, useEffect } from 'react';
import {
  Dialog, DialogActions, DialogContent, DialogTitle, TextField, Button, 
  Grid, CircularProgress, Typography
} from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { useForm, Controller } from 'react-hook-form';
import animalService from '../services/animalService';

const AnimalPreferencesDialog = ({ open, onClose, animalId, currentPreferences, onSuccess }) => {
  const theme = useTheme();
  const { control, handleSubmit, reset, formState: { isSubmitting } } = useForm({
    defaultValues: {
      gosta_de: '',
      nao_gosta_de: ''
    }
  });

  const [hasExistingPreferences, setHasExistingPreferences] = useState(false);

  useEffect(() => {
    if (open && currentPreferences) {
      reset({
        gosta_de: currentPreferences.gosta_de || '',
        nao_gosta_de: currentPreferences.nao_gosta_de || ''
      });
      setHasExistingPreferences(Boolean(currentPreferences.id));
    } else if (open) {
      reset({ gosta_de: '', nao_gosta_de: '' });
      setHasExistingPreferences(false);
    }
  }, [currentPreferences, open, reset]);

  const onSubmit = async (data) => {
    if (!animalId) {
      alert("Erro: ID do animal não encontrado.");
      return;
    }
    try {
      if (hasExistingPreferences) {
        await animalService.updateAnimalPreferences(animalId, data);
      } else {
        await animalService.createAnimalPreferences(animalId, data);
      }
      onSuccess();
    } catch (error) {
      alert(`Erro ao salvar preferências: ${error.message || 'Verifique os dados e tente novamente.'}`);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} PaperProps={{ sx: { backgroundColor: theme.palette.background.paper } }}>
      <DialogTitle sx={{ backgroundColor: theme.palette.primary.main, color: theme.palette.primary.contrastText }}>
        Gerenciar Preferências Alimentares
      </DialogTitle>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <DialogContent sx={{ pt: 2 }}>
          <Typography sx={{ mb: 2, color: theme.palette.text.secondary }}>
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
        <DialogActions sx={{ p: 2, backgroundColor: theme.palette.primary.main }}>
          <Button onClick={onClose} sx={{ color: theme.palette.primary.contrastText }} disabled={isSubmitting}>
            Cancelar
          </Button>
          <Button 
            type="submit" 
            variant="contained" 
            sx={{ 
              backgroundColor: theme.palette.secondary.main, 
              color: theme.palette.text.primary, 
              '&:hover': { backgroundColor: theme.palette.primary.main, color: 'white' }
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