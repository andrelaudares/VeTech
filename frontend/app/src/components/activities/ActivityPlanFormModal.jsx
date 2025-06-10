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
  Grid,
  Box,
  Typography,
  LinearProgress
} from '@mui/material';
import activityService from '../../services/activityService';

// Paleta de cores
const colors = {
  primaryAction: '#9DB8B2',
  primaryActionHover: '#82a8a0',
  textPrimary: '#333333',
  textSecondary: '#555555',
  paperBackground: '#FFFFFF',
  borderColor: '#E0E0E0',
  progressColor: '#9DB8B2',
};

const ActivityPlanFormModal = ({ 
    open, 
    onClose, 
    planData, 
    isEditing, 
    onSaveSuccess, 
    animalId, 
    availableActivityTypes 
}) => {
  const [formData, setFormData] = useState({
    atividade_id: '', // ID do tipo de atividade selecionado
    frequencia_semanal: '',
    duracao_minutos: '',
    intensidade: 'leve', // Default, conforme sprint5.md backend
    orientacoes: '',
    data_inicio: new Date().toISOString().split('T')[0], // Default to today
    data_fim: '', // Opcional
    status: 'ativo' // Default status
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const intensityOptions = [
    { value: 'leve', label: 'Leve' },
    { value: 'moderada', label: 'Moderada' },
    { value: 'intensa', label: 'Intensa' },
  ];

  const statusOptions = [
    { value: 'ativo', label: 'Ativo' },
    { value: 'inativo', label: 'Inativo' },
    { value: 'concluido', label: 'Concluído' },
  ];

  useEffect(() => {
    if (isEditing && planData) {
      setFormData({
        atividade_id: planData.atividade_id || '',
        frequencia_semanal: planData.frequencia_semanal !== null ? String(planData.frequencia_semanal) : '',
        duracao_minutos: planData.duracao_minutos !== null ? String(planData.duracao_minutos) : '',
        intensidade: planData.intensidade || 'leve',
        orientacoes: planData.orientacoes || '',
        data_inicio: planData.data_inicio ? new Date(planData.data_inicio).toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
        data_fim: planData.data_fim ? new Date(planData.data_fim).toISOString().split('T')[0] : '',
        status: planData.status || 'ativo',
      });
    } else {
      // Reset para criação
      setFormData({
        atividade_id: '',
        frequencia_semanal: '',
        duracao_minutos: '',
        intensidade: 'leve',
        orientacoes: '',
        data_inicio: new Date().toISOString().split('T')[0],
        data_fim: '',
        status: 'ativo',
      });
    }
    setError(null);
  }, [open, isEditing, planData]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSave = async () => {
    setError(null);
    if (!formData.atividade_id || !formData.data_inicio || !formData.frequencia_semanal || !formData.duracao_minutos) {
      setError("Atividade, Data de Início, Frequência Semanal e Duração são obrigatórios.");
      return;
    }
    if (!animalId) {
        setError("ID do animal não fornecido. Não é possível salvar.");
        return;
    }

    setLoading(true);
    try {
      const payload = {
        ...formData,
        frequencia_semanal: parseInt(formData.frequencia_semanal, 10) || null,
        duracao_minutos: parseInt(formData.duracao_minutos, 10) || null,
        // data_inicio e data_fim já estão formatados como YYYY-MM-DD
        data_fim: formData.data_fim || null, // Envia null se vazio
      };
      // O backend espera animal_id na URL e clinic_id é pego do token.
      // atividade_id está no payload.

      if (isEditing && planData?.id) {
        await activityService.updateActivityPlan(planData.id, payload);
      } else {
        // Para POST, o payload não deve conter o ID do plano
        const createPayload = { ...payload };
        delete createPayload.id; // Garantir que não há ID no payload de criação
        await activityService.createActivityPlan(animalId, createPayload);
      }
      onSaveSuccess();
      handleCloseModal();
    } catch (err) {
      console.error("Erro ao salvar plano de atividade:", err);
      setError(err.detail || err.message || "Erro ao salvar plano. Verifique os dados.");
    } finally {
      setLoading(false);
    }
  };

  const handleCloseModal = () => {
    if (loading) return;
    // Não resetar formData aqui para permitir que o usuário veja os dados em caso de erro
    // O useEffect já lida com o reset quando o modal reabre ou muda de modo.
    setError(null); // Limpar erro ao fechar explicitamente
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleCloseModal} maxWidth="md" fullWidth PaperProps={{ sx: { backgroundColor: colors.paperBackground } }}>
      <DialogTitle sx={{ backgroundColor: '#23e865', color: colors.textPrimary, borderBottom: `1px solid ${colors.borderColor}` }}>
        {isEditing ? 'Editar Plano de Atividade' : 'Novo Plano de Atividade'}
      </DialogTitle>
      <DialogContent sx={{ pt: '20px !important' }}>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        
        {/* Pré-visualização do Progresso (0% ao criar) */} 
        {!isEditing && (
            <Box sx={{mb: 2.5}}>
                <Typography variant="caption" sx={{color: colors.textSecondary}}>Progresso Inicial Estimado</Typography>
                <LinearProgress variant="determinate" value={0} sx={{ height: 8, borderRadius: 4, backgroundColor: '#e0e0e0', '& .MuiLinearProgress-bar': { backgroundColor: colors.progressColor } }}/>
            </Box>
        )}

        <Grid container spacing={2.5}>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth margin="dense" variant="outlined" error={!!error && !formData.atividade_id}>
              <InputLabel id="activity-type-select-label" shrink={true}>Tipo de Atividade *</InputLabel>
              <Select
                labelId="activity-type-select-label"
                name="atividade_id"
                value={formData.atividade_id}
                onChange={handleChange}
                label="Tipo de Atividade *"
                displayEmpty
              >
                <MenuItem value="">
                  <em>Selecione um tipo de atividade</em>
                </MenuItem>
                {(availableActivityTypes || []).map(type => (
                  <MenuItem key={type.id} value={type.id}>{type.nome}</MenuItem>
                ))}
              </Select>
              {!!error && !formData.atividade_id && <FormHelperText sx={{color: '#d32f2f'}}>Campo obrigatório</FormHelperText>}
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              margin="dense"
              name="frequencia_semanal"
              label="Frequência Semanal (vezes) *"
              type="number"
              fullWidth
              variant="outlined"
              value={formData.frequencia_semanal}
              onChange={handleChange}
              InputProps={{ inputProps: { min: 1 } }}
              error={!!error && !formData.frequencia_semanal}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              margin="dense"
              name="duracao_minutos"
              label="Duração por Sessão (minutos) *"
              type="number"
              fullWidth
              variant="outlined"
              value={formData.duracao_minutos}
              onChange={handleChange}
              InputProps={{ inputProps: { min: 1 } }}
              error={!!error && !formData.duracao_minutos}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth margin="dense" variant="outlined">
              <InputLabel id="intensity-select-label" shrink={true}>Intensidade</InputLabel>
              <Select
                labelId="intensity-select-label"
                name="intensidade"
                value={formData.intensidade}
                onChange={handleChange}
                label="Intensidade"
                displayEmpty
              >
                {intensityOptions.map(opt => (
                  <MenuItem key={opt.value} value={opt.value}>{opt.label}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              margin="dense"
              name="data_inicio"
              label="Data de Início *"
              type="date"
              fullWidth
              variant="outlined"
              value={formData.data_inicio}
              onChange={handleChange}
              InputLabelProps={{ shrink: true }}
              error={!!error && !formData.data_inicio}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              margin="dense"
              name="data_fim"
              label="Data de Fim (Opcional)"
              type="date"
              fullWidth
              variant="outlined"
              value={formData.data_fim}
              onChange={handleChange}
              InputLabelProps={{ shrink: true }}
              inputProps={{
                min: formData.data_inicio // Data fim não pode ser antes da data início
              }}
            />
          </Grid>
            <Grid item xs={12} sm={6}>
                <FormControl fullWidth margin="dense" variant="outlined">
                <InputLabel id="status-select-label">Status do Plano</InputLabel>
                <Select
                    labelId="status-select-label"
                    name="status"
                    value={formData.status}
                    onChange={handleChange}
                    label="Status do Plano"
                >
                    {statusOptions.map(opt => (
                    <MenuItem key={opt.value} value={opt.value}>{opt.label}</MenuItem>
                    ))}
                </Select>
                </FormControl>
            </Grid>
          <Grid item xs={12}>
            <TextField
              margin="dense"
              name="orientacoes"
              label="Orientações / Observações (Opcional)"
              type="text"
              fullWidth
              multiline
              rows={3}
              variant="outlined"
              value={formData.orientacoes}
              onChange={handleChange}
            />
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions sx={{ borderTop: `1px solid ${colors.borderColor}`, p: '16px 24px' }}>
        <Button onClick={handleCloseModal} disabled={loading} variant="outlined" sx={{ color: colors.textSecondary, borderColor: colors.textSecondary, '&:hover': { backgroundColor: 'rgba(0,0,0,0.04)', borderColor: colors.textPrimary}}}>Cancelar</Button>
        <Button onClick={handleSave} variant="contained" disabled={loading || !formData.atividade_id || !formData.data_inicio || !formData.frequencia_semanal || !formData.duracao_minutos} sx={{ backgroundColor: colors.primaryAction, '&:hover': { backgroundColor: colors.primaryActionHover } }}>
          {loading ? <CircularProgress size={24} color="inherit" /> : (isEditing ? 'Salvar Alterações' : 'Criar Plano')}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ActivityPlanFormModal; 