import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
// import { LockOutlined } from '@mui/icons-material'; // Não será mais usado
import logoVetech from '../assets/logo.svg'; // Importando o logo

// Importações do Material UI
// import Avatar from '@mui/material/Avatar'; // Não será mais usado para o ícone
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import Paper from '@mui/material/Paper'; // Para um card mais suave

// O tema darkTheme local não é mais necessário, pois o tema global está em main.jsx
// const darkTheme = createTheme({...}); 

const LoginPage = () => {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const { login, error: authError, loading } = useAuth(); // Renomeado error para authError para evitar conflito
  const navigate = useNavigate();
  // const [loginError, setLoginError] = useState(''); // Removido, usando authError diretamente

  const onSubmit = async (data) => {
    // setLoginError(''); // Removido
    try {
      await login(data.email, data.password);
      navigate('/dashboard');
    } catch (err) {
      // O AuthContext já deve estar tratando e expondo o erro através de 'authError'
      // Se precisar de uma mensagem específica aqui, pode-se adicionar, mas vamos tentar usar o erro global primeiro.
      console.error("Erro no login:", err.response || err);
    }
  };

  return (
    <Container component="main" maxWidth="xs" sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
      <Paper elevation={3} sx={{
        padding: 4, // Aumentar padding
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        width: '100%', // Garantir que o Paper ocupe a largura do Container
        borderRadius: '12px', // Bordas mais suaves
      }}>
        <Box sx={{ mb: 3 }}> {/* Adiciona margem abaixo do logo */}
          <img src={logoVetech} alt="VeTech Logo" style={{ height: '80px' }} />
        </Box>
        <Typography component="h1" variant="h5" sx={{ mb: 1 }}>
          Bem-vindo à VeTech
        </Typography>
        <Typography component="p" variant="body2" color="text.secondary" sx={{ mb: 3, textAlign: 'center' }}>
          Acesse sua conta para gerenciar sua clínica.
        </Typography>
        
        {authError && (
          <Alert severity="error" sx={{ width: '100%', mb: 2 }}>
            {typeof authError === 'string' ? authError : (authError.response?.data?.detail || 'Email ou senha incorretos.')}
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate sx={{ mt: 1, width: '100%' }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label="Endereço de Email"
            name="email"
            autoComplete="email"
            autoFocus
            {...register('email', {
              required: 'Email é obrigatório',
              pattern: {
                value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                message: 'Email inválido'
              }
            })}
            error={!!errors.email}
            helperText={errors.email?.message}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Senha"
            type="password"
            id="password"
            autoComplete="current-password"
            {...register('password', { required: 'Senha é obrigatória' })}
            error={!!errors.password}
            helperText={errors.password?.message}
            sx={{ mb: 2 }}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary" // Usa a cor primária do tema
            disabled={loading}
            sx={{ mt: 2, mb: 2, py: 1.2, fontSize: '1rem', borderRadius: '8px' }} // Ajustes no botão
          >
            {loading ? <CircularProgress size={24} color="inherit" /> : 'Entrar'}
          </Button>
          <Grid container justifyContent="flex-end">
            <Grid item>
              <Link href="#" variant="body2" onClick={() => alert('Funcionalidade de recuperação de senha estará disponível em breve!')} sx={{ color: 'secondary.main' }}>
                Esqueceu sua senha?
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Paper>
      <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 5, mb:4 }}>
        {'© '}
        {new Date().getFullYear()}
        {' VeTech. Todos os direitos reservados.'}
      </Typography>
    </Container>
  );
};

export default LoginPage; 