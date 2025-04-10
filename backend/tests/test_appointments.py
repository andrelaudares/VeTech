import pytest
from fastapi.testclient import TestClient
from datetime import date, time, timedelta
import uuid
import sys
import os

# Adiciona o diretório raiz ao path do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Agora importe o app com caminho absoluto
from main import app
from app.db.supabase import supabase_admin

client = TestClient(app)

# Dados de exemplo para os testes
CLINIC_ID = "dba93fba-3bfa-4254-8dd9-efcdc9608e0f"  # ID real da clínica
ANIMAL_ID = "9aeeac0e-211d-4b86-ac21-b78675098b81"  # ID real do animal

@pytest.fixture
def appointment_data():
    """Fixture que fornece dados básicos para criar um agendamento"""
    tomorrow = date.today() + timedelta(days=1)
    return {
        "animal_id": ANIMAL_ID,
        "date": tomorrow.isoformat(),
        "start_time": "14:30:00",
        "end_time": "15:00:00",
        "description": "Consulta de teste",
        "status": "scheduled"
    }

def test_create_appointment(appointment_data):
    """Testa a criação de um agendamento"""
    response = client.post(
        f"/api/v1/appointments?clinic_id={CLINIC_ID}",
        json=appointment_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["animal_id"] == ANIMAL_ID
    assert data["clinic_id"] == CLINIC_ID
    return data["id"]  # Retorna o ID para usar em outros testes

def test_get_appointments():
    """Testa a listagem de agendamentos"""
    response = client.get(f"/api/v1/appointments?clinic_id={CLINIC_ID}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_appointments_with_filters():
    """Testa a listagem de agendamentos com filtros"""
    today = date.today()
    response = client.get(
        f"/api/v1/appointments?clinic_id={CLINIC_ID}&date_from={today}&status=scheduled"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for appointment in data:
        assert appointment["status"] == "scheduled"

def test_get_specific_appointment(appointment_data):
    """Testa a busca de um agendamento específico"""
    # Primeiro cria um agendamento
    create_response = client.post(
        f"/api/v1/appointments?clinic_id={CLINIC_ID}",
        json=appointment_data
    )
    appointment_id = create_response.json()["id"]
    
    # Depois busca o agendamento criado
    response = client.get(
        f"/api/v1/appointments/{appointment_id}?clinic_id={CLINIC_ID}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == appointment_id

def test_update_appointment(appointment_data):
    """Testa a atualização de um agendamento"""
    # Primeiro cria um agendamento
    create_response = client.post(
        f"/api/v1/appointments?clinic_id={CLINIC_ID}",
        json=appointment_data
    )
    appointment_id = create_response.json()["id"]
    
    # Prepara dados para atualização
    update_data = {
        "description": "Consulta atualizada",
        "status": "completed"
    }
    
    # Atualiza o agendamento
    response = client.patch(
        f"/api/v1/appointments/{appointment_id}?clinic_id={CLINIC_ID}",
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Consulta atualizada"
    assert data["status"] == "completed"

def test_delete_appointment(appointment_data):
    """Testa a remoção de um agendamento"""
    # Primeiro cria um agendamento
    create_response = client.post(
        f"/api/v1/appointments?clinic_id={CLINIC_ID}",
        json=appointment_data
    )
    appointment_id = create_response.json()["id"]
    
    # Remove o agendamento
    response = client.delete(
        f"/api/v1/appointments/{appointment_id}?clinic_id={CLINIC_ID}"
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Agendamento removido com sucesso."
    
    # Verifica se realmente foi removido
    get_response = client.get(
        f"/api/v1/appointments/{appointment_id}?clinic_id={CLINIC_ID}"
    )
    assert get_response.status_code == 404

def test_create_appointment_invalid_animal():
    """Testa a criação de agendamento com animal inválido"""
    invalid_data = {
        "animal_id": str(uuid.uuid4()),  # UUID aleatório inválido
        "date": date.today().isoformat(),
        "start_time": "14:30:00",
        "end_time": "15:00:00",
        "description": "Teste com animal inválido",
        "status": "scheduled"
    }
    response = client.post(
        f"/api/v1/appointments?clinic_id={CLINIC_ID}",
        json=invalid_data
    )
    assert response.status_code == 404
    assert "Animal não encontrado" in response.json()["detail"]

def test_create_appointment_conflict(appointment_data):
    """Testa a criação de agendamento com conflito de horário"""
    # Primeiro cria um agendamento
    first_response = client.post(
        f"/api/v1/appointments?clinic_id={CLINIC_ID}",
        json=appointment_data
    )
    assert first_response.status_code == 200
    
    # Tenta criar outro agendamento no mesmo horário
    second_response = client.post(
        f"/api/v1/appointments?clinic_id={CLINIC_ID}",
        json=appointment_data
    )
    assert second_response.status_code == 400
    assert "Já existe um agendamento" in second_response.json()["detail"] 