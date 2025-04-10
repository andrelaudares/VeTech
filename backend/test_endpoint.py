import httpx
import json
import asyncio
from uuid import UUID
from datetime import date

async def test_api():
    # Dados para teste
    clinic_id = "dba93fba-3bfa-4254-8dd9-efcdc9608e0f"
    animal_id = "9aeeac0e-211d-4b86-ac21-b78675098b81"
    
    # URL da API
    base_url = "http://localhost:8000/api/v1"
    
    # Testar apenas a rota de teste
    async with httpx.AsyncClient() as client:
        try:
            # Teste para a rota de teste
            test_route = await client.get(f"{base_url}/appointments/test")
            print(f"\nTeste route status: {test_route.status_code}")
            print(f"Teste route response: {test_route.text}")
            
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    asyncio.run(test_api()) 