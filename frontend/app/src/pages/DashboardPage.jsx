import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
// import logoVetech from '../assets/logo.svg'; // Removido, pois está no AppHeader
import AppHeader from '../components/AppHeader'; // Importa o novo header

// Importações do Material UI (AppBar, Toolbar, IconButton, LogoutIcon etc. relacionados ao header foram removidos)
import {
  Box,
  Button,
  Card,
  CardContent,
  CardActions,
  Container,
  Grid,
  Typography,
} from '@mui/material';
import BarChartIcon from '@mui/icons-material/BarChart';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import RocketLaunchIcon from '@mui/icons-material/RocketLaunch';

const DashboardPage = () => {
  const { user } = useAuth(); // Logout foi removido daqui, pois está no AppHeader
  // const navigate = useNavigate(); // Removido se não for mais usado diretamente aqui

  // const handleLogout = async () => { // Removido, pois está no AppHeader
  //   await logout();
  //   navigate('/login');
  // };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppHeader /> {/* Usa o novo componente de header */}
      
      {/* Conteúdo da página abaixo do header */}
      <Container component="main" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 3, color: 'text.primary' }}>
          Bem-vindo à sua Página Inicial!
        </Typography>
        
        <Grid container spacing={3}>
          {/* Card Estatístico */}
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', backgroundColor: 'background.paper', borderRadius: '12px' }}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1.5 }}>
                  <BarChartIcon sx={{ mr: 1.5, fontSize: '2rem' }} color="secondary" />
                  <Typography variant="h5" component="h2" color="text.primary">
                    Estatísticas
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Visualize aqui as principais estatísticas da sua clínica. (Em desenvolvimento)
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small" disabled>Ver Detalhes</Button>
              </CardActions>
            </Card>
          </Grid>

          {/* Card Perfil */}
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', backgroundColor: 'background.paper', borderRadius: '12px' }}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1.5 }}>
                  <AccountCircleIcon sx={{ mr: 1.5, fontSize: '2rem' }} color="secondary" />
                  <Typography variant="h5" component="h2" color="text.primary">
                    Gerenciar Perfil
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Acesse e atualize as informações da sua clínica e do seu perfil.
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small" component={RouterLink} to="/perfil" color="primary">
                  Ir para Perfil
                </Button>
              </CardActions>
            </Card>
          </Grid>

          {/* Card Próximas Funcionalidades */}
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', backgroundColor: 'background.paper', borderRadius: '12px' }}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1.5 }}>
                  <RocketLaunchIcon sx={{ mr: 1.5, fontSize: '2rem' }} color="secondary" />
                  <Typography variant="h5" component="h2" color="text.primary">
                    Em Breve
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary" component="div">
                  Novas funcionalidades a caminho:
                  <ul style={{ paddingLeft: '20px', marginTop: '8px', color: 'text.secondary' }}>
                    <li>Gestão de Animais</li>
                    <li>Agendamentos Detalhados</li>
                    <li>Controle de Consultas</li>
                  </ul>
                </Typography>
              </CardContent>
               <CardActions>
                <Button size="small" disabled>Saiba Mais</Button>
              </CardActions>
            </Card>
          </Grid>
        </Grid>
      </Container>
      
      {/* Footer existente */}
      <Box
        component="footer"
        sx={{
          py: 3,
          px: 2,
          mt: 'auto',
          backgroundColor: 'background.paper',
          borderTop: (theme) => `1px solid ${theme.palette.divider}`
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

export default DashboardPage; 