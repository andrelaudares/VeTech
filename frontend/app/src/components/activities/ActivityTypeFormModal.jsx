import React, { useState, useEffect } from 'react';
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert,
  Box,
  Grid,
} from '@mui/material';
import activityService from '../../services/activityService';

// Paleta de cores (pode ser importada de um arquivo central no futuro)
const colors = {
  primaryAction: '#9DB8B2',
  primaryActionHover: '#82a8a0',
  textPrimary: '#333333',
  deleteButton: '#e57373', // Exemplo para botões de cancelar/fechar
  deleteButtonHover: '#d32f2f',
  paperBackground: '#FFFFFF',
};

// Opções para o campo 'tipo' (poderia vir de uma API ou constante global)
const activityKindOptions = [
  { value: 'cardiovascular', label: 'Cardiovascular' },
  { value: 'forca', label: 'Força' },
  { value: 'flexibilidade', label: 'Flexibilidade' },
  { value: 'equilibrio', label: 'Equilíbrio' },
  { value: 'mental', label: 'Mental/Cognitivo' },
  { value: 'outro', label: 'Outro' },
];

const ActivityTypeFormModal = ({ open, onClose, activityTypeData, isEditing, onSaveSuccess }) => {
  const [formData, setFormData] = useState({
    nome: '',
    tipo: '',
    calorias_estimadas_por_minuto: '', // Backend espera por minuto
    // icone: '' // Campo ícone será simples por agora, talvez um select de MUI icons ou string
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isEditing && activityTypeData) {
      setFormData({
        nome: activityTypeData.nome || '',
        tipo: activityTypeData.tipo || '',
        calorias_estimadas_por_minuto: activityTypeData.calorias_estimadas_por_minuto !== null && activityTypeData.calorias_estimadas_por_minuto !== undefined 
                                          ? String(activityTypeData.calorias_estimadas_por_minuto) 
                                          : '',
        // icone: activityTypeData.icone || ''
      });
    } else {
      setFormData({
        nome: '',
        tipo: '',
        calorias_estimadas_por_minuto: '',
        // icone: ''
      });
    }
    setError(null); // Limpar erro ao abrir/mudar modo
  }, [open, isEditing, activityTypeData]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSave = async () => {
    setError(null);
    if (!formData.nome || !formData.tipo) {
      setError("Nome e Tipo são obrigatórios.");
      return;
    }

    setLoading(true);
    try {
      const payload = {
        ...formData,
        calorias_estimadas_por_minuto: formData.calorias_estimadas_por_minuto 
                                          ? parseFloat(formData.calorias_estimadas_por_minuto) 
                                          : null,
      };
      // Remover campos vazios ou nulos que não devem ser enviados, se necessário
      if (payload.calorias_estimadas_por_minuto === null) {
          delete payload.calorias_estimadas_por_minuto;
      }

      if (isEditing && activityTypeData?.id) {
        await activityService.updateActivityType(activityTypeData.id, payload);
      } else {
        await activityService.createActivityType(payload);
      }
      onSaveSuccess(); // Callback para atualizar a lista na página principal
      handleClose(); // Fechar o modal
    } catch (err) {
      console.error("Erro ao salvar tipo de atividade:", err);
      setError(err.message || err.detail || "Erro ao salvar. Verifique os dados e tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    if (loading) return; // Não fechar se estiver carregando
    setFormData({ nome: '', tipo: '', calorias_estimadas_por_minuto: '' });
    setError(null);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth PaperProps={{ sx: { backgroundColor: colors.paperBackground } }}>
      <DialogTitle sx={{ color: colors.textPrimary, borderBottom: `1px solid ${colors.borderColor}` }}>
        {isEditing ? 'Editar Tipo de Atividade' : 'Novo Tipo de Atividade'}
      </DialogTitle>
      <DialogContent sx={{ pt: '20px !important' }}> {/* Adiciona padding top ao conteúdo */}
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        <Grid container spacing={2.5}>
          <Grid item xs={12}>
            <TextField
              autoFocus
              margin="dense"
              name="nome"
              label="Nome do Tipo de Atividade"
              type="text"
              fullWidth
              variant="outlined"
              value={formData.nome}
              onChange={handleChange}
              error={!!error && !formData.nome} // Exemplo de validação visual
              helperText={!!error && !formData.nome ? "Nome é obrigatório" : ""}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth margin="dense" variant="outlined" error={!!error && !formData.tipo}>
              <InputLabel id="tipo-atividade-label">Tipo</InputLabel>
              <Select
                labelId="tipo-atividade-label"
                name="tipo"
                value={formData.tipo}
                onChange={handleChange}
                label="Tipo"
              >
                <MenuItem value="">
                  <em>Selecione um tipo</em>
                </MenuItem>
                {activityKindOptions.map(option => (
                  <MenuItem key={option.value} value={option.value}>{option.label}</MenuItem>
                ))}
              </Select>
              {!!error && !formData.tipo && <Box sx={{color: '#d32f2f', fontSize: '0.75rem', ml: '14px', mt: '3px'}}>Tipo é obrigatório</Box>}
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              margin="dense"
              name="calorias_estimadas_por_minuto"
              label="Calorias por Minuto (opcional)"
              type="number"
              fullWidth
              variant="outlined"
              value={formData.calorias_estimadas_por_minuto}
              onChange={handleChange}
              InputProps={{
                inputProps: { min: 0, step: "0.1" } 
              }}
            />
          </Grid>
          {/* TODO: Adicionar campo para Ícone (simples, se necessário) */}
          {/* Exemplo: 
          <Grid item xs={12}>
            <TextField name="icone" label="Ícone (Nome MUI Icon - opcional)" ... />
          </Grid> 
          */}
        </Grid>
      </DialogContent>
      <DialogActions sx={{ borderTop: `1px solid ${colors.borderColor}`, p: '16px 24px' }}>
        <Button 
            onClick={handleClose} 
            disabled={loading}
            sx={{ 
                color: colors.textSecondary,
                borderColor: colors.textSecondary,
                '&:hover': { 
                    backgroundColor: 'rgba(0,0,0,0.04)',
                    borderColor: colors.textPrimary
                }
            }}
            variant="outlined"
        >
          Cancelar
        </Button>
        <Button 
            onClick={handleSave} 
            color="primary" 
            variant="contained" 
            disabled={loading || !formData.nome || !formData.tipo}
            sx={{ backgroundColor: colors.primaryAction, '&:hover': { backgroundColor: colors.primaryActionHover } }}
        >
          {loading ? <CircularProgress size={24} color="inherit" /> : (isEditing ? 'Salvar Alterações' : 'Criar Tipo')}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ActivityTypeFormModal; 