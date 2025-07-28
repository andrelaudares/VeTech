# Planejamento da Área do Cliente - VeTech

## 🎯 Visão Geral

### **Objetivo Principal**
Desenvolver uma área exclusiva para clientes (tutores de animais) acessarem informações sobre seus pets, acompanharem tratamentos, registrarem progresso de dietas e atividades, e interagirem com a clínica de forma digital.

### **Decisões Técnicas Definidas**
- **Autenticação**: Reutilizar sistema Supabase existente com verificação de tabela (`public.animals` ou `public.clinics`)
- **Estrutura Frontend**: Pastas separadas (`/clinic` e `/client`)
- **Roteamento**: Path-based (`/clinic/*` e `/client/*`)
- **Gamificação**: Sistema de pontos automático simples
- **Interface**: Responsiva (sem mobile-first dedicado)
- **Dados**: Sempre online, tempo real
- **MVP**: Sem customização por clínica, sem compliance GDPR

## 🗄️ ANÁLISE DO BANCO DE DADOS ATUAL

### Estrutura Existente
- **18 tabelas** organizadas por módulos
- **Relacionamento principal**: `clinics -> animals -> [demais entidades]`
- **Tabela animals** já possui campos para cliente: `tutor_name`, `email`, `senha`, `phone`
- **Sistema de gamificação** já implementado: `gamification_level`, `total_points`

### Relacionamentos Chave
```
clinics (1) -> (N) animals
animals (1) -> (N) appointments
animals (1) -> (N) consultations  
animals (1) -> (N) dietas
animals (1) -> (N) planos_atividade
animals (1) -> (N) atividades_realizadas
```

## 🚀 DESENVOLVIMENTO POR SPRINTS

### **SPRINT 1: SISTEMA DE ACESSO DO CLIENTE**
**Duração**: 1-2 semanas

#### Backend
1. **Modificar tabela `animals`**:
   - Adicionar campo `client_active` (boolean, default: false)
   - Validar campos existentes: `tutor_name`, `email`, `senha`, `phone`

2. **Criar endpoints em `/backend/app/api/animals.py`**:
   - `PUT /animals/{animal_id}/activate-client` - Ativar conta do cliente
   - `PUT /animals/{animal_id}/deactivate-client` - Desativar conta do cliente
   - `POST /animals/{animal_id}/client-register` - Cadastro do cliente

3. **Criar sistema de autenticação para clientes**:
   - Novo arquivo: `/backend/app/api/client_auth.py`
   - Endpoints: `/client/login`, `/client/register`
   - JWT separado para clientes (diferente das clínicas)

#### Frontend
1. **Modificar `AnimalsPage.jsx`**:
   - Adicionar botão "Ativar/Desativar Cliente" em cada animal
   - Modal para cadastro do cliente (nome, email, senha, telefone)
   - Indicador visual do status da conta do cliente

2. **Criar componentes**:
   - `ClientActivationModal.jsx`
   - `ClientStatusIndicator.jsx`

---

### **SPRINT 2: ESTRUTURA BASE DA ÁREA DO CLIENTE**
**Duração**: 2-3 semanas

#### Backend
1. **Middleware de autenticação para clientes**:
   - `get_current_client()` em `/backend/app/api/client_auth.py`
   - Validação de token JWT específico para clientes

2. **Endpoints base para área do cliente**:
   - `/client/profile` - Dados do perfil
   - `/client/animal` - Dados do animal vinculado

#### Frontend
1. **Criar estrutura de rotas para clientes**:
   - Nova pasta: `/frontend/app/src/client/`
   - Subpastas: `pages/`, `components/`, `contexts/`, `services/`

2. **Sistema de autenticação separado**:
   - `ClientAuthContext.jsx`
   - `clientAuthService.js`
   - Rotas: `/client/login`, `/client/*`

3. **Layout específico para clientes**:
   - `ClientLayout.jsx`
   - `ClientHeader.jsx`
   - Tema visual diferenciado

---

### **SPRINT 3: PÁGINAS PRINCIPAIS DA ÁREA DO CLIENTE**
**Duração**: 2-3 semanas

#### 3.1 Dashboard do Cliente
**Frontend**: `/frontend/app/src/client/pages/ClientDashboard.jsx`
- Cards com resumo de atividades e dietas
- Próximos agendamentos
- Progresso geral do animal
- Acesso rápido às funcionalidades

#### 3.2 Perfil do Cliente
**Frontend**: `/frontend/app/src/client/pages/ClientProfile.jsx`
- Edição de dados pessoais (nome, email, telefone)
- Edição de dados do animal (nome, peso, etc.)
- Alteração de senha

**Backend**: Endpoints em `/backend/app/api/client_profile.py`
- `GET /client/profile`
- `PUT /client/profile`
- `PUT /client/animal`

#### 3.3 Histórico de Consultas
**Frontend**: `/frontend/app/src/client/pages/ClientConsultations.jsx`
- Lista de consultas do animal
- Detalhes de cada consulta
- Filtros por data

**Backend**: Endpoint em `/backend/app/api/client_consultations.py`
- `GET /client/consultations` - Consultas do animal do cliente logado

---

### **SPRINT 4: SISTEMA DE AGENDAMENTOS**
**Duração**: 2-3 semanas

#### Backend
1. **Modificar tabela `appointments`**:
   - Adicionar campo `requested_by_client` (boolean)
   - Adicionar campo `client_notes` (text)

2. **Endpoints em `/backend/app/api/client_appointments.py`**:
   - `GET /client/appointments` - Agendamentos do animal
   - `POST /client/appointments/request` - Solicitar agendamento
   - `PUT /client/appointments/{id}/cancel` - Cancelar solicitação

3. **Modificar área da clínica**:
   - Indicar agendamentos solicitados por clientes
   - Aprovar/rejeitar/modificar solicitações

#### Frontend
1. **Página de agendamentos do cliente**:
   - `/frontend/app/src/client/pages/ClientAppointments.jsx`
   - Formulário para solicitar agendamento
   - Lista de agendamentos (confirmados e pendentes)
   - Status visual das solicitações

2. **Modificar `AppointmentsPage.jsx` da clínica**:
   - Seção para solicitações de clientes
   - Botões para aprovar/rejeitar

---

### **SPRINT 5: SISTEMA DE DIETAS GAMIFICADO**
**Duração**: 3-4 semanas

#### Backend
1. **Criar tabela `dieta_progresso`**:
```sql
CREATE TABLE dieta_progresso (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    animal_id UUID REFERENCES animals(id),
    dieta_id UUID REFERENCES dietas(id),
    opcao_dieta_id UUID REFERENCES opcoes_dieta(id),
    data DATE NOT NULL,
    refeicao_completa BOOLEAN DEFAULT false,
    observacoes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
```

2. **Endpoints em `/backend/app/api/client_diets.py`**:
   - `GET /client/diets` - Dietas ativas do animal
   - `GET /client/diets/{id}/progress` - Progresso da dieta
   - `POST /client/diets/{id}/log` - Registrar refeição
   - `GET /client/diets/{id}/calendar` - Calendário de progresso

#### Frontend
1. **Página de dietas do cliente**:
   - `/frontend/app/src/client/pages/ClientDiets.jsx`
   - Seleção de plano de dieta ativo
   - Interface gamificada para registro diário
   - Calendário de progresso
   - Barra de progresso semanal/mensal

2. **Componentes específicos**:
   - `DietProgressCalendar.jsx`
   - `DietDailyLogger.jsx`
   - `DietProgressBar.jsx`
   - `DietGameification.jsx`

---

### **SPRINT 6: SISTEMA DE ATIVIDADES GAMIFICADO**
**Duração**: 3-4 semanas

#### Backend
1. **Modificar tabela `atividades_realizadas`**:
   - Campo `observacao_tutor` já existe
   - Adicionar `pontos_obtidos` (integer)

2. **Endpoints em `/backend/app/api/client_activities.py`**:
   - `GET /client/activities` - Planos de atividade ativos
   - `GET /client/activities/{id}/progress` - Progresso do plano
   - `POST /client/activities/{id}/log` - Registrar atividade
   - `GET /client/activities/{id}/calendar` - Calendário de atividades

#### Frontend
1. **Página de atividades do cliente**:
   - `/frontend/app/src/client/pages/ClientActivities.jsx`
   - Seleção de plano de atividade ativo
   - Timer para atividades
   - Registro de duração e observações
   - Sistema de pontos e recompensas

2. **Componentes específicos**:
   - `ActivityTimer.jsx`
   - `ActivityLogger.jsx`
   - `ActivityProgressTracker.jsx`
   - `ActivityGameification.jsx`

---

### **SPRINT 7: GAMIFICAÇÃO E RECOMPENSAS**
**Duração**: 2-3 semanas

#### Backend
1. **Utilizar sistema existente**:
   - Tabelas: `gamificacao_metas`, `gamificacao_pontuacoes`, `gamificacao_recompensas`
   - Integrar com progresso de dietas e atividades

2. **Endpoints em `/backend/app/api/client_gamification.py`**:
   - `GET /client/gamification/stats` - Estatísticas do animal
   - `GET /client/gamification/achievements` - Conquistas
   - `GET /client/gamification/leaderboard` - Ranking (opcional)

#### Frontend
1. **Componentes de gamificação**:
   - `GamificationStats.jsx`
   - `AchievementsBadges.jsx`
   - `PointsDisplay.jsx`
   - `LevelProgress.jsx`

2. **Integração nas páginas existentes**:
   - Dashboard: resumo de pontos e nível
   - Dietas/Atividades: pontos por ação
   - Perfil: histórico de conquistas

---

### **SPRINT 8: POLIMENTO E TESTES**
**Duração**: 2-3 semanas

#### Tarefas
1. **Testes de integração**:
   - Fluxo completo clínica -> cliente
   - Sincronização de dados
   - Performance das consultas

2. **Melhorias de UX/UI**:
   - Responsividade mobile
   - Animações e transições
   - Feedback visual

3. **Documentação**:
   - API documentation
   - Manual do usuário
   - Guia de implementação

## 🔧 CONSIDERAÇÕES TÉCNICAS

### Autenticação
- **Dois sistemas JWT separados**: clínica e cliente
- **Middleware específico** para cada tipo de usuário
- **Rotas protegidas** com validação adequada

### Banco de Dados
- **Mínimas alterações** na estrutura existente
- **Novas tabelas** apenas quando necessário
- **Foreign keys** mantendo integridade referencial

### Frontend
- **Estrutura separada** para área do cliente
- **Reutilização** de componentes quando possível
- **Tema visual** diferenciado mas consistente

### Performance
- **Consultas otimizadas** com JOINs adequados
- **Cache** para dados frequentemente acessados
- **Paginação** em listas grandes

## 📊 MÉTRICAS DE SUCESSO

1. **Adoção**: % de animais com contas de cliente ativas
2. **Engajamento**: Frequência de uso da área do cliente
3. **Progresso**: % de conclusão de dietas e atividades
4. **Satisfação**: Feedback de clínicas e tutores

## 🚨 RISCOS E MITIGAÇÕES

### Riscos Identificados
1. **Complexidade de sincronização** entre áreas
2. **Performance** com muitos usuários simultâneos
3. **Segurança** dos dados dos clientes
4. **Usabilidade** da interface gamificada

### Mitigações
1. **Testes automatizados** extensivos
2. **Monitoramento** de performance
3. **Auditoria de segurança** regular
4. **Testes de usabilidade** com usuários reais

## 📝 PRÓXIMOS PASSOS

1. **Validação do planejamento** com stakeholders
2. **Configuração do ambiente** de desenvolvimento
3. **Início da Sprint 1** - Sistema de acesso do cliente
4. **Definição de cronograma** detalhado

---

**Documento criado em**: Janeiro 2025  
**Versão**: 1.0  
**Status**: Planejamento Inicial