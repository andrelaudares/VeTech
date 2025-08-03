import asyncio
import httpx
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

async def reset_user_password():
    """Reset a senha de um usuário no Supabase Auth"""
    
    user_id = "c637667c-dfd2-42f2-8b2c-34748356169f"  # ID do usuário teste@teste.com
    new_password = "senha123"
    
    url = f"{SUPABASE_URL}/auth/v1/admin/users/{user_id}"
    
    headers = {
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
        "apikey": SUPABASE_SERVICE_ROLE_KEY
    }
    
    data = {
        "password": new_password
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(url, headers=headers, json=data)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                print("✅ Senha resetada com sucesso!")
                print(f"📧 Email: teste@teste.com")
                print(f"🔑 Nova senha: {new_password}")
            else:
                print(f"❌ Erro ao resetar senha: {response.text}")
                
    except Exception as e:
        print(f"❌ Erro na requisição: {str(e)}")

if __name__ == "__main__":
    asyncio.run(reset_user_password())