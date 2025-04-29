import requests
import json

# URL do endpoint de login
LOGIN_URL = "http://localhost:8000/api/v1/auth/login"

# Credenciais (substitua pelas suas credenciais reais)
credentials = {
    "email": "admin@vetech.com",
    "password": "password123"
}

def test_login():
    print("Testando login...")
    
    # Fazer requisição de login
    response = requests.post(
        LOGIN_URL,
        json=credentials,
        headers={"Content-Type": "application/json"}
    )
    
    # Mostrar resultado
    print(f"Status code: {response.status_code}")
    
    try:
        response_data = response.json()
        print(f"Response: {json.dumps(response_data, indent=2)}")
        
        # Extrair o token caso o login tenha sido bem-sucedido
        if "access_token" in response_data:
            token = response_data["access_token"]
            print("\n=== TOKEN PARA USAR NAS REQUISIÇÕES ===")
            print(token)
            print("=======================================\n")
            
            # Mostrar como usar o token em requisições futuras
            print("Para usar o token, adicione o seguinte header nas requisições:")
            print(f'Authorization: Bearer {token}')
    except:
        print(f"Response text: {response.text}")

if __name__ == "__main__":
    test_login() 