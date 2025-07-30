import { useForm } from 'react-hook-form';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import logoVetech from '../assets/logo.svg';
import dualAuthService from '../services/dualAuthService';

import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import Paper from '@mui/material/Paper';
import { useState, useEffect } from 'react'; // Importar useState e useEffect

const LoginPage = () => {
  const { register, handleSubmit, formState: { errors } } = useForm();
  // Renomeamos 'error' para 'authError' no useAuth para evitar conflito com o nome padrão 'error'
  // Removendo 'loading' daqui pois usaremos um estado local para o botão.
  const { login, authError } = useAuth(); 
  const navigate = useNavigate();

  // Novo estado local para controlar o loading do botão
  const [isButtonLoading, setIsButtonLoading] = useState(false); 
  // Estado para a animação de shake
  const [shouldShake, setShouldShake] = useState(false); 

  const onSubmit = async (data) => {
    console.log("LoginPage: Formulário submetido. Dados:", data);
    setShouldShake(false); // Resetar tremor ao submeter
    setIsButtonLoading(true); // Ativar loading no botão

    try {
      console.log("LoginPage: Realizando login dual...");
      
      // Usar o serviço de login dual
      const loginResult = await dualAuthService.dualLogin(data.email, data.password);
      
      console.log("LoginPage: Login dual bem-sucedido:", loginResult);
      
      // Armazenar token no localStorage
      localStorage.setItem('token', loginResult.access_token);
      
      // Redirecionar baseado no tipo de usuário
      if (loginResult.user_type === 'clinic') {
        console.log("LoginPage: Usuário é clínica, redirecionando para área da clínica...");
        // Para clínicas, usar o sistema de autenticação existente
        await login(data.email, data.password);
        navigate('/inicio');
      } else if (loginResult.user_type === 'client') {
        console.log("LoginPage: Usuário é cliente, redirecionando para área do cliente...");
        // Para clientes, redirecionar para a área específica
        navigate('/client/dashboard');
      } else {
        throw new Error('Tipo de usuário não reconhecido');
      }
      
    } catch (err) {
      // O erro é capturado aqui
      console.error("LoginPage: Erro no login dual capturado no componente:", err.response || err);
      
      // Se for erro de credenciais inválidas, tentar login tradicional como fallback
      if (err.response?.status === 401 || err.response?.status === 404) {
        try {
          console.log("LoginPage: Tentando login tradicional como fallback...");
          await login(data.email, data.password);
          console.log("LoginPage: Login tradicional bem-sucedido. Navegando para /inicio...");
          navigate('/inicio');
        } catch (fallbackErr) {
          console.error("LoginPage: Erro no login tradicional:", fallbackErr);
          // O AuthContext já deve ter setado 'authError'
        }
      }
    } finally {
      setIsButtonLoading(false); // Desativar loading no botão, independente de sucesso ou falha
    }
  };

  // Efeito para limpar o tremor após a animação
  useEffect(() => {
    if (shouldShake) {
      const timer = setTimeout(() => {
        setShouldShake(false);
      }, 500); // Duração da animação
      return () => clearTimeout(timer);
    }
  }, [shouldShake]);

  // Efeito para ativar o tremor sempre que um novo erro de autenticação surgir
  useEffect(() => {
    if (authError) {
      setShouldShake(true);
      // console.log("LoginPage: authError atualizado, ativando shake.");
    }
  }, [authError]); // Depende do authError do contexto

  return (
    <Container component="main" maxWidth="xs" sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
      <Paper elevation={3} sx={{
        padding: 4,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        width: '100%',
        borderRadius: '12px',
      }} className={shouldShake ? 'shake-animation' : ''}> {/* Aplicar classe de animação */}
        <Box sx={{ mb: 3 }}>
          <img onClick={() => navigate('/')} src={logoVetech} alt="VeTech Logo" style={{ height: '80px', cursor: 'pointer'}} />
        </Box>
        <Typography component="h1" variant="h5" sx={{ mb: 1 }}>
          Bem-vindo à VeTech
        </Typography>
        <Typography component="p" variant="body2" color="text.secondary" sx={{ mb: 3, textAlign: 'center' }}>
          Acesse sua conta como clínica veterinária ou tutor.
        </Typography>
        
        {authError && (
          <Alert severity="error" sx={{ width: '100%', mb: 2 }}>
            {authError}
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
            color="primary"
            disabled={isButtonLoading} // Usa o novo estado local de loading
            sx={{ mt: 2, mb: 2, py: 1.2, fontSize: '1rem', borderRadius: '8px' }}
          >
            {isButtonLoading ? <CircularProgress size={24} color="inherit" /> : 'Entrar'}
          </Button>
          <Grid container justifyContent="space-between">
            <Grid item>
              <Link 
                component="button" 
                variant="body2" 
                onClick={() => navigate('/client/login')}
                sx={{ color: 'secondary.main', textDecoration: 'none' }}
              >
                Sou tutor de pet
              </Link>
            </Grid>
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