import requests
import json
import uuid
from datetime import datetime

# URL base da API (ajuste conforme sua configuração)
API_URL = "http://127.0.0.1:8000/api/v1"

# Dados de teste
# Substitua pelo ID de uma clínica existente no seu banco
CLINIC_ID = "dba93fba-3bfa-4254-8dd9-efcdc9608e0f" 

def test_create_animal():
    """Testa a criação de um animal"""
    
    # Dados para criar um animal
    animal_data = {
        "name": f"Animal Teste {datetime.now().strftime('%Y%m%d%H%M%S')}",
        "species": "Cachorro",
        "breed": "Labrador",
        "age": 5,
        "weight": 25.5,
        "medical_history": "Animal saudável com vacinas em dia."
    }
    
    # Fazendo a requisição POST para criar o animal
    response = requests.post(
        f"{API_URL}/animals?clinic_id={CLINIC_ID}",
        json=animal_data
    )
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        print("✅ Animal criado com sucesso!")
        print(json.dumps(response.json(), indent=2))
        
        # Salvando o ID do animal para os próximos testes
        animal_id = response.json().get("id")
        return animal_id
    else:
        print(f"❌ Erro ao criar animal: {response.status_code}")
        print(response.text)
        return None

def test_list_animals():
    """Testa a listagem de animais"""
    
    # Fazendo a requisição GET para listar os animais
    response = requests.get(
        f"{API_URL}/animals?clinic_id={CLINIC_ID}"
    )
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        animals = response.json()
        print(f"✅ {len(animals)} animais encontrados!")
        
        # Exibe resumo dos primeiros 3 animais (se houver)
        for i, animal in enumerate(animals[:3]):
            print(f"Animal {i+1}: {animal.get('name')} ({animal.get('species')})")
        
        return animals
    else:
        print(f"❌ Erro ao listar animais: {response.status_code}")
        print(response.text)
        return None

def test_get_animal(animal_id):
    """Testa a busca de um animal específico"""
    
    if not animal_id:
        print("❌ ID de animal não fornecido para o teste")
        return None
    
    # Fazendo a requisição GET para buscar um animal específico
    response = requests.get(
        f"{API_URL}/animals/{animal_id}?clinic_id={CLINIC_ID}"
    )
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        print("✅ Animal encontrado com sucesso!")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    else:
        print(f"❌ Erro ao buscar animal: {response.status_code}")
        print(response.text)
        return None

def test_update_animal(animal_id):
    """Testa a atualização de um animal"""
    
    if not animal_id:
        print("❌ ID de animal não fornecido para o teste")
        return None
    
    # Dados para atualizar o animal
    update_data = {
        "name": f"Animal Atualizado {datetime.now().strftime('%Y%m%d%H%M%S')}",
        "weight": 26.2,
        "medical_history": "Histórico médico atualizado no teste."
    }
    
    # Fazendo a requisição PATCH para atualizar o animal
    response = requests.patch(
        f"{API_URL}/animals/{animal_id}?clinic_id={CLINIC_ID}",
        json=update_data
    )
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        print("✅ Animal atualizado com sucesso!")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    else:
        print(f"❌ Erro ao atualizar animal: {response.status_code}")
        print(response.text)
        return None

def test_delete_animal(animal_id):
    """Testa a remoção de um animal"""
    
    if not animal_id:
        print("❌ ID de animal não fornecido para o teste")
        return False
    
    # Fazendo a requisição DELETE para remover o animal
    response = requests.delete(
        f"{API_URL}/animals/{animal_id}?clinic_id={CLINIC_ID}"
    )
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 204:
        print("✅ Animal removido com sucesso!")
        return True
    else:
        print(f"❌ Erro ao remover animal: {response.status_code}")
        print(response.text)
        return False

def run_tests():
    """Executa os testes em sequência"""
    
    print("\n🚀 Iniciando testes dos endpoints de animais...\n")
    
    # Testando a listagem inicial (antes de criar um novo)
    print("\n📋 Testando listagem inicial de animais...")
    existing_animals = test_list_animals()
    
    # Testando a criação de um animal
    print("\n➕ Testando criação de animal...")
    animal_id = test_create_animal()
    
    if animal_id:
        # Testando a listagem após criar um novo
        print("\n📋 Testando listagem após criação...")
        test_list_animals()
        
        # Testando a busca de um animal específico
        print(f"\n🔍 Testando busca do animal criado (ID: {animal_id})...")
        test_get_animal(animal_id)
        
        # Testando a atualização de um animal
        print(f"\n✏️ Testando atualização do animal (ID: {animal_id})...")
        test_update_animal(animal_id)
        
        # Testando a remoção de um animal
        print(f"\n❌ Testando remoção do animal (ID: {animal_id})...")
        test_delete_animal(animal_id)
        
        # Verificando se foi removido
        print(f"\n🔍 Verificando se animal foi removido (ID: {animal_id})...")
        result = test_get_animal(animal_id)
        if result is None:
            print("✅ Animal removido com sucesso!")
    
    print("\n🏁 Testes concluídos!")

if __name__ == "__main__":
    run_tests() 