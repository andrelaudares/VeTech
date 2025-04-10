import requests
import json

def test_basic_endpoints():
    base_url = "http://localhost:8000/api/v1"
    
    # 1. Testar a rota de teste
    test_response = requests.get(f"{base_url}/appointments/test")
    print(f"Test route: {test_response.status_code}")
    print(test_response.json())
    
    # 2. Verificar apenas a primeira consulta direta ao animal
    clinic_id = "dba93fba-3bfa-4254-8dd9-efcdc9608e0f"
    animal_id = "9aeeac0e-211d-4b86-ac21-b78675098b81"
    
    # URL que está sendo usada no código
    supabase_url = "https://ltaawmkfczzqjikdojxe.supabase.co"
    animals_endpoint = f"{supabase_url}/rest/v1/animals"
    
    print("\nTentando consulta direta (código do error):")
    print(f"URL: {animals_endpoint}?id=eq.{animal_id}&clinics_id=eq.{clinic_id}&select=*")
    
    # Consulta real
    print("\nTentando consulta correta (clinic_id):")
    print(f"URL: {animals_endpoint}?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=*")
    
    # Consultar supabase diretamente
    headers = {
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx0YWF3bWtmY3p6cWppa2Rvanhl",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx0YWF3bWtmY3p6cWppa2Rvanhl"
    }
    
    # Tentar com clinics_id (para verificar o erro)
    try:
        wrong_response = requests.get(
            f"{animals_endpoint}?id=eq.{animal_id}&clinics_id=eq.{clinic_id}&select=*",
            headers=headers
        )
        print(f"\nResposta com clinics_id: {wrong_response.status_code}")
        print(wrong_response.text)
    except Exception as e:
        print(f"Erro: {e}")
    
    # Tentar com clinic_id (correto)
    try:
        correct_response = requests.get(
            f"{animals_endpoint}?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=*",
            headers=headers
        )
        print(f"\nResposta com clinic_id: {correct_response.status_code}")
        print(correct_response.text)
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    test_basic_endpoints() 