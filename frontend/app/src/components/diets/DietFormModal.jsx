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
  DialogContentText
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
// Certifique-se de que o caminho para AdapterDateFns está correto para sua versão do MUI X Date Pickers
// Se estiver usando v5 ou anterior: import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
// Se estiver usando v6/v7+: import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFnsV3'; ou similar
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'; // Ajuste se necessário
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { ptBR } from 'date-fns/locale';
import dietService from '../../services/dietService';

// Paleta de cores para consistência
const colors = {
  primaryAction: '#9DB8B2',
  primaryActionHover: '#82a8a0',
  paperBackground: '#FFFFFF',
  textPrimary: '#333',
};

const DietFormModal = ({ open, onClose, animalId, dietData, isEditing, onSaveSuccess, onDietCreated }) => {
  const [formData, setFormData] = useState({
    tipo: '',
    objetivo: '',
    observacoes: '',
    data_inicio: null,
    data_fim: null,
    status: 'ativa',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showAddOptionDialog, setShowAddOptionDialog] = useState(false);
  const [createdDietId, setCreatedDietId] = useState(null);

  useEffect(() => {
    if (isEditing && dietData) {
      setFormData({
        tipo: dietData.tipo || '',
        objetivo: dietData.objetivo || '',
        observacoes: dietData.observacoes || '',
        data_inicio: dietData.data_inicio ? new Date(dietData.data_inicio) : null,
        data_fim: dietData.data_fim ? new Date(dietData.data_fim) : null,
        status: dietData.status || 'ativa',
      });
    } else {
      // Reset form para criação
      setFormData({
        tipo: '',
        objetivo: '',
        observacoes: '',
        data_inicio: new Date(), // Default para hoje
        data_fim: null,
        status: 'ativa',
      });
    }
    // Resetar erro ao abrir/mudar modo
    setError(null);
  }, [open, isEditing, dietData]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleDateChange = (name, date) => {
    setFormData(prev => ({ ...prev, [name]: date }));
  };

  const validateForm = () => {
    if (!formData.tipo || !formData.objetivo || !formData.data_inicio || !formData.status) {
      setError('Os campos Tipo, Objetivo, Data de Início e Status são obrigatórios.');
      return false;
    }
     if (formData.data_fim && formData.data_inicio && formData.data_fim < formData.data_inicio) {
      setError('A Data de Fim não pode ser anterior à Data de Início.');
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

    // Formatar datas para ISO string antes de enviar, se não forem nulas
    const dataToSend = {
      ...formData,
      data_inicio: formData.data_inicio ? formData.data_inicio.toISOString().split('T')[0] : null, // Enviar apenas YYYY-MM-DD
      data_fim: formData.data_fim ? formData.data_fim.toISOString().split('T')[0] : null, // Enviar apenas YYYY-MM-DD
    };

    try {
      if (isEditing && dietData?.id) {
        await dietService.updateDiet(dietData.id, dataToSend);
        onSaveSuccess(); // Chama a função de callback do pai
        handleCloseModal(); // Fecha o modal
      } else {
        if (!animalId) {
            setError("ID do animal não fornecido para criar a dieta.");
            setLoading(false);
            return;
        }
        const createdDiet = await dietService.createDiet(animalId, dataToSend);
        setCreatedDietId(createdDiet.id);
        setShowAddOptionDialog(true); // Mostrar diálogo para adicionar opção
      }
    } catch (err) {
      console.error("Erro ao salvar dieta:", err);
      setError(err.detail || err.message || 'Erro desconhecido ao salvar dieta.');
    } finally {
      setLoading(false);
    }
  };

  const handleCloseModal = () => { // Renomeado para evitar conflito de escopo com onClose prop
    if (loading) return; // Não fechar se estiver carregando
    setError(null);
    setShowAddOptionDialog(false);
    setCreatedDietId(null);
    onClose(); // Chama a função onClose passada pelo pai
  };

  const handleAddOptionYes = () => {
    setShowAddOptionDialog(false);
    onSaveSuccess(); // Atualizar a lista de dietas
    handleCloseModal(); // Fechar o modal de criação
    // Chamar callback para abrir modal de opção se fornecido
    if (onDietCreated && createdDietId) {
      onDietCreated(createdDietId);
    }
  };

  const handleAddOptionNo = () => {
    setShowAddOptionDialog(false);
    onSaveSuccess(); // Atualizar a lista de dietas
    handleCloseModal(); // Fechar o modal
  };


  // Opções para os Selects (poderiam vir de constantes ou API no futuro)
  const dietTypes = ['Caseira', 'Industrializada', 'Mista'];
  const dietObjectives = ['Emagrecimento', 'Manutenção de Peso', 'Ganho de Peso', 'Recuperação', 'Alergia Alimentar', 'Outro'];
  const dietStatus = ['Ativa', 'Pausada', 'Finalizada'];

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ptBR}>
      {/* Modal principal de criação/edição */}
      <Dialog open={open && !showAddOptionDialog} onClose={handleCloseModal} maxWidth="sm" fullWidth PaperProps={{ component: 'form', onSubmit: handleSubmit }}>
        <DialogTitle sx={{ backgroundColor: '#23e865', color: colors.paperBackground }}>
          {isEditing ? 'Editar Plano de Dieta' : 'Novo Plano de Dieta'}
        </DialogTitle>
        <DialogContent sx={{ pt: 3 }}>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth sx={{ marginTop: '1rem', minWidth: 200 }} required>
                <InputLabel id="tipo-dieta-label">Tipo</InputLabel>
                <Select
                  labelId="tipo-dieta-label"
                  id="tipo"
                  name="tipo"
                  value={formData.tipo}
                  label="Tipo"
                  onChange={handleChange}
                >
                  {dietTypes.map((type) => (
                    <MenuItem key={type} value={type.toLowerCase()}>{type}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth required sx={{ marginTop: '1rem', minWidth: 200 }}>
                <InputLabel id="objetivo-dieta-label">Objetivo</InputLabel>
                <Select
                  labelId="objetivo-dieta-label"
                  id="objetivo"
                  name="objetivo"
                  value={formData.objetivo}
                  label="Objetivo"
                  onChange={handleChange}
                >
                  {dietObjectives.map((obj) => (
                    <MenuItem key={obj} value={obj.toLowerCase()}>{obj}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12}>
              <TextField
                margin="dense"
                id="observacoes"
                name="observacoes"
                label="Nome do Alimento"
                type="text"
                fullWidth
                multiline
                rows={2}
                variant="outlined"
                value={formData.observacoes}
                onChange={handleChange}
              />
            </Grid>

            <Grid item xs={12} sm={4}>
              <DatePicker
                label="Data de Início *"
                value={formData.data_inicio}
                onChange={(date) => handleDateChange('data_inicio', date)}
                renderInput={(params) => <TextField {...params} fullWidth required />}
                format="dd/MM/yyyy"
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <DatePicker
                label="Data de Fim (Opcional)"
                value={formData.data_fim}
                onChange={(date) => handleDateChange('data_fim', date)}
                renderInput={(params) => <TextField {...params} fullWidth />}
                format="dd/MM/yyyy"
                minDate={formData.data_inicio || undefined}
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth required>
                <InputLabel id="status-dieta-label">Status</InputLabel>
                <Select
                  labelId="status-dieta-label"
                  id="status"
                  name="status"
                  value={formData.status}
                  label="Status"
                  onChange={handleChange}
                >
                  {dietStatus.map((stat) => (
                    <MenuItem key={stat} value={stat.toLowerCase()}>{stat}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </DialogContent>

        <DialogActions sx={{ p: '16px 24px' }}>
          <Button onClick={handleCloseModal} color="secondary" disabled={loading}>
            Cancelar
          </Button>
          <Button
            type="submit"
            variant="contained"
            disabled={loading}
            sx={{
              backgroundColor: '#23e865',
              '&:hover': { backgroundColor: '#209e41' },
              minWidth: '100px', // Largura mínima para o botão
            }}
          >
            {loading ? <CircularProgress size={24} color="inherit" /> : (isEditing ? 'Salvar Alterações' : 'Criar Dieta')}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Diálogo de confirmação para adicionar opção */}
      <Dialog open={showAddOptionDialog} onClose={() => {}} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ backgroundColor: colors.primaryAction, color: colors.paperBackground }}>
          Dieta Criada com Sucesso! 🎉
        </DialogTitle>
        <DialogContent sx={{ pt: 3 }}>
          <DialogContentText sx={{ mb: 2, fontSize: '1rem' }}>
            Sua dieta foi criada com sucesso! Agora você pode adicionar opções específicas com detalhes como:
          </DialogContentText>
          <Box component="ul" sx={{ pl: 2, mb: 2 }}>
            <li>Porções por refeição</li>
            <li>Número de refeições por dia</li>
            <li>Calorias totais diárias</li>
            <li>Valor mensal estimado</li>
            <li>Indicações específicas</li>
          </Box>
          <DialogContentText sx={{ fontWeight: '500' }}>
            Deseja adicionar uma opção de dieta agora?
          </DialogContentText>
        </DialogContent>
        <DialogActions sx={{ p: '16px 24px' }}>
          <Button onClick={handleAddOptionNo} color="secondary">
            Não, adicionar depois
          </Button>
          <Button
            onClick={handleAddOptionYes}
            variant="contained"
            sx={{
              backgroundColor: colors.primaryAction,
              '&:hover': { backgroundColor: colors.primaryActionHover }
            }}
          >
            Sim, adicionar opção
          </Button>
        </DialogActions>
      </Dialog>
    </LocalizationProvider>
  );
};

export default DietFormModal; 