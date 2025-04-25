import requests
import json
import uuid

# URL base da API
API_URL = "http://127.0.0.1:8000/api/v1"

def test_register():
    # Gerar email único para evitar conflitos
    unique_id = uuid.uuid4().hex[:8]
    email = f"teste_{unique_id}@exemplo.com"
    
    # Dados para registro
    data = {
        "name": "Clínica de Teste",
        "email": email,
        "password": "senha123",
        "phone": "11999999999", 
        "subscription_tier": "basic"
    }
    
    print(f"Tentando registrar com email: {email}")
    
    # Fazer a requisição
    response = requests.post(
        f"{API_URL}/auth/register",
        json=data
    )
    
    # Mostrar status da resposta
    print(f"Status: {response.status_code}")
    
    # Se houve sucesso, mostrar detalhes
    if response.status_code == 201:
        print("✅ Registro bem-sucedido!")
        try:
            resposta = response.json()
            print("\nDados retornados:")
            print(json.dumps(resposta, indent=2))
        except json.JSONDecodeError:
            print("Resposta não é JSON válido:")
            print(response.text)
    else:
        # Mostrar erro
        print("❌ Erro no registro!")
        print(f"Resposta: {response.text}")

if __name__ == "__main__":
    print("Testando registro na API VeTech...")
    test_register() 