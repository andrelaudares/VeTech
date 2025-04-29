import requests
import json
from datetime import date

# URL base da API
BASE_URL = "http://localhost:8000/api/v1"

# Token de autenticação (substitua pelo seu token válido)
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzQ1OTAzMzA3LCJzdWIiOiIyZTk1NmQ3MC0xZjhhLTQ3Y2UtOGZiZi01ZmI4NDQxMGI2ZWUiLCJlbWFpbCI6ImFkbWluQHZldGVjaC5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIn0sInVzZXJfbWV0YWRhdGEiOnt9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6InBhc3N3b3JkIiwidGltZXN0YW1wIjoxNzEzOTM2OTA3fV0sInNlc3Npb25faWQiOiJlMGQ0YzBmZC0wNGRmLTRmMWEtOGFkYy0wOTczOGEwZTY0NTIiLCJpYXQiOjE3MTM5MzY5MDcsImlzcyI6Imh0dHBzOi8vbHRhYXdta2ZjenpxamlrZG9qeGUuc3VwYWJhc2UuY28vYXV0aC92MSJ9.xJKZN41tMNIJOt7HQemXlrpd3-kA0Z3iEDTcFrHgDOY"

# Headers comuns para todas as requisições
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# ID do animal para teste
ANIMAL_ID = "3e2ce4a2-f75b-468c-9353-04ba4996f548"

def test_create_diet():
    print("Testando criação de dieta...")
    
    # Dados da dieta
    diet_data = {
        "tipo": "ração",
        "objetivo": "Emagrecimento",
        "observacoes": "Teste simplificado",
        "data_inicio": date.today().isoformat(),
        "status": "ativa"
    }
    
    # URL completa
    url = f"{BASE_URL}/animals/{ANIMAL_ID}/diets"
    
    print(f"Enviando requisição POST para: {url}")
    print(f"Headers: {json.dumps(HEADERS, indent=2)}")
    print(f"Dados: {json.dumps(diet_data, indent=2)}")
    
    # Fazer a requisição
    try:
        response = requests.post(url, headers=HEADERS, json=diet_data)
        
        # Mostrar resultado
        print(f"\nStatus code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        try:
            print(f"Response body: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response text: {response.text}")
            
    except Exception as e:
        print(f"Erro na requisição: {str(e)}")

if __name__ == "__main__":
    test_create_diet() 