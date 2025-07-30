import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Container,
  Grid,
  Paper,
  TextField,
  Button,
  Avatar,
  Divider,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  CardActions,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Cancel';
import PersonIcon from '@mui/icons-material/Person';
import EmailIcon from '@mui/icons-material/Email';
import PhoneIcon from '@mui/icons-material/Phone';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import PetsIcon from '@mui/icons-material/Pets';
import SecurityIcon from '@mui/icons-material/Security';
import NotificationsIcon from '@mui/icons-material/Notifications';
import { useClientAuth } from '../contexts/ClientAuthContext';

const ClientProfilePage = () => {
  const { isAuthenticated, loading: authLoading } = useClientAuth();
  
  // Estados para dados do perfil (mockup)
  const [profile, setProfile] = useState({
    name: 'João Silva',
    email: 'joao.silva@email.com',
    phone: '(11) 99999-9999',
    address: 'Rua das Flores, 123',
    city: 'São Paulo',
    state: 'SP',
    cep: '01234-567',
    birth_date: '1985-06-15',
    cpf: '123.456.789-00',
    emergency_contact: 'Maria Silva - (11) 88888-8888'
  });
  
  const [editMode, setEditMode] = useState(false);
  const [editedProfile, setEditedProfile] = useState({...profile});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [changePasswordDialog, setChangePasswordDialog] = useState(false);
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  // Configurações de notificação (mockup)
  const [notifications, setNotifications] = useState({
    email_appointments: true,
    email_reminders: true,
    sms_appointments: false,
    sms_reminders: true
  });

  // Função para buscar dados do perfil (mockup)
  const fetchProfile = async () => {
    if (!isAuthenticated) return;
    
    try {
      setLoading(true);
      setError(null);

      // Simular carregamento
      await new Promise(resolve => setTimeout(resolve, 800));

      // Dados já estão mockados no estado inicial
      
    } catch (err) {
      console.error('Erro ao buscar perfil:', err);
      setError('Erro ao carregar dados do perfil. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  // Função para salvar alterações do perfil (mockup)
  const handleSaveProfile = async () => {
    try {
      setLoading(true);
      setError(null);

      // Simular salvamento
      await new Promise(resolve => setTimeout(resolve, 1000));

      setProfile({...editedProfile});
      setEditMode(false);
      setSuccess(true);
      
      // Limpar mensagem de sucesso após 3 segundos
      setTimeout(() => setSuccess(false), 3000);

    } catch (err) {
      console.error('Erro ao salvar perfil:', err);
      setError('Erro ao salvar alterações. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  // Função para alterar senha (mockup)
  const handleChangePassword = async () => {
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setError('As senhas não coincidem.');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // Simular alteração de senha
      await new Promise(resolve => setTimeout(resolve, 1000));

      setChangePasswordDialog(false);
      setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
      setSuccess(true);
      
      setTimeout(() => setSuccess(false), 3000);

    } catch (err) {
      console.error('Erro ao alterar senha:', err);
      setError('Erro ao alterar senha. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  // Buscar dados quando a autenticação estiver pronta
  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      fetchProfile();
    }
  }, [isAuthenticated, authLoading]);

  // Função para cancelar edição
  const handleCancelEdit = () => {
    setEditedProfile({...profile});
    setEditMode(false);
    setError(null);
  };

  // Função para atualizar campo editado
  const handleFieldChange = (field, value) => {
    setEditedProfile(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Estados de carregamento e erro
  if (authLoading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <CircularProgress />
        <Typography sx={{ ml: 2 }}>Carregando...</Typography>
      </Container>
    );
  }

  if (!isAuthenticated) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="warning">Você precisa estar logado para acessar o perfil.</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h4" fontWeight="bold">Meu Perfil</Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
            Gerencie suas informações pessoais e configurações
          </Typography>
        </Box>
        {!editMode && (
          <Button
            variant="contained"
            startIcon={<EditIcon />}
            onClick={() => setEditMode(true)}
            disabled={loading}
          >
            Editar Perfil
          </Button>
        )}
      </Box>

      {/* Alertas */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}
      
      {success && (
        <Alert severity="success" sx={{ mb: 3 }} onClose={() => setSuccess(false)}>
          Informações atualizadas com sucesso!
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Informações Pessoais */}
        <Grid item xs={12} md={8}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
              <PersonIcon sx={{ mr: 1, color: '#23e865' }} />
              <Typography variant="h6" fontWeight="bold">Informações Pessoais</Typography>
            </Box>

            <Grid container spacing={3}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Nome Completo"
                  value={editMode ? editedProfile.name : profile.name}
                  onChange={(e) => handleFieldChange('name', e.target.value)}
                  disabled={!editMode || loading}
                  variant="outlined"
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="CPF"
                  value={editMode ? editedProfile.cpf : profile.cpf}
                  onChange={(e) => handleFieldChange('cpf', e.target.value)}
                  disabled={!editMode || loading}
                  variant="outlined"
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Email"
                  type="email"
                  value={editMode ? editedProfile.email : profile.email}
                  onChange={(e) => handleFieldChange('email', e.target.value)}
                  disabled={!editMode || loading}
                  variant="outlined"
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Telefone"
                  value={editMode ? editedProfile.phone : profile.phone}
                  onChange={(e) => handleFieldChange('phone', e.target.value)}
                  disabled={!editMode || loading}
                  variant="outlined"
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Data de Nascimento"
                  type="date"
                  value={editMode ? editedProfile.birth_date : profile.birth_date}
                  onChange={(e) => handleFieldChange('birth_date', e.target.value)}
                  disabled={!editMode || loading}
                  variant="outlined"
                  InputLabelProps={{ shrink: true }}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Contato de Emergência"
                  value={editMode ? editedProfile.emergency_contact : profile.emergency_contact}
                  onChange={(e) => handleFieldChange('emergency_contact', e.target.value)}
                  disabled={!editMode || loading}
                  variant="outlined"
                />
              </Grid>
            </Grid>

            <Divider sx={{ my: 3 }} />

            {/* Endereço */}
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
              <LocationOnIcon sx={{ mr: 1, color: '#23e865' }} />
              <Typography variant="h6" fontWeight="bold">Endereço</Typography>
            </Box>

            <Grid container spacing={3}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Endereço"
                  value={editMode ? editedProfile.address : profile.address}
                  onChange={(e) => handleFieldChange('address', e.target.value)}
                  disabled={!editMode || loading}
                  variant="outlined"
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Cidade"
                  value={editMode ? editedProfile.city : profile.city}
                  onChange={(e) => handleFieldChange('city', e.target.value)}
                  disabled={!editMode || loading}
                  variant="outlined"
                />
              </Grid>

              <Grid item xs={12} sm={3}>
                <TextField
                  fullWidth
                  label="Estado"
                  value={editMode ? editedProfile.state : profile.state}
                  onChange={(e) => handleFieldChange('state', e.target.value)}
                  disabled={!editMode || loading}
                  variant="outlined"
                />
              </Grid>

              <Grid item xs={12} sm={3}>
                <TextField
                  fullWidth
                  label="CEP"
                  value={editMode ? editedProfile.cep : profile.cep}
                  onChange={(e) => handleFieldChange('cep', e.target.value)}
                  disabled={!editMode || loading}
                  variant="outlined"
                />
              </Grid>
            </Grid>

            {/* Botões de Ação */}
            {editMode && (
              <Box sx={{ display: 'flex', gap: 2, mt: 3, justifyContent: 'flex-end' }}>
                <Button
                  variant="outlined"
                  startIcon={<CancelIcon />}
                  onClick={handleCancelEdit}
                  disabled={loading}
                >
                  Cancelar
                </Button>
                <Button
                  variant="contained"
                  startIcon={<SaveIcon />}
                  onClick={handleSaveProfile}
                  disabled={loading}
                >
                  {loading ? <CircularProgress size={20} /> : 'Salvar'}
                </Button>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Sidebar */}
        <Grid item xs={12} md={4}>
          {/* Avatar e Resumo */}
          <Paper elevation={2} sx={{ p: 3, mb: 3, textAlign: 'center' }}>
            <Avatar
              sx={{ 
                width: 80, 
                height: 80, 
                mx: 'auto', 
                mb: 2, 
                bgcolor: '#23e865',
                fontSize: '2rem'
              }}
            >
              {profile.name.charAt(0).toUpperCase()}
            </Avatar>
            <Typography variant="h6" fontWeight="bold">{profile.name}</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              {profile.email}
            </Typography>
            <Chip 
              label="Tutor Ativo" 
              color="success" 
              size="small"
              icon={<PetsIcon />}
            />
          </Paper>

          {/* Segurança */}
          <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <SecurityIcon sx={{ mr: 1, color: '#23e865' }} />
              <Typography variant="h6" fontWeight="bold">Segurança</Typography>
            </Box>
            <Button
              fullWidth
              variant="outlined"
              onClick={() => setChangePasswordDialog(true)}
              disabled={loading}
            >
              Alterar Senha
            </Button>
          </Paper>

          {/* Configurações de Notificação */}
          <Paper elevation={2} sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <NotificationsIcon sx={{ mr: 1, color: '#23e865' }} />
              <Typography variant="h6" fontWeight="bold">Notificações</Typography>
            </Box>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Configure como deseja receber notificações sobre seus pets
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <Chip 
                label="Email: Agendamentos" 
                color={notifications.email_appointments ? "primary" : "default"}
                size="small"
              />
              <Chip 
                label="Email: Lembretes" 
                color={notifications.email_reminders ? "primary" : "default"}
                size="small"
              />
              <Chip 
                label="SMS: Agendamentos" 
                color={notifications.sms_appointments ? "primary" : "default"}
                size="small"
              />
              <Chip 
                label="SMS: Lembretes" 
                color={notifications.sms_reminders ? "primary" : "default"}
                size="small"
              />
            </Box>
            <Button
              fullWidth
              variant="outlined"
              size="small"
              sx={{ mt: 2 }}
              disabled
            >
              Configurar (Em Breve)
            </Button>
          </Paper>
        </Grid>
      </Grid>

      {/* Dialog para Alterar Senha */}
      <Dialog 
        open={changePasswordDialog} 
        onClose={() => setChangePasswordDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Alterar Senha</DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <TextField
              fullWidth
              label="Senha Atual"
              type="password"
              value={passwordData.currentPassword}
              onChange={(e) => setPasswordData(prev => ({...prev, currentPassword: e.target.value}))}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Nova Senha"
              type="password"
              value={passwordData.newPassword}
              onChange={(e) => setPasswordData(prev => ({...prev, newPassword: e.target.value}))}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Confirmar Nova Senha"
              type="password"
              value={passwordData.confirmPassword}
              onChange={(e) => setPasswordData(prev => ({...prev, confirmPassword: e.target.value}))}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setChangePasswordDialog(false)}>
            Cancelar
          </Button>
          <Button 
            onClick={handleChangePassword}
            variant="contained"
            disabled={loading || !passwordData.currentPassword || !passwordData.newPassword || !passwordData.confirmPassword}
          >
            {loading ? <CircularProgress size={20} /> : 'Alterar Senha'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default ClientProfilePage;