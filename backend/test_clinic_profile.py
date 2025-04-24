import requests
import json
import uuid
from datetime import datetime

# URL base da API (ajuste conforme sua configuração)
API_URL = "http://127.0.0.1:8000/api/v1"

# Dados de teste para login
# Substitua por credenciais de uma clínica existente no seu banco
LOGIN_EMAIL = "andrelaudares@hotmail.com"  # Substitua por email válido
LOGIN_PASSWORD = "123456"  # Substitua por senha válida

def test_login():
    """Testa o login da clínica e retorna o token para os outros testes"""
    
    # Dados para login
    login_data = {
        "email": LOGIN_EMAIL,
        "password": LOGIN_PASSWORD
    }
    
    # Fazendo a requisição POST para login
    response = requests.post(
        f"{API_URL}/auth/login",
        json=login_data
    )
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        print("✅ Login realizado com sucesso!")
        data = response.json()
        
        # Mostrar dados básicos do usuário (sem exibir o token completo)
        print(f"Nome: {data.get('name')}")
        print(f"Email: {data.get('email')}")
        
        # Retornar o token de acesso para os próximos testes
        token = data.get("access_token", "")
        return token
    else:
        print(f"❌ Erro ao fazer login: {response.status_code}")
        print(response.text)
        return None

def test_get_profile(token):
    """Testa a obtenção do perfil da clínica"""
    
    if not token:
        print("❌ Token não fornecido para o teste")
        return None
    
    # Fazendo a requisição GET para obter o perfil
    response = requests.get(
        f"{API_URL}/clinic/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        print("✅ Perfil obtido com sucesso!")
        profile = response.json()
        print(json.dumps(profile, indent=2))
        return profile
    else:
        print(f"❌ Erro ao obter perfil: {response.status_code}")
        print(response.text)
        return None

def test_update_profile(token):
    """Testa a atualização do perfil da clínica"""
    
    if not token:
        print("❌ Token não fornecido para o teste")
        return None
    
    # Dados para atualização
    update_data = {
        "name": f"Clínica Teste Atualizada {datetime.now().strftime('%Y%m%d%H%M%S')}",
        "phone": f"11{datetime.now().strftime('%M%S%f')[:6]}"
    }
    
    # Fazendo a requisição PUT para atualizar o perfil
    response = requests.put(
        f"{API_URL}/clinic/profile",
        headers={"Authorization": f"Bearer {token}"},
        json=update_data
    )
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        print("✅ Perfil atualizado com sucesso!")
        profile = response.json()
        print(json.dumps(profile, indent=2))
        return profile
    else:
        print(f"❌ Erro ao atualizar perfil: {response.status_code}")
        print(response.text)
        return None

def test_logout(token):
    """Testa o logout da clínica"""
    
    if not token:
        print("❌ Token não fornecido para o teste")
        return False
    
    # Fazendo a requisição POST para logout
    response = requests.post(
        f"{API_URL}/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        print("✅ Logout realizado com sucesso!")
        print(response.json().get("message", ""))
        return True
    else:
        print(f"❌ Erro ao fazer logout: {response.status_code}")
        print(response.text)
        return False

def run_tests():
    """Executa os testes em sequência"""
    
    print("\n🚀 Iniciando testes de perfil da clínica...\n")
    
    # Testando login
    print("\n🔑 Testando login...")
    token = test_login()
    
    if token:
        # Testando obtenção do perfil
        print("\n📋 Testando obtenção do perfil...")
        profile = test_get_profile(token)
        
        # Testando atualização do perfil
        print("\n✏️ Testando atualização do perfil...")
        updated_profile = test_update_profile(token)
        
        # Testando logout
        print("\n🚪 Testando logout...")
        test_logout(token)
    
    print("\n🏁 Testes concluídos!")

if __name__ == "__main__":
    run_tests() 