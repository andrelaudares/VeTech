import httpx
import asyncio
import json

async def test_direct():
    # Dados
    clinic_id = "dba93fba-3bfa-4254-8dd9-efcdc9608e0f"
    animal_id = "9aeeac0e-211d-4b86-ac21-b78675098b81"
    appointment_data = {
        "animal_id": animal_id,
        "date": "2023-05-15",
        "start_time": "14:30:00",
        "end_time": "15:00:00",
        "description": "Consulta de teste",
        "status": "scheduled"
    }
    
    # Testar a API diretamente
    async with httpx.AsyncClient() as client:
        # 1. Testar a rota base
        test_response = await client.get("http://localhost:8000")
        print(f"Resposta: {test_response.text}")
        
        # 2. Testar a rota de teste
        test_route = await client.get("http://localhost:8000/api/v1/appointments/test")
        print(f"\nRota de teste: {test_route.status_code}")
        print(f"Resposta: {test_route.text}")
        
        # 3. Testar criar um agendamento
        create_url = f"http://localhost:8000/api/v1/appointments?clinic_id={clinic_id}"
        print(f"\nCriando agendamento em: {create_url}")
        print(f"Dados: {json.dumps(appointment_data)}")
        
        try:
            # Primeiro, vamos verificar se o animal existe diretamente no Supabase
            supabase_url = "https://ltaawmkfczzqjikdojxe.supabase.co"
            
            # API key completa (substitua pela sua API key real)
            api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx0YWF3bWtmY3p6cWppa2RvanhlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDI0MDk4OTgsImV4cCI6MjAxNzk4NTg5OH0.bzw0QJlXQkOsUCGpWs7ko0tq2lBOYxD7V_Z0-PYz8KE"
            
            headers = {
                "apikey": api_key,
                "Authorization": f"Bearer {api_key}"
            }
            
            # Consulta correta usando clinics_id (não clinic_id)
            animal_check_url = f"{supabase_url}/rest/v1/animals?select=*&id=eq.{animal_id}&clinics_id=eq.{clinic_id}"
            print(f"\nVerificando animal em: {animal_check_url}")
            
            animal_response = await client.get(
                animal_check_url,
                headers=headers
            )
            
            print(f"Status da verificação: {animal_response.status_code}")
            
            if animal_response.status_code != 200 or not animal_response.text or animal_response.text == "[]":
                print(f"Animal não encontrado. Status: {animal_response.status_code}")
                print(f"Resposta: {animal_response.text}")
            else:
                print(f"Animal encontrado: {animal_response.text}")
                print("Continuando com a criação do agendamento")
                
            # Agora tentamos criar o agendamento
            create_response = await client.post(
                create_url,
                json=appointment_data,
                headers={"Content-Type": "application/json"}
            )
            print(f"Status: {create_response.status_code}")
            print(f"Resposta: {create_response.text}")
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    asyncio.run(test_direct()) 