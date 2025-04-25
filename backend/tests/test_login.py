import requests
import json
import sys

# URL base da API
API_URL = "http://127.0.0.1:8000/api/v1"

# Credenciais para teste - utilizar um usuário que já exista no banco
LOGIN_EMAIL = "teste@teste.com"
LOGIN_PASSWORD = "123456"

# Você também pode informar as credenciais via linha de comando
if len(sys.argv) >= 3:
    LOGIN_EMAIL = sys.argv[1]
    LOGIN_PASSWORD = sys.argv[2]
    print(f"Usando credenciais da linha de comando: {LOGIN_EMAIL}")

def test_login():
    # Dados para o login
    data = {
        "email": LOGIN_EMAIL,
        "password": LOGIN_PASSWORD
    }
    
    # Fazer a requisição
    response = requests.post(
        f"{API_URL}/auth/login",
        json=data
    )
    
    # Mostrar status da resposta
    print(f"Status: {response.status_code}")
    
    # Se houve sucesso, mostrar detalhes
    if response.status_code == 200:
        # Obter JSON da resposta
        resposta = response.json()
        
        # Mostrar todos os campos
        print("\nTodos os campos da resposta:")
        print(json.dumps(resposta, indent=2))
        
        # Verificar campos específicos
        print("\nVerificação detalhada:")
        if "access_token" in resposta:
            print(f"✅ access_token encontrado: {resposta['access_token'][:10]}...")
        else:
            print("❌ access_token NÃO encontrado!")
            
        if "token_type" in resposta:
            print(f"✅ token_type: {resposta['token_type']}")
        else:
            print("❌ token_type NÃO encontrado!")
            
        if "clinic" in resposta:
            clinic = resposta["clinic"]
            print("✅ Dados da clínica encontrados:")
            print(f"   - id: {clinic.get('id', 'NÃO ENCONTRADO')}")
            print(f"   - name: {clinic.get('name', 'NÃO ENCONTRADO')}")
            print(f"   - email: {clinic.get('email', 'NÃO ENCONTRADO')}")
        else:
            print("❌ Dados da clínica NÃO encontrados!")
    else:
        # Mostrar erro
        print(f"Erro na resposta: {response.text}")

if __name__ == "__main__":
    print("Testando login na API VeTech...")
    test_login() 