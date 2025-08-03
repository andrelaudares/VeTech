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
  DialogActions,
  MenuItem,
  FormControl,
  InputLabel,
  Select
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Cancel';
import PersonIcon from '@mui/icons-material/Person';
import EmailIcon from '@mui/icons-material/Email';
import PhoneIcon from '@mui/icons-material/Phone';
import PetsIcon from '@mui/icons-material/Pets';
import SecurityIcon from '@mui/icons-material/Security';
import NotificationsIcon from '@mui/icons-material/Notifications';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import ScaleIcon from '@mui/icons-material/Scale';
import MedicalServicesIcon from '@mui/icons-material/MedicalServices';
import { useClientAuth } from '../contexts/ClientAuthContext';
import { clientAnimalService } from '../services/clientAnimalService';

const ClientProfilePage = () => {
  const { client, isAuthenticated, token } = useClientAuth();
  
  // Estados para dados do animal/tutor
  const [animalData, setAnimalData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Estados para edição
  const [editingTutor, setEditingTutor] = useState(false);
  const [editingAnimal, setEditingAnimal] = useState(false);
  const [saving, setSaving] = useState(false);
  
  // Estados para formulários
  const [tutorForm, setTutorForm] = useState({
    tutor_name: '',
    phone: '',
    email: ''
  });
  
  const [animalForm, setAnimalForm] = useState({
    name: '',
    species: '',
    breed: '',
    age: '',
    weight: '',
    date_birth: '',
    medical_history: ''
  });
  
  // Estados para mudança de senha
  const [passwordDialog, setPasswordDialog] = useState(false);
  const [passwordForm, setPasswordForm] = useState({
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

  // Carregar dados do animal ao montar o componente
  useEffect(() => {
    loadAnimalData();
  }, []);

  const loadAnimalData = async () => {
    try {
      setLoading(true);
      setError('');
      
      const data = await clientAnimalService.getMyAnimal();
      setAnimalData(data);
      
      // Preencher formulários com dados atuais
      setTutorForm({
        tutor_name: data.tutor_name || '',
        phone: data.phone || '',
        email: data.email || ''
      });
      
      setAnimalForm({
        name: data.name || '',
        species: data.species || '',
        breed: data.breed || '',
        age: data.age?.toString() || '',
        weight: data.weight?.toString() || '',
        date_birth: data.date_birth ? data.date_birth.split('T')[0] : '',
        medical_history: data.medical_history || ''
      });
      
    } catch (err) {
      console.error('Erro ao carregar dados:', err);
      setError('Erro ao carregar dados do perfil. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleTutorSave = async () => {
    try {
      setSaving(true);
      setError('');
      
      // Enviar apenas os campos que podem ser alterados
      const updateData = {
        tutor_name: tutorForm.tutor_name,
        phone: tutorForm.phone
        // email não pode ser alterado, então não enviamos
      };
      
      await clientAnimalService.updateMyAnimal(updateData);
      
      setSuccess('Dados do tutor atualizados com sucesso!');
      setEditingTutor(false);
      await loadAnimalData(); // Recarregar dados
      
    } catch (err) {
      console.error('Erro ao salvar dados do tutor:', err);
      setError('Erro ao salvar dados do tutor. Tente novamente.');
    } finally {
      setSaving(false);
    }
  };

  const handleAnimalSave = async () => {
    try {
      setSaving(true);
      setError('');
      
      const updateData = {
        name: animalForm.name,
        species: animalForm.species,
        breed: animalForm.breed,
        age: animalForm.age ? parseInt(animalForm.age) : null,
        weight: animalForm.weight ? parseFloat(animalForm.weight) : null,
        date_birth: animalForm.date_birth || null,
        medical_history: animalForm.medical_history
      };
      
      await clientAnimalService.updateMyAnimal(updateData);
      
      setSuccess('Dados do animal atualizados com sucesso!');
      setEditingAnimal(false);
      await loadAnimalData(); // Recarregar dados
      
    } catch (err) {
      console.error('Erro ao salvar dados do animal:', err);
      setError('Erro ao salvar dados do animal. Tente novamente.');
    } finally {
      setSaving(false);
    }
  };

  const handlePasswordChange = async () => {
    try {
      if (passwordForm.newPassword !== passwordForm.confirmPassword) {
        setError('As senhas não coincidem.');
        return;
      }
      
      if (passwordForm.newPassword.length < 6) {
        setError('A nova senha deve ter pelo menos 6 caracteres.');
        return;
      }
      
      setSaving(true);
      setError('');
      
      await clientAnimalService.changePassword(
        passwordForm.currentPassword,
        passwordForm.newPassword
      );
      
      setSuccess('Senha alterada com sucesso!');
      setPasswordDialog(false);
      setPasswordForm({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
      
    } catch (err) {
      console.error('Erro ao alterar senha:', err);
      setError('Erro ao alterar senha. Verifique a senha atual.');
    } finally {
      setSaving(false);
    }
  };

  const handleCancelEdit = (type) => {
    if (type === 'tutor') {
      setEditingTutor(false);
      // Restaurar dados originais
      if (animalData) {
        setTutorForm({
          tutor_name: animalData.tutor_name || '',
          phone: animalData.phone || '',
          email: animalData.email || ''
        });
      }
    } else if (type === 'animal') {
      setEditingAnimal(false);
      // Restaurar dados originais
      if (animalData) {
        setAnimalForm({
          name: animalData.name || '',
          species: animalData.species || '',
          breed: animalData.breed || '',
          age: animalData.age?.toString() || '',
          weight: animalData.weight?.toString() || '',
          date_birth: animalData.date_birth ? animalData.date_birth.split('T')[0] : '',
          medical_history: animalData.medical_history || ''
        });
      }
    }
  };

  // Limpar mensagens após 5 segundos
  useEffect(() => {
    if (success || error) {
      const timer = setTimeout(() => {
        setSuccess('');
        setError('');
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [success, error]);

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress size={60} />
        </Box>
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
      {/* Cabeçalho da página */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Meu Perfil
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Gerencie suas informações pessoais e dados do seu pet
        </Typography>
      </Box>

      {/* Alertas de sucesso e erro */}
      {success && (
        <Alert severity="success" sx={{ mb: 3 }}>
          {success}
        </Alert>
      )}
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Card de Dados do Tutor */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                <Box display="flex" alignItems="center">
                  <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                    <PersonIcon />
                  </Avatar>
                  <Typography variant="h6">Dados do Tutor</Typography>
                </Box>
                {!editingTutor && (
                  <IconButton 
                    onClick={() => setEditingTutor(true)}
                    color="primary"
                  >
                    <EditIcon />
                  </IconButton>
                )}
              </Box>

              <Divider sx={{ mb: 2 }} />

              {editingTutor ? (
                <Box 
                  component="form" 
                  noValidate
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleTutorSave();
                  }}
                >
                  <TextField
                    fullWidth
                    label="Nome"
                    value={tutorForm.tutor_name}
                    onChange={(e) => setTutorForm(prev => ({ ...prev, tutor_name: e.target.value }))}
                    margin="normal"
                    InputProps={{
                      startAdornment: <PersonIcon sx={{ mr: 1, color: 'text.secondary' }} />
                    }}
                  />
                  
                  <TextField
                    fullWidth
                    label="Telefone"
                    value={tutorForm.phone}
                    onChange={(e) => setTutorForm(prev => ({ ...prev, phone: e.target.value }))}
                    margin="normal"
                    InputProps={{
                      startAdornment: <PhoneIcon sx={{ mr: 1, color: 'text.secondary' }} />
                    }}
                  />
                  
                  <TextField
                    fullWidth
                    label="E-mail"
                    value={tutorForm.email}
                    disabled
                    margin="normal"
                    helperText="O e-mail não pode ser alterado"
                    InputProps={{
                      startAdornment: <EmailIcon sx={{ mr: 1, color: 'text.secondary' }} />
                    }}
                  />
                </Box>
              ) : (
                <Box>
                  <Box display="flex" alignItems="center" mb={2}>
                    <PersonIcon sx={{ mr: 1, color: 'text.secondary' }} />
                    <Box>
                      <Typography variant="body2" color="text.secondary">Nome</Typography>
                      <Typography variant="body1">{animalData?.tutor_name || 'Não informado'}</Typography>
                    </Box>
                  </Box>
                  
                  <Box display="flex" alignItems="center" mb={2}>
                    <PhoneIcon sx={{ mr: 1, color: 'text.secondary' }} />
                    <Box>
                      <Typography variant="body2" color="text.secondary">Telefone</Typography>
                      <Typography variant="body1">{animalData?.phone || 'Não informado'}</Typography>
                    </Box>
                  </Box>
                  
                  <Box display="flex" alignItems="center" mb={2}>
                    <EmailIcon sx={{ mr: 1, color: 'text.secondary' }} />
                    <Box>
                      <Typography variant="body2" color="text.secondary">E-mail</Typography>
                      <Typography variant="body1">{animalData?.email || 'Não informado'}</Typography>
                    </Box>
                  </Box>
                </Box>
              )}
            </CardContent>

            {editingTutor && (
              <CardActions>
                <Button
                  onClick={handleTutorSave}
                  variant="contained"
                  startIcon={<SaveIcon />}
                  disabled={saving}
                >
                  {saving ? 'Salvando...' : 'Salvar'}
                </Button>
                <Button
                  onClick={() => handleCancelEdit('tutor')}
                  startIcon={<CancelIcon />}
                  disabled={saving}
                >
                  Cancelar
                </Button>
              </CardActions>
            )}
          </Card>
        </Grid>

        {/* Card de Dados do Animal */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                <Box display="flex" alignItems="center">
                  <Avatar sx={{ bgcolor: 'secondary.main', mr: 2 }}>
                    <PetsIcon />
                  </Avatar>
                  <Typography variant="h6">Dados do Pet</Typography>
                </Box>
                {!editingAnimal && (
                  <IconButton 
                    onClick={() => setEditingAnimal(true)}
                    color="primary"
                  >
                    <EditIcon />
                  </IconButton>
                )}
              </Box>

              <Divider sx={{ mb: 2 }} />

              {editingAnimal ? (
                <Box 
                  component="form" 
                  noValidate
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleAnimalSave();
                  }}
                >
                  <TextField
                    fullWidth
                    label="Nome do Pet"
                    value={animalForm.name}
                    onChange={(e) => setAnimalForm(prev => ({ ...prev, name: e.target.value }))}
                    margin="normal"
                    InputProps={{
                      startAdornment: <PetsIcon sx={{ mr: 1, color: 'text.secondary' }} />
                    }}
                  />
                  
                  <FormControl fullWidth margin="normal">
                    <InputLabel>Espécie</InputLabel>
                    <Select
                      value={animalForm.species}
                      label="Espécie"
                      onChange={(e) => setAnimalForm(prev => ({ ...prev, species: e.target.value }))}
                    >
                      <MenuItem value="Cão">Cão</MenuItem>
                      <MenuItem value="Gato">Gato</MenuItem>
                      <MenuItem value="Pássaro">Pássaro</MenuItem>
                      <MenuItem value="Coelho">Coelho</MenuItem>
                      <MenuItem value="Hamster">Hamster</MenuItem>
                      <MenuItem value="Outro">Outro</MenuItem>
                    </Select>
                  </FormControl>
                  
                  <TextField
                    fullWidth
                    label="Raça"
                    value={animalForm.breed}
                    onChange={(e) => setAnimalForm(prev => ({ ...prev, breed: e.target.value }))}
                    margin="normal"
                  />
                  
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <TextField
                        fullWidth
                        label="Idade (anos)"
                        type="number"
                        value={animalForm.age}
                        onChange={(e) => setAnimalForm(prev => ({ ...prev, age: e.target.value }))}
                        margin="normal"
                        InputProps={{
                          startAdornment: <CalendarTodayIcon sx={{ mr: 1, color: 'text.secondary' }} />
                        }}
                      />
                    </Grid>
                    <Grid item xs={6}>
                      <TextField
                        fullWidth
                        label="Peso (kg)"
                        type="number"
                        step="0.1"
                        value={animalForm.weight}
                        onChange={(e) => setAnimalForm(prev => ({ ...prev, weight: e.target.value }))}
                        margin="normal"
                        InputProps={{
                          startAdornment: <ScaleIcon sx={{ mr: 1, color: 'text.secondary' }} />
                        }}
                      />
                    </Grid>
                  </Grid>
                  
                  <TextField
                    fullWidth
                    label="Data de Nascimento"
                    type="date"
                    value={animalForm.date_birth}
                    onChange={(e) => setAnimalForm(prev => ({ ...prev, date_birth: e.target.value }))}
                    margin="normal"
                    InputLabelProps={{
                      shrink: true,
                    }}
                  />
                  
                  <TextField
                    fullWidth
                    label="Histórico Médico"
                    multiline
                    rows={3}
                    value={animalForm.medical_history}
                    onChange={(e) => setAnimalForm(prev => ({ ...prev, medical_history: e.target.value }))}
                    margin="normal"
                    placeholder="Descreva o histórico médico do seu pet..."
                    InputProps={{
                      startAdornment: <MedicalServicesIcon sx={{ mr: 1, color: 'text.secondary', alignSelf: 'flex-start', mt: 1 }} />
                    }}
                  />
                </Box>
              ) : (
                <Box>
                  <Box display="flex" alignItems="center" mb={2}>
                    <PetsIcon sx={{ mr: 1, color: 'text.secondary' }} />
                    <Box>
                      <Typography variant="body2" color="text.secondary">Nome</Typography>
                      <Typography variant="body1">{animalData?.name || 'Não informado'}</Typography>
                    </Box>
                  </Box>
                  
                  <Box display="flex" alignItems="center" mb={2}>
                    <Box>
                      <Typography variant="body2" color="text.secondary">Espécie e Raça</Typography>
                      <Typography variant="body1">
                        {animalData?.species || 'Não informado'} 
                        {animalData?.breed && ` - ${animalData.breed}`}
                      </Typography>
                    </Box>
                  </Box>
                  
                  <Grid container spacing={2} mb={2}>
                    <Grid item xs={6}>
                      <Box display="flex" alignItems="center">
                        <CalendarTodayIcon sx={{ mr: 1, color: 'text.secondary' }} />
                        <Box>
                          <Typography variant="body2" color="text.secondary">Idade</Typography>
                          <Typography variant="body1">{animalData?.age ? `${animalData.age} anos` : 'Não informado'}</Typography>
                        </Box>
                      </Box>
                    </Grid>
                    <Grid item xs={6}>
                      <Box display="flex" alignItems="center">
                        <ScaleIcon sx={{ mr: 1, color: 'text.secondary' }} />
                        <Box>
                          <Typography variant="body2" color="text.secondary">Peso</Typography>
                          <Typography variant="body1">{animalData?.weight ? `${animalData.weight} kg` : 'Não informado'}</Typography>
                        </Box>
                      </Box>
                    </Grid>
                  </Grid>
                  
                  {animalData?.date_birth && (
                    <Box display="flex" alignItems="center" mb={2}>
                      <CalendarTodayIcon sx={{ mr: 1, color: 'text.secondary' }} />
                      <Box>
                        <Typography variant="body2" color="text.secondary">Data de Nascimento</Typography>
                        <Typography variant="body1">
                          {new Date(animalData.date_birth).toLocaleDateString('pt-BR')}
                        </Typography>
                      </Box>
                    </Box>
                  )}
                  
                  {animalData?.medical_history && (
                    <Box display="flex" alignItems="flex-start" mb={2}>
                      <MedicalServicesIcon sx={{ mr: 1, color: 'text.secondary', mt: 0.5 }} />
                      <Box>
                        <Typography variant="body2" color="text.secondary">Histórico Médico</Typography>
                        <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                          {animalData.medical_history}
                        </Typography>
                      </Box>
                    </Box>
                  )}
                </Box>
              )}
            </CardContent>

            {editingAnimal && (
              <CardActions>
                <Button
                  onClick={handleAnimalSave}
                  variant="contained"
                  startIcon={<SaveIcon />}
                  disabled={saving}
                >
                  {saving ? 'Salvando...' : 'Salvar'}
                </Button>
                <Button
                  onClick={() => handleCancelEdit('animal')}
                  startIcon={<CancelIcon />}
                  disabled={saving}
                >
                  Cancelar
                </Button>
              </CardActions>
            )}
          </Card>
        </Grid>

        {/* Card de Segurança */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Avatar sx={{ bgcolor: 'warning.main', mr: 2 }}>
                  <SecurityIcon />
                </Avatar>
                <Typography variant="h6">Segurança</Typography>
              </Box>

              <Divider sx={{ mb: 2 }} />

              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography variant="body1" gutterBottom>
                    Alterar Senha
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Mantenha sua conta segura alterando sua senha regularmente
                  </Typography>
                </Box>
                <Button
                  variant="outlined"
                  startIcon={<SecurityIcon />}
                  onClick={() => setPasswordDialog(true)}
                >
                  Alterar Senha
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Card de Gamificação (se disponível) */}
        {animalData && (animalData.gamification_level || animalData.total_points) && (
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <Avatar sx={{ bgcolor: 'success.main', mr: 2 }}>
                    <NotificationsIcon />
                  </Avatar>
                  <Typography variant="h6">Gamificação</Typography>
                </Box>

                <Divider sx={{ mb: 2 }} />

                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Box textAlign="center">
                      <Typography variant="h4" color="primary">
                        {animalData.gamification_level || 0}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Nível
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6}>
                    <Box textAlign="center">
                      <Typography variant="h4" color="secondary">
                        {animalData.total_points || 0}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Pontos Totais
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>

      {/* Dialog para alterar senha */}
      <Dialog 
        open={passwordDialog} 
        onClose={() => setPasswordDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Alterar Senha</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Senha Atual"
            type="password"
            value={passwordForm.currentPassword}
            onChange={(e) => setPasswordForm(prev => ({ ...prev, currentPassword: e.target.value }))}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Nova Senha"
            type="password"
            value={passwordForm.newPassword}
            onChange={(e) => setPasswordForm(prev => ({ ...prev, newPassword: e.target.value }))}
            margin="normal"
            helperText="Mínimo de 6 caracteres"
          />
          <TextField
            fullWidth
            label="Confirmar Nova Senha"
            type="password"
            value={passwordForm.confirmPassword}
            onChange={(e) => setPasswordForm(prev => ({ ...prev, confirmPassword: e.target.value }))}
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button 
            onClick={() => setPasswordDialog(false)}
            disabled={saving}
          >
            Cancelar
          </Button>
          <Button 
            onClick={handlePasswordChange}
            variant="contained"
            disabled={saving || !passwordForm.currentPassword || !passwordForm.newPassword || !passwordForm.confirmPassword}
          >
            {saving ? 'Alterando...' : 'Alterar Senha'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default ClientProfilePage;