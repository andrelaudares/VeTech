import { useState, useEffect } from 'react';
import { useClientAuth } from '../contexts/ClientAuthContext';
import { clientAuthService } from '../services/clientAuthService';

const ClientAnimalsPage = () => {
  const { client } = useClientAuth();
  const [animals, setAnimals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedAnimal, setSelectedAnimal] = useState(null);

  useEffect(() => {
    const loadAnimals = async () => {
      try {
        const animalsData = await clientAuthService.getAnimals();
        setAnimals(animalsData);
      } catch (error) {
        console.error('Erro ao carregar animais:', error);
      } finally {
        setLoading(false);
      }
    };

    loadAnimals();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Meus Pets</h1>
              <p className="text-gray-600">Gerencie as informações dos seus pets</p>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">{client?.name}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {animals.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {animals.map((animal) => (
              <div key={animal.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div className="p-6">
                  <div className="flex items-center space-x-4 mb-4">
                    <div className="h-16 w-16 rounded-full bg-blue-100 flex items-center justify-center">
                      <span className="text-blue-600 font-bold text-xl">
                        {animal.name?.charAt(0)?.toUpperCase()}
                      </span>
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{animal.name}</h3>
                      <p className="text-gray-600">{animal.species} • {animal.breed}</p>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Idade:</span>
                      <span className="text-sm font-medium">{animal.age} anos</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Peso:</span>
                      <span className="text-sm font-medium">{animal.weight} kg</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-500">Sexo:</span>
                      <span className="text-sm font-medium">{animal.gender}</span>
                    </div>
                  </div>

                  {animal.medical_conditions && (
                    <div className="mt-4">
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Condições Médicas:</h4>
                      <p className="text-sm text-gray-600 bg-yellow-50 p-2 rounded">
                        {animal.medical_conditions}
                      </p>
                    </div>
                  )}

                  <div className="mt-6">
                    <button
                      onClick={() => setSelectedAnimal(animal)}
                      className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
                    >
                      Ver Detalhes
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="mx-auto h-24 w-24 text-gray-400">
              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <h3 className="mt-4 text-lg font-medium text-gray-900">Nenhum pet cadastrado</h3>
            <p className="mt-2 text-gray-500">
              Você ainda não possui pets cadastrados no sistema.
            </p>
          </div>
        )}
      </div>

      {/* Modal de Detalhes */}
      {selectedAnimal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-bold text-gray-900">
                  Detalhes de {selectedAnimal.name}
                </h3>
                <button
                  onClick={() => setSelectedAnimal(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Nome</label>
                    <p className="mt-1 text-sm text-gray-900">{selectedAnimal.name}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Espécie</label>
                    <p className="mt-1 text-sm text-gray-900">{selectedAnimal.species}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Raça</label>
                    <p className="mt-1 text-sm text-gray-900">{selectedAnimal.breed}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Idade</label>
                    <p className="mt-1 text-sm text-gray-900">{selectedAnimal.age} anos</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Peso</label>
                    <p className="mt-1 text-sm text-gray-900">{selectedAnimal.weight} kg</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Sexo</label>
                    <p className="mt-1 text-sm text-gray-900">{selectedAnimal.gender}</p>
                  </div>
                </div>

                {selectedAnimal.medical_conditions && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Condições Médicas</label>
                    <p className="mt-1 text-sm text-gray-900 bg-yellow-50 p-3 rounded">
                      {selectedAnimal.medical_conditions}
                    </p>
                  </div>
                )}

                {selectedAnimal.notes && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Observações</label>
                    <p className="mt-1 text-sm text-gray-900 bg-gray-50 p-3 rounded">
                      {selectedAnimal.notes}
                    </p>
                  </div>
                )}
              </div>

              <div className="mt-6 flex justify-end">
                <button
                  onClick={() => setSelectedAnimal(null)}
                  className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded"
                >
                  Fechar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClientAnimalsPage;