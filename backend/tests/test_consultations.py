import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import uuid
import sys
import os

# Adiciona o diretório raiz ao path do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa o app com caminho absoluto
from main import app
from app.db.supabase import supabase_admin

client = TestClient(app)

# Dados de exemplo para os testes
CLINIC_ID = "dba93fba-3bfa-4254-8dd9-efcdc9608e0f"  # ID real da clínica
ANIMAL_ID = "9aeeac0e-211d-4b86-ac21-b78675098b81"  # ID real do animal

@pytest.fixture
def consultation_data():
    """Fixture que fornece dados básicos para criar uma consulta"""
    return {
        "animal_id": ANIMAL_ID,
        "description": "Consulta de teste via pytest",
        "date": datetime.utcnow().isoformat()
    }

def test_create_consultation(consultation_data):
    """Testa a criação de uma consulta"""
    response = client.post(
        f"/api/v1/consultations?clinic_id={CLINIC_ID}",
        json=consultation_data
    )
    print(f"Resposta da criação: {response.status_code}")
    print(f"Corpo da resposta: {response.json()}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["animal_id"] == ANIMAL_ID
    assert data["clinic_id"] == CLINIC_ID
    assert "description" in data
    assert data["description"] == consultation_data["description"]
    
    # return data["id"]  # Comentado ou removido - Testes não devem retornar valores

def test_get_consultations():
    """Testa a listagem de consultas"""
    response = client.get(f"/api/v1/consultations?clinic_id={CLINIC_ID}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    # Exibe o número de consultas encontradas
    print(f"Número de consultas encontradas: {len(data)}")
    if len(data) > 0:
        print(f"Primeira consulta: {data[0]}")

def test_get_consultations_by_animal():
    """Testa a listagem de consultas filtradas por animal"""
    response = client.get(
        f"/api/v1/consultations?clinic_id={CLINIC_ID}&animal_id={ANIMAL_ID}"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    # Verifica se todas as consultas retornadas são do animal especificado
    for consultation in data:
        assert consultation["animal_id"] == ANIMAL_ID

def test_update_consultation(consultation_data):
    """Testa a atualização de uma consulta"""
    # Primeiro cria uma consulta
    create_response = client.post(
        f"/api/v1/consultations?clinic_id={CLINIC_ID}",
        json=consultation_data
    )
    assert create_response.status_code == 200
    consultation_id = create_response.json()["id"]
    
    # Dados para atualização
    update_data = {
        "description": "Consulta atualizada via pytest"
    }
    
    # Atualiza a consulta
    response = client.patch(
        f"/api/v1/consultations/{consultation_id}?clinic_id={CLINIC_ID}",
        json=update_data
    )
    print(f"Resposta da atualização: {response.status_code}")
    print(f"Corpo da resposta: {response.json()}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == consultation_id
    assert data["description"] == update_data["description"]

def test_delete_consultation(consultation_data):
    """Testa a remoção de uma consulta"""
    # Primeiro cria uma consulta
    create_response = client.post(
        f"/api/v1/consultations?clinic_id={CLINIC_ID}",
        json=consultation_data
    )
    assert create_response.status_code == 200
    consultation_id = create_response.json()["id"]
    
    # Remove a consulta
    response = client.delete(
        f"/api/v1/consultations/{consultation_id}?clinic_id={CLINIC_ID}"
    )
    print(f"Resposta da exclusão: {response.status_code}")
    
    assert response.status_code == 204  # No Content
    
    # Verifica se realmente foi removida tentando buscá-la
    get_response = client.get(
        f"/api/v1/consultations?clinic_id={CLINIC_ID}"
    )
    assert get_response.status_code == 200
    consultations = get_response.json()
    
    # Verifica se a consulta não está mais na lista
    ids = [c["id"] for c in consultations]
    assert consultation_id not in ids

def test_create_consultation_invalid_animal():
    """Testa a criação de consulta com animal inválido"""
    invalid_data = {
        "animal_id": str(uuid.uuid4()),  # UUID aleatório inválido
        "description": "Teste com animal inválido",
        "date": datetime.utcnow().isoformat()
    }
    
    response = client.post(
        f"/api/v1/consultations?clinic_id={CLINIC_ID}",
        json=invalid_data
    )
    print(f"Resposta com animal inválido: {response.status_code}")
    print(f"Detalhe do erro: {response.json()}")
    
    assert response.status_code == 404
    assert "Animal não encontrado" in response.json()["detail"] 