import React, { useState, useEffect } from 'react';
import { useNavigate, Link as RouterLink, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useAnimal } from '../contexts/AnimalContext'; // Será criado a seguir
import logoVetech from '../assets/logo.svg';
import animalService from '../services/animalService'; // Será necessário criar ou usar um serviço existente

import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Box,
  Menu,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  CircularProgress,
  Avatar, // Para o ícone do perfil
  Tooltip
} from '@mui/material';
import LogoutIcon from '@mui/icons-material/Logout';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import PetsIcon from '@mui/icons-material/Pets'; // Ícone para o dropdown de animais
import DashboardIcon from '@mui/icons-material/Home'; // Trocado para Home ou similar para 'Início'
import EventNoteIcon from '@mui/icons-material/EventNote'; // Ícone para Agendamentos
import AssignmentIcon from '@mui/icons-material/Assignment'; // Ícone para Consultas (ou MedicalServicesIcon)

const AppHeader = () => {
  const { user, logout } = useAuth();
  const { selectedAnimal, setSelectedAnimal, animals, fetchAnimals } = useAnimal(); // Hook do AnimalContext
  const navigate = useNavigate();
  const location = useLocation(); // Adicionado para obter o pathname
  const [anchorElUser, setAnchorElUser] = useState(null);
  const [loadingAnimals, setLoadingAnimals] = useState(false);

  useEffect(() => {
    const loadAnimals = async () => {
      setLoadingAnimals(true);
      try {
        // A função fetchAnimals virá do AnimalContext e já lidará com o armazenamento no contexto
        await fetchAnimals();
      } catch (error) {
        console.error("Erro ao carregar animais no header:", error);
        // Tratar erro (ex: mostrar um toast/snackbar)
      }
      setLoadingAnimals(false);
    };
    if (user) { // Só busca animais se o usuário estiver logado
      loadAnimals();
    }
  }, [user, fetchAnimals]);

  const handleLogout = async () => {
    handleCloseUserMenu();
    await logout();
    navigate('/login');
  };

  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  const handleProfileNavigation = () => {
    handleCloseUserMenu();
    navigate('/perfil');
  };
  
  const handleAnimalChange = (event) => {
    const animalId = event.target.value;
    if (animalId === "") {
      setSelectedAnimal(null); // Opção "Todos os animais" ou similar
    } else {
      const animal = animals.find(a => a.id === animalId);
      setSelectedAnimal(animal);
    }
  };

  // Define as páginas que não devem mostrar o seletor de animal
  const noAnimalSelectorPages = ['/perfil', '/inicio', '/animais']; // Adicionado /animais
  // Verifica se a rota atual está na lista de páginas sem seletor
  const showAnimalSelector = !noAnimalSelectorPages.includes(location.pathname);


  return (
    <AppBar position="static" color="primary">
      <Toolbar sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <img src={logoVetech} alt="VeTech Logo" style={{ height: '40px', marginRight: '15px' }} />
          <Typography variant="h6" component="div" sx={{ color: 'white', cursor: 'pointer' }} onClick={() => navigate('/inicio')}>
            VeTech Painel
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {/* Navegação Principal - Pode ser expandida com mais links/abas */}
          <Button color="inherit" component={RouterLink} to="/inicio" startIcon={<DashboardIcon />}>
            Início
          </Button>
          <Button color="inherit" component={RouterLink} to="/animais" startIcon={<PetsIcon />}>
            Animais
          </Button>
          {/* Adicionar mais links de navegação aqui conforme necessário */}
          {/* Exemplo:
          <Button color="inherit" component={RouterLink} to="/agendamentos">Agendamentos</Button>
          */}
          <Button color="inherit" component={RouterLink} to="/agendamentos" startIcon={<EventNoteIcon />}>
            Agendamentos
          </Button>
          <Button color="inherit" component={RouterLink} to="/consultas" startIcon={<AssignmentIcon />}>
            Consultas
          </Button>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {showAnimalSelector && (
            <FormControl size="small" sx={{ m: 1, minWidth: 180, backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: 1 }}>
              <InputLabel id="select-animal-label" sx={{ color: 'white' }}>Selecionar Animal</InputLabel>
              <Select
                labelId="select-animal-label"
                id="animal-select"
                value={selectedAnimal ? selectedAnimal.id : ""}
                label="Selecionar Animal"
                onChange={handleAnimalChange}
                disabled={loadingAnimals || animals.length === 0}
                sx={{ color: 'white', '.MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255,255,255,0.3)' }, '&:hover .MuiOutlinedInput-notchedOutline': { borderColor: 'white' }, '.MuiSvgIcon-root': { color: 'white' } }}
              >
                <MenuItem value="">
                  <em>{loadingAnimals ? "Carregando..." : (animals.length === 0 ? "Nenhum animal" : "Todos os Animais")}</em>
                </MenuItem>
                {animals.map((animal) => (
                  <MenuItem key={animal.id} value={animal.id}>
                    {animal.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          )}

          <Typography sx={{ color: 'white', display: { xs: 'none', sm: 'block' } }}>
            Olá, {user?.name || 'Usuário'}
          </Typography>

          <Tooltip title="Abrir menu do usuário">
            <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
              <Avatar alt={user?.name || 'U'} sx={{ bgcolor: 'secondary.main' }}>
                {user?.name ? user.name.charAt(0).toUpperCase() : <AccountCircleIcon />}
              </Avatar>
            </IconButton>
          </Tooltip>
          <Menu
            sx={{ mt: '45px' }}
            id="menu-appbar-user"
            anchorEl={anchorElUser}
            anchorOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            keepMounted
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            open={Boolean(anchorElUser)}
            onClose={handleCloseUserMenu}
          >
            <MenuItem onClick={handleProfileNavigation}>
              <AccountCircleIcon sx={{ mr: 1 }} /> Perfil
            </MenuItem>
            <MenuItem onClick={handleLogout}>
              <LogoutIcon sx={{ mr: 1 }} /> Sair
            </MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default AppHeader; 