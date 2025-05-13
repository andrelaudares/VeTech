import React, { useState, useEffect } from 'react';
import {
  Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle,
  TextField, Button, Grid, MenuItem, CircularProgress, Box
} from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { useForm, Controller } from 'react-hook-form';
import animalService from '../services/animalService';

const AnimalFormDialog = ({ open, onClose, animal, onSuccess }) => {
  const theme = useTheme();
  const { control, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm({
    defaultValues: {
      name: '',
      species: '',
      breed: '',
      age: '',
      weight: '',
      medical_history: ''
    }
  });

  const isEditMode = Boolean(animal);

  useEffect(() => {
    if (isEditMode && animal) {
      reset({
        name: animal.name || '',
        species: animal.species || '',
        breed: animal.breed || '',
        age: animal.age !== null ? String(animal.age) : '',
        weight: animal.weight !== null ? String(animal.weight) : '',
        medical_history: animal.medical_history || ''
      });
    } else {
      reset({
        name: '',
        species: '',
        breed: '',
        age: '',
        weight: '',
        medical_history: ''
      });
    }
  }, [animal, open, reset, isEditMode]);

  const onSubmit = async (data) => {
    try {
      const payload = {
        ...data,
        age: data.age ? parseInt(data.age, 10) : null,
        weight: data.weight ? parseFloat(data.weight.replace(',', '.')) : null,
      };
      if (isEditMode) {
        await animalService.updateAnimal(animal.id, payload);
      } else {
        await animalService.createAnimal(payload);
      }
      onSuccess();
    } catch (error) {
      console.error('Erro ao salvar animal:', error);
      alert(`Erro ao salvar: ${error.message || 'Verifique os dados e tente novamente.'}`);
    }
  };

  const handleCloseDialog = () => {
    if (isSubmitting) return;
    onClose();
  };

  const especiesDisponiveis = ["Cachorro", "Gato", "Ave", "Réptil", "Roedor", "Outro"];

  return (
    <Dialog open={open} onClose={handleCloseDialog} PaperProps={{ sx: { backgroundColor: theme.palette.background.paper } }}>
      <DialogTitle sx={{ backgroundColor: theme.palette.primary.main, color: theme.palette.primary.contrastText }}>
        {isEditMode ? 'Editar Animal' : 'Cadastrar Novo Animal'}
      </DialogTitle>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <DialogContent sx={{ pt: 2 }}>
          <DialogContentText sx={{ mb: 2, color: theme.palette.text.secondary }}>
            Preencha os campos abaixo para {isEditMode ? 'atualizar os dados do' : 'registrar um novo'} animal.
          </DialogContentText>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <Controller
                name="name"
                control={control}
                rules={{ required: 'Nome é obrigatório' }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Nome do Animal"
                    fullWidth
                    required
                    error={!!errors.name}
                    helperText={errors.name?.message}
                    sx={{ backgroundColor: 'white' }}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12}>
              <Controller
                name="species"
                control={control}
                rules={{ required: 'Espécie é obrigatória' }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Espécie"
                    select
                    fullWidth
                    required
                    error={!!errors.species}
                    helperText={errors.species?.message}
                    sx={{ backgroundColor: 'white', minWidth: '120px' }}
                  >
                    {especiesDisponiveis.map((option) => (
                      <MenuItem key={option} value={option}>{option}</MenuItem>
                    ))}
                  </TextField>
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="breed"
                control={control}
                render={({ field }) => (
                  <TextField {...field} label="Raça" fullWidth sx={{ backgroundColor: 'white' }} />
                )}
              />
            </Grid>
            <Grid item xs={12} sm={3}>
              <Controller
                name="age"
                control={control}
                rules={{ 
                  min: { value: 0, message: 'Idade não pode ser negativa' },
                  pattern: { value: /^[0-9]*$/, message: 'Idade deve ser um número' }
                }}
                render={({ field }) => (
                  <TextField 
                    {...field} 
                    label="Idade (anos)" 
                    type="number" 
                    fullWidth 
                    error={!!errors.age}
                    helperText={errors.age?.message}
                    sx={{ backgroundColor: 'white' }}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} sm={3}>
              <Controller
                name="weight"
                control={control}
                rules={{ 
                  min: { value: 0, message: 'Peso não pode ser negativo' },
                  pattern: { value: /^[0-9]*[.,]?[0-9]+$/, message: 'Peso deve ser um número'}
                }}
                render={({ field }) => (
                  <TextField 
                    {...field} 
                    label="Peso (kg)" 
                    type="text"
                    fullWidth 
                    error={!!errors.weight}
                    helperText={errors.weight?.message}
                    sx={{ backgroundColor: 'white' }}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12}>
              <Controller
                name="medical_history"
                control={control}
                render={({ field }) => (
                  <TextField 
                    {...field} 
                    label="Histórico Médico (opcional)" 
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
          <Button onClick={handleCloseDialog} sx={{ color: theme.palette.primary.contrastText }} disabled={isSubmitting}>
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
            {isSubmitting ? <CircularProgress size={24} color="inherit" /> : (isEditMode ? 'Salvar Alterações' : 'Cadastrar Animal')}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};

export default AnimalFormDialog;
