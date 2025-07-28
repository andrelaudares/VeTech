# SPRINTS BACKEND - VeTech Área do Cliente (REFORMULADO)

## 🎯 CONTEXTO E ALINHAMENTO

### **Situação Atual do Projeto**
- ✅ **Área da Clínica**: Completamente funcional (AnimalsPage, AppointmentsPage, ConsultationsPage, etc.)
- ✅ **Banco de Dados**: Script Supabase executado com 18 tabelas estruturadas
- ✅ **Autenticação**: Sistema Supabase funcionando para clínicas
- 🔄 **Área do Cliente**: A ser desenvolvida com integração total à área da clínica

### **Estrutura do Banco Atual (Relevante para Cliente)**
```sql
-- Tabela animals já possui campos para cliente
animals: client_active, tutor_name, email, senha, phone, gamification_points, client_activated_at

-- Tabelas de dieta (estrutura hierárquica)
dietas -> opcoes_dieta -> alimentos_dieta
dieta_progresso (registro do cliente)

-- Tabelas de atividade (estrutura hierárquica)  
atividades -> planos_atividade
atividades_realizadas (registro do cliente)

-- Agendamentos com suporte a solicitações de cliente
appointments: solicitado_por_cliente, status_solicitacao, observacoes_cliente

-- Sistema de gamificação completo
gamificacao_metas, gamificacao_pontuacoes, gamificacao_recompensas
```

### **Fluxo de Integração Clínica ↔ Cliente**
1. **Clínica** cadastra animal e cria dietas/planos de atividade
2. **Clínica** ativa conta do cliente via AnimalsPage.jsx
3. **Cliente** acessa sua área, escolhe planos e registra progresso
4. **Sistema** gamifica automaticamente e notifica a clínica
5. **Clínica** acompanha progresso via dashboard dedicado

---

## 🚀 PLANEJAMENTO DE SPRINTS (6 SEMANAS)

### **SPRINT 1: ATIVAÇÃO DE CLIENTES NA ÁREA DA CLÍNICA**
**Duração**: 1 semana  
**Objetivo**: Implementar sistema de ativação de contas de cliente na AnimalsPage existente

#### **1.1 Modificações no Backend**

**Arquivo**: `backend/app/models/animal.py`
```python
# Adicionar novos modelos para ativação de cliente
class ClientActivationData(BaseModel):
    tutor_name: str
    email: str
    phone: str
    senha: str

class ClientStatusUpdate(BaseModel):
    client_active: bool
    
class AnimalResponse(BaseModel):
    # ... campos existentes ...
    client_active: Optional[bool] = None
    tutor_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    client_activated_at: Optional[datetime] = None
    gamification_points: Optional[int] = None
```

**Arquivo**: `backend/app/api/animals.py`
```python
# Novo endpoint para ativação de cliente
@router.put("/{animal_id}/client-activation")
async def toggle_client_activation(
    animal_id: str,
    activation_data: ClientActivationData,
    clinic_id: str = Depends(verify_clinic_session)
):
    """
    Ativa ou desativa conta de cliente para um animal
    - Cria usuário no Supabase Auth se ativando
    - Atualiza campos client_* na tabela animals
    - Envia email de boas-vindas
    """
    # Implementação completa
    
@router.get("/{animal_id}/client-status")
async def get_client_status(
    animal_id: str,
    clinic_id: str = Depends(verify_clinic_session)
):
    """Retorna status da conta do cliente para um animal"""
    # Implementação
```

#### **1.2 Função SQL de Verificação de Tipo de Usuário**

**Arquivo**: `backend/app/db/functions.sql`
```sql
-- Função para verificar tipo de usuário após login
CREATE OR REPLACE FUNCTION check_user_type(user_email TEXT)
RETURNS TABLE(
    user_type TEXT, 
    redirect_url TEXT, 
    user_id UUID,
    clinic_name TEXT,
    animal_name TEXT
) AS $$
BEGIN
    -- Verificar se é clínica
    IF EXISTS (SELECT 1 FROM clinics WHERE email = user_email) THEN
        RETURN QUERY 
        SELECT 
            'clinic'::TEXT, 
            '/dashboard'::TEXT, 
            c.id,
            c.name,
            NULL::TEXT
        FROM clinics c 
        WHERE c.email = user_email;
        RETURN;
    END IF;
    
    -- Verificar se é cliente ativo
    IF EXISTS (
        SELECT 1 FROM animals 
        WHERE email = user_email 
        AND client_active = TRUE
    ) THEN
        RETURN QUERY 
        SELECT 
            'client'::TEXT, 
            '/client'::TEXT, 
            a.id,
            c.name,
            a.name
        FROM animals a
        JOIN clinics c ON a.clinic_id = c.id
        WHERE a.email = user_email 
        AND a.client_active = TRUE;
        RETURN;
    END IF;
    
    -- Usuário não encontrado ou inativo
    RETURN QUERY 
    SELECT 
        'unknown'::TEXT, 
        '/login'::TEXT, 
        NULL::UUID,
        NULL::TEXT,
        NULL::TEXT;
END;
$$ LANGUAGE plpgsql;
```

#### **1.3 Entregáveis Sprint 1**
- [ ] Modelos de dados para ativação de cliente
- [ ] Endpoint de ativação/desativação de cliente
- [ ] Função SQL de verificação de tipo de usuário
- [ ] Integração com Supabase Auth para criação de usuários
- [ ] Testes unitários dos endpoints

---

### **SPRINT 2: AUTENTICAÇÃO E MIDDLEWARE DE CLIENTE**
**Duração**: 1 semana  
**Objetivo**: Implementar sistema de autenticação específico para clientes

#### **2.1 Sistema de Autenticação para Clientes**

**Arquivo**: `backend/app/api/client_auth.py`
```python
from fastapi import APIRouter, Depends, HTTPException, status
from supabase import create_client
from ..core.config import settings

router = APIRouter(prefix="/client/auth", tags=["client-auth"])

class ClientLoginData(BaseModel):
    email: str
    password: str

class ClientAuthResponse(BaseModel):
    access_token: str
    token_type: str
    user_type: str
    animal_id: str
    animal_name: str
    clinic_name: str

@router.post("/login", response_model=ClientAuthResponse)
async def client_login(credentials: ClientLoginData):
    """
    Login específico para clientes
    - Autentica via Supabase
    - Verifica se client_active = true
    - Retorna token e dados do animal
    """
    # Implementação completa
    
@router.post("/refresh")
async def refresh_client_token(refresh_token: str):
    """Renovar token de cliente"""
    # Implementação
    
@router.post("/logout")
async def client_logout(current_client = Depends(get_current_client)):
    """Logout do cliente"""
    # Implementação
```

#### **2.2 Middleware de Segurança**

**Arquivo**: `backend/app/core/client_security.py`
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from supabase import create_client

security = HTTPBearer()

async def verify_client_session(token: str = Depends(security)):
    """
    Middleware para verificar sessão de cliente
    - Valida token Supabase
    - Verifica se client_active = true
    - Retorna animal_id
    """
    # Implementação completa
    
async def get_current_client(animal_id: str = Depends(verify_client_session)):
    """Retorna dados do cliente atual"""
    # Implementação
    
class RateLimiter:
    """Rate limiting para APIs de cliente"""
    # Implementação
```

#### **2.3 Dashboard Base do Cliente**

**Arquivo**: `backend/app/api/client_dashboard.py`
```python
@router.get("/dashboard")
async def get_client_dashboard(
    current_client = Depends(get_current_client)
):
    """
    Dashboard principal do cliente
    Retorna: dados do animal, pontos, próximos agendamentos, 
    progresso de dietas/atividades
    """
    return {
        "animal": {
            "id": current_client.id,
            "name": current_client.name,
            "species": current_client.species,
            "breed": current_client.breed,
            "age": current_client.age,
            "weight": current_client.weight
        },
        "gamification": {
            "points": current_client.gamification_points,
            "level": calculate_level(current_client.gamification_points),
            "next_level_points": calculate_next_level_points(current_client.gamification_points)
        },
        "quick_stats": {
            "active_diets": await get_active_diets_count(current_client.id),
            "active_activities": await get_active_activities_count(current_client.id),
            "this_week_progress": await get_week_progress(current_client.id)
        },
        "next_appointments": await get_next_appointments(current_client.id),
        "recent_achievements": await get_recent_achievements(current_client.id)
    }
```

#### **2.4 Entregáveis Sprint 2**
- [ ] Sistema de login para clientes
- [ ] Middleware de segurança e rate limiting
- [ ] API do dashboard do cliente
- [ ] Integração com sistema de gamificação
- [ ] Documentação das APIs

---

### **SPRINT 3: SISTEMA DE DIETAS - VISUALIZAÇÃO E ATIVAÇÃO**
**Duração**: 1 semana  
**Objetivo**: Implementar APIs para visualização e ativação de dietas pelo cliente

#### **3.1 APIs de Dietas Disponíveis**

**Arquivo**: `backend/app/api/client_diets.py`
```python
@router.get("/available")
async def get_available_diets(
    current_client = Depends(get_current_client)
):
    """
    Retorna dietas criadas pela clínica para este animal
    - Dietas com status 'ativa' ou 'disponível'
    - Inclui opções de dieta e alimentos
    - Indica qual está atualmente ativa
    """
    # Query complexa com JOINs
    
@router.get("/current")
async def get_current_diet(
    current_client = Depends(get_current_client)
):
    """
    Retorna dieta atualmente ativa do animal
    - Detalhes completos da dieta
    - Opções de dieta escolhidas
    - Alimentos e horários
    - Progresso atual
    """
    # Implementação
    
@router.post("/{diet_id}/activate")
async def activate_diet(
    diet_id: str,
    opcao_dieta_id: str,
    current_client = Depends(get_current_client)
):
    """
    Ativa uma dieta específica para o animal
    - Desativa dieta anterior se existir
    - Ativa nova dieta com opção escolhida
    - Cria registros iniciais de progresso
    - Notifica clínica da escolha
    """
    # Implementação com transações
```

#### **3.2 Sistema de Progresso de Dieta**

```python
@router.post("/progress")
async def log_diet_progress(
    progress_data: DietProgressData,
    current_client = Depends(get_current_client)
):
    """
    Registra progresso diário da dieta
    - Marca refeição como completa
    - Calcula pontos automáticos
    - Atualiza estatísticas
    - Verifica conquistas
    """
    # Implementação com gamificação
    
@router.get("/progress/history")
async def get_diet_progress_history(
    start_date: date = None,
    end_date: date = None,
    current_client = Depends(get_current_client)
):
    """
    Histórico de progresso da dieta
    - Calendário de cumprimento
    - Estatísticas semanais/mensais
    - Pontos ganhos por período
    """
    # Implementação
```

#### **3.3 Triggers SQL para Gamificação Automática**

```sql
-- Trigger para pontuação automática de dieta
CREATE OR REPLACE FUNCTION update_diet_gamification()
RETURNS TRIGGER AS $$
BEGIN
    -- Calcular pontos baseado no cumprimento
    IF NEW.refeicao_completa = TRUE THEN
        -- Adicionar pontos base
        UPDATE animals 
        SET gamification_points = gamification_points + 10
        WHERE id = NEW.animal_id;
        
        -- Registrar pontuação
        INSERT INTO gamificacao_pontuacoes (
            animal_id, pontos_obtidos, data, descricao
        ) VALUES (
            NEW.animal_id, 10, NOW(), 
            'Refeição completa registrada'
        );
        
        -- Verificar conquistas semanais
        PERFORM check_weekly_diet_achievements(NEW.animal_id);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER diet_progress_gamification
    AFTER INSERT OR UPDATE ON dieta_progresso
    FOR EACH ROW EXECUTE FUNCTION update_diet_gamification();
```

#### **3.4 Entregáveis Sprint 3**
- [ ] APIs de visualização de dietas disponíveis
- [ ] Sistema de ativação de dietas
- [ ] APIs de registro de progresso
- [ ] Triggers de gamificação automática
- [ ] Histórico e estatísticas de dieta

---

### **SPRINT 4: SISTEMA DE ATIVIDADES COM TIMER**
**Duração**: 1 semana  
**Objetivo**: Implementar sistema completo de atividades com timer e registro

#### **4.1 APIs de Planos de Atividade**

**Arquivo**: `backend/app/api/client_activities.py`
```python
@router.get("/available")
async def get_available_activity_plans(
    current_client = Depends(get_current_client)
):
    """
    Retorna planos de atividade criados pela clínica
    - Planos ativos para este animal
    - Detalhes da atividade base
    - Frequência e duração
    - Status atual
    """
    # Query com JOINs atividades -> planos_atividade
    
@router.post("/{plan_id}/activate")
async def activate_activity_plan(
    plan_id: str,
    current_client = Depends(get_current_client)
):
    """
    Ativa plano de atividade
    - Desativa plano anterior se existir
    - Cria cronograma semanal automático
    - Notifica clínica da escolha
    """
    # Implementação
```

#### **4.2 Sistema de Timer e Execução**

```python
@router.post("/start-session")
async def start_activity_session(
    session_data: ActivitySessionStart,
    current_client = Depends(get_current_client)
):
    """
    Inicia sessão de atividade com timer
    - Registra horário de início
    - Cria sessão temporária
    - Retorna session_id para tracking
    """
    # Implementação
    
@router.post("/complete-session")
async def complete_activity_session(
    session_data: ActivitySessionComplete,
    current_client = Depends(get_current_client)
):
    """
    Finaliza sessão de atividade
    - Calcula duração real
    - Calcula calorias queimadas
    - Atribui pontos automáticos
    - Registra em atividades_realizadas
    """
    # Implementação com cálculos automáticos
```

#### **4.3 Histórico e Estatísticas**

```python
@router.get("/history")
async def get_activity_history(
    start_date: date = None,
    end_date: date = None,
    current_client = Depends(get_current_client)
):
    """
    Histórico de atividades realizadas
    - Calendário de atividades
    - Estatísticas de duração e calorias
    - Progresso vs. plano prescrito
    - Conquistas e badges
    """
    # Implementação
    
@router.get("/stats/weekly")
async def get_weekly_activity_stats(
    current_client = Depends(get_current_client)
):
    """Estatísticas semanais de atividade"""
    # Implementação
```

#### **4.4 Entregáveis Sprint 4**
- [ ] APIs de planos de atividade
- [ ] Sistema de timer e sessões
- [ ] Registro automático de atividades
- [ ] Cálculo de calorias e pontos
- [ ] Histórico e estatísticas

---

### **SPRINT 5: SISTEMA DE AGENDAMENTOS INTEGRADO**
**Duração**: 1 semana  
**Objetivo**: Implementar solicitação de agendamentos pelo cliente e integração com área da clínica

#### **5.1 APIs de Agendamento do Cliente**

**Arquivo**: `backend/app/api/client_appointments.py`
```python
@router.post("/request")
async def request_appointment(
    appointment_data: AppointmentRequestData,
    current_client = Depends(get_current_client)
):
    """
    Solicita agendamento com a clínica
    - Cria registro com status 'solicitado'
    - Marca solicitado_por_cliente = true
    - Envia notificação para clínica
    """
    # Implementação
    
@router.get("/")
async def get_client_appointments(
    status: str = None,
    current_client = Depends(get_current_client)
):
    """
    Lista agendamentos do animal
    - Confirmados, pendentes, cancelados
    - Histórico de consultas
    - Status das solicitações
    """
    # Implementação
    
@router.put("/{appointment_id}/cancel")
async def cancel_appointment_request(
    appointment_id: str,
    current_client = Depends(get_current_client)
):
    """Cancela solicitação de agendamento"""
    # Implementação
```

#### **5.2 Modificações na Área da Clínica**

**Arquivo**: `backend/app/api/appointments.py` (modificar existente)
```python
@router.get("/client-requests")
async def get_client_appointment_requests(
    clinic_id: str = Depends(verify_clinic_session)
):
    """
    Lista solicitações de agendamento de clientes
    - Apenas solicitações pendentes
    - Dados do animal e cliente
    - Observações do cliente
    """
    # Implementação
    
@router.put("/{appointment_id}/manage-request")
async def manage_client_request(
    appointment_id: str,
    action_data: AppointmentActionData,
    clinic_id: str = Depends(verify_clinic_session)
):
    """
    Gerencia solicitação de cliente
    - Aprovar: confirma agendamento
    - Rejeitar: cancela com motivo
    - Modificar: propõe novo horário
    """
    # Implementação
```

#### **5.3 Sistema de Notificações**

```python
# Arquivo: backend/app/core/notifications.py
class NotificationService:
    @staticmethod
    async def notify_clinic_new_request(clinic_id: str, appointment_data: dict):
        """Notifica clínica sobre nova solicitação"""
        # Implementação
        
    @staticmethod
    async def notify_client_request_status(animal_id: str, status: str, message: str):
        """Notifica cliente sobre status da solicitação"""
        # Implementação
```

#### **5.4 Entregáveis Sprint 5**
- [ ] APIs de solicitação de agendamento
- [ ] Modificações na área da clínica
- [ ] Sistema de notificações
- [ ] Gerenciamento de solicitações
- [ ] Integração completa clínica ↔ cliente

---

### **SPRINT 6: GAMIFICAÇÃO AVANÇADA E DASHBOARD DA CLÍNICA**
**Duração**: 1 semana  
**Objetivo**: Finalizar sistema de gamificação e criar dashboard de acompanhamento para clínicas

#### **6.1 APIs de Gamificação Avançada**

**Arquivo**: `backend/app/api/client_gamification.py`
```python
@router.get("/profile")
async def get_gamification_profile(
    current_client = Depends(get_current_client)
):
    """
    Perfil completo de gamificação
    - Pontos totais e nível atual
    - Conquistas desbloqueadas
    - Progresso para próximo nível
    - Ranking (se aplicável)
    """
    # Implementação
    
@router.get("/achievements")
async def get_achievements(
    current_client = Depends(get_current_client)
):
    """Lista todas as conquistas disponíveis e desbloqueadas"""
    # Implementação
    
@router.get("/leaderboard")
async def get_leaderboard(
    period: str = "month",
    current_client = Depends(get_current_client)
):
    """Ranking de pontuação (opcional)"""
    # Implementação
```

#### **6.2 Dashboard de Progresso para Clínicas**

**Arquivo**: `backend/app/api/clinic_client_progress.py`
```python
@router.get("/clients-overview")
async def get_clients_overview(
    clinic_id: str = Depends(verify_clinic_session)
):
    """
    Visão geral dos clientes ativos
    - Lista de animais com conta ativa
    - Status de engajamento
    - Alertas de baixa atividade
    """
    # Implementação
    
@router.get("/client/{animal_id}/progress")
async def get_client_detailed_progress(
    animal_id: str,
    clinic_id: str = Depends(verify_clinic_session)
):
    """
    Progresso detalhado de um cliente específico
    - Progresso de dietas e atividades
    - Pontuação e conquistas
    - Histórico de engajamento
    """
    # Implementação
    
@router.get("/analytics")
async def get_clinic_analytics(
    start_date: date = None,
    end_date: date = None,
    clinic_id: str = Depends(verify_clinic_session)
):
    """
    Analytics da clínica sobre engajamento dos clientes
    - Taxa de adesão a dietas/atividades
    - Média de pontuação
    - Clientes mais/menos engajados
    """
    # Implementação
```

#### **6.3 Sistema de Conquistas Automáticas**

```sql
-- Função para verificar conquistas automáticas
CREATE OR REPLACE FUNCTION check_achievements(p_animal_id UUID)
RETURNS VOID AS $$
DECLARE
    diet_streak INTEGER;
    activity_streak INTEGER;
    total_points INTEGER;
BEGIN
    -- Verificar sequência de dieta
    SELECT COUNT(*) INTO diet_streak
    FROM dieta_progresso 
    WHERE animal_id = p_animal_id 
    AND refeicao_completa = TRUE
    AND data >= CURRENT_DATE - INTERVAL '7 days';
    
    -- Verificar sequência de atividade
    SELECT COUNT(*) INTO activity_streak
    FROM atividades_realizadas 
    WHERE animal_id = p_animal_id 
    AND realizado = TRUE
    AND data >= CURRENT_DATE - INTERVAL '7 days';
    
    -- Verificar pontos totais
    SELECT gamification_points INTO total_points
    FROM animals WHERE id = p_animal_id;
    
    -- Atribuir conquistas baseadas nos critérios
    IF diet_streak >= 7 THEN
        INSERT INTO gamificacao_pontuacoes (animal_id, pontos_obtidos, data, descricao)
        VALUES (p_animal_id, 50, NOW(), 'Conquista: 7 dias seguidos de dieta!')
        ON CONFLICT DO NOTHING;
    END IF;
    
    -- Mais verificações de conquistas...
END;
$$ LANGUAGE plpgsql;
```

#### **6.4 Otimizações e Finalização**

```python
# Arquivo: backend/app/core/performance.py
class CacheManager:
    """Sistema de cache para APIs frequentes"""
    # Implementação
    
class DatabaseOptimizer:
    """Otimizações de queries e índices"""
    # Implementação
```

#### **6.5 Entregáveis Sprint 6**
- [ ] Sistema de gamificação completo
- [ ] Dashboard de progresso para clínicas
- [ ] Sistema de conquistas automáticas
- [ ] Analytics de engajamento
- [ ] Otimizações de performance
- [ ] Documentação completa das APIs

---

## 📊 CRONOGRAMA INTEGRADO (6 SEMANAS)

| Semana | Sprint | Foco Principal | Entregáveis Chave |
|--------|--------|----------------|-------------------|
| 1 | Sprint 1 | Ativação de Clientes | Modificação AnimalsPage + Endpoints de ativação |
| 2 | Sprint 2 | Autenticação Cliente | Sistema de login + Middleware + Dashboard base |
| 3 | Sprint 3 | Sistema de Dietas | APIs de dieta + Progresso + Gamificação |
| 4 | Sprint 4 | Sistema de Atividades | Timer + Registro + Histórico |
| 5 | Sprint 5 | Agendamentos | Solicitações + Integração com clínica |
| 6 | Sprint 6 | Finalização | Gamificação avançada + Dashboard clínica |

---

## ✅ CHECKLISTS DE VALIDAÇÃO

### **Checklist Sprint 1**
- [ ] AnimalsPage.jsx possui botão de ativação de cliente
- [ ] Modal de cadastro de cliente funcional
- [ ] Endpoint PUT /animals/{id}/client-activation implementado
- [ ] Função SQL check_user_type() criada e testada
- [ ] Integração com Supabase Auth funcionando
- [ ] Campos client_* atualizados na tabela animals
- [ ] Testes unitários passando

### **Checklist Sprint 2**
- [ ] Sistema de login para clientes funcionando
- [ ] Middleware de segurança implementado
- [ ] Dashboard do cliente retornando dados corretos
- [ ] Redirecionamento automático após login
- [ ] Rate limiting configurado
- [ ] Documentação das APIs atualizada

### **Checklist Sprint 3**
- [ ] APIs de dietas disponíveis funcionando
- [ ] Sistema de ativação de dietas implementado
- [ ] Registro de progresso com pontuação automática
- [ ] Triggers de gamificação funcionando
- [ ] Histórico de progresso disponível

### **Checklist Sprint 4**
- [ ] APIs de planos de atividade funcionando
- [ ] Sistema de timer implementado
- [ ] Registro automático de atividades
- [ ] Cálculo de calorias e pontos correto
- [ ] Histórico e estatísticas disponíveis

### **Checklist Sprint 5**
- [ ] Solicitação de agendamentos funcionando
- [ ] Integração com área da clínica implementada
- [ ] Sistema de notificações funcionando
- [ ] Gerenciamento de solicitações pela clínica
- [ ] Status de solicitações atualizando em tempo real

### **Checklist Sprint 6**
- [ ] Sistema de gamificação completo
- [ ] Dashboard de progresso para clínicas funcionando
- [ ] Conquistas automáticas implementadas
- [ ] Analytics de engajamento disponíveis
- [ ] Performance otimizada
- [ ] Documentação completa

---

## 🔗 INTEGRAÇÃO COM FRONTEND

Este documento de backend deve ser usado em conjunto com o documento de sprints de frontend, garantindo que:

1. **Sprint 1 Backend** → **Sprint 1 Frontend**: Modificação da AnimalsPage
2. **Sprint 2 Backend** → **Sprint 2 Frontend**: Sistema de autenticação e layout
3. **Sprint 3 Backend** → **Sprint 3 Frontend**: Interface de dietas
4. **Sprint 4 Backend** → **Sprint 4 Frontend**: Interface de atividades
5. **Sprint 5 Backend** → **Sprint 5 Frontend**: Interface de agendamentos
6. **Sprint 6 Backend** → **Sprint 6 Frontend**: Gamificação e dashboards

---

## 📝 OBSERVAÇÕES IMPORTANTES

1. **Banco de Dados**: Todas as tabelas necessárias já existem no script Supabase
2. **Autenticação**: Reutilizar sistema Supabase existente
3. **Gamificação**: Sistema automático via triggers SQL
4. **Integração**: Máxima reutilização do código da área da clínica
5. **Performance**: Implementar cache e otimizações desde o início
6. **Testes**: Cada sprint deve incluir testes unitários e de integração