import React from 'react';
import {
  Box,
  Typography,
  Container,
  Grid,
  Paper,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip
} from '@mui/material';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import PetsIcon from '@mui/icons-material/Pets';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import VaccinesIcon from '@mui/icons-material/Vaccines';
import { useNavigate } from 'react-router-dom';

const stats = [
  { label: 'Consultas Hoje', value: 12, icon: <CalendarTodayIcon /> },
  { label: 'Pendentes', value: 5, icon: <AccessTimeIcon /> },
  { label: 'Animais Ativos', value: 256, icon: <PetsIcon /> },
  { label: 'Vacinas Hoje', value: 8, icon: <VaccinesIcon /> },
];

const consultasHoje = [
  { nome: 'Rex', dono: 'Ana Souza', hora: '09:00', status: 'Agendado' },
  { nome: 'Luna', dono: 'Carlos Dias', hora: '10:30', status: 'Concluído' },
  { nome: 'Mimi', dono: 'João Pedro', hora: '13:00', status: 'Agendado' },
  { nome: 'Tobby', dono: 'Maria Clara', hora: '15:15', status: 'Cancelado' },
];

const DashboardPage = () => {

  const navigate = useNavigate()

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" fontWeight="bold" mb={4}>Dashboard</Typography>

      {/* Cards de Resumo */}
      <Grid container spacing={3}>
        {stats.map((item, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Paper sx={{ p: 3, display: 'flex', alignItems: 'center', gap: 2, borderRadius: 2 }} elevation={3}>
              <Box sx={{ fontSize: 32, color: '#23e865' }}>{item.icon}</Box>
              <Box>
                <Typography variant="h6" fontWeight="bold">{item.value}</Typography>
                <Typography variant="body2" color="text.secondary">{item.label}</Typography>
              </Box>
            </Paper>
          </Grid>
        ))}
      </Grid>

      {/* Tabela de Consultas */}
      <Box mt={6}>
        <Typography variant="h6" fontWeight="bold" mb={2}>Consultas de Hoje</Typography>
        <Paper elevation={2}>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Animal</TableCell>
                  <TableCell>Dono</TableCell>
                  <TableCell>Horário</TableCell>
                  <TableCell>Status</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {consultasHoje.map((row, index) => (
                  <TableRow key={index}>
                    <TableCell>{row.nome}</TableCell>
                    <TableCell>{row.dono}</TableCell>
                    <TableCell>{row.hora}</TableCell>
                    <TableCell>
                      <Chip
                        label={row.status}
                        color={
                          row.status === 'Concluído' ? 'success' :
                          row.status === 'Agendado' ? 'primary' :
                          row.status === 'Cancelado' ? 'error' : 'default'
                        }
                        size="small"
                      />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </Box>

      {/* Avisos e Ações Rápidas */}
      <Box mt={6}>
        <Typography variant="h6" fontWeight="bold" mb={2}>Avisos</Typography>
        <Paper sx={{ p: 3, backgroundColor: '#fff3cd' }} elevation={1}>
          <Typography variant="body2">⚠️ 2 vacinas vencem essa semana.</Typography>
          <Typography variant="body2">🔁 1 dieta personalizada está prestes a expirar.</Typography>
        </Paper>

        <Box display="flex" gap={2} mt={3}>
          <Button variant="contained" color="primary" onClick={() => navigate('/agendamentos')}>+ Novo Agendamento</Button>
          <Button variant="outlined" color="primary" onClick={() => {navigate('/animais')}}>+ Novo Animal</Button>
        </Box>
      </Box>
    </Container>
  );
};

export default DashboardPage;
