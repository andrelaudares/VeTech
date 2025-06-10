import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Grid,
  Divider
} from '@mui/material';
import EventIcon from '@mui/icons-material/Event'; // Data
import AccessTimeIcon from '@mui/icons-material/AccessTime'; // Hora
import PetsIcon from '@mui/icons-material/Pets'; // Animal
import DescriptionIcon from '@mui/icons-material/Description'; // Descrição
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline'; // Status Agendado/Concluído
import CancelIcon from '@mui/icons-material/Cancel'; // Status Cancelado
import HelpOutlineIcon from '@mui/icons-material/HelpOutline'; // Status Genérico

const colors = {
  tableHeader: '#D8CAB8', // Marrom-claro suave (para o título do modal)
  textPrimary: '#333',
  textSecondary: '#555',
  buttonPrimary: '#9DB8B2', // Cinza-esverdeado
  statusScheduled: '#2196f3', // Azul para Agendado
  statusCompleted: '#4caf50', // Verde para Concluído
  statusCancelled: '#f44336', // Vermelho para Cancelado
};

const DetailItem = ({ icon, label, value }) => (
  <Grid item xs={12} sm={6} sx={{ display: 'flex', alignItems: 'center', mb: 1.5 }}>
    {React.cloneElement(icon, { sx: { mr: 1.5, color: colors.buttonPrimary } })}
    <Box>
      <Typography variant="caption" color={colors.textSecondary} display="block">{label}</Typography>
      <Typography variant="body1" color={colors.textPrimary}>{value || '-'}</Typography>
    </Box>
  </Grid>
);

const getStatusProps = (status) => {
    switch (status) {
        case 'scheduled':
            return { text: 'Agendado', icon: <CheckCircleOutlineIcon />, color: colors.statusScheduled };
        case 'completed':
            return { text: 'Concluído', icon: <CheckCircleOutlineIcon />, color: colors.statusCompleted };
        case 'cancelled':
            return { text: 'Cancelado', icon: <CancelIcon />, color: colors.statusCancelled };
        default:
            return { text: status || 'Desconhecido', icon: <HelpOutlineIcon />, color: colors.textSecondary };
    }
};

const AppointmentDetailsModal = ({ open, onClose, appointment, getAnimalNameById, onEdit }) => {
  if (!appointment) return null;

  const animalName = getAnimalNameById(appointment.animal_id);
  const statusProps = getStatusProps(appointment.status);

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle sx={{ backgroundColor: '#23e865', color: colors.textPrimary }}>
        Detalhes do Agendamento
      </DialogTitle>
      <DialogContent sx={{ pt: '20px !important' }}>
        <Grid container spacing={1}>
          <DetailItem icon={<EventIcon />} label="Data" value={appointment.date ? new Date(appointment.date + 'T00:00:00').toLocaleDateString() : '-'} />
          <DetailItem icon={<AccessTimeIcon />} label="Hora" value={appointment.start_time ? appointment.start_time.substring(0,5) : '--'} />
          <DetailItem icon={<PetsIcon />} label="Animal" value={animalName} />
          <Grid item xs={12} sx={{ display: 'flex', alignItems: 'center', mb: 1.5 }}>
            {React.cloneElement(statusProps.icon, { sx: { mr: 1.5, color: statusProps.color } })}
            <Box>
                <Typography variant="caption" color={colors.textSecondary} display="block">Status</Typography>
                <Typography variant="body1" sx={{ color: statusProps.color, fontWeight: 'bold' }}>{statusProps.text}</Typography>
            </Box>
          </Grid>
          {appointment.description && (
            <Grid item xs={12} sx={{ mt: 1}}>
                <Divider sx={{mb:1.5}}/>
                <Box sx={{ display: 'flex', alignItems: 'flex-start' }}>
                    <DescriptionIcon sx={{ mr: 1.5, color: colors.buttonPrimary, mt: 0.5 }} />
                    <Box>
                        <Typography variant="caption" color={colors.textSecondary} display="block">Descrição</Typography>
                        <Typography variant="body1" color={colors.textPrimary} sx={{whiteSpace: 'pre-wrap'}}>{appointment.description}</Typography>
                    </Box>
                </Box>
            </Grid>
          )}
        </Grid>
      </DialogContent>
      <DialogActions sx={{ p: '16px 24px'}}>
        <Button onClick={onClose} sx={{ color: colors.textSecondary }}>Fechar</Button>
        <Button 
            onClick={() => {
                onClose(); // Fecha este modal primeiro
                onEdit(); // Depois chama a função para abrir o de edição
            }}
            variant="contained" 
            sx={{ backgroundColor: '#23e865', '&:hover': { backgroundColor: '#008a2e'} }}
        >
            Editar Agendamento
        </Button>
        {/* O botão de excluir já está na tabela principal, mas poderia estar aqui também */}
      </DialogActions>
    </Dialog>
  );
};

export default AppointmentDetailsModal; 