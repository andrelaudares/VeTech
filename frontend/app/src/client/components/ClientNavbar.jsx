import React, { useState } from 'react';
import { useNavigate, Link as RouterLink, useLocation } from 'react-router-dom';
import { useClientAuth } from '../contexts/ClientAuthContext';
import logoVetech from '../../assets/logo.svg';

import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Box,
  Menu,
  MenuItem,
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
import MenuIcon from '@mui/icons-material/Menu';

const ClientNavbar = () => {
  const { client, logout } = useClientAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [anchorElUser, setAnchorElUser] = useState(null);
  const [mobileOpen, setMobileOpen] = useState(false);

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

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
    navigate('/client/profile');
  };

  const drawer = (
    <Box onClick={() => setMobileOpen(false)} sx={{ width: 250 }}>
      <List>
        <ListItem button component={RouterLink} to="/client/dashboard">
          <ListItemIcon><DashboardIcon /></ListItemIcon>
          <ListItemText primary="Dashboard" />
        </ListItem>
        <ListItem button component={RouterLink} to="/client/animals">
          <ListItemIcon><PetsIcon /></ListItemIcon>
          <ListItemText primary="Meus Pets" />
        </ListItem>
        <ListItem button component={RouterLink} to="/client/appointments">
          <ListItemIcon><EventNoteIcon /></ListItemIcon>
          <ListItemText primary="Agendamentos" />
        </ListItem>
      </List>
    </Box>
  );

  return (
    <>
      <AppBar position="static" color="primary" sx={{ borderRadius: 0 }}>
        <Toolbar sx={{ display: 'flex', justifyContent: 'space-between' }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <img src={logoVetech} alt="VeTech Logo" style={{ height: '40px', marginRight: '15px' }} />
            <Typography variant="h6" component="div" sx={{ color: 'white', cursor: 'pointer' }} onClick={() => navigate('/client/dashboard')}>
              VeTech
            </Typography>
            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)', ml: 1 }}>
              Área do Tutor
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
              <Button 
                color="inherit" 
                component={RouterLink} 
                to="/client/dashboard" 
                startIcon={<DashboardIcon />}
                sx={{ 
                  textTransform: 'none', 
                  fontWeight: (location.pathname === '/client/dashboard' || location.pathname === '/client/') ? 'bold' : 'normal' 
                }}
              >
                Dashboard
              </Button>
              <Button 
                color="inherit" 
                component={RouterLink} 
                to="/client/animals" 
                startIcon={<PetsIcon />}
                sx={{ 
                  textTransform: 'none', 
                  fontWeight: location.pathname === '/client/animals' ? 'bold' : 'normal' 
                }}
              >
                Meus Pets
              </Button>
              <Button 
                color="inherit" 
                component={RouterLink} 
                to="/client/appointments" 
                startIcon={<EventNoteIcon />}
                sx={{ 
                  textTransform: 'none', 
                  fontWeight: location.pathname === '/client/appointments' ? 'bold' : 'normal' 
                }}
              >
                Agendamentos
              </Button>
            </Box>
          )}

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Typography sx={{ color: 'white', display: { xs: 'none', sm: 'block' } }}>
              Olá, {client?.name || 'Tutor'}
            </Typography>

            <Tooltip title="Abrir menu do usuário">
              <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                <Avatar alt={client?.name || 'T'} sx={{ bgcolor: 'secondary.main' }}>
                  {client?.name ? client.name.charAt(0).toUpperCase() : <AccountCircleIcon />}
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

export default ClientNavbar;