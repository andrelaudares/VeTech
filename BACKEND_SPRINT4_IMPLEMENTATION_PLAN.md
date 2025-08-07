# Plano de Implementação Backend - Sprint 4: Área do Tutor

## 📋 Visão Geral

Este documento detalha a implementação organizada do backend para a Sprint 4, focando na integração das funcionalidades da área do tutor com o sistema de agendamentos e consultas da clínica.

## 🗂️ Estrutura Atual do Backend

### Arquivos Existentes
- `/backend/app/api/appointments.py` - ✅ Funcional (rotas da clínica)
- `/backend/app/api/consultations.py` - ✅ Funcional (rotas da clínica)
- `/backend/app/api/client.py` - ⚠️ Precisa reorganização (contém rotas gerais do tutor)

### Estrutura do Banco de Dados (Supabase)

#### Tabela `appointments`
```sql
- id (uuid, PK)
- clinic_id (uuid, FK)
- animal_id (uuid, FK)
- date (date)
- start_time (time)
- end_time (time, nullable)
- description (text, nullable)
- status (varchar) - valores: 'agendado', 'concluido', 'cancelado'
- solicitado_por_cliente (boolean, nullable) - ✅ Campo já existe
- status_solicitacao (varchar, nullable) - ✅ Campo já existe
- observacoes_cliente (text, nullable) - ✅ Campo já existe
- created_at, updated_at (timestamp)
```

#### Tabela `consultations`
```sql
- id (uuid, PK)
- animal_id (uuid, FK)
- clinic_id (uuid, FK)
- date (timestamp)
- description (text) - ✅ Campo necessário para popup
- created_at, updated_at (timestamp)
```

#### Tabela `animals`
```sql
- id (uuid, PK)
- clinic_id (uuid, FK)
- tutor_user_id (uuid, FK) - ✅ Campo para identificar tutor
- tutor_name (text)
- email (text)
- phone (text) - ✅ Campo necessário para exibir na clínica
- [outros campos do animal...]
```

## 🎯 Objetivos da Sprint 4

### 1. Reorganização de Arquivos Backend
**Problema:** O arquivo `client.py` contém rotas gerais do tutor, mas nem todas as rotas do tutor devem ficar lá.

**Solução:** Criar estrutura organizada:
```
/backend/app/api/
├── appointments.py          # Rotas de agendamentos (clínica)
├── consultations.py         # Rotas de consultas (clínica)
├── client/                  # Nova pasta para área do tutor
│   ├── __init__.py
│   ├── profile.py          # Perfil do tutor (mover de client.py)
│   ├── animals.py          # Animais do tutor (mover de client.py)
│   ├── appointments.py     # Agendamentos do tutor (NOVO)
│   └── consultations.py    # Consultas do tutor (NOVO)
└── client.py               # Manter apenas para compatibilidade
```

### 2. Funcionalidades a Implementar

#### 2.1 Listagem de Agendamentos do Tutor
**Frontend:** `ClientAppointmentsPage.jsx`
**Backend:** `/backend/app/api/client/appointments.py`

**Rotas necessárias:**
```python
GET /api/client/appointments
- Lista agendamentos do tutor autenticado
- Filtra por tutor_user_id
- Inclui dados do animal e clínica
- Status: 'agendado', 'concluido', 'cancelado'

GET /api/client/appointments/{appointment_id}
- Detalhes de um agendamento específico
- Verificação de propriedade (tutor_user_id)
```

#### 2.2 Solicitação de Agendamentos pelo Tutor
**Frontend:** Modal de solicitação em `ClientAppointmentsPage.jsx`
**Backend:** `/backend/app/api/client/appointments.py`

**Rota necessária:**
```python
POST /api/client/appointments/request
- Campos: animal_id, date, start_time, service_type, observacoes_cliente
- Cria agendamento com:
  * solicitado_por_cliente = true
  * status_solicitacao = 'pendente'
  * status = 'pendente' (novo status)
- Notifica clínica (via frontend)
```

#### 2.3 Gestão de Solicitações na Clínica
**Frontend:** `AppointmentsPage.jsx` (modal de notificações já existe)
**Backend:** Expandir `/backend/app/api/appointments.py`

**Rotas necessárias:**
```python
GET /api/appointments/pending-requests
- Lista solicitações pendentes para a clínica
- Inclui dados do tutor (nome, telefone)
- Inclui dados do animal

PATCH /api/appointments/{appointment_id}/approve
- Aprova solicitação (status_solicitacao = 'aprovado', status = 'agendado')

PATCH /api/appointments/{appointment_id}/reject
- Rejeita e remove solicitação

PATCH /api/appointments/{appointment_id}/edit-and-approve
- Edita dados e aprova solicitação
```

#### 2.4 Consultas do Tutor
**Frontend:** Popup em `ClientAppointmentsPage.jsx`
**Backend:** `/backend/app/api/client/consultations.py`

**Rota necessária:**
```python
GET /api/client/consultations
- Lista consultas dos animais do tutor
- Filtra por tutor_user_id através da tabela animals
- Retorna campo 'description' para popup

GET /api/client/consultations/{consultation_id}
- Detalhes de consulta específica
- Verificação de propriedade via animal
```

## 🔧 Implementação Técnica

### Fase 1: Reorganização (1-2 horas)
1. **Criar estrutura de pastas**
   ```bash
   mkdir /backend/app/api/client
   touch /backend/app/api/client/__init__.py
   ```

2. **Mover rotas existentes**
   - Extrair rotas de perfil e animais de `client.py`
   - Criar `client/profile.py` e `client/animals.py`
   - Manter `client.py` com imports para compatibilidade

3. **Atualizar roteamento principal**
   - Modificar `/backend/app/main.py` para incluir novas rotas

### Fase 2: Agendamentos do Tutor (2-3 horas)
1. **Criar `/backend/app/api/client/appointments.py`**
   - Implementar GET para listagem
   - Implementar POST para solicitações
   - Usar autenticação de tutor

2. **Expandir `/backend/app/api/appointments.py`**
   - Adicionar rota para solicitações pendentes
   - Implementar aprovação/rejeição
   - Incluir dados do tutor nas respostas

### Fase 3: Consultas do Tutor (1-2 horas)
1. **Criar `/backend/app/api/client/consultations.py`**
   - Implementar GET com filtro por tutor
   - JOIN com tabela animals para verificar propriedade
   - Retornar campo description

### Fase 4: Testes e Integração (1-2 horas)
1. **Testar todas as rotas**
2. **Verificar integração frontend-backend**
3. **Documentar APIs**

## 📝 Modelos de Dados

### Novos Modelos Necessários

```python
# /backend/app/models/client_appointment.py
class ClientAppointmentRequest(BaseModel):
    animal_id: UUID
    date: date
    start_time: time
    service_type: str
    observacoes_cliente: Optional[str] = None

class ClientAppointmentResponse(BaseModel):
    id: UUID
    animal_id: UUID
    animal_name: str
    clinic_name: str
    date: date
    start_time: time
    end_time: Optional[time]
    service_type: str
    status: str
    status_solicitacao: Optional[str]
    observacoes_cliente: Optional[str]
    created_at: datetime

# /backend/app/models/pending_request.py
class PendingRequestResponse(BaseModel):
    id: UUID
    tutor_name: str
    phone: str
    animal_name: str
    service_type: str
    date: date
    start_time: time
    observacoes_cliente: Optional[str]
    created_at: datetime
```

## 🔗 Integração Frontend-Backend

### ClientAppointmentsPage.jsx
```javascript
// Listar agendamentos
GET /api/client/appointments

// Solicitar agendamento
POST /api/client/appointments/request

// Ver consulta (popup)
GET /api/client/consultations/{consultation_id}
```

### AppointmentsPage.jsx
```javascript
// Solicitações pendentes (já implementado no frontend)
GET /api/appointments/pending-requests

// Aprovar solicitação
PATCH /api/appointments/{id}/approve

// Rejeitar solicitação
DELETE /api/appointments/{id}

// Editar e aprovar
PATCH /api/appointments/{id}/edit-and-approve
```

## ✅ Checklist de Implementação

### Backend
- [ ] Reorganizar estrutura de arquivos
- [ ] Implementar rotas de agendamentos do tutor
- [ ] Expandir rotas de agendamentos da clínica
- [ ] Implementar rotas de consultas do tutor
- [ ] Criar modelos de dados
- [ ] Testar todas as rotas

### Frontend (já implementado)
- [x] ClientAppointmentsPage.jsx com Material-UI
- [x] Modal de solicitação de agendamentos
- [x] Modal de notificações em AppointmentsPage.jsx
- [x] Botão de editar em AppointmentsPage.jsx
- [x] Popup para consultas

### Integração
- [ ] Conectar frontend com novas rotas backend
- [ ] Testar fluxo completo tutor → clínica
- [ ] Verificar autenticação e autorização
- [ ] Documentar APIs finais

## 🚀 Próximos Passos

1. **Executar Fase 1** - Reorganização de arquivos
2. **Implementar Fase 2** - Agendamentos do tutor
3. **Implementar Fase 3** - Consultas do tutor
4. **Testar integração** - Frontend + Backend
5. **Deploy e validação** - Ambiente de produção

## 📞 Observações Importantes

- ✅ **Banco de dados já preparado** - Campos necessários já existem
- ✅ **Frontend já implementado** - Interface completa com Material-UI
- ✅ **Autenticação funcionando** - Sistema de auth já implementado
- ⚠️ **Botão editar já existe** - Confirmado em AppointmentsPage.jsx linha 440-450

**Foco principal:** Implementar apenas o backend seguindo esta estrutura organizada para conectar com o frontend já pronto.