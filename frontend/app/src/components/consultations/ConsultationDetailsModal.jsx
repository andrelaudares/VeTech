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
  Divider,
  useTheme
} from '@mui/material';
import EventIcon from '@mui/icons-material/Event';
import PetsIcon from '@mui/icons-material/Pets';
import DescriptionIcon from '@mui/icons-material/Description';

const DetailItem = ({ icon, label, value, fullWidth = false }) => {
  const theme = useTheme();

  return (
    <Grid
      item
      xs={12}
      sm={fullWidth ? 12 : 6}
      sx={{ display: 'flex', alignItems: 'flex-start', mb: 2 }}
    >
      {React.cloneElement(icon, {
        sx: {
          mr: 1.5,
          color: theme.palette.secondary.main,
          mt: 0.5,
        },
      })}
      <Box>
        <Typography
          variant="caption"
          color="text.secondary"
          display="block"
        >
          {label}
        </Typography>
        <Typography
          variant="body1"
          color="text.primary"
          sx={{ whiteSpace: 'pre-wrap' }}
        >
          {value || '-'}
        </Typography>
      </Box>
    </Grid>
  );
};

const ConsultationDetailsModal = ({ open, onClose, consultation, getAnimalNameById, onEdit }) => {
  const theme = useTheme();

  if (!consultation) return null;

  const animalName = getAnimalNameById(consultation.animal_id);

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle
        sx={{
          backgroundColor: theme.palette.primary.main,
          color: theme.palette.primary.contrastText,
        }}
      >
        Detalhes da Consulta
      </DialogTitle>

      <DialogContent sx={{ pt: 3 }}>
        <Grid container spacing={1}>
          <DetailItem
            icon={<EventIcon />}
            label="Data"
            value={new Date(consultation.date).toLocaleDateString()}
          />
          <DetailItem
            icon={<PetsIcon />}
            label="Animal"
            value={animalName}
          />
          {consultation.description && (
            <Grid item xs={12}>
              <Divider sx={{ my: 2 }} />
              <DetailItem
                icon={<DescriptionIcon />}
                label="Descrição"
                value={consultation.description}
                fullWidth
              />
            </Grid>
          )}
        </Grid>
      </DialogContent>

      <DialogActions sx={{ p: '16px 24px' }}>
        <Button onClick={onClose} sx={{ color: theme.palette.text.secondary }}>
          Fechar
        </Button>
        <Button
          onClick={() => {
            onClose();
            onEdit();
          }}
          variant="contained"
          sx={{
            backgroundColor: theme.palette.primary.main,
            color: theme.palette.primary.contrastText,
            '&:hover': { backgroundColor: theme.palette.secondary.main }
          }}
        >
          Editar Consulta
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ConsultationDetailsModal;
