import requests
import json
import uuid
from datetime import datetime, date

# URL base da API (ajuste conforme sua configuração)
API_URL = "http://127.0.0.1:8000/api/v1"

# Substitua pelo ID de uma clínica existente no seu banco
CLINIC_ID = "dba93fba-3bfa-4254-8dd9-efcdc9608e0f"  # Ex: "dba93fba-3bfa-4254-8dd9-efcdc9608e0f"
# ID de um animal para teste (substitua por um válido)
ANIMAL_ID = "9aeeac0e-211d-4b86-ac21-b78675098b81"  # Obtenha de test_animals_endpoints.py

#########################
# TESTES DE AGENDAMENTOS
#########################

def test_create_appointment():
    """Teste de criação de agendamento"""
    
    # Dados para criar um agendamento
    today = date.today().isoformat()
    appointment_data = {
        "animal_id": ANIMAL_ID,
        "date": today,
        "start_time": "14:30:00",
        "end_time": "15:00:00",
        "description": "Consulta de rotina",
        "status": "scheduled"
    }
    
    # Requisição
    response = requests.post(
        f"{API_URL}/appointments?clinic_id={CLINIC_ID}",
        json=appointment_data
    )
    
    # Verificação
    if response.status_code == 200:
        print("✅ Agendamento criado com sucesso!")
        appointment = response.json()
        print(json.dumps(appointment, indent=2))
        return appointment.get("id")
    else:
        print(f"❌ Erro ao criar agendamento: {response.status_code}")
        print(response.text)
        return None

def test_list_appointments():
    """Teste de listagem de agendamentos"""
    
    response = requests.get(
        f"{API_URL}/appointments?clinic_id={CLINIC_ID}"
    )
    
    if response.status_code == 200:
        appointments = response.json()
        print(f"✅ {len(appointments)} agendamentos encontrados!")
        
        # Mostrar resumo dos primeiros 3
        for i, appt in enumerate(appointments[:3]):
            print(f"Agendamento {i+1}: {appt.get('date')} {appt.get('start_time')} - {appt.get('description')}")
        
        return appointments
    else:
        print(f"❌ Erro ao listar agendamentos: {response.status_code}")
        print(response.text)
        return None

def test_get_appointment(appointment_id):
    """Teste de obtenção de detalhes de um agendamento"""
    
    if not appointment_id:
        print("❌ ID de agendamento não fornecido")
        return None
    
    response = requests.get(
        f"{API_URL}/appointments/{appointment_id}?clinic_id={CLINIC_ID}"
    )
    
    if response.status_code == 200:
        print("✅ Agendamento encontrado!")
        appointment = response.json()
        print(json.dumps(appointment, indent=2))
        return appointment
    else:
        print(f"❌ Erro ao buscar agendamento: {response.status_code}")
        print(response.text)
        return None

def test_update_appointment(appointment_id):
    """Teste de atualização de agendamento"""
    
    if not appointment_id:
        print("❌ ID de agendamento não fornecido")
        return None
    
    update_data = {
        "description": f"Consulta atualizada em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "status": "confirmed"
    }
    
    response = requests.patch(
        f"{API_URL}/appointments/{appointment_id}?clinic_id={CLINIC_ID}",
        json=update_data
    )
    
    if response.status_code == 200:
        print("✅ Agendamento atualizado com sucesso!")
        appointment = response.json()
        print(json.dumps(appointment, indent=2))
        return appointment
    else:
        print(f"❌ Erro ao atualizar agendamento: {response.status_code}")
        print(response.text)
        return None

def test_delete_appointment(appointment_id):
    """Teste de remoção de agendamento"""
    
    if not appointment_id:
        print("❌ ID de agendamento não fornecido")
        return False
    
    response = requests.delete(
        f"{API_URL}/appointments/{appointment_id}?clinic_id={CLINIC_ID}"
    )
    
    if response.status_code == 200:
        print("✅ Agendamento removido com sucesso!")
        print(response.json().get("message", ""))
        return True
    else:
        print(f"❌ Erro ao remover agendamento: {response.status_code}")
        print(response.text)
        return False

########################
# TESTES DE CONSULTAS
########################

def test_create_consultation():
    """Teste de criação de consulta"""
    
    consultation_data = {
        "animal_id": ANIMAL_ID,
        "description": f"Consulta de rotina criada em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "date": datetime.now().isoformat()
    }
    
    response = requests.post(
        f"{API_URL}/consultations?clinic_id={CLINIC_ID}",
        json=consultation_data
    )
    
    if response.status_code == 200:
        print("✅ Consulta criada com sucesso!")
        consultation = response.json()
        print(json.dumps(consultation, indent=2))
        return consultation.get("id")
    else:
        print(f"❌ Erro ao criar consulta: {response.status_code}")
        print(response.text)
        return None

def test_list_consultations():
    """Teste de listagem de consultas"""
    
    response = requests.get(
        f"{API_URL}/consultations?clinic_id={CLINIC_ID}"
    )
    
    if response.status_code == 200:
        consultations = response.json()
        print(f"✅ {len(consultations)} consultas encontradas!")
        
        # Mostrar resumo das primeiras 3
        for i, cons in enumerate(consultations[:3]):
            print(f"Consulta {i+1}: {cons.get('date')} - {cons.get('description')[:30]}...")
        
        return consultations
    else:
        print(f"❌ Erro ao listar consultas: {response.status_code}")
        print(response.text)
        return None

def test_update_consultation(consultation_id):
    """Teste de atualização de consulta"""
    
    if not consultation_id:
        print("❌ ID de consulta não fornecido")
        return None
    
    update_data = {
        "description": f"Descrição atualizada em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    }
    
    response = requests.patch(
        f"{API_URL}/consultations/{consultation_id}?clinic_id={CLINIC_ID}",
        json=update_data
    )
    
    if response.status_code == 200:
        print("✅ Consulta atualizada com sucesso!")
        consultation = response.json()
        print(json.dumps(consultation, indent=2))
        return consultation
    else:
        print(f"❌ Erro ao atualizar consulta: {response.status_code}")
        print(response.text)
        return None

def test_delete_consultation(consultation_id):
    """Teste de remoção de consulta"""
    
    if not consultation_id:
        print("❌ ID de consulta não fornecido")
        return False
    
    response = requests.delete(
        f"{API_URL}/consultations/{consultation_id}?clinic_id={CLINIC_ID}"
    )
    
    if response.status_code == 204:
        print("✅ Consulta removida com sucesso!")
        return True
    else:
        print(f"❌ Erro ao remover consulta: {response.status_code}")
        print(response.text)
        return False

#################################
# EXECUÇÃO DOS TESTES
#################################

def run_appointments_tests():
    """Executa todos os testes de agendamentos"""
    
    print("\n🔹 TESTES DE AGENDAMENTOS 🔹\n")
    
    # Listar agendamentos (antes)
    print("\n📋 Listando agendamentos existentes...")
    test_list_appointments()
    
    # Criar novo agendamento
    print("\n➕ Criando novo agendamento...")
    appointment_id = test_create_appointment()
    
    if appointment_id:
        # Obter detalhes
        print("\n🔍 Obtendo detalhes do agendamento...")
        test_get_appointment(appointment_id)
        
        # Atualizar
        print("\n✏️ Atualizando agendamento...")
        test_update_appointment(appointment_id)
        
        # Remover
        print("\n❌ Removendo agendamento...")
        test_delete_appointment(appointment_id)
        
        # Verificar remoção
        print("\n🔍 Verificando remoção...")
        result = test_get_appointment(appointment_id)
        if not result:
            print("✅ Agendamento removido com sucesso!")
    
    print("\n✅ Testes de agendamentos concluídos!\n")

def run_consultations_tests():
    """Executa todos os testes de consultas"""
    
    print("\n🔹 TESTES DE CONSULTAS 🔹\n")
    
    # Listar consultas (antes)
    print("\n📋 Listando consultas existentes...")
    test_list_consultations()
    
    # Criar nova consulta
    print("\n➕ Criando nova consulta...")
    consultation_id = test_create_consultation()
    
    if consultation_id:
        # Atualizar
        print("\n✏️ Atualizando consulta...")
        test_update_consultation(consultation_id)
        
        # Listar novamente
        print("\n📋 Listando consultas após criação/atualização...")
        test_list_consultations()
        
        # Remover
        print("\n❌ Removendo consulta...")
        test_delete_consultation(consultation_id)
    
    print("\n✅ Testes de consultas concluídos!\n")

if __name__ == "__main__":
    print("\n🚀 INICIANDO TESTES DE AGENDAMENTOS E CONSULTAS\n")
    print("⚠️ ATENÇÃO: Atualize as variáveis CLINIC_ID e ANIMAL_ID no início do script!")
    
    # Executar testes de agendamentos
    run_appointments_tests()
    
    # Executar testes de consultas
    run_consultations_tests()
    
    print("\n🏁 TODOS OS TESTES CONCLUÍDOS!") 