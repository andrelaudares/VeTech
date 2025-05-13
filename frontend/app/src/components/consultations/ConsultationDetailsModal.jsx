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
import EventIcon from '@mui/icons-material/Event';
import PetsIcon from '@mui/icons-material/Pets';
import DescriptionIcon from '@mui/icons-material/Description';

const colors = {
  tableHeader: '#D8CAB8',
  textPrimary: '#333',
  textSecondary: '#555',
  buttonPrimary: '#9DB8B2',
  buttonPrimaryHover: '#82a8a0',
};

const DetailItem = ({ icon, label, value, fullWidth = false }) => (
  <Grid item xs={12} sm={fullWidth ? 12 : 6} sx={{ display: 'flex', alignItems: 'flex-start', mb: 1.5 }}>
    {React.cloneElement(icon, { sx: { mr: 1.5, color: colors.buttonPrimary, mt: 0.5 } })}
    <Box>
      <Typography variant="caption" color={colors.textSecondary} display="block">{label}</Typography>
      <Typography variant="body1" color={colors.textPrimary} sx={{whiteSpace: 'pre-wrap'}}>{value || '-'}</Typography>
    </Box>
  </Grid>
);

const ConsultationDetailsModal = ({ open, onClose, consultation, getAnimalNameById, onEdit }) => {
  if (!consultation) return null;

  const animalName = getAnimalNameById(consultation.animal_id);

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle sx={{ backgroundColor: colors.tableHeader, color: colors.textPrimary }}>
        Detalhes da Consulta
      </DialogTitle>
      <DialogContent sx={{ pt: '20px !important' }}>
        <Grid container spacing={1}>
          <DetailItem icon={<EventIcon />} label="Data" value={new Date(consultation.date).toLocaleDateString()} />
          <DetailItem icon={<PetsIcon />} label="Animal" value={animalName} />
          {consultation.description && (
            <Grid item xs={12} sx={{ mt: 1}}>
                <Divider sx={{mb:1.5}}/>
                <DetailItem icon={<DescriptionIcon />} label="Descrição" value={consultation.description} fullWidth />
            </Grid>
          )}
        </Grid>
      </DialogContent>
      <DialogActions sx={{ p: '16px 24px'}}>
        <Button onClick={onClose} sx={{ color: colors.textSecondary }}>Fechar</Button>
        <Button 
            onClick={() => {
                onClose();
                onEdit(); 
            }}
            variant="contained" 
            sx={{ backgroundColor: colors.buttonPrimary, '&:hover': { backgroundColor: colors.buttonPrimaryHover } }}
        >
            Editar Consulta
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ConsultationDetailsModal; 