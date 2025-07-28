# Backlog e Planejamento de Sprints — Backend da Área do Cliente VeTech

Este documento apresenta o backlog de requisitos focado no desenvolvimento backend da área do cliente (tutores de animais) integrado com a área da clínica existente.

---

## 🎯 CONTEXTO DO PROJETO

### **Sistema VeTech - Visão Geral**
- **ERP Veterinário** com diferencial em dietas e atividades para animais
- **Duas áreas integradas**: Clínica (já desenvolvida) + Cliente (nova)
- **Banco de dados**: Supabase com script completo já executado
- **Autenticação**: Sistema único com redirecionamento baseado no tipo de usuário
- **Gamificação**: Sistema de pontos automático para engajamento do cliente

### **Fluxo Principal**
1. **Clínica** cadastra animais, cria dietas/atividades, agenda consultas
2. **Clínica** ativa conta do cliente para um animal específico
3. **Cliente** acessa sua área, escolhe planos, registra progresso
4. **Sistema** gamifica o progresso e mantém clínica informada

---

## 📋 Backlog de Requisitos (User Stories)

| ID    | User Story                                                                                       | Critérios de Aceitação                                                                                      | Endpoint/Função                                                 |
|-------|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| US-B1 | Como clínica, quero ativar/desativar conta de cliente para um animal.                          | Botão na AnimalsPage, modal de cadastro, campos atualizados na tabela animals.                             | `PUT /api/animals/{id}/client-activation`                      |
| US-B2 | Como sistema, quero verificar tipo de usuário após login no Supabase.                         | Função SQL que verifica email nas tabelas clinics/animals e retorna tipo + redirecionamento.               | Função SQL `check_user_type(email)`                            |
| US-B3 | Como cliente, quero fazer login e ser redirecionado para minha área.                           | Login via Supabase, verificação de tipo, redirecionamento automático para /client.                         | `POST /api/auth/client-login`                                  |
| US-B4 | Como cliente, quero acessar dashboard com dados do meu animal.                                 | Dashboard com dados do animal, pontos, próximos agendamentos, progresso de dietas/atividades.              | `GET /api/client/dashboard`                                     |
| US-B5 | Como cliente, quero visualizar dietas criadas pela clínica para meu animal.                   | Lista de dietas disponíveis, opções de dieta, status (ativa/inativa), detalhes completos.                  | `GET /api/client/diets/available`                              |
| US-B6 | Como cliente, quero escolher e ativar uma dieta criada pela clínica.                          | Seleção de dieta, ativação, desativação de dieta anterior, notificação para clínica.                       | `POST /api/client/diets/{id}/activate`                         |
| US-B7 | Como cliente, quero registrar progresso diário da minha dieta.                                 | Registro por refeição, pontuação automática, atualização de estatísticas.                                   | `POST /api/client/diets/progress`                              |
| US-B8 | Como cliente, quero visualizar histórico e estatísticas da dieta.                             | Calendário de progresso, gráficos, percentual de cumprimento, pontos ganhos.                               | `GET /api/client/diets/progress-history`                       |
| US-B9 | Como cliente, quero visualizar planos de atividade criados pela clínica.                      | Lista de planos disponíveis, detalhes da atividade, frequência, duração, orientações.                      | `GET /api/client/activities/available`                         |
| US-B10| Como cliente, quero escolher e ativar um plano de atividade.                                   | Seleção de plano, ativação, cronograma automático, notificação para clínica.                               | `POST /api/client/activities/{id}/activate`                    |
| US-B11| Como cliente, quero registrar atividades realizadas com timer.                                | Timer integrado, registro de duração real, pontuação automática, observações.                              | `POST /api/client/activities/complete`                         |
| US-B12| Como cliente, quero visualizar histórico de atividades e progresso.                           | Calendário de atividades, estatísticas semanais, metas cumpridas, pontos ganhos.                           | `GET /api/client/activities/history`                           |
| US-B13| Como cliente, quero solicitar agendamentos com a clínica.                                      | Formulário de solicitação, horário preferido, descrição, status pendente.                                   | `POST /api/client/appointments/request`                        |
| US-B14| Como cliente, quero visualizar meus agendamentos e consultas.                                  | Lista de agendamentos (confirmados/pendentes), histórico de consultas da clínica.                          | `GET /api/client/appointments`                                 |
| US-B15| Como clínica, quero gerenciar solicitações de agendamento dos clientes.                        | Seção na AppointmentsPage para aprovar/rejeitar/modificar solicitações de clientes.                        | `PUT /api/appointments/{id}/manage-request`                    |
| US-B16| Como clínica, quero visualizar progresso dos clientes nas dietas/atividades.                   | Dashboard da clínica com progresso dos animais com conta ativa, alertas de baixo engajamento.              | `GET /api/clinic/clients-progress`                             |
| US-B17| Como sistema, quero implementar gamificação automática.                                        | Pontuação automática por ações, níveis, conquistas, atualização em tempo real.                             | Triggers SQL + `POST /api/client/gamification/update`          |
| US-B18| Como sistema, quero implementar middleware de segurança para clientes.                         | Verificação de client_active, validação de sessão Supabase, rate limiting.                                 | Middleware de autenticação                                      |

---

## 🚀 Planejamento de Sprints

### **Sprint 1: Preparação e Ativação de Clientes (1 semana)**

**Objetivo:** Implementar sistema de ativação de contas de cliente na área da clínica.

**Tarefas Principais:**
1. **Modificação da AnimalsPage.jsx (Frontend da Clínica)**
   - Adicionar coluna "Status Cliente" na tabela
   - Botão "Ativar Cliente" / "Desativar Cliente"
   - Modal para cadastro de cliente (nome, email, telefone, senha)

2. **Backend - Endpoint de Ativação**
   ```python
   # backend/app/api/animals.py
   @router.put("/{animal_id}/client-activation")
   async def toggle_client_activation(
       animal_id: str,
       client_data: ClientActivationData,
       clinic_id: str = Depends(verify_clinic_session)
   ):
       # Ativar/desativar conta do cliente
       # Criar usuário no Supabase Auth
       # Atualizar tabela animals
   ```

3. **Função SQL de Verificação de Tipo**
   ```sql
   CREATE OR REPLACE FUNCTION check_user_type(user_email TEXT)
   RETURNS TABLE(user_type TEXT, redirect_url TEXT, animal_id UUID) AS $$
   BEGIN
     -- Verificar se é clínica
     IF EXISTS (SELECT 1 FROM clinics WHERE email = user_email) THEN
       RETURN QUERY SELECT 'clinic'::TEXT, '/dashboard'::TEXT, id FROM clinics WHERE email = user_email;
       RETURN;
     END IF;
     
     -- Verificar se é cliente ativo
     IF EXISTS (SELECT 1 FROM animals WHERE client_email = user_email AND client_active = TRUE) THEN
       RETURN QUERY SELECT 'client'::TEXT, '/client'::TEXT, id FROM animals WHERE client_email = user_email AND client_active = TRUE;
       RETURN;
     END IF;
     
     RETURN QUERY SELECT 'unknown'::TEXT, '/login'::TEXT, NULL::UUID;
   END;
   $$ LANGUAGE plpgsql;
   ```

**Entregáveis:**
- [ ] AnimalsPage.jsx modificada com sistema de ativação
- [ ] Endpoint de ativação de cliente
- [ ] Função SQL de verificação de tipo
- [ ] Integração com Supabase Auth

---

### **Sprint 2: Autenticação e Dashboard do Cliente (1 semana)**

**Objetivo:** Implementar sistema de login e dashboard inicial para clientes.

**Tarefas Principais:**
1. **Sistema de Autenticação**
   ```python
   # backend/app/api/auth.py
   @router.post("/client-login")
   async def client_login(credentials: ClientLoginData):
       # Login via Supabase
       # Verificar tipo de usuário
       # Retornar token + redirecionamento
   ```

2. **Dashboard do Cliente**
   ```python
   @router.get("/client/dashboard")
   async def get_client_dashboard(animal_id: str = Depends(verify_client_session)):
       return {
           "animal": animal_data,
           "client": client_data,
           "quick_stats": {
               "points": client_points,
               "level": client_level,
               "active_diet": diet_status,
               "active_activities": activities_status
           },
           "next_appointments": upcoming_appointments,
           "recent_progress": recent_progress
       }
   ```

3. **Middleware de Segurança**
   ```python
   async def verify_client_session(request: Request):
       # Verificar token Supabase
       # Validar client_active = TRUE
       # Retornar animal_id
   ```

**Estrutura de Resposta do Dashboard:**
```json
{
  "animal": {
    "id": "uuid",
    "name": "Rex",
    "species": "Cão",
    "breed": "Golden Retriever",
    "age": 3,
    "weight": 25.5,
    "photo_url": "url"
  },
  "client": {
    "name": "João Silva",
    "email": "joao@email.com",
    "phone": "(11) 99999-9999",
    "points": 1250,
    "level": 3,
    "achievements": ["first_week", "diet_champion"]
  },
  "quick_stats": {
    "diet_progress": 75,
    "activities_this_week": 4,
    "next_appointment": "2024-01-15T10:00:00Z"
  }
}
```

**Entregáveis:**
- [ ] Sistema de login para clientes
- [ ] Dashboard API completa
- [ ] Middleware de segurança
- [ ] Redirecionamento automático

---

### **Sprint 3: Sistema de Dietas - Escolha e Ativação (1 semana)**

**Objetivo:** Implementar sistema completo de dietas com escolha de planos.

**Tarefas Principais:**
1. **API de Dietas Disponíveis**
   ```python
   @router.get("/client/diets/available")
   async def get_available_diets(animal_id: str = Depends(verify_client_session)):
       # Buscar dietas criadas pela clínica para este animal
       # Incluir opções de dieta e alimentos
       # Status: disponível, ativa, concluída
   ```

2. **Sistema de Escolha e Ativação**
   ```python
   @router.post("/client/diets/{diet_id}/activate")
   async def activate_diet(
       diet_id: str, 
       animal_id: str = Depends(verify_client_session)
   ):
       # Desativar dieta anterior
       # Ativar nova dieta
       # Criar cronograma baseado nas opções
       # Notificar clínica via webhook/email
   ```

3. **Registro de Progresso Diário**
   ```python
   @router.post("/client/diets/progress")
   async def record_diet_progress(
       progress_data: DietProgressCreate,
       animal_id: str = Depends(verify_client_session)
   ):
       # Registrar por refeição (café, almoço, jantar, lanche)
       # Calcular pontos automáticos
       # Atualizar estatísticas
   ```

**Triggers SQL para Gamificação:**
```sql
CREATE OR REPLACE FUNCTION calculate_diet_points()
RETURNS TRIGGER AS $$
DECLARE
    points_to_add INTEGER := 0;
BEGIN
    -- Pontos baseados no cumprimento
    IF NEW.cumprido = TRUE THEN
        points_to_add := 10;
        
        -- Bonus por consistência
        IF (SELECT COUNT(*) FROM dieta_progresso 
            WHERE animal_id = NEW.animal_id 
            AND data >= CURRENT_DATE - INTERVAL '7 days'
            AND cumprido = TRUE) >= 6 THEN
            points_to_add := points_to_add + 5;
        END IF;
    END IF;
    
    -- Atualizar pontos do cliente
    UPDATE animals 
    SET client_points = client_points + points_to_add
    WHERE id = NEW.animal_id;
    
    NEW.points_earned := points_to_add;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Entregáveis:**
- [ ] API de dietas disponíveis
- [ ] Sistema de ativação de dietas
- [ ] Registro de progresso gamificado
- [ ] Triggers de pontuação automática

---

### **Sprint 4: Sistema de Atividades com Timer (1 semana)**

**Objetivo:** Implementar sistema de atividades físicas com timer integrado.

**Tarefas Principais:**
1. **API de Planos de Atividade**
   ```python
   @router.get("/client/activities/available")
   async def get_available_activities(animal_id: str = Depends(verify_client_session)):
       # Buscar planos criados pela clínica
       # Incluir detalhes: duração, frequência, orientações
   ```

2. **Sistema de Timer e Execução**
   ```python
   @router.post("/client/activities/{plan_id}/activate")
   async def activate_activity_plan(plan_id: str, animal_id: str = Depends(verify_client_session)):
       # Ativar plano de atividade
       # Criar cronograma semanal
   
   @router.post("/client/activities/start-session")
   async def start_activity_session(activity_id: str, animal_id: str = Depends(verify_client_session)):
       # Iniciar sessão com timestamp
       # Retornar session_id
   
   @router.post("/client/activities/complete")
   async def complete_activity(completion_data: ActivityCompletionData):
       # Registrar atividade realizada
       # Calcular pontos baseado na duração vs. planejado
       # Permitir observações do cliente
   ```

3. **Histórico e Estatísticas**
   ```python
   @router.get("/client/activities/history")
   async def get_activity_history(
       animal_id: str = Depends(verify_client_session),
       days: int = 30
   ):
       # Histórico de atividades realizadas
       # Estatísticas semanais/mensais
       # Progresso vs. metas
   ```

**Entregáveis:**
- [ ] API de planos de atividade
- [ ] Sistema de timer integrado
- [ ] Registro de atividades com pontuação
- [ ] Histórico e estatísticas

---

### **Sprint 5: Sistema de Agendamentos Integrado (1 semana)**

**Objetivo:** Implementar solicitações de agendamento e integração com área da clínica.

**Tarefas Principais:**
1. **Solicitação de Agendamento pelo Cliente**
   ```python
   @router.post("/client/appointments/request")
   async def request_appointment(
       request_data: AppointmentRequestCreate,
       animal_id: str = Depends(verify_client_session)
   ):
       # Criar solicitação com status "client_requested"
       # Incluir horário preferido e descrição
       # Notificar clínica
   ```

2. **Modificação na AppointmentsPage.jsx (Clínica)**
   - Nova seção "Solicitações de Clientes"
   - Botões: Aprovar, Rejeitar, Modificar Horário
   - Filtros por status: pendente, aprovado, rejeitado

3. **Gerenciamento pela Clínica**
   ```python
   @router.put("/appointments/{appointment_id}/manage-request")
   async def manage_client_request(
       appointment_id: str,
       action_data: AppointmentActionData,
       clinic_id: str = Depends(verify_clinic_session)
   ):
       # Aprovar: status = "confirmed"
       # Rejeitar: status = "rejected" + motivo
       # Modificar: novo horário + status = "modified"
       # Notificar cliente via email/push
   ```

4. **Histórico de Consultas para Cliente**
   ```python
   @router.get("/client/consultations/history")
   async def get_consultation_history(animal_id: str = Depends(verify_client_session)):
       # Buscar consultas realizadas pela clínica
       # Filtrar por animal_id
       # Incluir: data, tipo, observações, próximos passos
   ```

**Entregáveis:**
- [ ] API de solicitação de agendamentos
- [ ] Modificação na AppointmentsPage da clínica
- [ ] Sistema de gerenciamento de solicitações
- [ ] Histórico de consultas para clientes

---

### **Sprint 6: Gamificação e Dashboard da Clínica (1 semana)**

**Objetivo:** Finalizar gamificação e implementar dashboard de acompanhamento para clínicas.

**Tarefas Principais:**
1. **Sistema de Gamificação Avançado**
   ```python
   @router.get("/client/gamification/status")
   async def get_gamification_status(animal_id: str = Depends(verify_client_session)):
       # Pontos atuais, nível, próximo nível
       # Conquistas desbloqueadas
       # Ranking (opcional)
   
   @router.get("/client/gamification/achievements")
   async def get_achievements(animal_id: str = Depends(verify_client_session)):
       # Lista de conquistas disponíveis
       # Progresso para cada conquista
       # Recompensas desbloqueadas
   ```

2. **Dashboard de Progresso para Clínicas**
   ```python
   @router.get("/clinic/clients-progress")
   async def get_clients_progress(clinic_id: str = Depends(verify_clinic_session)):
       # Lista de animais com conta ativa
       # Progresso de dietas e atividades
       # Alertas de baixo engajamento
       # Estatísticas gerais da clínica
   ```

3. **Sistema de Notificações**
   ```python
   @router.post("/notifications/send")
   async def send_notification(notification_data: NotificationData):
       # Notificações push para clientes
       # Emails automáticos
       # Alertas para clínica
   ```

4. **Otimizações Finais**
   - Cache Redis para consultas frequentes
   - Índices adicionais no banco
   - Logs de auditoria
   - Rate limiting

**Entregáveis:**
- [ ] Sistema de gamificação completo
- [ ] Dashboard de progresso para clínicas
- [ ] Sistema de notificações
- [ ] Otimizações de performance

---

## 📅 Cronograma Integrado

| Sprint | Duração | Foco Principal | Dependências |
|--------|---------|----------------|--------------|
| 1 | 1 semana | Ativação de Clientes | Modificação AnimalsPage |
| 2 | 1 semana | Auth + Dashboard | Sprint 1 completa |
| 3 | 1 semana | Sistema de Dietas | Sprint 2 completa |
| 4 | 1 semana | Sistema de Atividades | Sprint 3 completa |
| 5 | 1 semana | Agendamentos | Sprint 4 completa |
| 6 | 1 semana | Gamificação + Clínica | Sprint 5 completa |

**Total: 6 semanas (1.5 mês)**

---

## ✅ Checklists Detalhados

### Sprint 1 - Ativação de Clientes
- [ ] Modificar AnimalsPage.jsx com coluna de status
- [ ] Implementar modal de cadastro de cliente
- [ ] Criar endpoint PUT /animals/{id}/client-activation
- [ ] Implementar função SQL check_user_type
- [ ] Integrar com Supabase Auth
- [ ] Testes de ativação/desativação

### Sprint 2 - Auth + Dashboard
- [ ] Implementar endpoint POST /auth/client-login
- [ ] Criar middleware verify_client_session
- [ ] Desenvolver API GET /client/dashboard
- [ ] Implementar redirecionamento automático
- [ ] Testes de autenticação
- [ ] Validações de segurança

### Sprint 3 - Sistema de Dietas
- [ ] API GET /client/diets/available
- [ ] API POST /client/diets/{id}/activate
- [ ] API POST /client/diets/progress
- [ ] Triggers SQL para pontuação
- [ ] Sistema de notificação para clínica
- [ ] Testes de fluxo completo

### Sprint 4 - Sistema de Atividades
- [ ] API GET /client/activities/available
- [ ] API POST /client/activities/{id}/activate
- [ ] Sistema de timer com sessions
- [ ] API POST /client/activities/complete
- [ ] API GET /client/activities/history
- [ ] Cálculo de pontos por duração

### Sprint 5 - Agendamentos
- [ ] API POST /client/appointments/request
- [ ] Modificar AppointmentsPage.jsx da clínica
- [ ] API PUT /appointments/{id}/manage-request
- [ ] API GET /client/consultations/history
- [ ] Sistema de notificações
- [ ] Testes de integração completa

### Sprint 6 - Gamificação + Clínica
- [ ] APIs de gamificação avançada
- [ ] Dashboard GET /clinic/clients-progress
- [ ] Sistema de notificações push
- [ ] Implementar cache Redis
- [ ] Otimizações de performance
- [ ] Documentação final
