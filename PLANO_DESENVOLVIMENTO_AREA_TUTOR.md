# PLANO DE DESENVOLVIMENTO - ÁREA DO TUTOR VETECH

## 🎯 VISÃO GERAL DO PROJETO

### **Contexto Atual**
- ✅ **Área da Clínica**: Totalmente funcional (AnimalsPage, AppointmentsPage, ConsultationsPage, etc.)
- ✅ **Banco de Dados**: 18 tabelas estruturadas no Supabase com relacionamentos completos
- ✅ **Autenticação**: Sistema Supabase funcionando para clínicas
- 🔄 **Área do Tutor**: A ser desenvolvida com integração total à área da clínica

### **Objetivo Principal**
Desenvolver uma área exclusiva para tutores de animais onde possam:
- Acessar informações sobre seus pets
- Gerenciar dietas e atividades de forma gamificada
- Solicitar agendamentos à clínica
- Visualizar histórico de consultas
- Acompanhar progresso através de sistema de pontuação

---

## 🗄️ ANÁLISE DO BANCO DE DADOS ATUAL

### **Estrutura Relevante para Área do Tutor**

#### Tabela `animals` (Principal)
```sql
-- Campos existentes para cliente/tutor:
- tutor_name (text) - Nome do tutor
- email (text) - Email para login
- senha (text) - Senha para login
- phone (text) - Telefone do tutor
- client_active (boolean) - Status da conta do cliente
- client_activated_at (timestamp) - Data de ativação
- client_last_login (timestamp) - Último login
- gamification_points (integer) - Pontos de gamificação
- gamification_level (integer) - Nível de gamificação
```

#### Relacionamentos Chave
```
clinics (1) ──→ (N) animals
animals (1) ──→ (N) appointments
animals (1) ──→ (N) consultations
animals (1) ──→ (N) dietas
animals (1) ──→ (N) planos_atividade
animals (1) ──→ (N) atividades_realizadas
```

#### Tabelas de Agendamento
```sql
appointments:
- solicitado_por_cliente (boolean) - Indica se foi solicitado pelo cliente
- status_solicitacao (varchar) - Status da solicitação
- observacoes_cliente (text) - Observações do cliente
```

#### Sistema de Dietas
```sql
dietas → opcoes_dieta → alimentos_dieta
dieta_progresso (para registro do cliente)
```

#### Sistema de Atividades
```sql
atividades → planos_atividade
atividades_realizadas (para registro do cliente)
```

---

## 🚀 DESENVOLVIMENTO POR SPRINTS

### **SPRINT 1: ATIVAÇÃO DE CLIENTES NA ÁREA DA CLÍNICA**
**Duração**: 1 semana  
**Foco**: Backend + Frontend da área da clínica

#### **1.1 Backend - Modificações**

**Arquivo**: `backend/app/models/animal.py`
```python
# Adicionar novos modelos
class ClientActivationData(BaseModel):
    tutor_name: str
    email: str
    phone: str
    senha: str

class ClientStatusResponse(BaseModel):
    client_active: bool
    tutor_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    client_activated_at: Optional[datetime] = None
    gamification_points: Optional[int] = None
```

**Arquivo**: `backend/app/api/animals.py`
```python
# Novos endpoints para ativação de cliente
@router.put("/{animal_id}/client-activation")
async def activate_client_account(
    animal_id: str,
    activation_data: ClientActivationData,
    clinic_id: str = Depends(verify_clinic_session)
):
    """
    Ativa conta de cliente para um animal
    - Atualiza campos client_* na tabela animals
    - Cria usuário no Supabase Auth
    - Define client_active = true
    """
    # Implementação completa

@router.put("/{animal_id}/client-deactivation")
async def deactivate_client_account(
    animal_id: str,
    clinic_id: str = Depends(verify_clinic_session)
):
    """Desativa conta de cliente para um animal"""
    # Implementação

@router.get("/{animal_id}/client-status")
async def get_client_status(
    animal_id: str,
    clinic_id: str = Depends(verify_clinic_session)
):
    """Retorna status da conta do cliente"""
    # Implementação
```

#### **1.2 Frontend - Modificações na AnimalsPage**

**Arquivo**: `frontend/app/src/pages/AnimalsPage.jsx`
```jsx
// Adicionar nova coluna "Status Cliente" na tabela
// Adicionar botões de ação para ativar/desativar cliente
// Modal para cadastro do cliente

const ClientActivationModal = ({ open, onClose, animal, onSuccess }) => {
  // Formulário para cadastro do tutor
  // Campos: nome, email, telefone, senha
  // Integração com API de ativação
};

const ClientStatusIndicator = ({ animal }) => {
  // Indicador visual do status da conta
  // Verde: Ativo | Cinza: Inativo
  // Botão para ativar/desativar
};
```

#### **1.3 Entregáveis Sprint 1**
- [ ] Endpoints de ativação/desativação de cliente
- [ ] Modificação da AnimalsPage com coluna "Status Cliente"
- [ ] Modal de cadastro de cliente
- [ ] Indicadores visuais de status
- [ ] Integração com Supabase Auth
- [ ] Testes dos endpoints

---

### **SPRINT 2: SISTEMA DE LOGIN DUAL E ESTRUTURA BASE**
**Duração**: 1 semana  
**Foco**: Autenticação e estrutura base da área do tutor

#### **2.1 Backend - Sistema de Autenticação Dual**

**Arquivo**: `backend/app/api/auth.py`
```python
# Função para verificar tipo de usuário
async def check_user_type(email: str) -> Dict[str, Any]:
    """
    Verifica se o usuário é clínica ou cliente
    Retorna tipo, dados e URL de redirecionamento
    """
    # Verificar na tabela clinics
    # Verificar na tabela animals (client_active = true)
    # Retornar tipo de usuário e dados

@router.post("/login-dual")
async def dual_login(credentials: LoginData):
    """
    Login que funciona para clínicas e clientes
    - Autentica via Supabase
    - Verifica tipo de usuário
    - Retorna dados específicos do tipo
    """
    # Implementação completa
```

**Arquivo**: `backend/app/api/client_auth.py` (NOVO)
```python
from fastapi import APIRouter, Depends, HTTPException
from ..models.client import ClientLoginData, ClientAuthResponse

router = APIRouter(prefix="/client/auth", tags=["client-auth"])

@router.post("/login", response_model=ClientAuthResponse)
async def client_login(credentials: ClientLoginData):
    """Login específico para clientes"""
    # Implementação

@router.get("/profile")
async def get_client_profile(current_client = Depends(get_current_client)):
    """Perfil do cliente logado"""
    # Implementação

async def get_current_client(authorization: str = Header(...)):
    """Dependência para obter cliente atual"""
    # Implementação similar ao get_current_user
```

#### **2.2 Frontend - Modificação do Login e Estrutura Base**

**Arquivo**: `frontend/app/src/pages/LoginPage.jsx`
```jsx
// Modificar para detectar tipo de usuário
// Adicionar seletor de tipo de login (Clínica/Tutor)
// Redirecionar baseado no tipo de usuário

const [userType, setUserType] = useState('clinic'); // 'clinic' ou 'client'

const handleLogin = async (data) => {
  const response = await authService.dualLogin({
    ...data,
    userType
  });
  
  if (response.userType === 'clinic') {
    navigate('/dashboard');
  } else if (response.userType === 'client') {
    navigate('/tutor');
  }
};
```

**Estrutura de Diretórios para Área do Tutor**:
```
frontend/app/src/
├── tutor/                    # Nova pasta para área do tutor
│   ├── components/
│   │   ├── layout/
│   │   │   ├── TutorLayout.jsx
│   │   │   ├── TutorHeader.jsx
│   │   │   ├── TutorSidebar.jsx
│   │   │   └── TutorFooter.jsx
│   │   ├── common/
│   │   │   ├── LoadingSpinner.jsx
│   │   │   ├── GameCard.jsx
│   │   │   └── ProgressBar.jsx
│   │   └── auth/
│   │       └── TutorAuthGuard.jsx
│   ├── pages/
│   │   ├── TutorDashboard.jsx
│   │   ├── TutorProfile.jsx
│   │   ├── TutorDiets.jsx
│   │   ├── TutorActivities.jsx
│   │   ├── TutorAppointments.jsx
│   │   └── TutorHistory.jsx
│   ├── contexts/
│   │   └── TutorAuthContext.jsx
│   ├── services/
│   │   ├── tutorAuthService.js
│   │   ├── tutorApiService.js
│   │   └── tutorStorageService.js
│   └── hooks/
│       ├── useTutorAuth.js
│       ├── useTutorData.js
│       └── useTutorGameification.js
```

#### **2.3 Entregáveis Sprint 2**
- [ ] Sistema de login dual (clínica/tutor)
- [ ] Estrutura de pastas da área do tutor
- [ ] Context de autenticação do tutor
- [ ] Layout base da área do tutor
- [ ] Roteamento específico para tutores
- [ ] Guards de autenticação

---

### **SPRINT 3: DASHBOARD E PERFIL DO TUTOR**
**Duração**: 1 semana  
**Foco**: Frontend - Páginas principais da área do tutor

#### **3.1 Dashboard do Tutor**

**Arquivo**: `frontend/app/src/tutor/pages/TutorDashboard.jsx`
```jsx
const TutorDashboard = () => {
  // Cards de resumo:
  // - Progresso de dietas (%)
  // - Atividades da semana
  // - Próximos agendamentos
  // - Pontos de gamificação
  // - Nível atual do pet
  
  return (
    <TutorLayout>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <DietProgressCard />
        </Grid>
        <Grid item xs={12} md={6}>
          <ActivityProgressCard />
        </Grid>
        <Grid item xs={12} md={6}>
          <UpcomingAppointmentsCard />
        </Grid>
        <Grid item xs={12} md={6}>
          <GameificationCard />
        </Grid>
      </Grid>
    </TutorLayout>
  );
};
```

#### **3.2 Perfil do Tutor**

**Arquivo**: `frontend/app/src/tutor/pages/TutorProfile.jsx`
```jsx
const TutorProfile = () => {
  // Seções:
  // - Dados do tutor (nome, email, telefone)
  // - Dados do animal (nome, espécie, raça, idade, peso)
  // - Alteração de senha
  // - Histórico de ativação da conta
  
  const [tutorData, setTutorData] = useState({});
  const [animalData, setAnimalData] = useState({});
  
  return (
    <TutorLayout>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4">Meu Perfil</Typography>
        
        <Box sx={{ mt: 3 }}>
          <Typography variant="h6">Dados do Tutor</Typography>
          <TutorDataForm data={tutorData} onSave={handleSaveTutor} />
        </Box>
        
        <Box sx={{ mt: 3 }}>
          <Typography variant="h6">Dados do {animalData.name}</Typography>
          <AnimalDataForm data={animalData} onSave={handleSaveAnimal} />
        </Box>
      </Paper>
    </TutorLayout>
  );
};
```

#### **3.3 Backend - Endpoints de Perfil**

**Arquivo**: `backend/app/api/client_profile.py` (NOVO)
```python
@router.get("/profile")
async def get_client_profile(current_client = Depends(get_current_client)):
    """Retorna dados do tutor e animal"""
    # Implementação

@router.put("/profile")
async def update_client_profile(
    profile_data: ClientProfileUpdate,
    current_client = Depends(get_current_client)
):
    """Atualiza dados do tutor"""
    # Implementação

@router.put("/animal")
async def update_animal_data(
    animal_data: AnimalUpdate,
    current_client = Depends(get_current_client)
):
    """Atualiza dados do animal"""
    # Implementação
```

#### **3.4 Entregáveis Sprint 3**
- [ ] Dashboard do tutor com cards informativos
- [ ] Página de perfil com edição de dados
- [ ] Endpoints de perfil do cliente
- [ ] Componentes reutilizáveis (cards, forms)
- [ ] Integração com sistema de gamificação

---

### **SPRINT 4: SISTEMA DE AGENDAMENTOS**
**Duração**: 1 semana  
**Foco**: Solicitação de agendamentos pelo tutor

#### **4.1 Backend - Agendamentos do Cliente**

**Arquivo**: `backend/app/api/client_appointments.py` (NOVO)
```python
@router.get("/appointments")
async def get_client_appointments(current_client = Depends(get_current_client)):
    """Lista agendamentos do animal do cliente"""
    # Implementação

@router.post("/appointments/request")
async def request_appointment(
    appointment_data: AppointmentRequest,
    current_client = Depends(get_current_client)
):
    """Solicita novo agendamento"""
    # Implementação

@router.put("/appointments/{appointment_id}/cancel")
async def cancel_appointment_request(
    appointment_id: str,
    current_client = Depends(get_current_client)
):
    """Cancela solicitação de agendamento"""
    # Implementação
```

#### **4.2 Frontend - Página de Agendamentos**

**Arquivo**: `frontend/app/src/tutor/pages/TutorAppointments.jsx`
```jsx
const TutorAppointments = () => {
  // Seções:
  // - Formulário para solicitar agendamento
  // - Lista de agendamentos confirmados
  // - Lista de solicitações pendentes
  // - Histórico de agendamentos
  
  return (
    <TutorLayout>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <AppointmentRequestForm onSubmit={handleRequestAppointment} />
        </Grid>
        <Grid item xs={12} md={6}>
          <UpcomingAppointmentsList appointments={confirmedAppointments} />
        </Grid>
        <Grid item xs={12}>
          <PendingRequestsList requests={pendingRequests} />
        </Grid>
      </Grid>
    </TutorLayout>
  );
};
```

#### **4.3 Modificações na Área da Clínica**

**Arquivo**: `frontend/app/src/pages/AppointmentsPage.jsx`
```jsx
// Adicionar seção para solicitações de clientes
// Botões para aprovar/rejeitar/modificar
// Indicadores visuais para agendamentos solicitados por clientes

const ClientRequestsSection = () => {
  // Lista de solicitações pendentes
  // Ações: Aprovar, Rejeitar, Modificar horário
};
```

#### **4.4 Entregáveis Sprint 4**
- [ ] Endpoints de agendamentos para clientes
- [ ] Página de agendamentos do tutor
- [ ] Formulário de solicitação de agendamento
- [ ] Modificações na área da clínica
- [ ] Sistema de notificações de status

---

### **SPRINT 5: SISTEMA DE DIETAS GAMIFICADO**
**Duração**: 2 semanas  
**Foco**: Interface gamificada para acompanhamento de dietas

#### **5.1 Backend - Dietas do Cliente**

**Arquivo**: `backend/app/api/client_diets.py` (NOVO)
```python
@router.get("/diets")
async def get_client_diets(current_client = Depends(get_current_client)):
    """Lista dietas ativas do animal"""
    # Implementação

@router.get("/diets/{diet_id}/progress")
async def get_diet_progress(
    diet_id: str,
    current_client = Depends(get_current_client)
):
    """Progresso da dieta específica"""
    # Implementação

@router.post("/diets/{diet_id}/log")
async def log_diet_progress(
    diet_id: str,
    progress_data: DietProgressLog,
    current_client = Depends(get_current_client)
):
    """Registra progresso da dieta"""
    # Implementação com gamificação

@router.get("/diets/{diet_id}/calendar")
async def get_diet_calendar(
    diet_id: str,
    month: int,
    year: int,
    current_client = Depends(get_current_client)
):
    """Calendário de progresso da dieta"""
    # Implementação
```

#### **5.2 Frontend - Página de Dietas**

**Arquivo**: `frontend/app/src/tutor/pages/TutorDiets.jsx`
```jsx
const TutorDiets = () => {
  // Componentes principais:
  // - Seletor de plano de dieta ativo
  // - Interface de registro diário
  // - Calendário de progresso
  // - Barra de progresso gamificada
  // - Sistema de pontos e conquistas
  
  return (
    <TutorLayout>
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <DietPlanSelector 
            plans={availablePlans}
            activePlan={activePlan}
            onSelectPlan={handleSelectPlan}
          />
          
          <DietDailyLogger 
            plan={activePlan}
            onLogMeal={handleLogMeal}
          />
          
          <DietProgressCalendar 
            dietId={activePlan?.id}
            progress={dietProgress}
          />
        </Grid>
        
        <Grid item xs={12} md={4}>
          <DietGameificationPanel 
            points={gamePoints}
            level={gameLevel}
            achievements={achievements}
          />
        </Grid>
      </Grid>
    </TutorLayout>
  );
};
```

#### **5.3 Componentes Específicos**

**DietDailyLogger.jsx**:
```jsx
const DietDailyLogger = ({ plan, onLogMeal }) => {
  // Interface para registrar refeições do dia
  // Checkboxes para cada refeição planejada
  // Botão de "Refeição Completa"
  // Feedback visual imediato
  // Animações de conquista
};
```

**DietGameificationPanel.jsx**:
```jsx
const DietGameificationPanel = ({ points, level, achievements }) => {
  // Exibição de pontos atuais
  // Barra de progresso para próximo nível
  // Lista de conquistas desbloqueadas
  // Metas semanais/mensais
};
```

#### **5.4 Entregáveis Sprint 5**
- [ ] Endpoints de dietas para clientes
- [ ] Página de dietas gamificada
- [ ] Sistema de registro diário
- [ ] Calendário de progresso
- [ ] Sistema de pontuação automática
- [ ] Interface de conquistas

---

### **SPRINT 6: SISTEMA DE ATIVIDADES GAMIFICADO**
**Duração**: 2 semanas  
**Foco**: Interface gamificada para acompanhamento de atividades

#### **6.1 Backend - Atividades do Cliente**

**Arquivo**: `backend/app/api/client_activities.py` (NOVO)
```python
@router.get("/activities")
async def get_client_activities(current_client = Depends(get_current_client)):
    """Lista planos de atividade ativos"""
    # Implementação

@router.post("/activities/{plan_id}/log")
async def log_activity(
    plan_id: str,
    activity_data: ActivityLog,
    current_client = Depends(get_current_client)
):
    """Registra atividade realizada"""
    # Implementação com timer e gamificação

@router.get("/activities/{plan_id}/progress")
async def get_activity_progress(
    plan_id: str,
    current_client = Depends(get_current_client)
):
    """Progresso do plano de atividade"""
    # Implementação
```

#### **6.2 Frontend - Página de Atividades**

**Arquivo**: `frontend/app/src/tutor/pages/TutorActivities.jsx`
```jsx
const TutorActivities = () => {
  // Componentes principais:
  // - Seletor de plano de atividade
  // - Timer para atividades
  // - Registro de atividades realizadas
  // - Progresso semanal/mensal
  // - Sistema de pontuação
  
  return (
    <TutorLayout>
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <ActivityPlanSelector 
            plans={availablePlans}
            activePlan={activePlan}
            onSelectPlan={handleSelectPlan}
          />
          
          <ActivityTimer 
            activity={currentActivity}
            onComplete={handleActivityComplete}
          />
          
          <ActivityProgressTracker 
            planId={activePlan?.id}
            progress={activityProgress}
          />
        </Grid>
        
        <Grid item xs={12} md={4}>
          <ActivityGameificationPanel 
            points={gamePoints}
            streak={currentStreak}
            weeklyGoal={weeklyGoal}
          />
        </Grid>
      </Grid>
    </TutorLayout>
  );
};
```

#### **6.3 Componentes Específicos**

**ActivityTimer.jsx**:
```jsx
const ActivityTimer = ({ activity, onComplete }) => {
  // Timer visual para atividades
  // Botões: Iniciar, Pausar, Finalizar
  // Progresso visual em tempo real
  // Notificações de conclusão
};
```

#### **6.4 Entregáveis Sprint 6**
- [ ] Endpoints de atividades para clientes
- [ ] Página de atividades com timer
- [ ] Sistema de registro de atividades
- [ ] Progresso visual de planos
- [ ] Gamificação de atividades
- [ ] Histórico de atividades

---

### **SPRINT 7: HISTÓRICO DE CONSULTAS**
**Duração**: 1 semana  
**Foco**: Visualização do histórico médico

#### **7.1 Backend - Consultas do Cliente**

**Arquivo**: `backend/app/api/client_consultations.py` (NOVO)
```python
@router.get("/consultations")
async def get_client_consultations(current_client = Depends(get_current_client)):
    """Lista consultas do animal do cliente"""
    # Implementação

@router.get("/consultations/{consultation_id}")
async def get_consultation_detail(
    consultation_id: str,
    current_client = Depends(get_current_client)
):
    """Detalhes de uma consulta específica"""
    # Implementação
```

#### **7.2 Frontend - Página de Histórico**

**Arquivo**: `frontend/app/src/tutor/pages/TutorHistory.jsx`
```jsx
const TutorHistory = () => {
  // Lista de consultas realizadas
  // Filtros por data, tipo de consulta
  // Detalhes de cada consulta
  // Download de relatórios (futuro)
  
  return (
    <TutorLayout>
      <ConsultationsList 
        consultations={consultations}
        onViewDetail={handleViewDetail}
      />
    </TutorLayout>
  );
};
```

#### **7.3 Entregáveis Sprint 7**
- [ ] Endpoints de consultas para clientes
- [ ] Página de histórico de consultas
- [ ] Filtros e busca
- [ ] Visualização de detalhes

---

## 📋 CRONOGRAMA ESTIMADO

| Sprint | Duração | Foco | Entregáveis Principais |
|--------|---------|------|------------------------|
| 1 | 1 semana | Backend + Frontend Clínica | Ativação de clientes na AnimalsPage |
| 2 | 1 semana | Autenticação + Estrutura | Login dual + estrutura base tutor |
| 3 | 1 semana | Frontend Tutor | Dashboard + Perfil |
| 4 | 1 semana | Agendamentos | Solicitação de agendamentos |
| 5 | 2 semanas | Dietas | Sistema gamificado de dietas |
| 6 | 2 semanas | Atividades | Sistema gamificado de atividades |
| 7 | 1 semana | Histórico | Consultas e relatórios |

**Total**: 9 semanas de desenvolvimento

---

## 🔧 CONSIDERAÇÕES TÉCNICAS

### **Segurança**
- Autenticação JWT separada para tutores
- Validação de acesso baseada em `client_active`
- Middleware de autorização específico

### **Performance**
- Cache de dados de gamificação
- Paginação em listas longas
- Otimização de queries do banco

### **UX/UI**
- Interface responsiva
- Feedback visual imediato
- Animações de gamificação
- Tema visual diferenciado da área da clínica

### **Gamificação**
- Sistema de pontos automático
- Níveis baseados em progresso
- Conquistas por metas atingidas
- Streaks de atividades

---

## 🎯 PRÓXIMOS PASSOS

1. **Revisar e aprovar este plano**
2. **Iniciar Sprint 1**: Ativação de clientes na AnimalsPage
3. **Preparar ambiente de desenvolvimento** para área do tutor
4. **Definir padrões visuais** específicos para área do tutor
5. **Configurar testes automatizados** para novos endpoints

---

## 📝 OBSERVAÇÕES IMPORTANTES

- **Banco de Dados**: Já possui estrutura necessária, apenas pequenos ajustes
- **Autenticação**: Reutilizar sistema Supabase existente
- **Integração**: Manter compatibilidade total com área da clínica
- **Escalabilidade**: Estrutura preparada para futuras funcionalidades
- **Manutenibilidade**: Código organizado e documentado

Este documento serve como guia principal para todo o desenvolvimento da área do tutor, garantindo organização, clareza e execução eficiente do projeto.