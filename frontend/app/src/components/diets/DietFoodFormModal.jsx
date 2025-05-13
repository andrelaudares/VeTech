import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert
} from '@mui/material';
import dietService from '../../services/dietService';

// Paleta de cores
const colors = {
  primaryAction: '#9DB8B2',
  primaryActionHover: '#82a8a0',
  paperBackground: '#FFFFFF',
  textPrimary: '#333',
};

// Tipos de alimentos (poderia ser mais dinâmico)
const foodTypes = [
    'Ração Seca', 'Ração Úmida', 'Carne Cozida', 'Vegetais Cozidos', 
    'Frutas Permitidas', 'Petisco Industrializado', 'Suplemento', 'Outro'
];

const DietFoodFormModal = ({ open, onClose, dietOptionId, foodData, isEditing, onSaveSuccess }) => {
  const [formData, setFormData] = useState({
    nome: '',
    tipo: '',
    quantidade: '',
    calorias: '',
    horario: '', // Ex: Manhã, Almoço, Jantar, Lanche Tarde
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isEditing && foodData) {
      setFormData({
        nome: foodData.nome || '',
        tipo: foodData.tipo || '',
        quantidade: foodData.quantidade || '',
        calorias: foodData.calorias || '',
        horario: foodData.horario || '',
      });
    } else {
      // Reset form para criação
      setFormData({
        nome: '',
        tipo: '',
        quantidade: '',
        calorias: '',
        horario: '',
      });
    }
    setError(null);
  }, [open, isEditing, foodData]);

  const handleChange = (event) => {
    const { name, value, type } = event.target;
     if (name === 'calorias') {
        if (value === '' || /^[0-9]*$/.test(value)) { // Apenas inteiros para calorias
            setFormData(prev => ({ ...prev, [name]: value }));
        }
    } else {
        setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const validateForm = () => {
    if (!formData.nome || !formData.tipo) {
      setError('Os campos Nome do Alimento e Tipo são obrigatórios.');
      return false;
    }
    setError(null);
    return true;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    setError(null);

    const dataToSend = {
      ...formData,
      calorias: formData.calorias ? parseInt(formData.calorias, 10) : null,
    };

    try {
      if (isEditing && foodData?.id) {
        await dietService.updateDietFood(foodData.id, dataToSend);
      } else {
         if (!dietOptionId) {
            setError("ID da opção de dieta não fornecido para adicionar alimento.");
            setLoading(false);
            return;
        }
        await dietService.addFoodToOption(dietOptionId, dataToSend);
      }
      onSaveSuccess();
      handleCloseModal();
    } catch (err) {
      console.error("Erro ao salvar alimento da dieta:", err);
      setError(err.detail || err.message || 'Erro desconhecido ao salvar alimento.');
    } finally {
      setLoading(false);
    }
  };

  const handleCloseModal = () => {
    if (loading) return;
    setError(null);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleCloseModal} maxWidth="xs" fullWidth PaperProps={{ component: 'form', onSubmit: handleSubmit }}>
      <DialogTitle sx={{ backgroundColor: colors.primaryAction, color: colors.paperBackground }}>
        {isEditing ? 'Editar Alimento' : 'Adicionar Alimento à Opção'}
      </DialogTitle>
      <DialogContent sx={{ pt: 3 }}>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              required
              autoFocus
              margin="dense"
              id="nome"
              name="nome"
              label="Nome do Alimento"
              type="text"
              fullWidth
              variant="outlined"
              value={formData.nome}
              onChange={handleChange}
            />
          </Grid>
           <Grid item xs={12}>
              <FormControl fullWidth required margin="dense">
                <InputLabel id="tipo-alimento-label">Tipo</InputLabel>
                <Select
                  labelId="tipo-alimento-label"
                  id="tipo"
                  name="tipo"
                  value={formData.tipo}
                  label="Tipo"
                  onChange={handleChange}
                >
                  {foodTypes.map((type) => (
                    <MenuItem key={type} value={type.toLowerCase()}>{type}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
                <TextField
                    margin="dense"
                    id="quantidade"
                    name="quantidade"
                    label="Quantidade (Ex: 100g)"
                    type="text"
                    fullWidth
                    variant="outlined"
                    value={formData.quantidade}
                    onChange={handleChange}
                    />
            </Grid>
            <Grid item xs={12} sm={6}>
                <TextField
                    margin="dense"
                    id="calorias"
                    name="calorias"
                    label="Calorias (kcal)"
                    type="number" // Permitir apenas números
                    fullWidth
                    variant="outlined"
                    value={formData.calorias}
                    onChange={handleChange}
                    InputProps={{ inputProps: { step: "1" } }}
                    />
            </Grid>
             <Grid item xs={12}>
                <TextField
                    margin="dense"
                    id="horario"
                    name="horario"
                    label="Horário Sugerido (Ex: Manhã, Após passeio)"
                    type="text"
                    fullWidth
                    variant="outlined"
                    value={formData.horario}
                    onChange={handleChange}
                    />
            </Grid>
        </Grid>
      </DialogContent>
      <DialogActions sx={{ p: '16px 24px' }}>
        <Button onClick={handleCloseModal} color="inherit" disabled={loading}>
          Cancelar
        </Button>
        <Button
          type="submit"
          variant="contained"
          disabled={loading}
          sx={{
            backgroundColor: colors.primaryAction,
            '&:hover': { backgroundColor: colors.primaryActionHover },
            minWidth: '120px',
          }}
        >
          {loading ? <CircularProgress size={24} color="inherit" /> : (isEditing ? 'Salvar Alimento' : 'Adicionar')}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default DietFoodFormModal; 