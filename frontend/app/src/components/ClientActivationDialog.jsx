import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Grid,
  Alert,
  Typography,
  Box,
  Switch,
  FormControlLabel,
  Divider,
  Paper,
  CircularProgress
} from '@mui/material';
import {
  PersonAdd as PersonAddIcon,
  Key as KeyIcon,
  Email as EmailIcon
} from '@mui/icons-material';
import { animalService } from '../services/animalService';

const ClientActivationDialog = ({ open, onClose, animal, onSuccess }) => {
  const [formData, setFormData] = useState({
    tutor_name: animal?.tutor_name || '',
    email: animal?.email || '',
    phone: animal?.phone || '',
    generate_password: true
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activationResult, setActivationResult] = useState(null);

  const handleInputChange = (field) => (event) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.value
    }));
    setError('');
  };

  const handleSwitchChange = (field) => (event) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.checked
    }));
  };

  const validateForm = () => {
    if (!formData.tutor_name.trim()) {
      setError('Nome do tutor é obrigatório');
      return false;
    }
    if (!formData.email.trim()) {
      setError('Email é obrigatório');
      return false;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      setError('Email inválido');
      return false;
    }
    if (!formData.phone.trim()) {
      setError('Telefone é obrigatório');
      return false;
    }
    return true;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    setLoading(true);
    setError('');

    try {
      const result = await animalService.activateClientAccess(animal.id, formData);
      setActivationResult(result);
      
      // Se não gerou senha, pode fechar imediatamente
      if (!result.temporary_password) {
        setTimeout(() => {
          onSuccess();
        }, 1500);
      }
    } catch (err) {
      setError(err.message || 'Erro ao ativar cliente');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    if (activationResult && !activationResult.temporary_password) {
      onSuccess();
    } else {
      onClose();
    }
  };

  const resetForm = () => {
    setFormData({
      tutor_name: animal?.tutor_name || '',
      email: animal?.email || '',
      phone: animal?.phone || '',
      generate_password: true
    });
    setError('');
    setActivationResult(null);
  };

  React.useEffect(() => {
    if (open) {
      resetForm();
    }
  }, [open, animal]);

  if (activationResult) {
    return (
      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ textAlign: 'center', pb: 1 }}>
          <PersonAddIcon sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
          <Typography variant="h5" component="div">
            Cliente Ativado com Sucesso!
          </Typography>
        </DialogTitle>
        <DialogContent>
          <Box sx={{ textAlign: 'center', mb: 3 }}>
            <Alert severity="success" sx={{ mb: 2 }}>
              {activationResult.message}
            </Alert>
            
            {activationResult.temporary_password && (
              <Paper sx={{ p: 2, bgcolor: 'grey.50', border: '1px dashed', borderColor: 'grey.300' }}>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <KeyIcon sx={{ mr: 1 }} />
                  Senha Temporária
                </Typography>
                <Typography 
                  variant="h4" 
                  sx={{ 
                    fontFamily: 'monospace', 
                    fontWeight: 'bold', 
                    color: 'primary.main',
                    letterSpacing: 2,
                    mb: 2
                  }}
                >
                  {activationResult.temporary_password}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Compartilhe esta senha com o tutor. Ela deve ser alterada no primeiro acesso.
                </Typography>
              </Paper>
            )}

            <Box sx={{ mt: 2 }}>
              <Typography variant="body1" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 1 }}>
                <EmailIcon sx={{ mr: 1 }} />
                Email: {formData.email}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                O tutor pode acessar o sistema através da área do cliente
              </Typography>
            </Box>
          </Box>
        </DialogContent>
        <DialogActions sx={{ justifyContent: 'center', pb: 3 }}>
          <Button 
            onClick={handleClose} 
            variant="contained" 
            size="large"
            sx={{ minWidth: 120 }}
          >
            Fechar
          </Button>
        </DialogActions>
      </Dialog>
    );
  }

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <PersonAddIcon sx={{ mr: 1, color: 'primary.main' }} />
          Ativar Acesso do Cliente
        </Box>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          Animal: {animal?.name} ({animal?.species})
        </Typography>
      </DialogTitle>
      
      <DialogContent>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Nome do Tutor"
              value={formData.tutor_name}
              onChange={handleInputChange('tutor_name')}
              required
              disabled={loading}
              variant="outlined"
            />
          </Grid>
          
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Email"
              type="email"
              value={formData.email}
              onChange={handleInputChange('email')}
              required
              disabled={loading}
              variant="outlined"
              helperText="Este será o login do tutor no sistema"
            />
          </Grid>
          
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Telefone"
              value={formData.phone}
              onChange={handleInputChange('phone')}
              required
              disabled={loading}
              variant="outlined"
              placeholder="(11) 99999-9999"
            />
          </Grid>

          <Grid item xs={12}>
            <Divider sx={{ my: 1 }} />
            <FormControlLabel
              control={
                <Switch
                  checked={formData.generate_password}
                  onChange={handleSwitchChange('generate_password')}
                  disabled={loading}
                  color="primary"
                />
              }
              label={
                <Box>
                  <Typography variant="body1">Gerar senha temporária</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Uma senha será gerada automaticamente para o primeiro acesso
                  </Typography>
                </Box>
              }
            />
          </Grid>
        </Grid>

        <Box sx={{ mt: 2 }}>
          <Alert severity="info">
            <Typography variant="body2">
              Após a ativação, o tutor poderá acessar o sistema para acompanhar 
              a saúde do pet, visualizar dietas, atividades e histórico de consultas.
            </Typography>
          </Alert>
        </Box>
      </DialogContent>
      
      <DialogActions sx={{ p: 2 }}>
        <Button 
          onClick={onClose} 
          disabled={loading}
          color="inherit"
        >
          Cancelar
        </Button>
        <Button 
          onClick={handleSubmit} 
          variant="contained" 
          disabled={loading}
          startIcon={loading ? <CircularProgress size={20} /> : <PersonAddIcon />}
        >
          {loading ? 'Ativando...' : 'Ativar Cliente'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ClientActivationDialog;