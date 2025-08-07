# Sprint 4 - Backend Implementation Plan
## Área do Tutor - Sistema de Agendamentos e Consultas

### 📋 Visão Geral
Este documento detalha a implementação backend necessária para completar a funcionalidade da área do tutor, focando em agendamentos e consultas.

### 🗂️ Reorganização de Arquivos Backend

#### Estrutura Atual
```
/backend/app/api/
├── appointments.py     # ✅ Bem organizado
├── consultations.py    # ✅ Bem organizado  
├── client.py          # ⚠️ Nome genérico demais
└── ...
```

#### Estrutura Proposta
```
/backend/app/api/
├── appointments.py           # Agendamentos da clínica
├── consultations.py         # Consultas realizadas
├── tutor_profile.py        # Perfil e dados do tutor (renomear client.py)
├── tutor_appointments.py   # Agendamentos específicos do tutor
├── appointment_requests.py # Solicitações de agendamento
└── ...
```

### 🎯 Objetivos da Sprint 4

#### 1. Listagem de Agendamentos do Tutor
**Frontend:** `ClientAppointmentsPage.jsx`
**Backend:** Reutilizar/adaptar `appointments.py`

**Análise da Rota Existente:**
- ✅ GET `/appointments/` - Lista todos os agendamentos
- ⚠️ Precisa filtrar por tutor específico
- ✅ Estrutura de dados compatível

**Implementação Necessária:**
```python
# Em appointments.py - adicionar endpoint específico
@router.get("/tutor/{tutor_id}")
async def get_tutor_appointments(tutor_id: int, db: Session = Depends(get_db)):
    """Lista agendamentos de um tutor específico"""
    pass
```

#### 2. Sistema de Solicitação de Agendamentos
**Frontend:** Modal em `ClientAppointmentsPage.jsx`
**Backend:** Novo arquivo `appointment_requests.py`

**Campos da Solicitação:**
- `date` (data solicitada)
- `time` (horário solicitado)
- `type` (tipo de serviço)
- `observation` (observações do tutor)
- `tutor_id` (ID do tutor)
- `animal_id` (ID do animal)
- `status` (sempre 'pending' inicialmente)

**Endpoints Necessários:**
```python
# appointment_requests.py
POST /appointment-requests/     # Criar solicitação
GET /appointment-requests/      # Listar pendentes (para clínica)
PUT /appointment-requests/{id}  # Editar/confirmar
DELETE /appointment-requests/{id} # Recusar/deletar
```

#### 3. Gestão de Solicitações na Clínica
**Frontend:** `AppointmentsPage.jsx` (modal de notificações)
**Backend:** Integração com `appointment_requests.py`

**Funcionalidades:**
- ✅ Listar solicitações pendentes
- ✅ Mostrar dados do tutor (incluindo telefone)
- ✅ Confirmar → mover para appointments
- ✅ Editar → atualizar e confirmar
- ✅ Recusar → deletar solicitação

#### 4. Detalhes de Consultas para Tutores
**Frontend:** Popup em `ClientAppointmentsPage.jsx`
**Backend:** Adaptar `consultations.py`

**Implementação:**
```python
# Em consultations.py - adicionar endpoint
@router.get("/tutor/{tutor_id}/appointment/{appointment_id}")
async def get_consultation_details(tutor_id: int, appointment_id: int, db: Session = Depends(get_db)):
    """Retorna detalhes da consulta (campo description)"""
    pass
```

### 🗄️ Estrutura do Banco de Dados

#### Tabelas Relevantes:
```sql
-- appointments (existente)
id, date, time, tutor_id, animal_id, service_type, status, notes, created_at, updated_at

-- consultations (existente) 
id, appointment_id, description, diagnosis, treatment, recommendations, created_at, updated_at

-- animals (existente)
id, name, species, breed, age, tutor_id, created_at, updated_at
```

#### Nova Tabela Sugerida:
```sql
-- appointment_requests (nova)
CREATE TABLE appointment_requests (
    id SERIAL PRIMARY KEY,
    tutor_id INTEGER REFERENCES users(id),
    animal_id INTEGER REFERENCES animals(id),
    requested_date DATE NOT NULL,
    requested_time TIME NOT NULL,
    service_type VARCHAR(100) NOT NULL,
    notes TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 🔧 Implementação Técnica

#### Fase 1: Reorganização
1. Renomear `client.py` → `tutor_profile.py`
2. Atualizar imports nos arquivos que referenciam
3. Testar funcionalidades existentes

#### Fase 2: Agendamentos do Tutor
1. Adicionar endpoint em `appointments.py` para filtrar por tutor
2. Conectar ao frontend `ClientAppointmentsPage.jsx`
3. Testar listagem e filtros

#### Fase 3: Sistema de Solicitações
1. Criar `appointment_requests.py`
2. Implementar CRUD completo
3. Integrar com frontend (modal de solicitação)
4. Integrar com clínica (modal de notificações)

#### Fase 4: Consultas Detalhadas
1. Adaptar `consultations.py`
2. Criar endpoint específico para tutores
3. Integrar com popup no frontend

### 📊 Modelos de Dados

#### AppointmentRequest
```python
class AppointmentRequestCreate(BaseModel):
    animal_id: int
    requested_date: date
    requested_time: time
    service_type: str
    notes: Optional[str] = None

class AppointmentRequestResponse(BaseModel):
    id: int
    tutor_id: int
    animal_id: int
    animal_name: str
    tutor_name: str
    tutor_phone: str
    requested_date: date
    requested_time: time
    service_type: str
    notes: Optional[str]
    status: str
    created_at: datetime
```

#### ConsultationDetails
```python
class ConsultationDetailsResponse(BaseModel):
    id: int
    appointment_id: int
    description: str
    diagnosis: Optional[str]
    treatment: Optional[str]
    recommendations: Optional[str]
    created_at: datetime
```

### 🔗 Integração Frontend-Backend

#### ClientAppointmentsPage.jsx
```javascript
// Listar agendamentos do tutor
GET /api/appointments/tutor/{tutorId}

// Solicitar agendamento
POST /api/appointment-requests/

// Ver detalhes da consulta
GET /api/consultations/tutor/{tutorId}/appointment/{appointmentId}
```

#### AppointmentsPage.jsx
```javascript
// Listar solicitações pendentes
GET /api/appointment-requests/?status=pending

// Confirmar solicitação
PUT /api/appointment-requests/{id} → POST /api/appointments/

// Recusar solicitação
DELETE /api/appointment-requests/{id}
```

### ✅ Checklist de Implementação

#### Backend
- [ ] Renomear `client.py` → `tutor_profile.py`
- [ ] Criar `appointment_requests.py`
- [ ] Adicionar endpoint de agendamentos por tutor
- [ ] Adaptar `consultations.py` para tutores
- [ ] Criar tabela `appointment_requests`
- [ ] Implementar modelos Pydantic
- [ ] Adicionar validações e tratamento de erros
- [ ] Testar todos os endpoints

#### Frontend
- [ ] Conectar listagem de agendamentos
- [ ] Conectar solicitação de agendamentos
- [ ] Conectar detalhes de consultas
- [ ] Testar fluxo completo tutor → clínica
- [ ] Validar responsividade
- [ ] Testar tratamento de erros

### 🚀 Próximos Passos

1. **Análise Detalhada:** Examinar código atual dos arquivos backend
2. **Reorganização:** Implementar nova estrutura de arquivos
3. **Desenvolvimento:** Criar novos endpoints necessários
4. **Integração:** Conectar frontend com backend
5. **Testes:** Validar fluxo completo
6. **Documentação:** Atualizar documentação da API

### 📝 Observações Importantes

- ✅ O botão "Editar" já existe em `AppointmentsPage.jsx`
- ✅ A estrutura do banco suporta as funcionalidades necessárias
- ✅ O frontend está preparado para receber os dados
- ⚠️ Atenção especial à autenticação e autorização
- ⚠️ Validar permissões (tutor só vê seus dados)
- ⚠️ Implementar logs para auditoria

---

**Documento criado para Sprint 4 - Área do Tutor**  
**Data:** $(date)  
**Versão:** 1.0