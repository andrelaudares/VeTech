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
  Alert,
  Box,
  Typography
} from '@mui/material';
import dietService from '../../services/dietService';

// Paleta de cores
const colors = {
  primaryAction: '#9DB8B2',
  primaryActionHover: '#82a8a0',
  secondaryAction: '#CFE0C3',
  paperBackground: '#FFFFFF',
  textPrimary: '#333',
};

const DietOptionFormModal = ({ open, onClose, dietId, optionData, isEditing, onSaveSuccess }) => {
  const [formData, setFormData] = useState({
    nome: '',
    valor_mensal_estimado: '',
    calorias_totais_dia: '',
    porcao_refeicao: '',
    refeicoes_por_dia: '',
    indicacao: '', // Novo campo
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isEditing && optionData) {
      setFormData({
        nome: optionData.nome || '',
        valor_mensal_estimado: optionData.valor_mensal_estimado || '',
        calorias_totais_dia: optionData.calorias_totais_dia || '',
        porcao_refeicao: optionData.porcao_refeicao || '',
        refeicoes_por_dia: optionData.refeicoes_por_dia || '',
        indicacao: optionData.indicacao || '',
      });
    } else {
      // Reset form para criação
      setFormData({
        nome: '',
        valor_mensal_estimado: '',
        calorias_totais_dia: '',
        porcao_refeicao: '',
        refeicoes_por_dia: '',
        indicacao: '',
      });
    }
    setError(null);
  }, [open, isEditing, optionData]);

  const handleChange = (event) => {
    const { name, value, type } = event.target;
    // Permitir apenas números (ou vazio) para campos numéricos
    if (type === 'number') {
        if (value === '' || /^[0-9]*\.?[0-9]*$/.test(value)) { // Permite decimais para valor
             setFormData(prev => ({ ...prev, [name]: value }));
        } else if (name === 'refeicoes_por_dia' && value === '' || /^[0-9]*$/.test(value)) { // Apenas inteiros para refeicoes
             setFormData(prev => ({ ...prev, [name]: value }));
        }
    } else {
        setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const validateForm = () => {
    if (!formData.nome) {
      setError('O campo Nome da Opção é obrigatório.');
      return false;
    }
    // Adicionar mais validações se necessário (ex: valores numéricos > 0)
    setError(null);
    return true;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    setError(null);

    // Converter campos numéricos de string para número ou null se vazio
    const dataToSend = {
      ...formData,
      valor_mensal_estimado: formData.valor_mensal_estimado ? parseFloat(formData.valor_mensal_estimado) : null,
      calorias_totais_dia: formData.calorias_totais_dia ? parseInt(formData.calorias_totais_dia, 10) : null,
      refeicoes_por_dia: formData.refeicoes_por_dia ? parseInt(formData.refeicoes_por_dia, 10) : null,
    };

    try {
      if (isEditing && optionData?.id) {
        await dietService.updateDietOption(optionData.id, dataToSend);
      } else {
        if (!dietId) {
            setError("ID da dieta principal não fornecido para criar a opção.");
            setLoading(false);
            return;
        }
        await dietService.createDietOption(dietId, dataToSend);
      }
      onSaveSuccess(); // Chama a função de callback do pai (geralmente para atualizar a lista no DietDetailsModal)
      handleCloseModal();
    } catch (err) {
      console.error("Erro ao salvar opção de dieta:", err);
      setError(err.detail || err.message || 'Erro desconhecido ao salvar opção de dieta.');
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
    <Dialog open={open} onClose={handleCloseModal} maxWidth="sm" fullWidth PaperProps={{ component: 'form', onSubmit: handleSubmit }}>
      <DialogTitle sx={{ backgroundColor: colors.secondaryAction, color: colors.textPrimary }}>
        {isEditing ? 'Editar Opção de Dieta' : 'Nova Opção de Dieta'}
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
              label="Nome da Opção (Ex: Ração Manhã, Almoço Caseiro)"
              type="text"
              fullWidth
              variant="outlined"
              value={formData.nome}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              margin="dense"
              id="valor_mensal_estimado"
              name="valor_mensal_estimado"
              label="Valor Mensal Estimado (R$)"
              type="number" // Usar type number para validação básica do navegador
              fullWidth
              variant="outlined"
              value={formData.valor_mensal_estimado}
              onChange={handleChange}
              InputProps={{ inputProps: { step: "0.01" } }} // Para permitir decimais
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              margin="dense"
              id="calorias_totais_dia"
              name="calorias_totais_dia"
              label="Calorias Totais / Dia (kcal)"
              type="number"
              fullWidth
              variant="outlined"
              value={formData.calorias_totais_dia}
              onChange={handleChange}
              InputProps={{ inputProps: { step: "1" } }} // Apenas inteiros
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              margin="dense"
              id="porcao_refeicao"
              name="porcao_refeicao"
              label="Porção por Refeição (Ex: 100g, 1 copo)"
              type="text"
              fullWidth
              variant="outlined"
              value={formData.porcao_refeicao}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              margin="dense"
              id="refeicoes_por_dia"
              name="refeicoes_por_dia"
              label="Refeições por Dia"
              type="number"
              fullWidth
              variant="outlined"
              value={formData.refeicoes_por_dia}
              onChange={handleChange}
              InputProps={{ inputProps: { step: "1", min: "1" } }} // Apenas inteiros positivos
            />
          </Grid>
           <Grid item xs={12}>
            <TextField
              margin="dense"
              id="indicacao"
              name="indicacao"
              label="Indicação / Observações da Opção"
              type="text"
              fullWidth
              multiline
              rows={3}
              variant="outlined"
              value={formData.indicacao}
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
            minWidth: '120px', // Ajustar largura
          }}
        >
          {loading ? <CircularProgress size={24} color="inherit" /> : (isEditing ? 'Salvar Opção' : 'Adicionar Opção')}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default DietOptionFormModal; 