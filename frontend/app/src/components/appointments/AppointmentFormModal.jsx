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
  FormHelperText,
  Box
} from '@mui/material';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider, DatePicker, TimePicker } from '@mui/x-date-pickers';
import { ptBR } from 'date-fns/locale';
import appointmentService from '../../services/appointmentService';

const AppointmentFormModal = ({
  open,
  onClose,
  appointment,
  isEditing,
  allAnimals,
  selectedAnimalContext, // Animal selecionado no header
}) => {
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  
  // Usar allAnimals da prop ao invés do contexto que pode ter apenas o animal selecionado
  const animalsToShow = allAnimals || [];
  const loadingAnimals = false; // Não bloquear o dropdown, apenas mostrar mensagem apropriada

  useEffect(() => {
    if (open) {
      if (isEditing && appointment) {
        setFormData({
          animal_id: appointment.animal_id || '',
          date: appointment.date ? new Date(appointment.date) : null,
          start_time: appointment.start_time ? `T${appointment.start_time}` : null, // Ajustar para formato que TimePicker espera se necessário
          description: appointment.description || '',
          service_type: appointment.service_type || appointment.description || '',
          status: appointment.status || 'scheduled', // Padrão para "Agendado"
        });
      } else {
        // Novo agendamento
        setFormData({
          animal_id: selectedAnimalContext ? selectedAnimalContext.id : '',
          date: null,
          start_time: null,
          description: '',
          service_type: '',
          status: 'scheduled', // Padrão para "Agendado"
        });
      }
      setErrors({}); // Limpar erros ao abrir
    }
  }, [open, isEditing, appointment, selectedAnimalContext]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleTimeChange = (newTime) => {
    // O TimePicker pode retornar um objeto Date completo, precisamos apenas da hora.
    // Formatar para HH:mm:ss
    if (newTime) {
        const hours = newTime.getHours().toString().padStart(2, '0');
        const minutes = newTime.getMinutes().toString().padStart(2, '0');
        const seconds = newTime.getSeconds().toString().padStart(2, '0');
        setFormData(prev => ({ ...prev, start_time: `${hours}:${minutes}:${seconds}` }));
    } else {
        setFormData(prev => ({ ...prev, start_time: null }));
    }
  };
  
  const validateForm = () => {
    const newErrors = {};
    if (!formData.animal_id) newErrors.animal_id = 'Animal é obrigatório';
    if (!formData.date) newErrors.date = 'Data é obrigatória';
    if (!formData.start_time) newErrors.start_time = 'Hora é obrigatória';
    if (!formData.status) newErrors.status = 'Status é obrigatório';
    // Adicionar mais validações se necessário (ex: formato da hora, data no futuro etc)
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    setLoading(true);
    try {
      const submissionData = {
        ...formData,
        date: formData.date ? formData.date.toISOString().split('T')[0] : null, // Formato YYYY-MM-DD
        // start_time já deve estar como HH:mm:ss
      };

      if (isEditing) {
        await appointmentService.updateAppointment(appointment.id, submissionData);
      } else {
        await appointmentService.createAppointment(submissionData);
      }
      onClose(); // Fecha o modal e dispara a re-busca na página principal
    } catch (error) {
      console.error("Erro ao salvar agendamento:", error);
      setErrors(prev => ({ ...prev, form: error.response?.data?.detail || 'Erro ao salvar. Tente novamente.' }));
    }
    setLoading(false);
  };

  // Para o TimePicker, precisamos converter a string HH:mm:ss de volta para um objeto Date no dia de hoje
  const getStartTimeAsDateObject = () => {
    if (formData.start_time && typeof formData.start_time === 'string') {
        const [hours, minutes, seconds] = formData.start_time.split(':').map(Number);
        const dateObj = new Date();
        dateObj.setHours(hours, minutes, seconds || 0);
        return dateObj;
    }
    return null;
  };


  return (
    <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ptBR}>
      <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ backgroundColor: '#23e865', color: '#fff'}}>
          {isEditing ? 'Editar Agendamento' : 'Novo Agendamento'}
        </DialogTitle>
        <DialogContent dividers sx={{ pt: 3 }}>
          {errors.form && <Typography color="error" sx={{ mb: 2 }}>{errors.form}</Typography>}
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth error={Boolean(errors.animal_id)} required sx={{ minWidth: 200 }}>
                <InputLabel id="animal-select-label">Animal</InputLabel>
                <Select
                  labelId="animal-select-label"
                  name="animal_id"
                  value={formData.animal_id}
                  onChange={handleChange}
                  label="Animal"
                  disabled={loadingAnimals || !!appointment}
                >
                  {loadingAnimals ? (
                    <MenuItem value="" disabled><em>Carregando animais...</em></MenuItem>
                  ) : animalsToShow.length === 0 ? (
                    <MenuItem value="" disabled><em>Nenhum animal cadastrado</em></MenuItem>
                  ) : (
                    animalsToShow.map((animal) => (
                      <MenuItem key={animal.id} value={animal.id}>
                        {animal.name} ({animal.species})
                      </MenuItem>
                    ))
                  )}
                </Select>
                {errors.animal_id && <FormHelperText>{errors.animal_id}</FormHelperText>}
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <DatePicker
                label="Data *"
                value={formData.date}
                onChange={(newValue) => {
                  setFormData({ ...formData, date: newValue });
                  if (errors.date) {
                    setErrors(prev => ({ ...prev, date: null }));
                  }
                }}
                slotProps={{
                  textField: {
                    fullWidth: true,
                    required: true,
                    error: Boolean(errors.date),
                    helperText: errors.date
                  }
                }}
                disablePast
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TimePicker
                label="Hora *"
                value={getStartTimeAsDateObject()}
                onChange={handleTimeChange}
                slotProps={{
                  textField: {
                    fullWidth: true,
                    required: true,
                    error: Boolean(errors.start_time),
                    helperText: errors.start_time
                  }
                }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth required error={Boolean(errors.status)} sx={{ minWidth: 200 }}>
                <InputLabel id="status-select-label">Status</InputLabel>
                <Select
                  labelId="status-select-label"
                  name="status"
                  value={formData.status}
                  onChange={handleChange}
                  label="Status"
                >
                  <MenuItem value="Agendado">Agendado</MenuItem>
                  <MenuItem value="Confirmado">Confirmado</MenuItem>
                  <MenuItem value="Realizado">Realizado</MenuItem>
                  <MenuItem value="Cancelado">Cancelado</MenuItem>
                </Select>
                {errors.status && <FormHelperText>{errors.status}</FormHelperText>}
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Serviço"
                name="service_type"
                value={formData.service_type}
                onChange={handleChange}
                fullWidth
                placeholder="Ex: Consulta, Vacina, Banho, etc."
                error={Boolean(errors.service_type)}
                helperText={errors.service_type}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Descrição"
                name="description"
                value={formData.description}
                onChange={handleChange}
                multiline
                rows={3}
                fullWidth
                placeholder="Informações adicionais sobre o agendamento"
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
            sx={{ backgroundColor: '#23e865', '&:hover': { backgroundColor: '#209e41' } }}
          >
            {loading ? <CircularProgress size={24} color="inherit" /> : (isEditing ? 'Salvar Alterações' : 'Criar Agendamento')}
          </Button>
        </DialogActions>
      </Dialog>
    </LocalizationProvider>
  );
};

export default AppointmentFormModal; 