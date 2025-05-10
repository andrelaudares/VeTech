import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useAuth } from '../contexts/AuthContext';
import clinicService from '../services/clinicService';
import { useNavigate } from 'react-router-dom';
import AppHeader from '../components/AppHeader'; // Importa o novo header

// Importações do Material UI
import {
  Box,
  Button,
  Card,
  CardContent,
  CardActions,
  Container,
  Grid,
  Typography,
  TextField,
  Modal,
  CircularProgress,
  Alert,
  Paper // Para o conteúdo do Modal e talvez para o card principal
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import BusinessIcon from '@mui/icons-material/Business';
import EmailIcon from '@mui/icons-material/Email';
import PhoneIcon from '@mui/icons-material/Phone';
import PaymentsIcon from '@mui/icons-material/Payments';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';

// Estilo para o Modal (pode ser mantido ou ajustado conforme o novo tema)
const modalStyle = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: { xs: '90%', sm: 450, md: 500 }, // Responsivo
  bgcolor: 'background.paper',
  // border: '2px solid #000', // Remover borda padrão, usar elevação do Paper
  borderRadius: '12px',
  boxShadow: 24,
  p: { xs: 2, sm: 3, md: 4 }, // Padding responsivo
};

const ProfilePage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [profileData, setProfileData] = useState(null);
  const [loadingData, setLoadingData] = useState(true); // Renomeado para evitar conflito
  const [fetchError, setFetchError] = useState(null); // Renomeado para evitar conflito
  const [showEditModal, setShowEditModal] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);
  const [updateSuccess, setUpdateSuccess] = useState(false);
  const [updateError, setUpdateError] = useState(null); // Erro específico para atualização
  
  const { register, handleSubmit, reset, formState: { errors: formErrors } } = useForm();

  useEffect(() => {
    fetchProfileData();
  }, []);

  const fetchProfileData = async () => {
    try {
      setLoadingData(true);
      setFetchError(null);
      const response = await clinicService.getProfile();
      setProfileData(response.data);
      setLoadingData(false);
    } catch (err) {
      console.error('Erro ao buscar dados do perfil:', err);
      setFetchError(err.response?.data?.detail || 'Não foi possível carregar os dados do perfil. Por favor, tente novamente.');
      setLoadingData(false);
    }
  };

  const openEditModal = () => {
    reset({
      name: profileData?.name || '',
      phone: profileData?.phone || ''
    });
    setUpdateError(null); // Limpa erros de atualização anteriores ao abrir o modal
    setUpdateSuccess(false);
    setShowEditModal(true);
  };

  const closeEditModal = () => {
    setShowEditModal(false);
    setUpdateSuccess(false);
    setUpdateError(null);
  };

  const onSubmitUpdate = async (data) => {
    setIsUpdating(true);
    setUpdateSuccess(false);
    setUpdateError(null);
    try {
      await clinicService.updateProfile(data);
      await fetchProfileData(); 
      setUpdateSuccess(true);
      // Manter o modal aberto para mostrar a mensagem de sucesso
      // setTimeout(() => {
      //   closeEditModal();
      // }, 2000); 
    } catch (err) {
      console.error('Erro ao atualizar perfil:', err);
      setUpdateError(err.response?.data?.detail || 'Não foi possível atualizar o perfil. Verifique os dados e tente novamente.');
    }
    setIsUpdating(false);
  };

  if (loadingData && !profileData) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', bgcolor: 'background.default' }}>
        <CircularProgress color="primary" />
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppHeader /> {/* Usa o novo componente de header */}

      <Container component="main" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 3, color: 'text.primary' }}>
          Informações da Clínica
        </Typography>

        {fetchError && !showEditModal && (
          <Alert severity="error" sx={{ mb: 3 }} onClose={() => setFetchError(null)}>
            {fetchError}
          </Alert>
        )}
        
        {profileData ? (
          <Paper elevation={3} sx={{ p: { xs: 2, md: 3 }, borderRadius: '12px', backgroundColor: 'background.paper' }}>
            <Grid container spacing={3}>
              {[ // Array para facilitar a renderização dos campos do perfil
                { label: 'Nome da Clínica', value: profileData.name, icon: <BusinessIcon color="secondary" sx={{ fontSize: '2rem'}} /> },
                { label: 'Email', value: profileData.email, icon: <EmailIcon color="secondary" sx={{ fontSize: '2rem'}} /> },
                { label: 'Telefone', value: profileData.phone, icon: <PhoneIcon color="secondary" sx={{ fontSize: '2rem'}} /> },
                { label: 'Plano de Assinatura', value: profileData.subscription_tier, icon: <PaymentsIcon color="secondary" sx={{ fontSize: '2rem'}} /> },
              ].map((item, index) => (
                <Grid item xs={12} sm={6} key={index} sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  {item.icon && <Box sx={{ mr: 2, display: 'flex', alignItems: 'center' }}>{item.icon}</Box>}
                  <Box>
                    <Typography variant="caption" color="text.secondary" display="block">
                      {item.label}
                    </Typography>
                    <Typography variant="h6" component="p" color="text.primary">
                      {item.value || 'N/A'}
                    </Typography>
                  </Box>
                </Grid>
              ))}
            </Grid>
            <CardActions sx={{ justifyContent: 'flex-end', p:2, pt:3 }}>
              <Button 
                variant="contained" 
                color="primary"
                startIcon={<EditIcon />} 
                onClick={openEditModal}
                sx={{ borderRadius: '8px', px: 3, py: 1 }}
              >
                Editar Perfil
              </Button>
            </CardActions>
          </Paper>
        ) : (
           !loadingData && <Alert severity="warning">Não foi possível carregar os dados do perfil.</Alert>
        )}
      </Container>

      <Modal
        open={showEditModal}
        onClose={closeEditModal}
        aria-labelledby="edit-profile-modal-title"
        aria-describedby="edit-profile-modal-description"
      >
        <Paper sx={modalStyle}> {/* Usando Paper para o conteúdo do modal com elevação */}
          <Typography id="edit-profile-modal-title" variant="h5" component="h2" sx={{ mb: 3, textAlign: 'center', color: 'primary.main' }}>
            Editar Perfil da Clínica
          </Typography>
          
          {updateSuccess && (
            <Alert icon={<CheckCircleOutlineIcon fontSize="inherit" />} severity="success" sx={{ mb: 2 }}>
              Perfil atualizado com sucesso!
            </Alert>
          )}
          {updateError && (
              <Alert severity="error" sx={{ mb: 2 }} onClose={() => setUpdateError(null)}>
                  {updateError}
              </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit(onSubmitUpdate)} noValidate>
            <TextField
              margin="normal"
              required
              fullWidth
              id="name"
              label="Nome da Clínica"
              autoFocus
              defaultValue={profileData?.name || ''} // Usar defaultValue para campos controlados por react-hook-form no reset
              {...register('name', { required: 'Nome é obrigatório' })}
              error={!!formErrors.name}
              helperText={formErrors.name?.message}
              sx={{ mb: 2 }}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="phone"
              label="Telefone"
              defaultValue={profileData?.phone || ''} // Usar defaultValue
              {...register('phone', { 
                required: 'Telefone é obrigatório', 
                pattern: { value: /^\d{10,11}$/, message: 'Telefone inválido (10 ou 11 dígitos)'}
              })}
              error={!!formErrors.phone}
              helperText={formErrors.phone?.message}
              sx={{ mb: 2 }}
            />
            <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end', gap: 1 }}>
                <Button onClick={closeEditModal} color="secondary" variant="outlined" sx={{ borderRadius: '8px' }}>
                    Cancelar
                </Button>
                <Button 
                    type="submit" 
                    variant="contained" 
                    color="primary"
                    disabled={isUpdating}
                    startIcon={isUpdating ? <CircularProgress size={20} color="inherit" /> : <EditIcon />}
                    sx={{ borderRadius: '8px' }}
                >
                    {isUpdating ? 'Salvando...' : 'Salvar Alterações'}
                </Button>
            </Box>
          </Box>
        </Paper>
      </Modal>
      
      {/* Footer similar ao DashboardPage para consistência */}
      <Box
        component="footer"
        sx={{
          py: 3,
          px: 2,
          mt: 'auto',
          backgroundColor: 'background.paper',
          borderTop: (theme) => `1px solid ${theme.palette.divider || '#D8CAB8'}` // Usar cor do tema ou fallback
        }}
      >
        <Container maxWidth="sm">
          <Typography variant="body2" color="text.secondary" align="center">
            {'© '}{new Date().getFullYear()}{' VeTech. Todos os direitos reservados.'}
          </Typography>
        </Container>
      </Box>
    </Box>
  );
};

export default ProfilePage; 