
# Backlog e Planejamento de Sprints — Frontend da Área do Cliente

Este documento apresenta o backlog de requisitos focado no desenvolvimento frontend da área do cliente (tutores de animais) e o planejamento de sprints.

---

## 📋 Backlog de Requisitos (User Stories)

| ID    | User Story                                                                                       | Critérios de Aceitação                                                                                      | Componente/Página                                               |
|-------|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| US-F1 | Como cliente, quero ser redirecionado para minha área após login.                               | Redirecionamento automático para `/client` após verificação de tipo de usuário.                            | `ClientAuthRedirect.jsx`                                       |
| US-F2 | Como cliente, quero navegar pela minha área com menu intuitivo.                                 | Layout responsivo com header, sidebar e navegação clara.                                                    | `ClientLayout.jsx`, `ClientHeader.jsx`                         |
| US-F3 | Como cliente, quero visualizar um dashboard com informações do meu pet.                         | Cards informativos com dados do pet, pontos, próximas consultas e progresso.                               | `ClientDashboard.jsx`                                          |
| US-F4 | Como cliente, quero ver meus pontos de gamificação em tempo real.                               | Atualização automática de pontos, indicadores visuais de progresso.                                         | `GamificationCard.jsx`                                         |
| US-F5 | Como cliente, quero visualizar minha dieta atual e opções disponíveis.                         | Interface clara com dieta prescrita, opções e alimentos permitidos/proibidos.                               | `DietPage.jsx`, `DietCurrentPlan.jsx`                          |
| US-F6 | Como cliente, quero registrar quando completo uma refeição.                                     | Checkbox/botão para marcar refeição completa com feedback visual imediato.                                  | `DietDailyLogger.jsx`                                          |
| US-F7 | Como cliente, quero ver meu progresso de dieta em gráficos.                                     | Gráficos de progresso semanal/mensal, calendário de cumprimento.                                            | `DietProgressChart.jsx`, `DietCalendar.jsx`                    |
| US-F8 | Como cliente, quero visualizar minhas atividades prescritas.                                    | Lista de atividades do dia, plano semanal, orientações detalhadas.                                          | `ActivitiesPage.jsx`, `ActivityPlan.jsx`                       |
| US-F9 | Como cliente, quero registrar atividades realizadas com cronômetro.                             | Timer/cronômetro integrado, registro de duração, feedback de conclusão.                                     | `ActivityTimer.jsx`, `ActivityLogger.jsx`                      |
| US-F10| Como cliente, quero ver meu histórico de atividades e conquistas.                               | Histórico visual, badges de conquistas, estatísticas de progresso.                                          | `ActivityHistory.jsx`, `AchievementsBadges.jsx`                |
| US-F11| Como cliente, quero solicitar agendamentos com a clínica.                                       | Formulário de solicitação, seleção de data/hora, campo de observações.                                      | `AppointmentRequest.jsx`                                       |
| US-F12| Como cliente, quero visualizar meus agendamentos (confirmados e pendentes).                     | Lista de agendamentos com status visual, filtros por data e status.                                         | `AppointmentsPage.jsx`, `AppointmentsList.jsx`                 |
| US-F13| Como cliente, quero cancelar solicitações de agendamento.                                       | Botão de cancelamento com confirmação, atualização de status em tempo real.                                 | `AppointmentCancel.jsx`                                        |
| US-F14| Como cliente, quero receber notificações em tempo real.                                         | Sistema de notificações push, indicadores visuais, histórico de notificações.                               | `NotificationSystem.jsx`                                       |
| US-F15| Como cliente, quero uma interface responsiva em todos os dispositivos.                          | Layout adaptativo, componentes flexíveis, experiência consistente mobile/desktop.                           | Todos os componentes com CSS responsivo                        |

---

## 🚀 Planejamento de Sprints
Assumindo sprints de 1 semana cada:

### Sprint 1F — Estrutura Base e Autenticação
**Período:** Semana 1  
**Responsável:** Frontend Developer

#### **Objetivos**
- Criar estrutura de pastas para área do cliente
- Implementar redirecionamento pós-login
- Configurar roteamento protegido
- Desenvolver layout base responsivo

#### **Tarefas Detalhadas**
- **US-F1**: Redirecionamento Pós-Login
  - Componente `ClientAuthRedirect.jsx`
  - Integração com API `/api/auth/user-type`
  - Redirecionamento automático baseado no tipo de usuário
  
- **US-F2**: Layout e Navegação
  - Componente `ClientLayout.jsx` com header, sidebar e footer
  - Componente `ClientHeader.jsx` com menu de navegação
  - Roteamento protegido para `/client/*`
  - CSS responsivo base

#### **Estrutura de Pastas a Criar**
```
src/
├── client/
│   ├── components/
│   │   ├── layout/
│   │   ├── common/
│   │   └── forms/
│   ├── pages/
│   │   ├── Dashboard/
│   │   ├── Diet/
│   │   ├── Activities/
│   │   └── Appointments/
│   ├── hooks/
│   ├── services/
│   ├── utils/
│   └── styles/
└── shared/
    ├── components/
    ├── hooks/
    └── utils/
```

#### **Componentes Base**
```javascript
// ClientLayout.jsx - Layout principal
// ClientHeader.jsx - Header com navegação
// ClientSidebar.jsx - Menu lateral
// ProtectedRoute.jsx - Rota protegida
// LoadingSpinner.jsx - Componente de loading
```

#### **Entregáveis**
- ✅ Estrutura de pastas criada
- ✅ Redirecionamento funcionando
- ✅ Rotas protegidas implementadas
- ✅ Layout base responsivo
- ✅ Navegação funcional

---

### Sprint 2F — Dashboard do Cliente
**Período:** Semana 2  
**Responsável:** Frontend Developer

#### **Objetivos**
- Criar dashboard principal com cards informativos
- Implementar sistema de pontuação visual
- Configurar atualizações em tempo real
- Desenvolver componentes reutilizáveis

#### **Tarefas Detalhadas**
- **US-F3**: Dashboard Principal
  - Página `ClientDashboard.jsx`
  - Integração com API `/api/client/dashboard`
  - Layout em grid responsivo
  - Cards informativos organizados
  
- **US-F4**: Sistema de Gamificação Visual
  - Componente `GamificationCard.jsx`
  - Indicadores de pontos em tempo real
  - Barras de progresso animadas
  - Feedback visual para conquistas

#### **Cards do Dashboard**
```javascript
// PetInfoCard.jsx - Informações do pet
// GamificationCard.jsx - Pontos e progresso
// NextAppointmentCard.jsx - Próxima consulta
// WeeklySummaryCard.jsx - Resumo semanal
// QuickActionsCard.jsx - Ações rápidas
```

#### **Funcionalidades de Tempo Real**
```javascript
// Real-time updates via Supabase subscriptions
// Automatic point updates
// Live appointment notifications
// Progress bar animations
```

#### **Design Responsivo**
```css
/* Grid adaptativo para diferentes telas */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

/* Cards flexíveis */
.dashboard-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
```

#### **Entregáveis**
- ✅ Dashboard funcional e responsivo
- ✅ Cards informativos implementados
- ✅ Sistema de pontuação visual
- ✅ Updates em tempo real funcionando
- ✅ Animações e feedback visual

---

### Sprint 3F — Interface de Dieta
**Período:** Semana 3  
**Responsável:** Frontend Developer

#### **Objetivos**
- Criar interface completa para acompanhamento de dieta
- Implementar registro de refeições com gamificação
- Desenvolver visualizações de progresso
- Adicionar calendário de cumprimento

#### **Tarefas Detalhadas**
- **US-F5**: Página de Dieta
  - Componente `DietPage.jsx`
  - Integração com API `/api/client/diet/current`
  - Visualização da dieta prescrita
  - Lista de alimentos permitidos/proibidos
  
- **US-F6**: Registro de Refeições
  - Componente `DietDailyLogger.jsx`
  - Integração com API `/api/client/diet/progress`
  - Checkbox para marcar refeição completa
  - Feedback visual imediato com animações
  
- **US-F7**: Progresso Visual
  - Componente `DietProgressChart.jsx`
  - Componente `DietCalendar.jsx`
  - Gráficos de progresso semanal/mensal
  - Calendário com indicadores de cumprimento

#### **Componentes de Dieta**
```javascript
// DietPage.jsx - Página principal
// DietCurrentPlan.jsx - Plano atual
// DietDailyLogger.jsx - Registro diário
// DietProgressChart.jsx - Gráficos de progresso
// DietCalendar.jsx - Calendário de cumprimento
// DietFoodList.jsx - Lista de alimentos
// DietGamification.jsx - Elementos de gamificação
```

#### **Funcionalidades de Gamificação**
```javascript
// Animação ao completar refeição
// Pontos visuais (+10 pontos)
// Progresso da meta diária
// Streak de dias consecutivos
// Badges por conquistas
```

#### **Visualizações de Dados**
```javascript
// Gráfico de barras - progresso semanal
// Gráfico de linha - tendência mensal
// Calendário heat map - cumprimento diário
// Indicadores de meta - porcentagem de sucesso
```

#### **Entregáveis**
- ✅ Interface de dieta completa
- ✅ Registro de refeições funcionando
- ✅ Progresso visual implementado
- ✅ Calendário de cumprimento
- ✅ Gamificação visual ativa

---

### Sprint 4F — Interface de Atividades
**Período:** Semana 4  
**Responsável:** Frontend Developer

#### **Objetivos**
- Criar interface para registro de atividades
- Implementar timer/cronômetro integrado
- Desenvolver sistema de conquistas
- Adicionar histórico visual de atividades

#### **Tarefas Detalhadas**
- **US-F8**: Página de Atividades
  - Componente `ActivitiesPage.jsx`
  - Integração com API `/api/client/activities/current`
  - Lista de atividades prescritas
  - Plano semanal de atividades
  
- **US-F9**: Timer e Registro
  - Componente `ActivityTimer.jsx`
  - Componente `ActivityLogger.jsx`
  - Cronômetro integrado
  - Integração com API `/api/client/activities/complete`
  
- **US-F10**: Histórico e Conquistas
  - Componente `ActivityHistory.jsx`
  - Componente `AchievementsBadges.jsx`
  - Integração com API `/api/client/activities/history`
  - Sistema visual de badges

#### **Componentes de Atividades**
```javascript
// ActivitiesPage.jsx - Página principal
// ActivityPlan.jsx - Plano de atividades
// ActivityTimer.jsx - Timer/cronômetro
// ActivityLogger.jsx - Registro de atividade
// ActivityHistory.jsx - Histórico
// AchievementsBadges.jsx - Sistema de conquistas
// ActivityProgress.jsx - Progresso visual
```

#### **Funcionalidades do Timer**
```javascript
// Cronômetro com start/pause/stop
// Registro automático de duração
// Feedback visual durante atividade
// Notificação de conclusão
// Cálculo automático de pontos
```

#### **Sistema de Conquistas**
```javascript
// Badges por metas atingidas
// Progresso visual de conquistas
// Histórico de achievements
// Animações de desbloqueio
// Compartilhamento social (futuro)
```

#### **Entregáveis**
- ✅ Interface de atividades completa
- ✅ Timer/cronômetro funcionando
- ✅ Sistema de conquistas implementado
- ✅ Histórico visual de atividades
- ✅ Feedback visual e animações

---

### Sprint 5F — Sistema de Agendamentos
**Período:** Semana 5  
**Responsável:** Frontend Developer

#### **Objetivos**
- Criar interface para solicitação de agendamentos
- Implementar visualização de agendamentos
- Desenvolver sistema de cancelamento
- Adicionar notificações em tempo real

#### **Tarefas Detalhadas**
- **US-F11**: Solicitação de Agendamentos
  - Componente `AppointmentRequest.jsx`
  - Integração com API `/api/client/appointments/request`
  - Formulário com validações
  - Seleção de data/hora disponível
  
- **US-F12**: Visualização de Agendamentos
  - Componente `AppointmentsPage.jsx`
  - Componente `AppointmentsList.jsx`
  - Integração com API `/api/client/appointments`
  - Filtros por status e data
  
- **US-F13**: Cancelamento de Agendamentos
  - Componente `AppointmentCancel.jsx`
  - Integração com API `/api/client/appointments/:id/cancel`
  - Modal de confirmação
  - Atualização em tempo real

#### **Componentes de Agendamentos**
```javascript
// AppointmentsPage.jsx - Página principal
// AppointmentRequest.jsx - Formulário de solicitação
// AppointmentsList.jsx - Lista de agendamentos
// AppointmentCard.jsx - Card individual
// AppointmentCancel.jsx - Modal de cancelamento
// AppointmentStatus.jsx - Indicadores de status
```

#### **Funcionalidades do Formulário**
```javascript
// Seleção de data com calendário
// Horários disponíveis dinâmicos
// Campo de observações
// Validação de dados
// Feedback de envio
```

#### **Status de Agendamentos**
```javascript
// Pendente - aguardando aprovação
// Aprovado - confirmado pela clínica
// Rejeitado - negado pela clínica
// Cancelado - cancelado pelo cliente
// Realizado - consulta concluída
```

#### **Entregáveis**
- ✅ Interface de agendamentos completa
- ✅ Formulário de solicitação funcionando
- ✅ Sistema de cancelamento implementado
- ✅ Filtros e busca funcionais
- ✅ Status visuais claros

---

### Sprint 6F — Notificações e Polimento
**Período:** Semana 6  
**Responsável:** Frontend Developer

#### **Objetivos**
- Implementar sistema de notificações em tempo real
- Finalizar responsividade em todos os componentes
- Adicionar animações e micro-interações
- Realizar testes de usabilidade e correções

#### **Tarefas Detalhadas**
- **US-F14**: Sistema de Notificações
  - Componente `NotificationSystem.jsx`
  - Notificações push em tempo real
  - Histórico de notificações
  - Configurações de preferências
  
- **US-F15**: Responsividade Final
  - Revisão de todos os componentes
  - Testes em diferentes dispositivos
  - Ajustes de CSS responsivo
  - Otimização de performance

#### **Sistema de Notificações**
```javascript
// Notificações de pontos ganhos
// Lembretes de refeições
// Confirmações de agendamento
// Alertas de atividades
// Mensagens da clínica
```

#### **Micro-interações**
```javascript
// Animações de loading
// Feedback de hover
// Transições suaves
// Animações de sucesso
// Indicadores de progresso
```

#### **Otimizações Finais**
```javascript
// Lazy loading de componentes
// Otimização de imagens
// Minificação de CSS
// Cache de dados
// Performance monitoring
```

#### **Entregáveis**
- ✅ Sistema de notificações funcionando
- ✅ Responsividade 100% implementada
- ✅ Animações e micro-interações
- ✅ Performance otimizada
- ✅ Testes de usabilidade realizados

---

## 📊 Cronograma Integrado

| Semana | Sprint Frontend | Principais Entregas |
|--------|-----------------|---------------------|
| 1      | Sprint 1F       | Estrutura base, layout, navegação |
| 2      | Sprint 2F       | Dashboard completo com gamificação |
| 3      | Sprint 3F       | Interface de dieta com progresso |
| 4      | Sprint 4F       | Interface de atividades com timer |
| 5      | Sprint 5F       | Sistema de agendamentos completo |
| 6      | Sprint 6F       | Notificações e polimento final |

---

## ✅ Checklist de Cada Sprint

### **Checklist Sprint Frontend**
- [ ] Componentes implementados e testados
- [ ] Design responsivo validado
- [ ] Integração com APIs funcionando
- [ ] Testes de usabilidade realizados
- [ ] Code review realizado
- [ ] Deploy em ambiente de desenvolvimento
- [ ] Validação com dados reais

### **Checklist Design e UX**
- [ ] Interface intuitiva e acessível
- [ ] Feedback visual adequado
- [ ] Animações suaves e funcionais
- [ ] Responsividade em todos os dispositivos
- [ ] Performance otimizada
- [ ] Compatibilidade entre navegadores

### **Checklist Integração**
- [ ] APIs integradas corretamente
- [ ] Dados fluindo em tempo real
- [ ] Tratamento de erros implementado
- [ ] Loading states configurados
- [ ] Validações de formulário funcionando
- [ ] Notificações em tempo real ativas

---

## 🎯 Próximos Passos

1. **Executar Sprint 1F**: Estrutura base e autenticação
2. **Configurar ambiente**: React, Supabase client, CSS framework
3. **Iniciar desenvolvimento**: Seguir cronograma de 6 semanas
4. **Integração contínua**: Testes com backend a cada sprint
5. **Deploy gradual**: Ambiente de desenvolvimento → produção

---

## 🎨 Considerações de Design

### **Paleta de Cores**
```css
:root {
  --primary-color: #2563eb;
  --secondary-color: #10b981;
  --accent-color: #f59e0b;
  --success-color: #22c55e;
  --warning-color: #f97316;
  --error-color: #ef4444;
  --background-color: #f8fafc;
  --card-background: #ffffff;
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
}
```

### **Tipografia**
```css
/* Fonte principal */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

/* Hierarquia */
h1: 2.5rem / 40px
h2: 2rem / 32px
h3: 1.5rem / 24px
body: 1rem / 16px
small: 0.875rem / 14px
```

### **Componentes Base**
- Cards com sombra sutil e bordas arredondadas
- Botões com estados hover/active/disabled
- Inputs com validação visual
- Loading spinners consistentes
- Modais com overlay escuro

---

**Observações:**
- Priorizar experiência do usuário em todos os componentes
- Manter consistência visual em toda a aplicação
- Implementar feedback visual para todas as ações
- Garantir acessibilidade (WCAG 2.1)
- Realizar testes em diferentes dispositivos e navegadores
- Documentar componentes reutilizáveis

Boa codificação! 🚀