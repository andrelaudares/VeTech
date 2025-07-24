import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Chip,
  IconButton,
  Tooltip,
  Divider,
  Grid,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Paper
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import PlaylistAddIcon from '@mui/icons-material/PlaylistAdd';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import FoodIcon from '@mui/icons-material/Restaurant';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import NoFoodIcon from '@mui/icons-material/NoFood';

// Paleta de cores para consistência
const colors = {
  primaryAction: '#9DB8B2',
  primaryActionHover: '#82a8a0',
  secondaryAction: '#CFE0C3',
  secondaryActionHover: '#b8d4a8',
  paperBackground: '#FFFFFF',
  textPrimary: '#333',
  textSecondary: '#555',
  borderColor: '#E0E0E0',
  background: '#F9F9F9',
  accordionHeader: '#f5f5f5',
  foodListBackground: '#fafafa'
};

const DietDetailsModal = ({ open, onClose, diet, onEdit, onDelete, onAddOption, onEditOption, onDeleteOption, onAddFood, onEditFood, onDeleteFood }) => {

  if (!diet) return null; // Não renderizar nada se não houver dados da dieta

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString();
  };

  // Placeholder para a função de adicionar alimento
  const handleAddFood = (optionId) => {
    console.log("Abrir modal de adicionar alimento (Grupo 6) para a opção:", optionId);
    // onAddFood(optionId); // Será implementado depois
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth scroll="paper">
      <DialogTitle sx={{ backgroundColor: '#23e865', color: colors.paperBackground, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        Detalhes do Plano de Dieta
        <IconButton onClick={onClose} sx={{ color: colors.paperBackground }}>
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      <DialogContent dividers sx={{ backgroundColor: colors.background, p: 0 }}>
         {/* Seção de Informações Básicas */}
         <Box sx={{ p: 3, backgroundColor: colors.paperBackground, borderBottom: `1px solid ${colors.borderColor}` }}>
             <Grid container spacing={2.5}>
                 <Grid item xs={12} sm={4}>
                    <Typography variant="subtitle2" color={colors.textSecondary}>Tipo:</Typography>
                    <Typography variant="body1" color={colors.textPrimary} gutterBottom>{diet.tipo || '-'}</Typography>
                 </Grid>
                 <Grid item xs={12} sm={4}>
                     <Typography variant="subtitle2" color={colors.textSecondary}>Objetivo:</Typography>
                     <Typography variant="body1" color={colors.textPrimary} gutterBottom>{diet.objetivo || '-'}</Typography>
                 </Grid>
                 <Grid item xs={12} sm={4} sx={{textAlign: {sm: 'right'}}}>
                     <Typography variant="subtitle2" color={colors.textSecondary}>Status:</Typography>
                     <Chip
                        label={diet.status || '-'}
                        size="small"
                        color={diet.status === 'ativa' ? 'success' : diet.status === 'finalizada' ? 'default' : diet.status === 'pausada' ? 'warning' : 'default'}
                        sx={{ fontWeight: '500', minWidth: '80px'}}
                      />
                 </Grid>
                 <Grid item xs={12} sm={6}>
                     <Typography variant="subtitle2" color={colors.textSecondary}>Data de Início:</Typography>
                     <Typography variant="body1" color={colors.textPrimary}>{formatDate(diet.data_inicio)}</Typography>
                 </Grid>
                 <Grid item xs={12} sm={6}>
                     <Typography variant="subtitle2" color={colors.textSecondary}>Data de Fim:</Typography>
                     <Typography variant="body1" color={colors.textPrimary}>{diet.data_fim ? formatDate(diet.data_fim) : 'Em andamento'}</Typography>
                 </Grid>
                 {diet.observacoes && (
                    <Grid item xs={12}>
                        <Typography variant="subtitle2" color={colors.textSecondary} sx={{mt: 1}}>Observações:</Typography>
                        <Typography variant="body2" color={colors.textPrimary} sx={{ whiteSpace: 'pre-wrap' }}>{diet.observacoes}</Typography>
                    </Grid>
                 )}
             </Grid>
         </Box>

         {/* Seção de Opções de Dieta (Grupo 5) */}
         <Box sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" sx={{ color: colors.textPrimary, fontWeight: '500' }}>Opções da Dieta</Typography>
                <Button
                    variant="contained"
                    startIcon={<PlaylistAddIcon />}
                    onClick={() => onAddOption(diet.id)} // Chama handleOpenAddOptionModal da DietsPage
                    size="small"
                    sx={{
                        backgroundColor: '#23e865',
                        color: colors.textPrimary,
                        '&:hover': { backgroundColor: '#008a2e' },
                    }}
                    >Adicionar Opção
                </Button>
            </Box>

            {diet.opcoes_dieta && diet.opcoes_dieta.length > 0 ? (
                diet.opcoes_dieta.map((option) => (
                    <Accordion key={option.id} sx={{ mb: 1.5, boxShadow: '0 1px 3px rgba(0,0,0,0.1)', '&:before': { display: 'none' } }} >
                        <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            aria-controls={`option-${option.id}-content`}
                            id={`option-${option.id}-header`}
                            sx={{ backgroundColor: colors.accordionHeader, borderBottom: `1px solid ${colors.borderColor}`, minHeight: '52px', '& .MuiAccordionSummary-content': { alignItems: 'center' } }}
                        >
                            <Typography sx={{ fontWeight: '500', flexBasis: '40%', flexShrink: 0, mr: 2 }}>{option.nome}</Typography>
                            <Typography sx={{ color: colors.textSecondary, fontSize: '0.875rem' }}>
                                {option.calorias_totais_dia ? `${option.calorias_totais_dia} kcal/dia` : ''}
                                {option.refeicoes_por_dia ? ` - ${option.refeicoes_por_dia}x/dia` : ''}
                            </Typography>
                            <Box sx={{ ml: 'auto', display: 'flex', alignItems: 'center' }}>
                                <Tooltip title="Editar Opção">
                                    <IconButton size="small" sx={{ color: colors.secondaryAction, '&:hover': { color: colors.secondaryActionHover }, mr: 0.5 }} onClick={(e) => { e.stopPropagation(); onEditOption(option); }}>
                                        <EditIcon fontSize="small" />
                                    </IconButton>
                                </Tooltip>
                                <Tooltip title="Excluir Opção">
                                    <IconButton size="small" sx={{ color: '#e57373', '&:hover': { color: '#d32f2f' } }} onClick={(e) => { e.stopPropagation(); onDeleteOption(option.id); }}>
                                        <DeleteIcon fontSize="small" />
                                    </IconButton>
                                </Tooltip>
                            </Box>
                        </AccordionSummary>
                        <AccordionDetails sx={{ backgroundColor: colors.paperBackground, p: 2 }}>
                            <Grid container spacing={1.5} sx={{mb: 2}}>
                                {option.valor_mensal_estimado && (
                                    <Grid item xs={6} sm={4}>
                                        <Typography variant="caption" display="block" color={colors.textSecondary}>Valor Mensal (R$):</Typography>
                                        <Typography variant="body2">{option.valor_mensal_estimado.toFixed(2)}</Typography>
                                    </Grid>
                                )}
                                {option.porcao_refeicao && (
                                     <Grid item xs={6} sm={4}>
                                        <Typography variant="caption" display="block" color={colors.textSecondary}>Porção/Refeição:</Typography>
                                        <Typography variant="body2">{option.porcao_refeicao}</Typography>
                                    </Grid>
                                )}
                                {option.indicacao && (
                                    <Grid item xs={12}>
                                        <Typography variant="caption" display="block" color={colors.textSecondary}>Indicação/Obs:</Typography>
                                        <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>{option.indicacao}</Typography>
                                    </Grid>
                                )}
                            </Grid>

                            <Divider sx={{ my: 2 }}><Typography variant="overline">Alimentos</Typography></Divider>

                            {/* Listagem de Alimentos (Grupo 6) */}
                            {option.alimentos && option.alimentos.length > 0 ? (
                                <List dense sx={{ backgroundColor: colors.foodListBackground, borderRadius: '4px', p: 1, mb:1.5 }}>
                                    {option.alimentos.map((food) => (
                                        <ListItem
                                            key={food.id}
                                            divider
                                            secondaryAction={
                                                <Box>
                                                    <Tooltip title="Editar Alimento">
                                                        <IconButton edge="end" aria-label="edit" size="small" onClick={() => onEditFood(food)} sx={{mr: 0.5}}>
                                                            <EditIcon fontSize="small" />
                                                        </IconButton>
                                                    </Tooltip>
                                                    <Tooltip title="Excluir Alimento">
                                                        <IconButton edge="end" aria-label="delete" size="small" onClick={() => onDeleteFood(food.id)}>
                                                            <DeleteIcon fontSize="small" />
                                                        </IconButton>
                                                    </Tooltip>
                                                </Box>
                                            }
                                        >
                                            <ListItemIcon sx={{minWidth: '36px'}}><FoodIcon fontSize="small" sx={{color: colors.primaryAction}} /></ListItemIcon>
                                            <ListItemText 
                                                primary={food.nome}
                                                secondary={`${food.quantidade || '-'} (${food.tipo}) - ${food.calorias || '?'} kcal - ${food.horario || 'S/ Horário'}`}
                                                primaryTypographyProps={{ fontWeight: '500' }}
                                                secondaryTypographyProps={{ fontSize: '0.8rem' }}
                                            />
                                        </ListItem>
                                    ))}
                                </List>
                            ) : (
                                <Box sx={{display: 'flex', flexDirection: 'column', alignItems: 'center', color: colors.textSecondary, my: 2}}>
                                    <NoFoodIcon sx={{fontSize: '2rem', mb: 0.5}}/>
                                    <Typography sx={{ fontStyle: 'italic' }}>Nenhum alimento cadastrado para esta opção.</Typography>
                                </Box>
                            )}

                            <Button
                                startIcon={<AddCircleOutlineIcon />}
                                size="small"
                                onClick={() => onAddFood(option.id)} // Chama handleOpenAddFoodModal da DietsPage
                                sx={{ mt: 0.5, color: colors.primaryAction, fontWeight: '500' }}
                            >
                                Adicionar Alimento
                            </Button>

                        </AccordionDetails>
                    </Accordion>
                ))
            ) : (
                <Typography sx={{ textAlign: 'center', color: colors.textSecondary, mt: 3, fontStyle: 'italic' }}>
                    Nenhuma opção de dieta cadastrada para este plano.
                </Typography>
            )}
         </Box>

      </DialogContent>
      <DialogActions sx={{ p: '12px 24px', borderTop: `1px solid ${colors.borderColor}`, backgroundColor: colors.paperBackground }}>
        <Tooltip title="Excluir Dieta">
            <Button
                startIcon={<DeleteIcon />}
                color="error"
                onClick={() => onDelete(diet.id)}
            >
                Excluir
            </Button>
        </Tooltip>
        <Tooltip title="Editar Dieta">
            <Button
                startIcon={<EditIcon />}
                variant="outlined"
                onClick={() => onEdit(diet)} // Passa o objeto da dieta para edição
                sx={{ color: colors.primaryAction, borderColor: colors.primaryAction, '&:hover': { borderColor: colors.primaryActionHover, backgroundColor: 'rgba(157, 184, 178, 0.1)'} }}
            >
                Editar
            </Button>
        </Tooltip>
        <Button onClick={onClose} variant="contained" sx={{backgroundColor: colors.primaryAction, '&:hover': { backgroundColor: colors.primaryActionHover }}}>Fechar</Button>
      </DialogActions>
    </Dialog>
  );
};

export default DietDetailsModal; 