import requests
import json

# URL do endpoint de registro
REGISTER_URL = "http://localhost:8000/api/v1/auth/register"

# Dados do usuário para registro
user_data = {
    "name": "Teste VeTech",
    "email": "teste@vetech.com",
    "password": "senha123",
    "phone": "1234567890",
    "subscription_tier": "basic"
}

def test_register():
    print("Testando registro de usuário...")
    
    # Fazer requisição de registro
    response = requests.post(
        REGISTER_URL,
        json=user_data,
        headers={"Content-Type": "application/json"}
    )
    
    # Mostrar resultado
    print(f"Status code: {response.status_code}")
    
    try:
        response_data = response.json()
        print(f"Response: {json.dumps(response_data, indent=2)}")
    except:
        print(f"Response text: {response.text}")
    
    # Se o registro for bem-sucedido, tentar fazer login
    if response.status_code == 201:
        print("\nTentando fazer login com o usuário recém-criado...")
        
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        login_response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status code do login: {login_response.status_code}")
        
        try:
            login_response_data = login_response.json()
            print(f"Response do login: {json.dumps(login_response_data, indent=2)}")
            
            if "access_token" in login_response_data:
                token = login_response_data["access_token"]
                print("\n=== TOKEN PARA USAR NAS REQUISIÇÕES ===")
                print(token)
                print("=======================================\n")
        except:
            print(f"Response text do login: {login_response.text}")

if __name__ == "__main__":
    test_register() 