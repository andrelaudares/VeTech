# Testes da API VeTech

Este documento contém instruções para executar os testes das rotas da API VeTech.

## Pré-requisitos

Antes de executar os testes, certifique-se de que:

1. O servidor da API está em execução
2. Você possui credenciais válidas de uma clínica cadastrada
3. As dependências Python estão instaladas (`requests`)

## Configuração dos Testes

### 1. Configurar o teste de perfil da clínica

Abra o arquivo `test_clinic_profile.py` e modifique as seguintes variáveis:

```python
# Substitua por credenciais de uma clínica existente no seu banco
LOGIN_EMAIL = "sua-clinica@example.com"  # Substitua por email válido
LOGIN_PASSWORD = "sua-senha-aqui"  # Substitua por senha válida
```

### 2. Configurar o teste de animais

Abra o arquivo `test_animals_endpoints.py` e modifique a seguinte variável:

```python
# Substitua pelo ID de uma clínica existente no seu banco
CLINIC_ID = "seu-clinic-id-aqui"  # Substitua por um UUID válido da tabela clinics
```

Você pode obter o UUID da clínica após fazer login no teste do perfil da clínica.

### 3. Configurar o teste de preferências alimentares

Abra o arquivo `test_animal_preferences.py` e modifique as seguintes variáveis:

```python
# Substitua pelo ID de uma clínica existente no seu banco
CLINIC_ID = "seu-clinic-id-aqui"  # Ex: "dba93fba-3bfa-4254-8dd9-efcdc9608e0f"
# Substitua pelo ID de um animal existente no seu banco
ANIMAL_ID = "id-de-um-animal-existente"
```

### 4. Configurar o teste de agendamentos e consultas

Abra o arquivo `test_appointments_consultations.py` e modifique as seguintes variáveis:

```python
# Substitua pelo ID de uma clínica existente no seu banco
CLINIC_ID = "seu-clinic-id-aqui"  # Ex: "dba93fba-3bfa-4254-8dd9-efcdc9608e0f"
# ID de um animal para teste (substitua por um válido)
ANIMAL_ID = "id-de-um-animal-existente"
```

## Executando os Testes

### Iniciar o servidor

Primeiro, certifique-se de que o servidor da API está em execução:

```bash
cd backend
python main.py
```

Ou usando o script de debug:

```bash
cd backend
python debug_server.py
```

### Executar o teste de perfil da clínica

```bash
cd backend
python test_clinic_profile.py
```

### Executar o teste de endpoints de animais

```bash
cd backend
python test_animals_endpoints.py
```

### Executar o teste de preferências alimentares

```bash
cd backend
python test_animal_preferences.py
```

### Executar o teste de agendamentos e consultas

```bash
cd backend
python test_appointments_consultations.py
```

## Estrutura dos Testes

### Teste de Perfil da Clínica (`test_clinic_profile.py`)

Este teste verifica as seguintes funcionalidades:

1. Login da clínica
2. Obtenção dos dados do perfil
3. Atualização dos dados do perfil
4. Logout da clínica

### Teste de Endpoints de Animais (`test_animals_endpoints.py`)

Este teste verifica as seguintes funcionalidades:

1. Listagem de animais
2. Criação de um novo animal
3. Obtenção dos detalhes de um animal específico
4. Atualização dos dados de um animal
5. Remoção de um animal

### Teste de Preferências Alimentares (`test_animal_preferences.py`)

Este teste verifica as seguintes funcionalidades:

1. Criação de preferências alimentares para um animal
2. Obtenção das preferências alimentares
3. Atualização das preferências alimentares

### Teste de Agendamentos e Consultas (`test_appointments_consultations.py`)

Este teste verifica as seguintes funcionalidades:

**Agendamentos:**
1. Criação de um agendamento
2. Listagem de agendamentos
3. Visualização dos detalhes de um agendamento
4. Atualização de um agendamento
5. Remoção de um agendamento

**Consultas:**
1. Criação de uma consulta
2. Listagem de consultas
3. Atualização de uma consulta
4. Remoção de uma consulta

## Resultados Esperados

Os testes exibirão mensagens de sucesso (✅) ou erro (❌) para cada operação realizada, juntamente com detalhes das respostas da API.

## Solução de Problemas

- **Erro de conexão**: Verifique se o servidor da API está em execução e acessível no endereço e porta corretos.
- **Erro de autenticação**: Certifique-se de que as credenciais fornecidas são válidas.
- **Erro 404 (Not Found)**: Verifique se os IDs utilizados nos testes correspondem a registros existentes no banco de dados.
- **Erro 500 (Internal Server Error)**: Verifique os logs do servidor para obter mais detalhes sobre o erro. 