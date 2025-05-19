import React from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Paper,
  useTheme
} from '@mui/material';

const features = [
  {
    title: 'Gestão Completa de Animais',
    description: 'Cadastre, visualize e gerencie facilmente todos os animais da clínica.',
    icon: '🐾'
  },
  {
    title: 'Consultas e Agendamentos',
    description: 'Crie, edite e acompanhe consultas, além de organizar todos os agendamentos da semana.',
    icon: '📅'
  },
  {
    title: 'Plano de Dieta Personalizada',
    description: 'Monte dietas sob medida para cada pet, levando em conta a saúde e necessidades nutricionais.',
    icon: '🥗'
  },
  {
    title: 'App para Clientes + Gamificação',
    description: 'Clientes ganham recompensas por cuidar do pet!',
    icon: '🎁'
  }
];

const LandingPage = () => {
  const theme = useTheme();

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: `linear-gradient(to bottom right, ${theme.palette.primary.light}, ${theme.palette.background.default})`,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        pt: 8,
        pb: 10,
      }}
    >
      <Container maxWidth="lg">
        {/* HERO SECTION */}
        <Box
          sx={{
            textAlign: 'center',
            mb: 8,
          }}
        >
          <Box
            sx={{
              width: 100,
              height: 100,
              borderRadius: '50%',
              backgroundColor: theme.palette.primary.main,
              color: theme.palette.primary.contrastText,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 52,
              mx: 'auto',
              mb: 2,
              boxShadow: '0 8px 20px rgba(0,0,0,0.1)'
            }}
          >
            🐶
          </Box>
          <Typography variant="h2" fontWeight="bold" gutterBottom color="primary">
            VeTech
          </Typography>
          <Typography
            variant="h6"
            sx={{ color: theme.palette.text.secondary, maxWidth: 700, mx: 'auto' }}
          >
            Sistema moderno para clínicas veterinárias. <br />
            Gestão, tecnologia e carinho para seu pet e sua clínica.
          </Typography>
          <Button
            variant="contained"
            size="large"
            href="/login"
            sx={{
              mt: 4,
              px: 6,
              py: 1.5,
              fontSize: 18,
              borderRadius: '12px',
              fontWeight: 'bold',
              boxShadow: '0 6px 20px rgba(0,0,0,0.15)',
              transition: '0.3s',
              '&:hover': {
                backgroundColor: theme.palette.secondary.main,
                transform: 'translateY(-2px)'
              }
            }}
          >
            Entrar no Sistema
          </Button>
        </Box>

        {/* FEATURES SECTION */}
        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={6} key={index} sx={{ display: 'flex' }}>
              <Paper
                elevation={3}
                sx={{
                  p: 4,
                  borderRadius: '16px',
                  height: '100%',
                  width: '100vw',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'flex-start',
                  backgroundColor: '#ffffff',
                  transition: '0.3s',
                  '&:hover': {
                    transform: 'translateY(-5px)',
                    boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
                  }
                }}
              >
                <Box
                  sx={{
                    fontSize: 36,
                    backgroundColor: theme.palette.primary.light,
                    color: theme.palette.primary.main,
                    borderRadius: '50%',
                    width: 60,
                    height: 60,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    mb: 2
                  }}
                >
                  {feature.icon}
                </Box>
                <Typography variant="h6" fontWeight="bold" gutterBottom color="primary">
                  {feature.title}
                </Typography>
                <Typography variant="body1" sx={{ color: theme.palette.text.secondary }}>
                  {feature.description}
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>

        {/* FOOTER */}
        <Box sx={{ textAlign: 'center', mt: 10, color: theme.palette.text.disabled }}>
          <Typography variant="body2">
            &copy; {new Date().getFullYear()} VeTech — Sistema para Clínicas Veterinárias.
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default LandingPage;
