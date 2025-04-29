import requests
import json
from datetime import date, datetime

# Configurações
BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzQ1OTAzMzA3LCJzdWIiOiIyZTk1NmQ3MC0xZjhhLTQ3Y2UtOGZiZi01ZmI4NDQxMGI2ZWUiLCJlbWFpbCI6ImFkbWluQHZldGVjaC5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIn0sInVzZXJfbWV0YWRhdGEiOnt9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6InBhc3N3b3JkIiwidGltZXN0YW1wIjoxNzEzOTM2OTA3fV0sInNlc3Npb25faWQiOiJlMGQ0YzBmZC0wNGRmLTRmMWEtOGFkYy0wOTczOGEwZTY0NTIiLCJpYXQiOjE3MTM5MzY5MDcsImlzcyI6Imh0dHBzOi8vbHRhYXdta2ZjenpxamlrZG9qeGUuc3VwYWJhc2UuY28vYXV0aC92MSJ9.xJKZN41tMNIJOt7HQemXlrpd3-kA0Z3iEDTcFrHgDOY",
    "Content-Type": "application/json"
}

# Testes
def test_create_diet():
    print("Testando criação de dieta...")
    animal_id = "3e2ce4a2-f75b-468c-9353-04ba4996f548"
    data = {
        "tipo": "ração",
        "objetivo": "Emagrecimento",
        "observacoes": "Teste via script Python",
        "data_inicio": date.today().isoformat(),
        "status": "ativa"
    }
    
    response = requests.post(
        f"{BASE_URL}/animals/{animal_id}/diets",
        headers=HEADERS,
        json=data
    )
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200 or response.status_code == 201:
        print("Dieta criada com sucesso!")
        print(json.dumps(response.json(), indent=2))
        return response.json().get("id")
    else:
        print(f"Erro: {response.text}")
        return None

def test_list_diets(animal_id):
    print("\nTestando listagem de dietas...")
    response = requests.get(
        f"{BASE_URL}/animals/{animal_id}/diets",
        headers=HEADERS
    )
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        diets = response.json()
        print(f"Encontradas {len(diets)} dietas")
        if diets:
            print(json.dumps(diets[0], indent=2))
        return diets
    else:
        print(f"Erro: {response.text}")
        return []

def test_get_diet(diet_id):
    print(f"\nTestando obtenção da dieta {diet_id}...")
    response = requests.get(
        f"{BASE_URL}/diets/{diet_id}",
        headers=HEADERS
    )
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("Dieta obtida com sucesso!")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    else:
        print(f"Erro: {response.text}")
        return None

def test_update_diet(diet_id):
    print(f"\nTestando atualização da dieta {diet_id}...")
    data = {
        "objetivo": "Nutrição Geral",
        "observacoes": "Atualizado via script Python"
    }
    
    response = requests.put(
        f"{BASE_URL}/diets/{diet_id}",
        headers=HEADERS,
        json=data
    )
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("Dieta atualizada com sucesso!")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    else:
        print(f"Erro: {response.text}")
        return None

# Executar testes
if __name__ == "__main__":
    # Criar uma dieta
    created_diet_id = test_create_diet()
    
    if created_diet_id:
        # Listar dietas
        animal_id = "3e2ce4a2-f75b-468c-9353-04ba4996f548"
        test_list_diets(animal_id)
        
        # Obter dieta específica
        test_get_diet(created_diet_id)
        
        # Atualizar dieta
        test_update_diet(created_diet_id) 