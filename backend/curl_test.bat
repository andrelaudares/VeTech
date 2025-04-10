@echo off
echo Testando API de Agendamentos

:: Testar a rota de teste
echo Testando rota /appointments/test
curl -X GET "http://localhost:8000/api/v1/appointments/test"
echo.

:: Testar criar agendamento
echo Testando criacao de agendamento
curl -X POST "http://localhost:8000/api/v1/appointments?clinic_id=dba93fba-3bfa-4254-8dd9-efcdc9608e0f" ^
  -H "Content-Type: application/json" ^
  -d "{\"animal_id\": \"9aeeac0e-211d-4b86-ac21-b78675098b81\", \"date\": \"2023-05-15\", \"start_time\": \"14:30:00\", \"end_time\": \"15:00:00\", \"description\": \"Consulta de teste\", \"status\": \"scheduled\"}"
echo.

pause 