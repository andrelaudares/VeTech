import requests

try:
    # Usar localhost
    response = requests.get("http://localhost:8000")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Verificar documentação
    swagger = requests.get("http://localhost:8000/docs")
    print(f"\nSwagger Status: {swagger.status_code}")
    print(f"Swagger disponível: {'Sim' if swagger.status_code == 200 else 'Não'}")
    
    # Verificar rota de teste
    test_route = requests.get("http://localhost:8000/api/v1/appointments/test")
    print(f"\nTeste appointments Status: {test_route.status_code}")
    print(f"Teste appointments Response: {test_route.text}")
    
except Exception as e:
    print(f"Erro: {e}") 