import React, { createContext, useState, useContext, useCallback } from 'react';
import animalService from '../services/animalService'; // Certifique-se que este serviço existe e tem o método getAnimals
import { useAuth } from './AuthContext'; // Para obter o token ou clinic_id, se necessário para o serviço

const AnimalContext = createContext();

export const AnimalProvider = ({ children }) => {
  const [animals, setAnimals] = useState([]);
  const [selectedAnimal, setSelectedAnimal] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { user } = useAuth(); // Para garantir que o usuário está logado antes de buscar

  const fetchAnimals = useCallback(async () => {
    if (!user) return; // Não busca se não houver usuário logado

    setLoading(true);
    setError(null);
    try {
      // Assumindo que animalService.getAnimals() busca os animais da clínica logada
      // Se o seu animalService.getAnimals precisar do token/clinic_id, ele deve obtê-lo internamente ou via AuthContext
      const response = await animalService.getAnimals(); 
      setAnimals(response.data || []); // Ajuste conforme a estrutura da sua API response
    } catch (err) {
      console.error("Erro ao buscar animais no AnimalContext:", err);
      setError(err.response?.data?.detail || "Não foi possível carregar os animais.");
      setAnimals([]); // Limpa os animais em caso de erro
    }
    setLoading(false);
  }, [user]); // Dependência do usuário para re-buscar se o usuário mudar (login/logout)

  return (
    <AnimalContext.Provider value={{ 
        animals, 
        selectedAnimal, 
        setSelectedAnimal, 
        fetchAnimals, 
        loading,
        error
    }}>
      {children}
    </AnimalContext.Provider>
  );
};

export const useAnimal = () => useContext(AnimalContext); 