import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, Button, Grid, Container } from '@mui/material';
import logoVetech from '../assets/logo.svg';
import calendar from '../assets/calendar.png';
import dog from '../assets/dog.png';
import hospital from '../assets/hospital.png';
import diet from '../assets/diet.png'

const LandingPage = () => {

  const navigate = useNavigate()

  return (
    <Box>
      {/* Header */}
      <Box component="header" sx={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        px: '5%', py: 2, backgroundColor: 'white', boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)'
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <img src={logoVetech} alt="Logo Vetech" width={60} height={60} />
          <Typography variant="h6" sx={{ color: '#1e3a1e', fontWeight: 700 }}>VetCare Clinic</Typography>
        </Box>
        <Button onClick={() => navigate('/login')} sx={{ backgroundColor: '#23e865', color: 'white', fontWeight: 600, px: 2.5, py: 1, borderRadius: 1, '&:hover': { backgroundColor: '#1dd457', opacity: 0.9 } }}>Entrar</Button>
      </Box>

      {/* Hero Section */}
      <Box sx={{ display: 'flex', alignItems: 'center', px: '5%', py: 8, gap: 6,
        backgroundColor: '#f5f7fa', flexWrap: 'wrap-reverse' }}>
        <Box sx={{ flex: 1 }}>
          <Typography variant="h3" sx={{ color: '#1e3a1e', mb: 2, fontWeight: 700 }}>
            Cuidando do seu pet com amor e tecnologia
          </Typography>
          <Typography variant="body1" sx={{ color: '#555', fontSize: '1.1rem', mb: 4 }}>
            Agende consultas, acesse prontuários e receba lembretes de vacina em um só lugar.
          </Typography>
          <Button onClick={() => navigate('/login')} sx={{ backgroundColor: '#23e865', color: 'white', fontWeight: 600, px: 3, py: 1.5, borderRadius: 1,
            transition: 'transform 0.3s, box-shadow 0.3s',
            '&:hover': {
              transform: 'translateY(-3px)',
              boxShadow: '0 5px 15px rgba(35, 232, 101, 0.3)'
            }}}>Acessar Sistema</Button>
        </Box>
        <Box sx={{ flex: 1, textAlign: 'center' }}>
          <img src={dog} alt="Cachorro sorrindo" style={{ maxWidth: '100%', height: 'auto', borderRadius: '10px' }} />
        </Box>
      </Box>

      {/* Funcionalidades */}
      <Box sx={{ py: 10, px: '5%', backgroundColor: 'white', textAlign: 'center' }}>
        <Typography variant="h4" sx={{ color: '#1e3a1e', mb: 6, fontWeight: 600 }}>
          Como podemos ajudar?
        </Typography>
        <Grid container spacing={4} justifyContent="center">
          {[
            {
              title: 'Agendamento Online',
              description: 'Marque consultas 24h sem sair de casa.',
              icon: calendar
            },
            {
              title: 'Prontuário Digital',
              description: 'Histórico completo de saúde do seu pet.',
              icon: hospital
            },
            {
              title: 'Dietas Personalizadas',
              description: 'Planos alimentares sob medida para cada animal.',
              icon: diet
            }
          ].map((feature, idx) => (
            <Grid item xs={12} sm={6} md={4} key={idx}>
              <Box sx={{ backgroundColor: '#f5f7fa', p: 4, borderRadius: 2, transition: 'transform 0.3s', '&:hover': { transform: 'translateY(-10px)' } }}>
                <img src={feature.icon} alt={feature.title} width={60} height={60} style={{ marginBottom: 20 }} />
                <Typography variant="h6" sx={{ color: '#1e3a1e', mb: 1 }}>{feature.title}</Typography>
                <Typography variant="body2" sx={{ color: '#666' }}>{feature.description}</Typography>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Rodapé */}
      <Box sx={{ textAlign: 'center', py: 3, backgroundColor: '#1e3a1e', color: 'white', fontSize: '0.9rem' }}>
        <Typography>
          © 2025 Vetech Clinic | Contato: contato@vetech.com.br
        </Typography>
      </Box>
    </Box>
  );
};

export default LandingPage;
