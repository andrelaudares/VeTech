import requests
import json
from datetime import date

# Configurações
BASE_URL = "http://localhost:8000/api/v1"
TOKEN = "eyJhbGciOiJIUzI1NiIsImtpZCI6ImhOWUxyakhCWXhoMFhiYUIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2x0YWF3bWtmY3p6cWppa2RvanhlLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI0YThjYzJhYy1hNzc4LTQ2MjctOGRmYy0yMzU5MDJhMGQwNDEiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzQ1OTA1OTk5LCJpYXQiOjE3NDU5MDIzOTksImVtYWlsIjoidGVzdGVAdmV0ZWNoLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJ0ZXN0ZUB2ZXRlY2guY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJUZXN0ZSBWZVRlY2giLCJwaG9uZSI6IjEyMzQ1Njc4OTAiLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInN1YiI6IjRhOGNjMmFjLWE3NzgtNDYyNy04ZGZjLTIzNTkwMmEwZDA0MSJ9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6InBhc3N3b3JkIiwidGltZXN0YW1wIjoxNzQ1OTAyMzk5fV0sInNlc3Npb25faWQiOiIxNzM4NWUyYy1iMjJiLTQ5ODItOTAwMy1mZjIxMzRhOTAzZTUiLCJpc19hbm9ueW1vdXMiOmZhbHNlfQ.udYoF_ORlYvyp8JaL-xp25muBwo7awHA6DOSVMHXvkY"
CLINIC_ID = "4a8cc2ac-a778-4627-8dfc-235902a0d041"  # ID da clínica (mesmo ID do usuário logado)
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Primeiro, vamos criar um animal para usar nos testes
def create_animal():
    print("Criando um animal para teste...")
    
    animal_data = {
        "name": "Animal de Teste",
        "species": "cachorro",
        "breed": "SRD",
        "birth_date": "2022-01-01",
        "owner_name": "Dono de Teste",
        "owner_email": "dono@teste.com",
        "owner_phone": "1234567890"
    }
    
    response = requests.post(
        f"{BASE_URL}/animals?clinic_id={CLINIC_ID}",
        headers=HEADERS,
        json=animal_data
    )
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200 or response.status_code == 201:
        animal = response.json()
        print(f"Animal criado com ID: {animal.get('id')}")
        return animal.get('id')
    else:
        try:
            print(f"Erro: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Erro: {response.text}")
        return None

# Testa a criação de uma dieta
def create_diet(animal_id):
    print(f"\nCriando dieta para o animal ID: {animal_id}")
    
    diet_data = {
        "tipo": "ração",
        "objetivo": "Emagrecimento",
        "observacoes": "Dieta de teste",
        "data_inicio": date.today().isoformat(),
        "status": "ativa"
    }
    
    response = requests.post(
        f"{BASE_URL}/animals/{animal_id}/diets",
        headers=HEADERS,
        json=diet_data
    )
    
    print(f"Status code: {response.status_code}")
    
    try:
        result = response.json()
        print(f"Resposta: {json.dumps(result, indent=2)}")
        return result.get('id') if 'id' in result else None
    except:
        print(f"Erro: {response.text}")
        return None

# Testa a listagem de dietas
def list_diets(animal_id):
    print(f"\nListando dietas do animal ID: {animal_id}")
    
    response = requests.get(
        f"{BASE_URL}/animals/{animal_id}/diets",
        headers=HEADERS
    )
    
    print(f"Status code: {response.status_code}")
    
    try:
        diets = response.json()
        print(f"Encontradas {len(diets)} dietas")
        if diets:
            print(f"Primeira dieta: {json.dumps(diets[0], indent=2)}")
        return diets
    except:
        print(f"Erro: {response.text}")
        return []

# Testa obtenção de uma dieta específica
def get_diet(diet_id):
    print(f"\nObtendo detalhes da dieta ID: {diet_id}")
    
    response = requests.get(
        f"{BASE_URL}/diets/{diet_id}",
        headers=HEADERS
    )
    
    print(f"Status code: {response.status_code}")
    
    try:
        diet = response.json()
        print(f"Dieta: {json.dumps(diet, indent=2)}")
        return diet
    except:
        print(f"Erro: {response.text}")
        return None

# Testa atualização de uma dieta
def update_diet(diet_id):
    print(f"\nAtualizando dieta ID: {diet_id}")
    
    update_data = {
        "objetivo": "Manutenção",
        "observacoes": "Dieta atualizada via teste"
    }
    
    response = requests.put(
        f"{BASE_URL}/diets/{diet_id}",
        headers=HEADERS,
        json=update_data
    )
    
    print(f"Status code: {response.status_code}")
    
    try:
        updated_diet = response.json()
        print(f"Dieta atualizada: {json.dumps(updated_diet, indent=2)}")
        return updated_diet
    except:
        print(f"Erro: {response.text}")
        return None

# Testa a remoção de uma dieta
def delete_diet(diet_id):
    print(f"\nRemovendo dieta ID: {diet_id}")
    
    response = requests.delete(
        f"{BASE_URL}/diets/{diet_id}",
        headers=HEADERS
    )
    
    print(f"Status code: {response.status_code}")
    
    try:
        result = response.json()
        print(f"Resultado: {json.dumps(result, indent=2)}")
        return True if response.status_code == 200 else False
    except:
        print(f"Erro: {response.text}")
        return False

# Executa os testes
if __name__ == "__main__":
    # Criar animal
    animal_id = create_animal()
    
    if animal_id:
        # Criar dieta
        diet_id = create_diet(animal_id)
        
        if diet_id:
            # Listar dietas
            list_diets(animal_id)
            
            # Obter dieta específica
            get_diet(diet_id)
            
            # Atualizar dieta
            update_diet(diet_id)
            
            # Remover dieta
            delete_diet(diet_id)
    else:
        print("Não foi possível criar o animal para teste.") 