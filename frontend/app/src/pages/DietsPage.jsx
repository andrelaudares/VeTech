import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Typography,
  Container,
  CircularProgress,
  Alert,
  Paper,
  Grid,
  Button,
  Tabs,
  Tab,
  useTheme,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  IconButton,
  Tooltip,
  Chip,
  TextField,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { useAnimal } from '../contexts/AnimalContext';
import dietService from '../services/dietService';
import DietFormModal from '../components/diets/DietFormModal';
import DietDetailsModal from '../components/diets/DietDetailsModal';
import DietOptionFormModal from '../components/diets/DietOptionFormModal';
import DietFoodFormModal from '../components/diets/DietFoodFormModal';

// Ícones para um design mais atraente
import RestaurantMenuIcon from '@mui/icons-material/RestaurantMenu'; // Dietas
import PlaylistAddCheckIcon from '@mui/icons-material/PlaylistAddCheck'; // Opções?
import FastfoodIcon from '@mui/icons-material/Fastfood'; // Alimentos/Snacks
import NoMealsIcon from '@mui/icons-material/NoMeals'; // Alimentos Restritos
import AddIcon from '@mui/icons-material/Add';
import PetsIcon from '@mui/icons-material/Pets'; // Ícone para mensagem de seleção
import VisibilityIcon from '@mui/icons-material/Visibility';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import SearchIcon from '@mui/icons-material/Search';
import FilterListIcon from '@mui/icons-material/FilterList';
import BlockIcon from '@mui/icons-material/Block'; // Para Alimentos Restritos
import CookieIcon from '@mui/icons-material/Cookie'; // Para Snacks
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Cancel';

// Paleta de cores definida no guia:
const colors = {
  background: '#F9F9F9',
  tableHeader: '#24EC64', // Marrom-claro suave
  primaryAction: '#24EC64', // Cinza-esverdeado
  primaryActionHover: '#82a8a0', // Tom mais escuro para hover
  secondaryAction: '#24EC64', // Verde-oliva suave
  secondaryActionHover: '#b8d4a8', // Tom mais escuro para hover
  textPrimary: '#333',
  textSecondary: '#555',
  paperBackground: '#FFFFFF',
  borderColor: '#E0E0E0',
  accent: '#FFA726', // Cor de destaque (ex: Amarelo/Laranja)
  tabIndicator: '#9DB8B2',
  tabBackgroundHover: 'rgba(157, 184, 178, 0.1)',
  deleteColor: '#e57373',
  deleteColorHover: '#d32f2f'
};

const DietsPage = () => {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const { selectedAnimal, loading: animalLoading } = useAnimal();
  const theme = useTheme(); // Acessar tema padrão se necessário ou para consistência

  const [diets, setDiets] = useState([]);
  const [restrictedFoods, setRestrictedFoods] = useState([]);
  const [snacks, setSnacks] = useState([]);
  const [loadingData, setLoadingData] = useState(false);
  const [error, setError] = useState(null);
  const [currentTab, setCurrentTab] = useState(0); // 0: Dietas, 1: Alimentos Restritos, 2: Snacks

  // Estados para o Grupo 1: Listagem de Dietas
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5); // Conforme especificação, até 10, começando com 5
  const [searchTermDiets, setSearchTermDiets] = useState('');

  // Estados para Modais
  const [openDietFormModal, setOpenDietFormModal] = useState(false);
  const [isEditingDiet, setIsEditingDiet] = useState(false);
  const [selectedDiet, setSelectedDiet] = useState(null);
  const [openDietDetailsModal, setOpenDietDetailsModal] = useState(false);
  const [openOptionFormModal, setOpenOptionFormModal] = useState(false);
  const [isEditingOption, setIsEditingOption] = useState(false);
  const [selectedOptionData, setSelectedOptionData] = useState(null);
  const [selectedDietIdForOption, setSelectedDietIdForOption] = useState(null);
  const [openFoodFormModal, setOpenFoodFormModal] = useState(false);
  const [isEditingFood, setIsEditingFood] = useState(false);
  const [selectedFoodData, setSelectedFoodData] = useState(null);
  const [selectedOptionIdForFood, setSelectedOptionIdForFood] = useState(null);

  // Estados para Alimentos Restritos (Grupo 7)
  const [loadingRestricted, setLoadingRestricted] = useState(false);
  const [errorRestricted, setErrorRestricted] = useState(null);
  const [newRestrictedFood, setNewRestrictedFood] = useState({ nome: '', motivo: '' });
  const [editingRestrictedFoodId, setEditingRestrictedFoodId] = useState(null);
  const [editRestrictedFoodData, setEditRestrictedFoodData] = useState({ nome: '', motivo: '' });

  // Estados para Snacks (Grupo 8)
  const [loadingSnacks, setLoadingSnacks] = useState(false);
  const [errorSnacks, setErrorSnacks] = useState(null);
  const [newSnack, setNewSnack] = useState({ nome: '', frequencia: '', quantidade: '', observacoes: '' });
  const [editingSnackId, setEditingSnackId] = useState(null);
  const [editSnackData, setEditSnackData] = useState({ nome: '', frequencia: '', quantidade: '', observacoes: '' });

  const fetchDataForAnimal = useCallback(async () => {
    if (!selectedAnimal || !isAuthenticated) {
      setDiets([]);
      setRestrictedFoods([]);
      setSnacks([]);
      setError(null);
      setErrorRestricted(null);
      setErrorSnacks(null);
      setPage(0); // Resetar paginação
      return;
    }

    // Reset states before fetching
    setLoadingData(true); // Indicate general loading start
    setLoadingRestricted(true);
    setLoadingSnacks(true);
    setError(null);
    setErrorRestricted(null);
    setErrorSnacks(null);
    setDiets([]); // Clear previous data
    setRestrictedFoods([]);
    setSnacks([]);

    let fetchError = null; // Track if any fetch failed

    console.log(`[DietsPage] Fetching data for animal: ${selectedAnimal?.id}, Tab: ${currentTab}`); // Log início

    // Fetch Diets
    try {
      console.log(`[DietsPage] Calling getDietsByAnimal for ${selectedAnimal.id}`);
      const dietsResponse = await dietService.getDietsByAnimal(selectedAnimal.id);
      console.log('[DietsPage] Response from getDietsByAnimal:', dietsResponse);
      setDiets(dietsResponse || []);
    } catch (err) {
      console.error("Erro ao buscar dietas:", err);
      const errorMsg = err.message || err.detail || "Falha ao carregar planos de dieta.";
      setError(errorMsg); // Set general error for the diets tab
      fetchError = errorMsg;
    } finally {
      // We handle general loadingData state at the very end
    }

    // Fetch Restricted Foods
    try {
      const restrictedFoodsResponse = await dietService.getRestrictedFoods(selectedAnimal.id);
      setRestrictedFoods(restrictedFoodsResponse || []);
    } catch (err) {
      console.error("Erro ao buscar alimentos restritos:", err);
      const errorMsg = err.message || err.detail || "Falha ao carregar alimentos restritos.";
      setErrorRestricted(errorMsg); // Set specific error for the restricted tab
      if (!fetchError) fetchError = errorMsg; // Keep the first error encountered for general state
    } finally {
      setLoadingRestricted(false); // Restricted food loading finished
    }

    // Fetch Snacks
    try {
      const snacksResponse = await dietService.getSnacks(selectedAnimal.id);
      setSnacks(snacksResponse || []);
    } catch (err) {
      console.error("Erro ao buscar snacks:", err);
      const errorMsg = err.message || err.detail || "Falha ao carregar snacks permitidos.";
      setErrorSnacks(errorMsg); // Set specific error for the snacks tab
      if (!fetchError) fetchError = errorMsg;
    } finally {
      setLoadingSnacks(false); // Snacks loading finished
      console.log('[DietsPage] Finished fetching snacks. States:', { loadingSnacks, errorSnacks, snacks });
    }

    // Update general loading and error states after all fetches attempted
    setLoadingData(false);
    console.log('[DietsPage] All fetches attempted. Final states:', { loadingData, error, diets, errorRestricted, restrictedFoods, errorSnacks, snacks });
    if (fetchError && !error) {
      // If a specific error was set but not the general one (diets fetch succeeded)
      // Optionally, set the general error as well, or rely on specific error displays per tab
      // setError(fetchError); 
    }

  }, [selectedAnimal, isAuthenticated, currentTab]);

  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      fetchDataForAnimal();
    }
    // Resetar paginação e busca ao mudar de animal ou aba
    setPage(0);
    setSearchTermDiets('');
  }, [fetchDataForAnimal, isAuthenticated, authLoading, selectedAnimal, currentTab]);

  const handleTabChange = (event, newValue) => {
    setCurrentTab(newValue);
  };

  const handleOpenCreateDietModal = () => {
    setSelectedDiet(null);
    setIsEditingDiet(false);
    setOpenDietFormModal(true);
  };

  const handleOpenViewDietModal = (diet) => {
    console.log("Abrindo detalhes para:", diet);
    setSelectedDiet(diet);
    setOpenDietDetailsModal(true);
  };

  const handleOpenEditDietModal = (diet) => {
    console.log("Abrir modal de edição de Dieta (Grupo 2 com dados)", diet);
    setSelectedDiet(diet);
    setIsEditingDiet(true);
    setOpenDietFormModal(true);
    handleCloseDietDetailsModal();
  };

  const handleCloseDietFormModal = () => {
    setOpenDietFormModal(false);
    setSelectedDiet(null);
    setIsEditingDiet(false);
  };

  const handleCloseDietDetailsModal = () => {
    setOpenDietDetailsModal(false);
    setSelectedDiet(null);
  };

  const handleSaveDietSuccess = () => {
    handleCloseDietFormModal();
    handleCloseDietDetailsModal();
    fetchDataForAnimal();
  };

  const handleDeleteDiet = async (dietId) => {
    handleCloseDietDetailsModal();
    handleCloseDietFormModal();
    if (window.confirm("Tem certeza que deseja excluir esta dieta e todas as suas informações relacionadas?")) {
      console.log("Excluir dieta (Grupo 1)", dietId);
      setLoadingData(true);
      try {
        await dietService.deleteDiet(dietId);
        // Refrescar dados após exclusão
        fetchDataForAnimal();
        // Mostrar snackbar de sucesso aqui
      } catch (err) {
        console.error("Erro ao excluir dieta:", err);
        setError(err.message || err.detail || "Erro ao excluir dieta.");
        // Mostrar snackbar de erro aqui
      } finally {
        setLoadingData(false);
      }
    }
  };

  // Funções de Paginação e Busca para Dietas (Grupo 1)
  const handleChangePageDiets = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPageDiets = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleSearchDietsChange = (event) => {
    setSearchTermDiets(event.target.value.toLowerCase());
    setPage(0);
  };

  const filteredDiets = diets.filter(diet => {
    const searchTermLower = searchTermDiets.toLowerCase();
    const tipo = diet.tipo?.toLowerCase() || '';
    const objetivo = diet.objetivo?.toLowerCase() || '';
    return tipo.includes(searchTermLower) || objetivo.includes(searchTermLower);
  });

  // ---- Handlers para Alimentos Restritos (Grupo 7) ----
  const handleRestrictedInputChange = (event) => {
    const { name, value } = event.target;
    setNewRestrictedFood(prev => ({ ...prev, [name]: value }));
  };

  const handleAddRestrictedFood = async () => {
    if (!newRestrictedFood.nome || !selectedAnimal?.id) {
      // Idealmente, mostrar o erro no próprio TextField
      console.error("Nome do alimento restrito é obrigatório.");
      return;
    }
    setLoadingRestricted(true);
    setErrorRestricted(null);
    try {
      await dietService.addRestrictedFood(selectedAnimal.id, newRestrictedFood);
      setNewRestrictedFood({ nome: '', motivo: '' }); // Limpar form
      fetchDataForAnimal(); // Recarregar tudo (incluindo restritos)
    } catch (err) {
      console.error("Erro ao adicionar alimento restrito:", err);
      setErrorRestricted(err.detail || err.message || "Erro ao adicionar alimento restrito.");
    } finally {
      setLoadingRestricted(false);
    }
  };

  const handleDeleteRestrictedFood = async (foodId) => {
    if (window.confirm("Tem certeza que deseja remover este alimento restrito?")) {
      setLoadingRestricted(true);
      setErrorRestricted(null);
      try {
        await dietService.deleteRestrictedFood(foodId);
        fetchDataForAnimal(); // Recarregar
      } catch (err) {
        console.error("Erro ao excluir alimento restrito:", err);
        setErrorRestricted(err.detail || err.message || "Erro ao excluir alimento restrito.");
      } finally {
        setLoadingRestricted(false);
      }
    }
  };

  const handleEditRestrictedInputChange = (event) => {
    const { name, value } = event.target;
    setEditRestrictedFoodData(prev => ({ ...prev, [name]: value }));
  };

  const handleStartEditRestricted = (food) => {
    setEditingRestrictedFoodId(food.id);
    setEditRestrictedFoodData({ nome: food.nome, motivo: food.motivo || '' });
    setNewRestrictedFood({ nome: '', motivo: '' }); // Limpar form de adição se estiver editando
    setErrorRestricted(null);
  };

  const handleCancelEditRestricted = () => {
    setEditingRestrictedFoodId(null);
    setEditRestrictedFoodData({ nome: '', motivo: '' });
    setErrorRestricted(null);
  };

  const handleSaveEditRestricted = async (foodId) => {
    if (!editRestrictedFoodData.nome) {
      // Mostrar erro no TextField?
      console.error("O nome do alimento não pode ficar vazio.");
      return;
    }
    setLoadingRestricted(true);
    setErrorRestricted(null);
    try {
      await dietService.updateRestrictedFood(foodId, editRestrictedFoodData);
      setEditingRestrictedFoodId(null); // Sair do modo de edição
      fetchDataForAnimal(); // Recarregar
    } catch (err) {
      console.error("Erro ao salvar alimento restrito:", err);
      setErrorRestricted(err.detail || err.message || "Erro ao salvar alimento restrito.");
    } finally {
      setLoadingRestricted(false);
    }
  };

  // ---- Handlers para Snacks (Grupo 8) ----
  const handleSnackInputChange = (event) => {
    const { name, value } = event.target;
    setNewSnack(prev => ({ ...prev, [name]: value }));
  };

  const handleAddSnack = async () => {
    if (!newSnack.nome || !selectedAnimal?.id) {
      console.error("Nome do snack é obrigatório.");
      return;
    }
    setLoadingSnacks(true);
    setErrorSnacks(null);
    try {
      await dietService.addSnack(selectedAnimal.id, newSnack);
      setNewSnack({ nome: '', frequencia: '', quantidade: '', observacoes: '' }); // Limpar form
      fetchDataForAnimal(); // Recarregar tudo
    } catch (err) {
      console.error("Erro ao adicionar snack:", err);
      setErrorSnacks(err.detail || err.message || "Erro ao adicionar snack.");
    } finally {
      setLoadingSnacks(false);
    }
  };

  const handleDeleteSnack = async (snackId) => {
    if (window.confirm("Tem certeza que deseja remover este snack?")) {
      setLoadingSnacks(true);
      setErrorSnacks(null);
      try {
        await dietService.deleteSnack(snackId);
        fetchDataForAnimal(); // Recarregar
      } catch (err) {
        console.error("Erro ao excluir snack:", err);
        setErrorSnacks(err.detail || err.message || "Erro ao excluir snack.");
      } finally {
        setLoadingSnacks(false);
      }
    }
  };

  const handleEditSnackInputChange = (event) => {
    const { name, value } = event.target;
    setEditSnackData(prev => ({ ...prev, [name]: value }));
  };

  const handleStartEditSnack = (snack) => {
    setEditingSnackId(snack.id);
    setEditSnackData({
      nome: snack.nome,
      frequencia: snack.frequencia || '',
      quantidade: snack.quantidade || '',
      observacoes: snack.observacoes || ''
    });
    setNewSnack({ nome: '', frequencia: '', quantidade: '', observacoes: '' }); // Limpar form de adição
    setErrorSnacks(null);
  };

  const handleCancelEditSnack = () => {
    setEditingSnackId(null);
    setEditSnackData({ nome: '', frequencia: '', quantidade: '', observacoes: '' });
    setErrorSnacks(null);
  };

  const handleSaveEditSnack = async (snackId) => {
    if (!editSnackData.nome) {
      console.error("O nome do snack não pode ficar vazio.");
      return;
    }
    setLoadingSnacks(true);
    setErrorSnacks(null);
    try {
      await dietService.updateSnack(snackId, editSnackData);
      setEditingSnackId(null); // Sair do modo de edição
      fetchDataForAnimal(); // Recarregar
    } catch (err) {
      console.error("Erro ao salvar snack:", err);
      setErrorSnacks(err.detail || err.message || "Erro ao salvar snack.");
    } finally {
      setLoadingSnacks(false);
    }
  };

  // ---- Handlers para o modal de Opção de Dieta (Grupo 4) ----
  const handleOpenAddOptionModal = (dietId) => {
    console.log("Abrir modal de adicionar Opção de Dieta (Grupo 4) para a dieta:", dietId);
    setSelectedDietIdForOption(dietId);
    setSelectedOptionData(null);
    setIsEditingOption(false);
    setOpenOptionFormModal(true);
  };

  const handleOpenEditOptionModal = (optionData) => {
    console.log("Abrir modal de edição de Opção de Dieta (Grupo 4) com dados:", optionData);
    setSelectedDietIdForOption(optionData.diet_id); // Garanta que diet_id está sendo passado
    setSelectedOptionData(optionData);
    setIsEditingOption(true);
    setOpenOptionFormModal(true);
  };

  const handleCloseOptionFormModal = () => {
    setOpenOptionFormModal(false);
    setSelectedDietIdForOption(null);
    setSelectedOptionData(null);
    setIsEditingOption(false);
  };

  const handleSaveOptionSuccess = async () => {
    console.log("Opção de dieta salva com sucesso (Grupo 4), atualizando detalhes da dieta...");
    handleCloseOptionFormModal();
    if (selectedDiet?.id) {
      setLoadingData(true);
      try {
        const updatedDietDetails = await dietService.getDietById(selectedDiet.id);
        setSelectedDiet(updatedDietDetails);
      } catch (error) {
        console.error("Erro ao re-buscar detalhes da dieta após salvar opção:", error);
        setError("Erro ao atualizar detalhes da dieta.");
        fetchDataForAnimal();
      } finally {
        setLoadingData(false);
      }
    } else {
      fetchDataForAnimal();
    }
  };

  const handleDeleteOption = async (optionId) => {
    if (window.confirm("Tem certeza que deseja excluir esta opção de dieta e todos os seus alimentos?")) {
      console.log("Excluir opção de dieta (Grupo 5)", optionId);
      setLoadingData(true);
      try {
        await dietService.deleteDietOption(optionId);
        if (selectedDiet?.id) {
          const updatedDietDetails = await dietService.getDietById(selectedDiet.id);
          setSelectedDiet(updatedDietDetails);
        }
        else {
          fetchDataForAnimal();
        }
      } catch (err) {
        console.error("Erro ao excluir opção de dieta:", err);
        setError(err.message || err.detail || "Erro ao excluir opção de dieta.");
      } finally {
        setLoadingData(false);
      }
    }
  };

  // ---- Handlers para o modal de Alimento da Dieta (Grupo 6) ----
  const handleOpenAddFoodModal = (optionId) => {
    console.log("Abrir modal de adicionar Alimento (Grupo 6) para a opção:", optionId);
    setSelectedOptionIdForFood(optionId);
    setSelectedFoodData(null);
    setIsEditingFood(false);
    setOpenFoodFormModal(true);
  };

  const handleOpenEditFoodModal = (foodData) => {
    console.log("Abrir modal de edição de Alimento (Grupo 6) com dados:", foodData);
    setSelectedOptionIdForFood(foodData.diet_option_id); // Garanta que diet_option_id está sendo passado
    setSelectedFoodData(foodData);
    setIsEditingFood(true);
    setOpenFoodFormModal(true);
  };

  const handleCloseFoodFormModal = () => {
    setOpenFoodFormModal(false);
    setSelectedOptionIdForFood(null);
    setSelectedFoodData(null);
    setIsEditingFood(false);
  };

  const handleSaveFoodSuccess = async () => {
    console.log("Alimento salvo com sucesso (Grupo 6), atualizando detalhes da dieta...");
    handleCloseFoodFormModal();
    if (selectedDiet?.id) {
      setLoadingData(true);
      try {
        const updatedDietDetails = await dietService.getDietById(selectedDiet.id);
        setSelectedDiet(updatedDietDetails);
      } catch (error) {
        console.error("Erro ao re-buscar detalhes da dieta após salvar alimento:", error);
        setError("Erro ao atualizar detalhes da dieta.");
        fetchDataForAnimal();
      } finally {
        setLoadingData(false);
      }
    } else {
      fetchDataForAnimal();
    }
  };

  const handleDeleteFood = async (foodId) => {
    if (window.confirm("Tem certeza que deseja excluir este alimento da dieta?")) {
      console.log("Excluir alimento da dieta (Grupo 6)", foodId);
      setLoadingData(true);
      try {
        await dietService.deleteDietFood(foodId);
        if (selectedDiet?.id) {
          const updatedDietDetails = await dietService.getDietById(selectedDiet.id);
          setSelectedDiet(updatedDietDetails);
        }
        else {
          fetchDataForAnimal();
        }
      } catch (err) {
        console.error("Erro ao excluir alimento da dieta:", err);
        setError(err.message || err.detail || "Erro ao excluir alimento da dieta.");
      } finally {
        setLoadingData(false);
      }
    }
  };

  // ---- Renderização Condicional ----

  if (authLoading || animalLoading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <CircularProgress />
        <Typography sx={{ ml: 2 }}>{authLoading ? 'Verificando autenticação...' : 'Carregando dados do animal...'}</Typography>
      </Container>
    );
  }

  if (!isAuthenticated) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="warning">Você precisa estar logado para acessar esta página.</Alert>
      </Container>
    );
  }

  if (!selectedAnimal) {
    return (
      <Container maxWidth="sm" sx={{ mt: 8, mb: 4, textAlign: 'center' }}>
        <Paper elevation={3} sx={{ p: { xs: 3, sm: 5 }, borderRadius: 2, backgroundColor: colors.paperBackground }}>
          <PetsIcon sx={{ fontSize: 60, color: colors.primaryAction, mb: 2 }} />
          <Typography variant="h5" component="h1" gutterBottom sx={{ color: colors.textPrimary, fontWeight: '500' }}>
            Selecione um Animal
          </Typography>
          <Typography variant="body1" sx={{ color: colors.textSecondary }}>
            Por favor, selecione um animal no menu superior para gerenciar as informações nutricionais e dietas.
          </Typography>
        </Paper>
      </Container>
    );
  }

  // ---- Layout Principal da Página ----
  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4, backgroundColor: colors.background, p: { xs: 2, md: 3 }, borderRadius: 2 }}>
      {/* Cabeçalho da Página */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3, flexWrap: 'wrap', gap: 2 }}>
        <Typography variant="h4" component="h1" sx={{ color: colors.textPrimary, fontWeight: '500' }}>
          Nutrição e Dietas de <span style={{ color: colors.primaryAction }}>{selectedAnimal.name}</span>
        </Typography>
        {/* Botão principal de ação (Nova Dieta) só aparece na tab de Dietas */}
        {currentTab === 0 && (
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleOpenCreateDietModal}
            sx={{
              backgroundColor: colors.primaryAction,
              color: colors.paperBackground,
              '&:hover': { backgroundColor: colors.primaryActionHover },
              padding: '10px 20px', // Botão mais destacado
              fontSize: '1rem',
              boxShadow: '0px 4px 12px rgba(0,0,0,0.1)' // Sombra suave
            }}
          >
            Nova Dieta
          </Button>
        )}
      </Box>

      {/* Abas para Navegação Principal (Dietas, Restritos, Snacks) */}
      <Paper elevation={1} sx={{ mb: 3, borderRadius: '8px 8px 0 0', overflow: 'hidden' }}>
        <Tabs
          value={currentTab}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          variant="fullWidth"
          aria-label="abas de nutrição"
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab icon={<RestaurantMenuIcon />} iconPosition="start" label="Planos de Dieta" sx={{ fontWeight: currentTab === 0 ? '600' : 'normal' }} />
          <Tab icon={<BlockIcon />} iconPosition="start" label="Alimentos Restritos" sx={{ fontWeight: currentTab === 1 ? '600' : 'normal' }} />
          <Tab icon={<CookieIcon />} iconPosition="start" label="Snacks Permitidos" sx={{ fontWeight: currentTab === 2 ? '600' : 'normal' }} />
        </Tabs>
      </Paper>

      {/* Indicador de Carregamento ou Erro Geral */}
      {loadingData && (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', my: 5, color: colors.primaryAction }}>
          <CircularProgress color="inherit" />
          <Typography sx={{ ml: 2 }}>Carregando dados de nutrição...</Typography>
        </Box>
      )}
      {error && (
        <Paper sx={{ p: 2, textAlign: 'center', my: 3, backgroundColor: '#ffebee', color: '#c62828', borderRadius: 2 }} elevation={3}>
          <Typography variant="h6">Oops!</Typography>
          <Typography>{error}</Typography>
        </Paper>
      )}

      {/* Conteúdo das Abas */}
      {!loadingData && !error && (
        <Box>
          {/* Grupo 1: Listagem de Dietas (Renderiza quando currentTab === 0) */}
          {currentTab === 0 && (
            <Paper elevation={2} sx={{ p: { xs: 1.5, md: 2.5 }, borderRadius: 2, backgroundColor: colors.paperBackground, mt: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2.5, flexWrap: 'wrap', gap: 1.5 }}>
                <Typography variant="h6" sx={{ color: colors.textPrimary, fontWeight: '500' }}>
                  Planos de Dieta Registrados
                </Typography>
                <TextField
                  label="Buscar por Tipo ou Objetivo"
                  variant="outlined"
                  size="small"
                  value={searchTermDiets}
                  onChange={handleSearchDietsChange}
                  InputProps={{
                    startAdornment: (
                      <SearchIcon position="start" sx={{ color: colors.textSecondary, mr: 0.5 }} />
                    ),
                  }}
                  sx={{ minWidth: '280px' }}
                />
                {/* TODO: Botão de Filtros Avançados */}
              </Box>

              {diets.length === 0 && !loadingData && (
                <Typography sx={{ textAlign: 'center', color: colors.textSecondary, py: 4 }}>Nenhum plano de dieta cadastrado para {selectedAnimal.name}.</Typography>
              )}

              {diets.length > 0 && (
                <>
                  <TableContainer sx={{ borderRadius: 1.5, border: `1px solid ${colors.borderColor}` }}>
                    <Table sx={{ minWidth: 700 }} aria-label="tabela de dietas">
                      <TableHead sx={{ backgroundColor: colors.tableHeader }}>
                        <TableRow>
                          <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold', py: 1.5 }}>Tipo</TableCell>
                          <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold', py: 1.5 }}>Objetivo</TableCell>
                          <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold', py: 1.5 }}>Início</TableCell>
                          <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold', py: 1.5 }}>Fim</TableCell>
                          <TableCell sx={{ color: colors.textPrimary, fontWeight: 'bold', py: 1.5 }} align="center">Status</TableCell>
                          <TableCell align="right" sx={{ color: colors.textPrimary, fontWeight: 'bold', py: 1.5, pr: 2.5 }}>Ações</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {filteredDiets.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((diet) => (
                          <TableRow key={diet.id} hover sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                            <TableCell sx={{ py: 1 }}>{diet.tipo || '-'}</TableCell>
                            <TableCell sx={{ py: 1 }}>{diet.objetivo || '-'}</TableCell>
                            <TableCell sx={{ py: 1 }}>{diet.data_inicio ? new Date(diet.data_inicio).toLocaleDateString() : '-'}</TableCell>
                            <TableCell sx={{ py: 1 }}>{diet.data_fim ? new Date(diet.data_fim).toLocaleDateString() : 'Em andamento'}</TableCell>
                            <TableCell sx={{ py: 1 }} align="center">
                              <Chip
                                label={diet.status || '-'}
                                size="small"
                                color={diet.status === 'ativa' ? 'success' : diet.status === 'finalizada' ? 'default' : 'warning'}
                                sx={{ fontWeight: '500', minWidth: '80px' }}
                              />
                            </TableCell>
                            <TableCell align="right" sx={{ py: 0.5, pr: 1.5 }}>
                              <Tooltip title="Visualizar Detalhes">
                                <IconButton size="small" sx={{ color: colors.primaryAction, mr: 0.5, '&:hover': { backgroundColor: 'rgba(157, 184, 178, 0.1)' } }} onClick={() => handleOpenViewDietModal(diet)}>
                                  <VisibilityIcon fontSize="small" />
                                </IconButton>
                              </Tooltip>
                              <Tooltip title="Editar Dieta">
                                <IconButton size="small" sx={{ color: colors.secondaryAction, '&:hover': { color: colors.secondaryActionHover, backgroundColor: 'rgba(207, 224, 195, 0.15)' }, mr: 0.5 }} onClick={() => handleOpenEditDietModal(diet)}>
                                  <EditIcon fontSize="small" />
                                </IconButton>
                              </Tooltip>
                              <Tooltip title="Excluir Dieta">
                                <IconButton size="small" sx={{ color: colors.deleteColor, '&:hover': { color: colors.deleteColorHover, backgroundColor: 'rgba(229, 115, 115, 0.1)' } }} onClick={() => handleDeleteDiet(diet.id)}>
                                  <DeleteIcon fontSize="small" />
                                </IconButton>
                              </Tooltip>
                            </TableCell>
                          </TableRow>
                        ))}
                        {filteredDiets.length === 0 && searchTermDiets && (
                          <TableRow>
                            <TableCell colSpan={6} sx={{ textAlign: 'center', py: 4, color: colors.textSecondary }}>
                              Nenhuma dieta encontrada com o termo "{searchTermDiets}".
                            </TableCell>
                          </TableRow>
                        )}
                      </TableBody>
                    </Table>
                  </TableContainer>
                  <TablePagination
                    rowsPerPageOptions={[5, 10, 25]}
                    component="div"
                    count={filteredDiets.length}
                    rowsPerPage={rowsPerPage}
                    page={page}
                    onPageChange={handleChangePageDiets}
                    onRowsPerPageChange={handleChangeRowsPerPageDiets}
                    labelRowsPerPage="Dietas por página:"
                    labelDisplayedRows={({ from, to, count }) => `${from}–${to} de ${count !== -1 ? count : `mais de ${to}`}`}
                    sx={{ borderTop: `1px solid ${colors.borderColor}`, mt: 0, borderBottomLeftRadius: '8px', borderBottomRightRadius: '8px', backgroundColor: colors.paperBackground }}
                  />
                </>
              )}
            </Paper>
          )}

          {/* Grupo 7: Gerenciamento de Alimentos Restritos (Renderiza quando currentTab === 1) */}
          {currentTab === 1 && (
            <Paper elevation={2} sx={{ p: { xs: 1.5, md: 2.5 }, borderRadius: 2, backgroundColor: colors.paperBackground }}>
              <Typography variant="h6" sx={{ mb: 2, color: colors.textPrimary }}>Alimentos a Evitar</Typography>
              {/* Exibir erro geral da aba aqui */}
              {errorRestricted && !loadingRestricted && <Alert severity="error" sx={{ my: 2 }}>{errorRestricted}</Alert>}

              {/* Formulário Inline para Adicionar */}
              {!loadingRestricted && (
                <Paper elevation={2} sx={{ p: 2, mb: 3, backgroundColor: colors.background }}>
                  <Typography variant="subtitle1" sx={{ mb: 1.5, fontWeight: '500' }}>Adicionar Novo Alimento Restrito</Typography>
                  <Grid container spacing={2} alignItems="flex-start"> { /* Mudar para flex-start */}
                    <Grid item xs={12} sm={5}>
                      <TextField
                        fullWidth
                        size="small"
                        label="Nome do Alimento"
                        name="nome"
                        value={newRestrictedFood.nome}
                        onChange={handleRestrictedInputChange}
                        disabled={loadingRestricted || !!editingRestrictedFoodId} // Desabilitar se estiver editando outro item
                        error={!newRestrictedFood.nome && !!errorRestricted} // Exemplo de erro inline
                        helperText={!newRestrictedFood.nome && !!errorRestricted ? "Nome obrigatório" : ""}
                      />
                    </Grid>
                    <Grid item xs={12} sm={5}>
                      <TextField
                        fullWidth
                        size="small"
                        label="Motivo (Opcional)"
                        name="motivo"
                        value={newRestrictedFood.motivo}
                        onChange={handleRestrictedInputChange}
                        disabled={loadingRestricted || !!editingRestrictedFoodId}
                      />
                    </Grid>
                    <Grid item xs={12} sm={2} sx={{ textAlign: { xs: 'left', sm: 'right' }, pt: { xs: 1, sm: 'inherit' } }}> { /* Ajustar padding/align */}
                      <Button
                        variant="contained"
                        startIcon={<AddIcon />}
                        onClick={handleAddRestrictedFood}
                        disabled={loadingRestricted || !newRestrictedFood.nome || !!editingRestrictedFoodId}
                        size="small"
                        sx={{ backgroundColor: colors.secondaryAction, color: colors.textPrimary, '&:hover': { backgroundColor: colors.secondaryActionHover } }}
                      >
                        Adicionar
                      </Button>
                    </Grid>
                  </Grid>
                </Paper>
              )}

              {/* Indicador de loading da tabela */}
              {loadingRestricted && <Box sx={{ display: 'flex', justifyContent: 'center', my: 3 }}><CircularProgress sx={{ color: colors.primaryAction }} /></Box>}

              {/* Tabela de Alimentos Restritos */}
              {!loadingRestricted && !errorRestricted && restrictedFoods.length === 0 && (
                <Typography sx={{ textAlign: 'center', color: colors.textSecondary, my: 3 }}>Nenhum alimento restrito cadastrado.</Typography>
              )}
              {!loadingRestricted && restrictedFoods.length > 0 && (
                <TableContainer component={Paper} elevation={1} sx={{ border: `1px solid ${colors.borderColor}` }}>
                  <Table size="small">
                    <TableHead sx={{ backgroundColor: colors.background }}>
                      <TableRow>
                        <TableCell sx={{ fontWeight: 'bold' }}>Alimento</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>Motivo</TableCell>
                        <TableCell sx={{ fontWeight: 'bold', textAlign: 'right' }}>Ações</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {restrictedFoods.map((food) => (
                        <TableRow key={food.id} hover sx={{ backgroundColor: editingRestrictedFoodId === food.id ? colors.tabBackgroundHover : 'inherit' }}>
                          {editingRestrictedFoodId === food.id ? (
                            <>
                              {/* Modo de Edição */}
                              <TableCell sx={{ py: 0.5, width: '40%' }}> { /* Ajustar padding/width */}
                                <TextField
                                  size="small"
                                  name="nome"
                                  value={editRestrictedFoodData.nome}
                                  onChange={handleEditRestrictedInputChange}
                                  fullWidth
                                  error={!editRestrictedFoodData.nome}
                                  sx={{ backgroundColor: colors.paperBackground }}
                                />
                              </TableCell>
                              <TableCell sx={{ py: 0.5, width: '40%' }}>
                                <TextField
                                  size="small"
                                  name="motivo"
                                  value={editRestrictedFoodData.motivo}
                                  onChange={handleEditRestrictedInputChange}
                                  fullWidth
                                  sx={{ backgroundColor: colors.paperBackground }}
                                />
                              </TableCell>
                              <TableCell align="right" sx={{ whiteSpace: 'nowrap', py: 0.5 }}>
                                <Tooltip title="Salvar">
                                  <IconButton size="small" onClick={() => handleSaveEditRestricted(food.id)} disabled={loadingRestricted || !editRestrictedFoodData.nome} sx={{ color: 'green', mr: 0.5 }}>
                                    <SaveIcon fontSize="small" />
                                  </IconButton>
                                </Tooltip>
                                <Tooltip title="Cancelar">
                                  <IconButton size="small" onClick={handleCancelEditRestricted} disabled={loadingRestricted} sx={{ color: colors.textSecondary }}>
                                    <CancelIcon fontSize="small" />
                                  </IconButton>
                                </Tooltip>
                              </TableCell>
                            </>
                          ) : (
                            <>
                              {/* Modo de Visualização */}
                              <TableCell>{food.nome}</TableCell>
                              <TableCell>{food.motivo || '-'}</TableCell>
                              <TableCell align="right" sx={{ whiteSpace: 'nowrap' }}>
                                <Tooltip title="Editar">
                                  <IconButton size="small" onClick={() => handleStartEditRestricted(food)} sx={{ color: colors.secondaryAction, '&:hover': { color: colors.secondaryActionHover }, mr: 0.5 }} disabled={loadingRestricted || !!editingRestrictedFoodId}>
                                    <EditIcon fontSize="small" />
                                  </IconButton>
                                </Tooltip>
                                <Tooltip title="Excluir">
                                  <IconButton size="small" onClick={() => handleDeleteRestrictedFood(food.id)} sx={{ color: colors.deleteColor, '&:hover': { color: colors.deleteColorHover } }} disabled={loadingRestricted || !!editingRestrictedFoodId}>
                                    <DeleteIcon fontSize="small" />
                                  </IconButton>
                                </Tooltip>
                              </TableCell>
                            </>
                          )}
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </Paper>
          )}

          {/* Grupo 8: Gerenciamento de Snacks (Renderiza quando currentTab === 2) */}
          {currentTab === 2 && (
            <Paper elevation={2} sx={{ p: { xs: 1.5, md: 2.5 }, borderRadius: 2, backgroundColor: colors.paperBackground }}>
              <Typography variant="h6" sx={{ mb: 2, color: colors.textPrimary }}>Snacks Permitidos</Typography>
              {/* Exibir erro geral da aba aqui */}
              {errorSnacks && !loadingSnacks && <Alert severity="error" sx={{ my: 2 }}>{errorSnacks}</Alert>}

              {/* Formulário Inline para Adicionar Snack */}
              {!loadingSnacks && (
                <Paper elevation={2} sx={{ p: 2, mb: 3, backgroundColor: colors.background }}>
                  <Typography variant="subtitle1" sx={{ mb: 1.5, fontWeight: '500' }}>Adicionar Novo Snack</Typography>
                  <Grid container spacing={2} alignItems="flex-start">
                    <Grid item xs={12} sm={6} md={3}>
                      <TextField
                        fullWidth size="small" label="Nome do Snack"
                        name="nome" value={newSnack.nome}
                        onChange={handleSnackInputChange}
                        disabled={loadingSnacks || !!editingSnackId}
                        error={!newSnack.nome && !!errorSnacks}
                        helperText={!newSnack.nome && !!errorSnacks ? "Nome obrigatório" : ""}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6} md={2}>
                      <TextField
                        fullWidth size="small" label="Frequência"
                        name="frequencia" value={newSnack.frequencia}
                        onChange={handleSnackInputChange}
                        disabled={loadingSnacks || !!editingSnackId}
                        placeholder="Ex: Diária, 2x/semana"
                      />
                    </Grid>
                    <Grid item xs={12} sm={6} md={2}>
                      <TextField
                        fullWidth size="small" label="Quantidade"
                        name="quantidade" value={newSnack.quantidade}
                        onChange={handleSnackInputChange}
                        disabled={loadingSnacks || !!editingSnackId}
                        placeholder="Ex: 1 unidade, 10g"
                      />
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                      <TextField
                        fullWidth size="small" label="Observações"
                        name="observacoes" value={newSnack.observacoes}
                        onChange={handleSnackInputChange}
                        disabled={loadingSnacks || !!editingSnackId}
                      />
                    </Grid>
                    <Grid item xs={12} md={2} sx={{ textAlign: { xs: 'left', md: 'right' }, pt: { xs: 1, md: 'inherit' } }}>
                      <Button
                        variant="contained" startIcon={<AddIcon />}
                        onClick={handleAddSnack}
                        disabled={loadingSnacks || !newSnack.nome || !!editingSnackId}
                        size="small"
                        sx={{ backgroundColor: colors.secondaryAction, color: colors.textPrimary, '&:hover': { backgroundColor: colors.secondaryActionHover } }}
                      >
                        Adicionar
                      </Button>
                    </Grid>
                  </Grid>
                </Paper>
              )}

              {/* Indicador de loading da tabela */}
              {loadingSnacks && <Box sx={{ display: 'flex', justifyContent: 'center', my: 3 }}><CircularProgress sx={{ color: colors.primaryAction }} /></Box>}

              {/* Tabela de Snacks */}
              {!loadingSnacks && !errorSnacks && snacks.length === 0 && (
                <Typography sx={{ textAlign: 'center', color: colors.textSecondary, my: 3 }}>Nenhum snack permitido cadastrado.</Typography>
              )}
              {!loadingSnacks && snacks.length > 0 && (
                <TableContainer component={Paper} elevation={1} sx={{ border: `1px solid ${colors.borderColor}` }}>
                  <Table size="small">
                    <TableHead sx={{ backgroundColor: colors.background }}>
                      <TableRow>
                        <TableCell sx={{ fontWeight: 'bold' }}>Snack</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>Frequência</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>Quantidade</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>Observações</TableCell>
                        <TableCell sx={{ fontWeight: 'bold', textAlign: 'right' }}>Ações</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {snacks.map((snack) => (
                        <TableRow key={snack.id} hover sx={{ backgroundColor: editingSnackId === snack.id ? colors.tabBackgroundHover : 'inherit' }}>
                          {editingSnackId === snack.id ? (
                            <>
                              {/* Modo de Edição */}
                              <TableCell sx={{ py: 0.5 }}><TextField size="small" name="nome" value={editSnackData.nome} onChange={handleEditSnackInputChange} fullWidth error={!editSnackData.nome} sx={{ backgroundColor: colors.paperBackground }} /></TableCell>
                              <TableCell sx={{ py: 0.5 }}><TextField size="small" name="frequencia" value={editSnackData.frequencia} onChange={handleEditSnackInputChange} fullWidth sx={{ backgroundColor: colors.paperBackground }} /></TableCell>
                              <TableCell sx={{ py: 0.5 }}><TextField size="small" name="quantidade" value={editSnackData.quantidade} onChange={handleEditSnackInputChange} fullWidth sx={{ backgroundColor: colors.paperBackground }} /></TableCell>
                              <TableCell sx={{ py: 0.5 }}><TextField size="small" name="observacoes" value={editSnackData.observacoes} onChange={handleEditSnackInputChange} fullWidth sx={{ backgroundColor: colors.paperBackground }} /></TableCell>
                              <TableCell align="right" sx={{ whiteSpace: 'nowrap', py: 0.5 }}>
                                <Tooltip title="Salvar">
                                  <IconButton size="small" onClick={() => handleSaveEditSnack(snack.id)} disabled={loadingSnacks || !editSnackData.nome} sx={{ color: 'green', mr: 0.5 }}><SaveIcon fontSize="small" /></IconButton>
                                </Tooltip>
                                <Tooltip title="Cancelar">
                                  <IconButton size="small" onClick={handleCancelEditSnack} disabled={loadingSnacks} sx={{ color: colors.textSecondary }}><CancelIcon fontSize="small" /></IconButton>
                                </Tooltip>
                              </TableCell>
                            </>
                          ) : (
                            <>
                              {/* Modo de Visualização */}
                              <TableCell>{snack.nome}</TableCell>
                              <TableCell>{snack.frequencia || '-'}</TableCell>
                              <TableCell>{snack.quantidade || '-'}</TableCell>
                              <TableCell>{snack.observacoes || '-'}</TableCell>
                              <TableCell align="right" sx={{ whiteSpace: 'nowrap' }}>
                                <Tooltip title="Editar">
                                  <IconButton size="small" onClick={() => handleStartEditSnack(snack)} sx={{ color: colors.secondaryAction, '&:hover': { color: colors.secondaryActionHover }, mr: 0.5 }} disabled={loadingSnacks || !!editingSnackId}><EditIcon fontSize="small" /></IconButton>
                                </Tooltip>
                                <Tooltip title="Excluir">
                                  <IconButton size="small" onClick={() => handleDeleteSnack(snack.id)} sx={{ color: colors.deleteColor, '&:hover': { color: colors.deleteColorHover } }} disabled={loadingSnacks || !!editingSnackId}><DeleteIcon fontSize="small" /></IconButton>
                                </Tooltip>
                              </TableCell>
                            </>
                          )}
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </Paper>
          )}
        </Box>
      )}

      {/* Modais (Serão adicionados aqui) */}
      {selectedAnimal && (
        <DietFormModal
          open={openDietFormModal}
          onClose={handleCloseDietFormModal}
          animalId={selectedAnimal.id} // Passar o ID do animal selecionado
          dietData={selectedDiet}
          isEditing={isEditingDiet}
          onSaveSuccess={handleSaveDietSuccess}
        />
      )}
      {openDietDetailsModal && selectedDiet && (
        <DietDetailsModal
          open={openDietDetailsModal}
          onClose={handleCloseDietDetailsModal}
          diet={selectedDiet}
          onEdit={handleOpenEditDietModal}
          onDelete={handleDeleteDiet}
          onAddOption={handleOpenAddOptionModal}
          onEditOption={handleOpenEditOptionModal}
          onDeleteOption={handleDeleteOption}
          onAddFood={handleOpenAddFoodModal}
          onEditFood={handleOpenEditFoodModal}
          onDeleteFood={handleDeleteFood}
        />
      )}
      <DietOptionFormModal
        open={openOptionFormModal}
        onClose={handleCloseOptionFormModal}
        dietId={selectedDietIdForOption}
        optionData={selectedOptionData}
        isEditing={isEditingOption}
        onSaveSuccess={handleSaveOptionSuccess}
      />
      <DietFoodFormModal
        open={openFoodFormModal}
        onClose={handleCloseFoodFormModal}
        dietOptionId={selectedOptionIdForFood}
        foodData={selectedFoodData}
        isEditing={isEditingFood}
        onSaveSuccess={handleSaveFoodSuccess}
      />

    </Container>
  );
};

export default DietsPage; 