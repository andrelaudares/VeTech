import requests
import json
import uuid
from datetime import datetime

# URL base da API
API_URL = "http://127.0.0.1:8000/api/v1"

# Substitua pelo ID de uma clínica existente no seu banco
CLINIC_ID = "dba93fba-3bfa-4254-8dd9-efcdc9608e0f"  # Ex: "dba93fba-3bfa-4254-8dd9-efcdc9608e0f"
# Substitua pelo ID de um animal existente no seu banco
ANIMAL_ID = "9aeeac0e-211d-4b86-ac21-b78675098b81"

def test_create_preferences():
    """Testa a criação de preferências alimentares para um animal"""
    
    # Dados para criar preferências
    preferences_data = {
        "gosta_de": "Ração Premium, Frango, Cenoura",
        "nao_gosta_de": "Ração de baixa qualidade, Vegetais verdes"
    }
    
    # Requisição
    response = requests.post(
        f"{API_URL}/animals/{ANIMAL_ID}/preferences?clinic_id={CLINIC_ID}",
        json=preferences_data
    )
    
    # Verificação
    if response.status_code == 200:
        print("✅ Preferências criadas com sucesso!")
        preferences = response.json()
        print(json.dumps(preferences, indent=2))
        return preferences.get("id")
    elif response.status_code == 400 and "Já existem preferências" in response.text:
        print("⚠️ Já existem preferências para este animal. Prosseguindo com testes de atualização.")
        return "existente"
    else:
        print(f"❌ Erro ao criar preferências: {response.status_code}")
        print(response.text)
        return None

def test_get_preferences():
    """Testa a obtenção de preferências alimentares de um animal"""
    
    # Requisição
    response = requests.get(
        f"{API_URL}/animals/{ANIMAL_ID}/preferences?clinic_id={CLINIC_ID}"
    )
    
    # Verificação
    if response.status_code == 200:
        print("✅ Preferências obtidas com sucesso!")
        preferences = response.json()
        print(json.dumps(preferences, indent=2))
        return preferences
    else:
        print(f"❌ Erro ao obter preferências: {response.status_code}")
        print(response.text)
        return None

def test_update_preferences():
    """Testa a atualização de preferências alimentares de um animal"""
    
    # Dados para atualização
    update_data = {
        "gosta_de": f"Ração Premium, Frango, Cenoura, Petiscos (atualizado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
        "nao_gosta_de": "Ração de baixa qualidade, Brócolis, Couve-flor"
    }
    
    # Requisição
    response = requests.put(
        f"{API_URL}/animals/{ANIMAL_ID}/preferences?clinic_id={CLINIC_ID}",
        json=update_data
    )
    
    # Verificação
    if response.status_code == 200:
        print("✅ Preferências atualizadas com sucesso!")
        preferences = response.json()
        print(json.dumps(preferences, indent=2))
        return preferences
    else:
        print(f"❌ Erro ao atualizar preferências: {response.status_code}")
        print(response.text)
        return None

def run_tests():
    """Executa os testes em sequência"""
    
    print("\n🚀 INICIANDO TESTES DE PREFERÊNCIAS ALIMENTARES\n")
    print("⚠️ ATENÇÃO: Atualize as variáveis CLINIC_ID e ANIMAL_ID no início do script!")
    
    # Criar preferências (ou verificar se já existem)
    print("\n➕ Criando preferências alimentares...")
    result = test_create_preferences()
    
    if result:
        # Obter preferências
        print("\n🔍 Obtendo preferências alimentares...")
        test_get_preferences()
        
        # Atualizar preferências
        print("\n✏️ Atualizando preferências alimentares...")
        test_update_preferences()
        
        # Verificar atualização
        print("\n🔍 Verificando atualização das preferências...")
        test_get_preferences()
    
    print("\n🏁 TESTES CONCLUÍDOS!")

if __name__ == "__main__":
    run_tests() 