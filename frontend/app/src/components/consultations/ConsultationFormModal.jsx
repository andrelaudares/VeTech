import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  CircularProgress,
  Typography,
  FormHelperText
} from '@mui/material';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { ptBR } from 'date-fns/locale';
import consultationService from '../../services/consultationService';
import { useAnimal } from '../../contexts/AnimalContext';

const colors = {
  buttonPrimary: '#9DB8B2',
  buttonPrimaryHover: '#82a8a0',
  tableHeader: '#D8CAB8', 
  textPrimary: '#333',
  textSecondary: '#555',
};

const ConsultationFormModal = ({
  open,
  onClose,
  consultation,
  isEditing,
  allAnimals,
  selectedAnimalContext,
}) => {
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const { animals, loadingAnimals } = useAnimal();

  useEffect(() => {
    if (open) {
      if (isEditing && consultation) {
        setFormData({
          animal_id: consultation.animal_id || '',
          date: consultation.date ? new Date(consultation.date) : new Date(), // Padrão para data atual se editando e não tiver
          description: consultation.description || '',
        });
      } else {
        setFormData({
          animal_id: selectedAnimalContext ? selectedAnimalContext.id : '',
          date: new Date(), // Padrão para data atual em nova consulta
          description: '',
        });
      }
      setErrors({});
    }
  }, [open, isEditing, consultation, selectedAnimalContext]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleDateChange = (newDate) => {
    setFormData(prev => ({ ...prev, date: newDate }));
  };

  const validateForm = () => {
    const newErrors = {};
    if (!formData.animal_id) newErrors.animal_id = 'Animal é obrigatório';
    if (!formData.date) newErrors.date = 'Data é obrigatória';
    if (!formData.description?.trim()) newErrors.description = 'Descrição é obrigatória';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;
    setLoading(true);
    try {
      const submissionData = {
        ...formData,
        // A API espera a data como YYYY-MM-DDTHH:mm:ssZ ou apenas YYYY-MM-DD.
        // O backend trata a data, se apenas YYYY-MM-DD for enviado, ele pode adicionar T00:00:00Z.
        // Para simplificar, enviamos a data completa com horário atual.
        date: formData.date ? formData.date.toISOString() : new Date().toISOString(),
      };

      if (isEditing) {
        await consultationService.updateConsultation(consultation.id, submissionData);
      } else {
        await consultationService.createConsultation(submissionData);
      }
      onClose();
    } catch (error) {
      console.error("Erro ao salvar consulta:", error);
      setErrors(prev => ({ ...prev, form: error.response?.data?.detail || 'Erro ao salvar. Tente novamente.' }));
    }
    setLoading(false);
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ptBR}>
      <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ backgroundColor: colors.tableHeader, color: colors.textPrimary}}>
          {isEditing ? 'Editar Consulta' : 'Nova Consulta'}
        </DialogTitle>
        <DialogContent dividers>
          {errors.form && <Typography color="error" sx={{ mb: 2 }}>{errors.form}</Typography>}
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <FormControl fullWidth error={Boolean(errors.animal_id)} required>
                <InputLabel id="animal-select-label">Animal</InputLabel>
                <Select
                  labelId="animal-select-label"
                  name="animal_id"
                  value={formData.animal_id}
                  onChange={handleChange}
                  label="Animal"
                  disabled={loadingAnimals || !!consultation}
                >
                  {loadingAnimals ? (
                    <MenuItem value="" disabled><em>Carregando animais...</em></MenuItem>
                  ) : (
                    animals.map((animal) => (
                      <MenuItem key={animal.id} value={animal.id}>
                        {animal.name} ({animal.species})
                      </MenuItem>
                    ))
                  )}
                </Select>
                {errors.animal_id && <FormHelperText>{errors.animal_id}</FormHelperText>}
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <DatePicker
                label="Data *"
                value={formData.date}
                onChange={(newValue) => {
                  setFormData({ ...formData, date: newValue });
                  if (errors.date) {
                    setErrors(prev => ({ ...prev, date: null }));
                  }
                }}
                renderInput={(params) => 
                  <TextField {...params} fullWidth required error={Boolean(errors.date)} helperText={errors.date} />
                }
                disablePast
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Descrição *"
                name="description"
                value={formData.description}
                onChange={handleChange}
                multiline
                rows={4}
                fullWidth
                required
                error={Boolean(errors.description)}
                helperText={errors.description}
              />
            </Grid>
            {errors.general && (
              <Grid item xs={12}>
                <Typography color="error" variant="body2">{errors.general}</Typography>
              </Grid>
            )}
          </Grid>
        </DialogContent>
        <DialogActions sx={{ padding: '16px 24px' }}>
          <Button onClick={onClose} disabled={loading}>Cancelar</Button>
          <Button 
            onClick={handleSubmit} 
            variant="contained" 
            disabled={loading}
            sx={{ backgroundColor: colors.buttonPrimary, '&:hover': { backgroundColor: colors.buttonPrimaryHover } }}
          >
            {loading ? <CircularProgress size={24} color="inherit" /> : (isEditing ? 'Salvar Alterações' : 'Criar Consulta')}
          </Button>
        </DialogActions>
      </Dialog>
    </LocalizationProvider>
  );
};

export default ConsultationFormModal; 