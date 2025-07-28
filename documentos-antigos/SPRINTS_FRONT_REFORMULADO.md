# SPRINTS FRONTEND REFORMULADO - ÁREA DO CLIENTE VETECH

## CONTEXTO DO PROJETO

### Objetivo Principal
Desenvolver uma área do cliente completa e integrada ao sistema VeTech existente, permitindo que tutores de animais acessem informações, gerenciem dietas/atividades e interajam com a clínica de forma gamificada.

### Estrutura Frontend Atual
- **Framework**: React com Vite
- **Roteamento**: React Router
- **Estado**: Context API + useState/useEffect
- **Estilização**: CSS Modules + Tailwind CSS
- **Autenticação**: JWT com Supabase
- **Estrutura**: `/frontend/app/src/`

### Integração com Backend
- **API Base**: `/api/client/` (nova área)
- **Autenticação**: JWT separado para clientes
- **Dados**: Integração com tabelas existentes via endpoints específicos

---

## SPRINT 1: INFRAESTRUTURA E AUTENTICAÇÃO DO CLIENTE

### Objetivos
- Criar estrutura base da área do cliente
- Implementar sistema de autenticação separado
- Estabelecer roteamento e layout específico

### Entregáveis Frontend

#### 1. Estrutura de Diretórios
```
/frontend/app/src/
├── client/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── ClientLayout.jsx
│   │   │   ├── ClientHeader.jsx
│   │   │   ├── ClientSidebar.jsx
│   │   │   └── ClientFooter.jsx
│   │   ├── auth/
│   │   │   ├── ClientLogin.jsx
│   │   │   ├── ClientRegister.jsx
│   │   │   └── ClientAuthGuard.jsx
│   │   └── common/
│   │       ├── LoadingSpinner.jsx
│   │       ├── ErrorMessage.jsx
│   │       └── SuccessMessage.jsx
│   ├── pages/
│   │   ├── ClientDashboard.jsx
│   │   ├── ClientProfile.jsx
│   │   ├── ClientDiets.jsx
│   │   ├── ClientActivities.jsx
│   │   ├── ClientAppointments.jsx
│   │   └── ClientHistory.jsx
│   ├── contexts/
│   │   └── ClientAuthContext.jsx
│   ├── services/
│   │   ├── clientAuthService.js
│   │   ├── clientApiService.js
│   │   └── clientStorageService.js
│   ├── hooks/
│   │   ├── useClientAuth.js
│   │   ├── useClientData.js
│   │   └── useClientNotifications.js
│   └── utils/
│       ├── clientValidation.js
│       ├── clientFormatters.js
│       └── clientConstants.js
```

#### 2. Sistema de Autenticação do Cliente

**ClientAuthContext.jsx**
```jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { clientAuthService } from '../services/clientAuthService';

const ClientAuthContext = createContext();

export const useClientAuth = () => {
  const context = useContext(ClientAuthContext);
  if (!context) {
    throw new Error('useClientAuth must be used within ClientAuthProvider');
  }
  return context;
};

export const ClientAuthProvider = ({ children }) => {
  const [client, setClient] = useState(null);
  const [animal, setAnimal] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('client_token');
      if (token) {
        const clientData = await clientAuthService.validateToken(token);
        setClient(clientData.client);
        setAnimal(clientData.animal);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      setLoading(true);
      setError(null);
      const response = await clientAuthService.login(email, password);
      
      localStorage.setItem('client_token', response.token);
      setClient(response.client);
      setAnimal(response.animal);
      
      return response;
    } catch (error) {
      setError(error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('client_token');
    setClient(null);
    setAnimal(null);
    setError(null);
  };

  const value = {
    client,
    animal,
    loading,
    error,
    login,
    logout,
    isAuthenticated: !!client
  };

  return (
    <ClientAuthContext.Provider value={value}>
      {children}
    </ClientAuthContext.Provider>
  );
};
```

**clientAuthService.js**
```javascript
const API_BASE = '/api/client';

class ClientAuthService {
  async login(email, password) {
    const response = await fetch(`${API_BASE}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Erro no login');
    }

    return response.json();
  }

  async validateToken(token) {
    const response = await fetch(`${API_BASE}/validate`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Token inválido');
    }

    return response.json();
  }

  async requestAccess(animalId, tutorData) {
    const response = await fetch(`${API_BASE}/request-access`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ animal_id: animalId, ...tutorData }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Erro na solicitação');
    }

    return response.json();
  }
}

export const clientAuthService = new ClientAuthService();
```

#### 3. Componentes de Layout

**ClientLayout.jsx**
```jsx
import React from 'react';
import { Outlet } from 'react-router-dom';
import ClientHeader from './ClientHeader';
import ClientSidebar from './ClientSidebar';
import ClientFooter from './ClientFooter';
import { useClientAuth } from '../../contexts/ClientAuthContext';

const ClientLayout = () => {
  const { animal } = useClientAuth();

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <ClientHeader />
      
      <div className="flex flex-1">
        <ClientSidebar />
        
        <main className="flex-1 p-6">
          <div className="max-w-7xl mx-auto">
            {animal && (
              <div className="mb-6 bg-white rounded-lg shadow-sm p-4">
                <h1 className="text-2xl font-bold text-gray-900">
                  Área do {animal.name}
                </h1>
                <p className="text-gray-600">
                  {animal.species} • {animal.breed} • {animal.age} anos
                </p>
              </div>
            )}
            
            <Outlet />
          </div>
        </main>
      </div>
      
      <ClientFooter />
    </div>
  );
};

export default ClientLayout;
```

#### 4. Páginas de Autenticação

**ClientLogin.jsx**
```jsx
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useClientAuth } from '../../contexts/ClientAuthContext';

const ClientLogin = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  
  const { login, loading, error } = useClientAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(formData.email, formData.password);
      navigate('/client/dashboard');
    } catch (error) {
      // Error is handled by context
    }
  };

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            VeTech Cliente
          </h1>
          <p className="text-gray-600">
            Acesse a área do seu pet
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="seu@email.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Senha
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent pr-10"
                placeholder="Sua senha"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600"
              >
                {showPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-600">
            Não tem acesso?{' '}
            <Link 
              to="/client/request-access" 
              className="text-blue-600 hover:text-blue-700 font-medium"
            >
              Solicitar acesso
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default ClientLogin;
```

#### 5. Roteamento do Cliente

**Modificação em App.jsx**
```jsx
// Adicionar rotas do cliente
import { ClientAuthProvider } from './client/contexts/ClientAuthContext';
import ClientRoutes from './client/ClientRoutes';

function App() {
  return (
    <Router>
      <Routes>
        {/* Rotas existentes da clínica */}
        <Route path="/*" element={<ClinicRoutes />} />
        
        {/* Rotas do cliente */}
        <Route path="/client/*" element={
          <ClientAuthProvider>
            <ClientRoutes />
          </ClientAuthProvider>
        } />
      </Routes>
    </Router>
  );
}
```

### Critérios de Aceitação
- [ ] Estrutura de diretórios criada
- [ ] Sistema de autenticação funcionando
- [ ] Layout responsivo implementado
- [ ] Roteamento configurado
- [ ] Integração com backend testada

---

## SPRINT 2: DASHBOARD E PERFIL DO CLIENTE

### Objetivos
- Implementar dashboard principal
- Criar página de perfil com edição
- Desenvolver componentes de visualização de dados

### Entregáveis Frontend

#### 1. Dashboard Principal

**ClientDashboard.jsx**
```jsx
import React, { useState, useEffect } from 'react';
import { useClientAuth } from '../contexts/ClientAuthContext';
import { clientApiService } from '../services/clientApiService';
import DashboardCard from '../components/common/DashboardCard';
import QuickActions from '../components/dashboard/QuickActions';
import RecentActivity from '../components/dashboard/RecentActivity';
import HealthSummary from '../components/dashboard/HealthSummary';

const ClientDashboard = () => {
  const { animal } = useClientAuth();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const data = await clientApiService.getDashboardData();
      setDashboardData(data);
    } catch (error) {
      console.error('Erro ao carregar dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>;
  }

  return (
    <div className="space-y-6">
      {/* Cards de Resumo */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <DashboardCard
          title="Próxima Consulta"
          value={dashboardData?.nextAppointment?.date || 'Nenhuma agendada'}
          icon="📅"
          color="blue"
        />
        <DashboardCard
          title="Dieta Atual"
          value={dashboardData?.currentDiet?.name || 'Não definida'}
          icon="🍽️"
          color="green"
        />
        <DashboardCard
          title="Atividades Hoje"
          value={`${dashboardData?.todayActivities || 0} atividades`}
          icon="🏃"
          color="purple"
        />
        <DashboardCard
          title="Pontos XP"
          value={dashboardData?.totalXP || 0}
          icon="⭐"
          color="yellow"
        />
      </div>

      {/* Ações Rápidas */}
      <QuickActions />

      {/* Conteúdo Principal */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <HealthSummary data={dashboardData?.healthSummary} />
        <RecentActivity activities={dashboardData?.recentActivities} />
      </div>
    </div>
  );
};

export default ClientDashboard;
```

#### 2. Página de Perfil

**ClientProfile.jsx**
```jsx
import React, { useState, useEffect } from 'react';
import { useClientAuth } from '../contexts/ClientAuthContext';
import { clientApiService } from '../services/clientApiService';
import ProfileSection from '../components/profile/ProfileSection';
import AnimalSection from '../components/profile/AnimalSection';
import SecuritySection from '../components/profile/SecuritySection';

const ClientProfile = () => {
  const { client, animal } = useClientAuth();
  const [activeTab, setActiveTab] = useState('personal');
  const [profileData, setProfileData] = useState({
    personal: {
      tutor_name: client?.tutor_name || '',
      email: client?.email || '',
      phone: client?.phone || ''
    },
    animal: {
      name: animal?.name || '',
      species: animal?.species || '',
      breed: animal?.breed || '',
      age: animal?.age || '',
      weight: animal?.weight || '',
      observations: animal?.observations || ''
    }
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  const tabs = [
    { id: 'personal', label: 'Dados Pessoais', icon: '👤' },
    { id: 'animal', label: 'Dados do Pet', icon: '🐕' },
    { id: 'security', label: 'Segurança', icon: '🔒' }
  ];

  const handleSave = async (section, data) => {
    setLoading(true);
    try {
      await clientApiService.updateProfile(section, data);
      setMessage({ type: 'success', text: 'Dados atualizados com sucesso!' });
      
      // Atualizar dados locais
      setProfileData(prev => ({
        ...prev,
        [section]: data
      }));
    } catch (error) {
      setMessage({ type: 'error', text: error.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm">
        {/* Header */}
        <div className="border-b border-gray-200 px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-900">Meu Perfil</h1>
          <p className="text-gray-600">Gerencie suas informações pessoais e do seu pet</p>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        <div className="p-6">
          {message && (
            <div className={`mb-4 p-3 rounded-lg ${
              message.type === 'success' 
                ? 'bg-green-50 text-green-700 border border-green-200'
                : 'bg-red-50 text-red-700 border border-red-200'
            }`}>
              {message.text}
            </div>
          )}

          {activeTab === 'personal' && (
            <ProfileSection
              data={profileData.personal}
              onSave={(data) => handleSave('personal', data)}
              loading={loading}
            />
          )}

          {activeTab === 'animal' && (
            <AnimalSection
              data={profileData.animal}
              onSave={(data) => handleSave('animal', data)}
              loading={loading}
            />
          )}

          {activeTab === 'security' && (
            <SecuritySection
              onSave={(data) => handleSave('security', data)}
              loading={loading}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default ClientProfile;
```

#### 3. Componentes de Dashboard

**DashboardCard.jsx**
```jsx
import React from 'react';

const DashboardCard = ({ title, value, icon, color = 'blue', onClick }) => {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-700 border-blue-200',
    green: 'bg-green-50 text-green-700 border-green-200',
    purple: 'bg-purple-50 text-purple-700 border-purple-200',
    yellow: 'bg-yellow-50 text-yellow-700 border-yellow-200',
    red: 'bg-red-50 text-red-700 border-red-200'
  };

  return (
    <div 
      className={`p-6 rounded-lg border ${colorClasses[color]} ${
        onClick ? 'cursor-pointer hover:shadow-md transition-shadow' : ''
      }`}
      onClick={onClick}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium opacity-75">{title}</p>
          <p className="text-2xl font-bold mt-1">{value}</p>
        </div>
        <div className="text-3xl">{icon}</div>
      </div>
    </div>
  );
};

export default DashboardCard;
```

### Critérios de Aceitação
- [ ] Dashboard funcional com dados reais
- [ ] Perfil editável implementado
- [ ] Componentes reutilizáveis criados
- [ ] Interface responsiva
- [ ] Validação de formulários

---

## SPRINT 3: SISTEMA DE DIETAS GAMIFICADO

### Objetivos
- Implementar visualização de dietas
- Criar sistema de registro diário
- Desenvolver gamificação com XP e conquistas

### Entregáveis Frontend

#### 1. Página Principal de Dietas

**ClientDiets.jsx**
```jsx
import React, { useState, useEffect } from 'react';
import { clientApiService } from '../services/clientApiService';
import DietPlanCard from '../components/diets/DietPlanCard';
import DietProgress from '../components/diets/DietProgress';
import DietCalendar from '../components/diets/DietCalendar';
import DietLogger from '../components/diets/DietLogger';
import GameificationPanel from '../components/gamification/GameificationPanel';

const ClientDiets = () => {
  const [currentDiet, setCurrentDiet] = useState(null);
  const [availableDiets, setAvailableDiets] = useState([]);
  const [progress, setProgress] = useState(null);
  const [showLogger, setShowLogger] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDietData();
  }, []);

  const loadDietData = async () => {
    try {
      const [dietsData, progressData] = await Promise.all([
        clientApiService.getDiets(),
        clientApiService.getDietProgress()
      ]);
      
      setCurrentDiet(dietsData.current);
      setAvailableDiets(dietsData.available);
      setProgress(progressData);
    } catch (error) {
      console.error('Erro ao carregar dietas:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogMeal = async (mealData) => {
    try {
      await clientApiService.logMeal(mealData);
      await loadDietData(); // Recarregar dados
      setShowLogger(false);
    } catch (error) {
      console.error('Erro ao registrar refeição:', error);
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>;
  }

  return (
    <div className="space-y-6">
      {/* Header com Gamificação */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dietas</h1>
          <p className="text-gray-600">Acompanhe a alimentação do seu pet</p>
        </div>
        <GameificationPanel type="diet" />
      </div>

      {currentDiet ? (
        <>
          {/* Dieta Atual */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Dieta Atual</h2>
              <button
                onClick={() => setShowLogger(true)}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                📝 Registrar Refeição
              </button>
            </div>
            
            <DietPlanCard diet={currentDiet} isActive={true} />
          </div>

          {/* Progresso */}
          <DietProgress progress={progress} />

          {/* Calendário */}
          <DietCalendar progress={progress} />
        </>
      ) : (
        /* Seleção de Dieta */
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">Escolha uma Dieta</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {availableDiets.map(diet => (
              <DietPlanCard
                key={diet.id}
                diet={diet}
                onSelect={() => handleSelectDiet(diet.id)}
              />
            ))}
          </div>
        </div>
      )}

      {/* Modal de Registro */}
      {showLogger && (
        <DietLogger
          diet={currentDiet}
          onSave={handleLogMeal}
          onClose={() => setShowLogger(false)}
        />
      )}
    </div>
  );
};

export default ClientDiets;
```

#### 2. Componentes de Dieta

**DietPlanCard.jsx**
```jsx
import React from 'react';

const DietPlanCard = ({ diet, isActive = false, onSelect }) => {
  return (
    <div className={`border rounded-lg p-4 ${
      isActive 
        ? 'border-green-500 bg-green-50' 
        : 'border-gray-200 hover:border-blue-300'
    }`}>
      <div className="flex justify-between items-start mb-3">
        <h3 className="font-semibold text-lg">{diet.nome}</h3>
        {isActive && (
          <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
            Ativa
          </span>
        )}
      </div>

      <div className="space-y-2 text-sm text-gray-600">
        <div className="flex justify-between">
          <span>Calorias/dia:</span>
          <span className="font-medium">{diet.calorias_totais_dia}</span>
        </div>
        <div className="flex justify-between">
          <span>Refeições:</span>
          <span className="font-medium">{diet.refeicoes_por_dia}x/dia</span>
        </div>
        <div className="flex justify-between">
          <span>Porção:</span>
          <span className="font-medium">{diet.porcao_refeicao}g</span>
        </div>
        <div className="flex justify-between">
          <span>Valor estimado:</span>
          <span className="font-medium">R$ {diet.valor_mensal_estimado}</span>
        </div>
      </div>

      {diet.indicacao && (
        <div className="mt-3 p-2 bg-blue-50 rounded text-sm text-blue-700">
          <strong>Indicação:</strong> {diet.indicacao}
        </div>
      )}

      {!isActive && onSelect && (
        <button
          onClick={onSelect}
          className="w-full mt-4 bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition-colors"
        >
          Selecionar Dieta
        </button>
      )}
    </div>
  );
};

export default DietPlanCard;
```

**DietLogger.jsx**
```jsx
import React, { useState } from 'react';

const DietLogger = ({ diet, onSave, onClose }) => {
  const [mealData, setMealData] = useState({
    meal_type: '',
    portion_given: '',
    time_given: '',
    notes: '',
    photo: null
  });

  const mealTypes = [
    { value: 'breakfast', label: 'Café da manhã' },
    { value: 'lunch', label: 'Almoço' },
    { value: 'dinner', label: 'Jantar' },
    { value: 'snack', label: 'Lanche' }
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(mealData);
  };

  const handlePhotoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setMealData(prev => ({ ...prev, photo: file }));
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold">Registrar Refeição</h3>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Tipo de Refeição
              </label>
              <select
                value={mealData.meal_type}
                onChange={(e) => setMealData(prev => ({ ...prev, meal_type: e.target.value }))}
                required
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Selecione...</option>
                {mealTypes.map(type => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Porção Oferecida (g)
              </label>
              <input
                type="number"
                value={mealData.portion_given}
                onChange={(e) => setMealData(prev => ({ ...prev, portion_given: e.target.value }))}
                required
                min="0"
                step="0.1"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500"
                placeholder={`Recomendado: ${diet.porcao_refeicao}g`}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Horário
              </label>
              <input
                type="time"
                value={mealData.time_given}
                onChange={(e) => setMealData(prev => ({ ...prev, time_given: e.target.value }))}
                required
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Observações
              </label>
              <textarea
                value={mealData.notes}
                onChange={(e) => setMealData(prev => ({ ...prev, notes: e.target.value }))}
                rows="3"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500"
                placeholder="Como o pet reagiu? Comeu tudo?"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Foto (opcional)
              </label>
              <input
                type="file"
                accept="image/*"
                onChange={handlePhotoChange}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="flex space-x-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 border border-gray-300 text-gray-700 py-2 rounded-lg hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                type="submit"
                className="flex-1 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
              >
                Registrar
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default DietLogger;
```

### Critérios de Aceitação
- [ ] Visualização de dietas implementada
- [ ] Sistema de registro funcionando
- [ ] Gamificação básica ativa
- [ ] Interface intuitiva e responsiva
- [ ] Upload de fotos funcionando

---

## SPRINT 4: SISTEMA DE ATIVIDADES E EXERCÍCIOS

### Objetivos
- Implementar gestão de atividades físicas
- Criar sistema de acompanhamento
- Integrar com gamificação

### Entregáveis Frontend

#### 1. Página de Atividades

**ClientActivities.jsx**
```jsx
import React, { useState, useEffect } from 'react';
import { clientApiService } from '../services/clientApiService';
import ActivityPlanCard from '../components/activities/ActivityPlanCard';
import ActivityTracker from '../components/activities/ActivityTracker';
import ActivityCalendar from '../components/activities/ActivityCalendar';
import ActivityLogger from '../components/activities/ActivityLogger';

const ClientActivities = () => {
  const [currentPlan, setCurrentPlan] = useState(null);
  const [availablePlans, setAvailablePlans] = useState([]);
  const [todayActivities, setTodayActivities] = useState([]);
  const [progress, setProgress] = useState(null);
  const [showLogger, setShowLogger] = useState(false);
  const [selectedActivity, setSelectedActivity] = useState(null);

  useEffect(() => {
    loadActivityData();
  }, []);

  const loadActivityData = async () => {
    try {
      const [plansData, progressData, todayData] = await Promise.all([
        clientApiService.getActivityPlans(),
        clientApiService.getActivityProgress(),
        clientApiService.getTodayActivities()
      ]);
      
      setCurrentPlan(plansData.current);
      setAvailablePlans(plansData.available);
      setProgress(progressData);
      setTodayActivities(todayData);
    } catch (error) {
      console.error('Erro ao carregar atividades:', error);
    }
  };

  const handleLogActivity = async (activityData) => {
    try {
      await clientApiService.logActivity(activityData);
      await loadActivityData();
      setShowLogger(false);
      setSelectedActivity(null);
    } catch (error) {
      console.error('Erro ao registrar atividade:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Atividades</h1>
          <p className="text-gray-600">Mantenha seu pet ativo e saudável</p>
        </div>
      </div>

      {currentPlan ? (
        <>
          {/* Plano Atual */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-xl font-semibold mb-4">Plano de Atividades</h2>
            <ActivityPlanCard plan={currentPlan} isActive={true} />
          </div>

          {/* Atividades de Hoje */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Atividades de Hoje</h2>
              <span className="text-sm text-gray-600">
                {todayActivities.filter(a => a.completed).length} de {todayActivities.length} concluídas
              </span>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {todayActivities.map(activity => (
                <div
                  key={activity.id}
                  className={`border rounded-lg p-4 ${
                    activity.completed 
                      ? 'border-green-200 bg-green-50' 
                      : 'border-gray-200'
                  }`}
                >
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-medium">{activity.name}</h3>
                    {activity.completed && (
                      <span className="text-green-600">✓</span>
                    )}
                  </div>
                  
                  <div className="text-sm text-gray-600 space-y-1">
                    <div>Duração: {activity.duration} min</div>
                    <div>Intensidade: {activity.intensity}</div>
                  </div>

                  {!activity.completed && (
                    <button
                      onClick={() => {
                        setSelectedActivity(activity);
                        setShowLogger(true);
                      }}
                      className="mt-3 w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition-colors"
                    >
                      Registrar Atividade
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Progresso Semanal */}
          <ActivityTracker progress={progress} />

          {/* Calendário */}
          <ActivityCalendar progress={progress} />
        </>
      ) : (
        /* Seleção de Plano */
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">Escolha um Plano de Atividades</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {availablePlans.map(plan => (
              <ActivityPlanCard
                key={plan.id}
                plan={plan}
                onSelect={() => handleSelectPlan(plan.id)}
              />
            ))}
          </div>
        </div>
      )}

      {/* Modal de Registro */}
      {showLogger && selectedActivity && (
        <ActivityLogger
          activity={selectedActivity}
          onSave={handleLogActivity}
          onClose={() => {
            setShowLogger(false);
            setSelectedActivity(null);
          }}
        />
      )}
    </div>
  );
};

export default ClientActivities;
```

#### 2. Componentes de Atividade

**ActivityTracker.jsx**
```jsx
import React from 'react';

const ActivityTracker = ({ progress }) => {
  const weekDays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
  
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h3 className="text-lg font-semibold mb-4">Progresso da Semana</h3>
      
      {/* Estatísticas */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-600">
            {progress?.weeklyMinutes || 0}
          </div>
          <div className="text-sm text-gray-600">Minutos esta semana</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-green-600">
            {progress?.completedActivities || 0}
          </div>
          <div className="text-sm text-gray-600">Atividades concluídas</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-purple-600">
            {progress?.streak || 0}
          </div>
          <div className="text-sm text-gray-600">Dias consecutivos</div>
        </div>
      </div>

      {/* Calendário Semanal */}
      <div className="grid grid-cols-7 gap-2">
        {weekDays.map((day, index) => {
          const dayProgress = progress?.weeklyProgress?.[index] || {};
          const isCompleted = dayProgress.completed;
          const isToday = index === new Date().getDay();
          
          return (
            <div
              key={day}
              className={`text-center p-3 rounded-lg border ${
                isCompleted 
                  ? 'bg-green-100 border-green-300 text-green-700'
                  : isToday
                    ? 'bg-blue-100 border-blue-300 text-blue-700'
                    : 'bg-gray-50 border-gray-200 text-gray-600'
              }`}
            >
              <div className="text-xs font-medium">{day}</div>
              <div className="mt-1">
                {isCompleted ? '✓' : dayProgress.minutes ? `${dayProgress.minutes}min` : '-'}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ActivityTracker;
```

### Critérios de Aceitação
- [ ] Sistema de atividades funcionando
- [ ] Tracking de progresso implementado
- [ ] Interface de registro intuitiva
- [ ] Calendário de atividades
- [ ] Integração com gamificação

---

## SPRINT 5: AGENDAMENTOS E COMUNICAÇÃO

### Objetivos
- Implementar sistema de agendamentos
- Criar comunicação com a clínica
- Desenvolver notificações

### Entregáveis Frontend

#### 1. Página de Agendamentos

**ClientAppointments.jsx**
```jsx
import React, { useState, useEffect } from 'react';
import { clientApiService } from '../services/clientApiService';
import AppointmentCard from '../components/appointments/AppointmentCard';
import AppointmentRequest from '../components/appointments/AppointmentRequest';
import AppointmentCalendar from '../components/appointments/AppointmentCalendar';

const ClientAppointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [availableSlots, setAvailableSlots] = useState([]);
  const [showRequestForm, setShowRequestForm] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAppointments();
  }, []);

  const loadAppointments = async () => {
    try {
      const [appointmentsData, slotsData] = await Promise.all([
        clientApiService.getAppointments(),
        clientApiService.getAvailableSlots()
      ]);
      
      setAppointments(appointmentsData);
      setAvailableSlots(slotsData);
    } catch (error) {
      console.error('Erro ao carregar agendamentos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRequestAppointment = async (requestData) => {
    try {
      await clientApiService.requestAppointment(requestData);
      await loadAppointments();
      setShowRequestForm(false);
    } catch (error) {
      console.error('Erro ao solicitar agendamento:', error);
    }
  };

  const handleCancelAppointment = async (appointmentId) => {
    if (confirm('Tem certeza que deseja cancelar este agendamento?')) {
      try {
        await clientApiService.cancelAppointment(appointmentId);
        await loadAppointments();
      } catch (error) {
        console.error('Erro ao cancelar agendamento:', error);
      }
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Agendamentos</h1>
          <p className="text-gray-600">Gerencie as consultas do seu pet</p>
        </div>
        <button
          onClick={() => setShowRequestForm(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          📅 Solicitar Consulta
        </button>
      </div>

      {/* Próximas Consultas */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-semibold mb-4">Próximas Consultas</h2>
        {appointments.filter(apt => apt.status === 'confirmed' && new Date(apt.date) >= new Date()).length > 0 ? (
          <div className="space-y-4">
            {appointments
              .filter(apt => apt.status === 'confirmed' && new Date(apt.date) >= new Date())
              .map(appointment => (
                <AppointmentCard
                  key={appointment.id}
                  appointment={appointment}
                  onCancel={handleCancelAppointment}
                />
              ))}
          </div>
        ) : (
          <p className="text-gray-600">Nenhuma consulta agendada</p>
        )}
      </div>

      {/* Solicitações Pendentes */}
      {appointments.filter(apt => apt.status === 'pending').length > 0 && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">Solicitações Pendentes</h2>
          <div className="space-y-4">
            {appointments
              .filter(apt => apt.status === 'pending')
              .map(appointment => (
                <AppointmentCard
                  key={appointment.id}
                  appointment={appointment}
                  onCancel={handleCancelAppointment}
                />
              ))}
          </div>
        </div>
      )}

      {/* Histórico */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-semibold mb-4">Histórico de Consultas</h2>
        {appointments.filter(apt => apt.status === 'completed' || new Date(apt.date) < new Date()).length > 0 ? (
          <div className="space-y-4">
            {appointments
              .filter(apt => apt.status === 'completed' || new Date(apt.date) < new Date())
              .slice(0, 5)
              .map(appointment => (
                <AppointmentCard
                  key={appointment.id}
                  appointment={appointment}
                  isHistory={true}
                />
              ))}
          </div>
        ) : (
          <p className="text-gray-600">Nenhuma consulta no histórico</p>
        )}
      </div>

      {/* Modal de Solicitação */}
      {showRequestForm && (
        <AppointmentRequest
          availableSlots={availableSlots}
          onSubmit={handleRequestAppointment}
          onClose={() => setShowRequestForm(false)}
        />
      )}
    </div>
  );
};

export default ClientAppointments;
```

### Critérios de Aceitação
- [ ] Sistema de agendamentos funcionando
- [ ] Solicitação de consultas implementada
- [ ] Histórico de consultas visível
- [ ] Cancelamento de agendamentos
- [ ] Interface responsiva

---

## SPRINT 6: GAMIFICAÇÃO AVANÇADA E FINALIZAÇÃO

### Objetivos
- Implementar sistema completo de gamificação
- Criar sistema de conquistas e badges
- Finalizar integração e testes

### Entregáveis Frontend

#### 1. Sistema de Gamificação

**GameificationPanel.jsx**
```jsx
import React, { useState, useEffect } from 'react';
import { clientApiService } from '../../services/clientApiService';

const GameificationPanel = ({ type = 'general' }) => {
  const [gameData, setGameData] = useState(null);
  const [showAchievements, setShowAchievements] = useState(false);

  useEffect(() => {
    loadGameData();
  }, [type]);

  const loadGameData = async () => {
    try {
      const data = await clientApiService.getGameificationData(type);
      setGameData(data);
    } catch (error) {
      console.error('Erro ao carregar dados de gamificação:', error);
    }
  };

  if (!gameData) return null;

  return (
    <div className="bg-gradient-to-r from-purple-500 to-blue-600 text-white rounded-lg p-4">
      <div className="flex items-center justify-between mb-3">
        <div>
          <h3 className="font-bold text-lg">Nível {gameData.level}</h3>
          <p className="text-sm opacity-90">{gameData.title}</p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold">{gameData.totalXP}</div>
          <div className="text-xs opacity-90">XP Total</div>
        </div>
      </div>

      {/* Barra de Progresso */}
      <div className="mb-3">
        <div className="flex justify-between text-xs mb-1">
          <span>{gameData.currentLevelXP} XP</span>
          <span>{gameData.nextLevelXP} XP</span>
        </div>
        <div className="w-full bg-white bg-opacity-20 rounded-full h-2">
          <div
            className="bg-white rounded-full h-2 transition-all duration-300"
            style={{ width: `${gameData.progressPercent}%` }}
          />
        </div>
      </div>

      {/* Conquistas Recentes */}
      {gameData.recentAchievements?.length > 0 && (
        <div className="mb-3">
          <div className="text-xs opacity-90 mb-1">Conquistas Recentes:</div>
          <div className="flex space-x-1">
            {gameData.recentAchievements.slice(0, 3).map(achievement => (
              <span key={achievement.id} className="text-lg" title={achievement.name}>
                {achievement.icon}
              </span>
            ))}
          </div>
        </div>
      )}

      <button
        onClick={() => setShowAchievements(true)}
        className="w-full bg-white bg-opacity-20 hover:bg-opacity-30 rounded py-2 text-sm font-medium transition-colors"
      >
        Ver Todas as Conquistas
      </button>

      {/* Modal de Conquistas */}
      {showAchievements && (
        <AchievementsModal
          achievements={gameData.allAchievements}
          onClose={() => setShowAchievements(false)}
        />
      )}
    </div>
  );
};

export default GameificationPanel;
```

#### 2. Sistema de Notificações

**NotificationCenter.jsx**
```jsx
import React, { useState, useEffect } from 'react';
import { clientApiService } from '../services/clientApiService';

const NotificationCenter = () => {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [showPanel, setShowPanel] = useState(false);

  useEffect(() => {
    loadNotifications();
    
    // Polling para novas notificações
    const interval = setInterval(loadNotifications, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadNotifications = async () => {
    try {
      const data = await clientApiService.getNotifications();
      setNotifications(data.notifications);
      setUnreadCount(data.unreadCount);
    } catch (error) {
      console.error('Erro ao carregar notificações:', error);
    }
  };

  const markAsRead = async (notificationId) => {
    try {
      await clientApiService.markNotificationAsRead(notificationId);
      await loadNotifications();
    } catch (error) {
      console.error('Erro ao marcar como lida:', error);
    }
  };

  const markAllAsRead = async () => {
    try {
      await clientApiService.markAllNotificationsAsRead();
      await loadNotifications();
    } catch (error) {
      console.error('Erro ao marcar todas como lidas:', error);
    }
  };

  return (
    <div className="relative">
      <button
        onClick={() => setShowPanel(!showPanel)}
        className="relative p-2 text-gray-600 hover:text-gray-900 transition-colors"
      >
        🔔
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {showPanel && (
        <div className="absolute right-0 top-full mt-2 w-80 bg-white rounded-lg shadow-lg border z-50">
          <div className="p-4 border-b">
            <div className="flex justify-between items-center">
              <h3 className="font-semibold">Notificações</h3>
              {unreadCount > 0 && (
                <button
                  onClick={markAllAsRead}
                  className="text-sm text-blue-600 hover:text-blue-700"
                >
                  Marcar todas como lidas
                </button>
              )}
            </div>
          </div>

          <div className="max-h-96 overflow-y-auto">
            {notifications.length > 0 ? (
              notifications.map(notification => (
                <div
                  key={notification.id}
                  className={`p-4 border-b hover:bg-gray-50 cursor-pointer ${
                    !notification.read ? 'bg-blue-50' : ''
                  }`}
                  onClick={() => !notification.read && markAsRead(notification.id)}
                >
                  <div className="flex items-start space-x-3">
                    <div className="text-2xl">{notification.icon}</div>
                    <div className="flex-1">
                      <h4 className="font-medium text-sm">{notification.title}</h4>
                      <p className="text-gray-600 text-xs mt-1">{notification.message}</p>
                      <p className="text-gray-400 text-xs mt-1">{notification.timeAgo}</p>
                    </div>
                    {!notification.read && (
                      <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                    )}
                  </div>
                </div>
              ))
            ) : (
              <div className="p-4 text-center text-gray-600">
                Nenhuma notificação
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default NotificationCenter;
```

### Critérios de Aceitação
- [ ] Sistema de gamificação completo
- [ ] Conquistas e badges funcionando
- [ ] Notificações em tempo real
- [ ] Interface polida e responsiva
- [ ] Testes de integração realizados

---

## CONSIDERAÇÕES TÉCNICAS

### Performance
- Lazy loading de componentes
- Otimização de imagens
- Cache de dados frequentes
- Debounce em buscas

### Acessibilidade
- Navegação por teclado
- Contraste adequado
- Labels descritivos
- Suporte a screen readers

### Responsividade
- Mobile-first design
- Breakpoints consistentes
- Touch-friendly interfaces
- Orientação landscape/portrait

### Segurança
- Validação client-side
- Sanitização de inputs
- Proteção contra XSS
- Headers de segurança

---

## CRONOGRAMA ESTIMADO

| Sprint | Duração | Entregáveis Principais |
|--------|---------|------------------------|
| 1 | 2 semanas | Infraestrutura e autenticação |
| 2 | 2 semanas | Dashboard e perfil |
| 3 | 2 semanas | Sistema de dietas |
| 4 | 2 semanas | Sistema de atividades |
| 5 | 2 semanas | Agendamentos |
| 6 | 2 semanas | Gamificação e finalização |

**Total: 12 semanas**

---

## PRÓXIMOS PASSOS

1. **Validação do escopo** com stakeholders
2. **Setup do ambiente** de desenvolvimento
3. **Criação dos wireframes** detalhados
4. **Início da Sprint 1** - Infraestrutura
5. **Testes contínuos** durante desenvolvimento
6. **Deploy em ambiente** de homologação
7. **Treinamento** da equipe da clínica
8. **Go-live** da área do cliente