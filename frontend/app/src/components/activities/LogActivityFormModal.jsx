import React, { useState, useEffect } from 'react';
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  TextField,
  CircularProgress,
  Alert,
  Grid,
  Box,
  Typography,
  Rating, // Para satisfação
  Slider, // Para esforço percebido
} from '@mui/material';
import { LocalizationProvider, DateTimePicker } from '@mui/x-date-pickers'; // Para data e hora
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'; // Adapter para date-fns
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';
import NotesIcon from '@mui/icons-material/Notes';
import SentimentVerySatisfiedIcon from '@mui/icons-material/SentimentVerySatisfied';
import SentimentSatisfiedAltIcon from '@mui/icons-material/SentimentSatisfiedAlt';
import SentimentSatisfiedIcon from '@mui/icons-material/SentimentSatisfied';
import SentimentDissatisfiedIcon from '@mui/icons-material/SentimentDissatisfied';
import SentimentVeryDissatisfiedIcon from '@mui/icons-material/SentimentVeryDissatisfied';

import activityService from '../../services/activityService';

const colors = {
  primaryAction: '#9DB8B2',
  primaryActionHover: '#82a8a0',
  textPrimary: '#333333',
  textSecondary: '#555555',
  paperBackground: '#FFFFFF',
  borderColor: '#E0E0E0',
};

const effortMarks = [
  { value: 0, label: 'Muito Leve' },
  { value: 25, label: 'Leve' },
  { value: 50, label: 'Moderado' },
  { value: 75, label: 'Intenso' },
  { value: 100, label: 'Máximo' },
];

const satisfactionIcons = {
  1: { icon: <SentimentVeryDissatisfiedIcon fontSize="inherit" />, label: 'Muito Insatisfeito' },
  2: { icon: <SentimentDissatisfiedIcon fontSize="inherit" />, label: 'Insatisfeito' },
  3: { icon: <SentimentSatisfiedIcon fontSize="inherit" />, label: 'Neutro' },
  4: { icon: <SentimentSatisfiedAltIcon fontSize="inherit" />, label: 'Satisfeito' },
  5: { icon: <SentimentVerySatisfiedIcon fontSize="inherit" />, label: 'Muito Satisfeito' },
};

function IconContainer(props) {
  const { value, ...other } = props;
  return <span {...other}>{satisfactionIcons[value].icon}</span>;
}

const LogActivityFormModal = ({ open, onClose, onSaveSuccess, planToLog, animalId }) => {
  const [formData, setFormData] = useState({
    data_hora_inicio: null, // Será um objeto Date
    duracao_realizada_minutos: '',
    esforco_percebido: 50, // Default para moderado
    satisfacao: 3, // Default para neutro
    observacoes: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (open && planToLog) {
      setFormData({
        data_hora_inicio: new Date(), // Default para agora
        duracao_realizada_minutos: planToLog.duracao_minutos ? String(planToLog.duracao_minutos) : '',
        esforco_percebido: 50,
        satisfacao: 3,
        observacoes: '',
      });
    } else if (!open) {
        // Limpar ao fechar para não persistir dados entre aberturas com planos diferentes
        setFormData({ data_hora_inicio: null, duracao_realizada_minutos: '', esforco_percebido: 50, satisfacao: 3, observacoes: '' });
    }
    setError(null);
  }, [open, planToLog]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleDateTimeChange = (newValue) => {
    setFormData(prev => ({ ...prev, data_hora_inicio: newValue }));
  };
  
  const handleSliderChange = (event, newValue) => {
    setFormData(prev => ({ ...prev, esforco_percebido: newValue }));
  };

  const handleRatingChange = (event, newValue) => {
    setFormData(prev => ({ ...prev, satisfacao: newValue }));
  };

  const handleSave = async () => {
    setError(null);
    if (!formData.data_hora_inicio || !formData.duracao_realizada_minutos) {
      setError("Data/Hora de Início e Duração Realizada são obrigatórios.");
      return;
    }
    if (!planToLog?.id || !animalId) {
      setError("Informações do plano ou do animal ausentes. Não é possível salvar.");
      return;
    }

    setLoading(true);
    try {
      const payload = {
        ...formData,
        data_hora_inicio: formData.data_hora_inicio.toISOString(),
        duracao_realizada_minutos: parseInt(formData.duracao_realizada_minutos, 10),
        // animal_id e plano_atividade_id são passados na URL pelo serviço
      };

      await activityService.logActivityExecution(animalId, planToLog.id, payload);
      onSaveSuccess(); // Callback para atualizar dados na página principal (histórico, progresso do plano)
      handleCloseModal();
    } catch (err) {
      console.error("Erro ao registrar atividade:", err);
      setError(err.detail || err.message || "Erro ao registrar atividade. Verifique os dados.");
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
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Dialog open={open} onClose={handleCloseModal} maxWidth="sm" fullWidth PaperProps={{ sx: { backgroundColor: colors.paperBackground } }}>
        <DialogTitle sx={{ color: colors.textPrimary, borderBottom: `1px solid ${colors.borderColor}` }}>
          Registrar Atividade Realizada
        </DialogTitle>
        <DialogContent sx={{ pt: '20px !important' }}>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          
          {planToLog && (
            <Box sx={{ mb: 2, p: 1.5, backgroundColor: '#f7f7f7', borderRadius: 1, border: `1px solid ${colors.borderColor}`}}>
              <Typography variant="subtitle1" sx={{fontWeight: '500', color: colors.textPrimary}}>Plano: {planToLog.nome_atividade || 'N/A'}</Typography>
              <Typography variant="body2" sx={{color: colors.textSecondary}}>Duração Planejada: {planToLog.duracao_minutos || 'N/A'} min</Typography>
            </Box>
          )}

          <Grid container spacing={3}>
            <Grid item xs={12}>
              <DateTimePicker
                label="Data e Hora de Início *"
                value={formData.data_hora_inicio}
                onChange={handleDateTimeChange}
                ampm={false} // Formato 24h
                renderInput={(params) => <TextField {...params} fullWidth margin="dense" variant="outlined" error={!!error && !formData.data_hora_inicio} />}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                margin="dense"
                name="duracao_realizada_minutos"
                label="Duração Realizada (minutos) *"
                type="number"
                fullWidth
                variant="outlined"
                value={formData.duracao_realizada_minutos}
                onChange={handleChange}
                InputProps={{ inputProps: { min: 1 }, startAdornment: <AccessTimeIcon sx={{mr:1, color: colors.textSecondary}}/> }}
                error={!!error && !formData.duracao_realizada_minutos}
              />
            </Grid>

            <Grid item xs={12}>
                <Typography gutterBottom sx={{color: colors.textSecondary, mt:1}}>Esforço Percebido</Typography>
                <Slider
                    name="esforco_percebido"
                    value={formData.esforco_percebido}
                    onChange={handleSliderChange}
                    aria-labelledby="effort-slider"
                    valueLabelDisplay="auto"
                    step={5}
                    marks={effortMarks}
                    min={0}
                    max={100}
                    sx={{color: colors.primaryAction}}
                />
            </Grid>

            <Grid item xs={12}>
                <Typography component="legend" sx={{color: colors.textSecondary, mb: 0.5}}>Nível de Satisfação</Typography>
                <Box sx={{display: 'flex', alignItems: 'center'}}>
                    <Rating
                        name="satisfacao"
                        value={formData.satisfacao}
                        onChange={handleRatingChange}
                        IconContainerComponent={IconContainer}
                        getLabelText={(value) => satisfactionIcons[value].label}
                        highlightSelectedOnly
                        sx={{mr: 2}}
                    />
                    {formData.satisfacao !== null && (
                        <Typography variant="caption">{satisfactionIcons[formData.satisfacao]?.label}</Typography>
                    )}
                </Box>
            </Grid>

            <Grid item xs={12}>
              <TextField
                margin="dense"
                name="observacoes"
                label="Observações (Opcional)"
                type="text"
                fullWidth
                multiline
                rows={3}
                variant="outlined"
                value={formData.observacoes}
                onChange={handleChange}
                InputProps={{ startAdornment: <NotesIcon sx={{mr:1, color: colors.textSecondary, alignSelf: 'flex-start'}}/> }}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions sx={{ borderTop: `1px solid ${colors.borderColor}`, p: '16px 24px' }}>
          <Button onClick={handleCloseModal} disabled={loading} variant="outlined" sx={{ color: colors.textSecondary, borderColor: colors.textSecondary, '&:hover': { backgroundColor: 'rgba(0,0,0,0.04)', borderColor: colors.textPrimary}}}>Cancelar</Button>
          <Button onClick={handleSave} variant="contained" disabled={loading || !formData.data_hora_inicio || !formData.duracao_realizada_minutos} sx={{ backgroundColor: colors.primaryAction, '&:hover': { backgroundColor: colors.primaryActionHover } }}>
            {loading ? <CircularProgress size={24} color="inherit" /> : 'Registrar Atividade'}
          </Button>
        </DialogActions>
      </Dialog>
    </LocalizationProvider>
  );
};

export default LogActivityFormModal; 