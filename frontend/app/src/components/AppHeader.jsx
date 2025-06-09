import React, { useState, useEffect } from 'react';
import { useNavigate, Link as RouterLink, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useAnimal } from '../contexts/AnimalContext';
import logoVetech from '../assets/logo.svg';
// import animalService from '../services/animalService';

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
  Avatar,
  Tooltip,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  useMediaQuery
} from '@mui/material';
import { useTheme } from '@mui/material/styles';

import LogoutIcon from '@mui/icons-material/Logout';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import PetsIcon from '@mui/icons-material/Pets';
import DashboardIcon from '@mui/icons-material/Home';
import EventNoteIcon from '@mui/icons-material/EventNote';
import AssignmentIcon from '@mui/icons-material/Assignment';
import RestaurantMenuIcon from '@mui/icons-material/RestaurantMenu';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';
import MenuIcon from '@mui/icons-material/Menu';

const AppHeader = () => {
  const { user, logout } = useAuth();
  const { selectedAnimal, setSelectedAnimal, animals, fetchAnimals } = useAnimal();
  const navigate = useNavigate();
  const location = useLocation();
  const [anchorElUser, setAnchorElUser] = useState(null);
  const [loadingAnimals, setLoadingAnimals] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  useEffect(() => {
    const loadAnimals = async () => {
      setLoadingAnimals(true);
      try {
        await fetchAnimals();
      } catch (error) {
        console.error("Erro ao carregar animais no header:", error);
      }
      setLoadingAnimals(false);
    };
    if (user) {
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
      setSelectedAnimal(null);
    } else {
      const animal = animals.find(a => a.id === animalId);
      setSelectedAnimal(animal);
    }
  };

  const noAnimalSelectorPages = ['/perfil', '/inicio', '/animais'];
  const showAnimalSelector = !noAnimalSelectorPages.includes(location.pathname);

  const drawer = (
    <Box onClick={() => setMobileOpen(false)} sx={{ width: 250 }}>
      <List>
        <ListItem button component={RouterLink} to="/inicio">
          <ListItemIcon><DashboardIcon /></ListItemIcon>
          <ListItemText primary="Início" />
        </ListItem>
        <ListItem button component={RouterLink} to="/animais">
          <ListItemIcon><PetsIcon /></ListItemIcon>
          <ListItemText primary="Animais" />
        </ListItem>
        <ListItem button component={RouterLink} to="/agendamentos">
          <ListItemIcon><EventNoteIcon /></ListItemIcon>
          <ListItemText primary="Agendamentos" />
        </ListItem>
        <ListItem button component={RouterLink} to="/consultas">
          <ListItemIcon><AssignmentIcon /></ListItemIcon>
          <ListItemText primary="Consultas" />
        </ListItem>
        <ListItem button component={RouterLink} to="/dietas">
          <ListItemIcon><RestaurantMenuIcon /></ListItemIcon>
          <ListItemText primary="Dietas" />
        </ListItem>
        <ListItem button component={RouterLink} to="/atividades">
          <ListItemIcon><FitnessCenterIcon /></ListItemIcon>
          <ListItemText primary="Atividades" />
        </ListItem>
      </List>

      {/* Seletor de animal no drawer */}
      {showAnimalSelector && (
        <Box sx={{ px: 2, pb: 2 }}>
          <FormControl fullWidth size="small" sx={{ mt: 2 }}>
            <InputLabel id="select-animal-mobile-label">Selecionar Animal</InputLabel>
            <Select
              labelId="select-animal-mobile-label"
              id="animal-select-mobile"
              value={selectedAnimal ? selectedAnimal.id : ""}
              label="Selecionar Animal"
              onChange={handleAnimalChange}
              disabled={loadingAnimals || animals.length === 0}
            >
              <MenuItem value="">
                <em>{loadingAnimals ? "Carregando..." : (animals.length === 0 ? "Nenhum animal" : "Selecionar Animal")}</em>
              </MenuItem>
              {animals.map((animal) => (
                <MenuItem key={animal.id} value={animal.id}>
                  {animal.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
      )}
    </Box>
  );


  return (
    <>
      <AppBar position="static" color="primary" sx={{ borderRadius: 0 }}>
        <Toolbar sx={{ display: 'flex', justifyContent: 'space-between' }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <img src={logoVetech} alt="VeTech Logo" style={{ height: '40px', marginRight: '15px' }} />
            <Typography variant="h6" component="div" sx={{ color: 'white', cursor: 'pointer' }} onClick={() => navigate('/inicio')}>
              VeTech Painel
            </Typography>
          </Box>

          {isMobile ? (
            <>
              <IconButton color="inherit" onClick={() => setMobileOpen(true)} edge="start">
                <MenuIcon />
              </IconButton>
              <Drawer anchor="left" open={mobileOpen} onClose={() => setMobileOpen(false)}>
                {drawer}
              </Drawer>
            </>
          ) : (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
              <Button color="inherit" component={RouterLink} to="/inicio" startIcon={<DashboardIcon />}
                sx={{ textTransform: 'none', fontWeight: location.pathname === '/inicio' ? 'bold' : 'normal' }}
              >
                Início
              </Button>
              <Button color="inherit" component={RouterLink} to="/animais" startIcon={<PetsIcon />}
                sx={{ textTransform: 'none', fontWeight: location.pathname === '/animais' ? 'bold' : 'normal' }}
              >
                Animais
              </Button>
              <Button color="inherit" component={RouterLink} to="/agendamentos" startIcon={<EventNoteIcon />}
                sx={{ textTransform: 'none', fontWeight: location.pathname === '/agendamentos' ? 'bold' : 'normal' }}
              >
                Agendamentos
              </Button>
              <Button color="inherit" component={RouterLink} to="/consultas" startIcon={<AssignmentIcon />}
                sx={{ textTransform: 'none', fontWeight: location.pathname === '/consultas' ? 'bold' : 'normal' }}
              >
                Consultas
              </Button>
              <Button color="inherit" component={RouterLink} to="/dietas" startIcon={<RestaurantMenuIcon />}
                sx={{ textTransform: 'none', fontWeight: location.pathname === '/dietas' ? 'bold' : 'normal' }}
              >
                Dietas
              </Button>
              <Button color="inherit" component={RouterLink} to="/atividades" startIcon={<FitnessCenterIcon />}
                sx={{ textTransform: 'none', fontWeight: location.pathname === '/atividades' ? 'bold' : 'normal' }}
              >
                Atividades
              </Button>
            </Box>
          )}

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            {showAnimalSelector && !isMobile && (
              <FormControl size="small" sx={{ m: 1, minWidth: 180, backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: 1 }}>
                <InputLabel id="select-animal-label" sx={{ color: 'white' }}>Selecionar Animal</InputLabel>
                <Select
                  labelId="select-animal-label"
                  id="animal-select"
                  value={selectedAnimal ? selectedAnimal.id : ""}
                  label="Selecionar Animal"
                  onChange={handleAnimalChange}
                  disabled={loadingAnimals || animals.length === 0}
                  sx={{
                    color: 'white',
                    '.MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255,255,255,0.3)' },
                    '&:hover .MuiOutlinedInput-notchedOutline': { borderColor: 'white' },
                    '.MuiSvgIcon-root': { color: 'white' }
                  }}
                >
                  <MenuItem value="">
                    <em>{loadingAnimals ? "Carregando..." : (animals.length === 0 ? "Nenhum animal" : "Selecionar Animal")}</em>
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
              anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
              keepMounted
              transformOrigin={{ vertical: 'top', horizontal: 'right' }}
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
    </>
  );
};

export default AppHeader;
