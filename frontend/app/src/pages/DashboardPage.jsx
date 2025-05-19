import React from 'react';
// import { useAuth } from '../contexts/AuthContext';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  CardActions,
  Container,
  Grid,
  Typography,
  useTheme,
} from '@mui/material';
import BarChartIcon from '@mui/icons-material/BarChart';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import RocketLaunchIcon from '@mui/icons-material/RocketLaunch';

const DashboardPage = () => {
  // const { user } = useAuth();
  const theme = useTheme();

  const cardStyle = {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: theme.palette.background.paper,
    borderRadius: 1,
    boxShadow: theme.shadows[2],
    transition: 'transform 0.2s ease-in-out',
    '&:hover': {
      transform: 'translateY(-4px)',
      boxShadow: theme.shadows[6],
    },
  };

  const iconBoxStyle = {
    display: 'flex',
    alignItems: 'center',
    mb: 1.5,
    color: theme.palette.secondary.main,
  };

  return (
    <Container component="main" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
      <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 3, color: 'text.primary' }}>
        Bem-vindo à sua Página Inicial!
      </Typography>

      <Grid container spacing={6}>
        {/* Linha com dois cards */}
        <Grid container spacing={3} item xs={12} md={8}>
          <Grid item xs={12} md={6}>
            <Card sx={cardStyle}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={iconBoxStyle}>
                  <BarChartIcon sx={{ mr: 1.5, fontSize: '2rem' }} />
                  <Typography variant="h6" component="h2">
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

          <Grid item xs={12} md={6}>
            <Card sx={cardStyle}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={iconBoxStyle}>
                  <AccountCircleIcon sx={{ mr: 1.5, fontSize: '2rem' }} />
                  <Typography variant="h6" component="h2">
                    Gerenciar Perfil
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Acesse e atualize as informações da sua clínica e do seu perfil.
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small" component={RouterLink} to="/perfil" variant="outlined">
                  Ir para Perfil
                </Button>
              </CardActions>
            </Card>
          </Grid>
        </Grid>

        {/* Card Em Breve ocupando toda a largura */}
        <Grid item xs={12} md={8}>
          <Card sx={cardStyle}>
            <CardContent sx={{ flexGrow: 1 }}>
              <Box sx={iconBoxStyle}>
                <RocketLaunchIcon sx={{ mr: 1.5, fontSize: '2rem' }} />
                <Typography variant="h6" component="h2">
                  Em Breve
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" component="div">
                Novas funcionalidades a caminho:
                <ul style={{ paddingLeft: '20px', marginTop: '8px' }}>
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
  );
};

export default DashboardPage;
