@echo off
echo **************************************************
echo *        TESTES DA API VeTech - INICIO          *
echo **************************************************
echo.

echo Verificando se o servidor esta em execucao...
powershell -Command "& {if ((Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue).Count -gt 0) { exit 0 } else { exit 1 }}"
if %ERRORLEVEL% EQU 0 (
    echo Servidor encontrado na porta 8000. Prosseguindo com os testes.
) else (
    echo AVISO: Servidor nao encontrado na porta 8000.
    echo Iniciando o servidor em modo debug em outra janela...
    start cmd /k "python debug_server.py"
    echo Aguardando 5 segundos para o servidor iniciar...
    timeout /t 5 /nobreak >nul
)

echo.
echo 1. TESTES DE PERFIL DA CLINICA
echo -------------------------------
python test_clinic_profile.py
echo.

echo 2. TESTES DE GESTAO DE ANIMAIS
echo ------------------------------
python test_animals_endpoints.py
echo.

echo 3. TESTES DE PREFERENCIAS ALIMENTARES
echo ------------------------------------
python test_animal_preferences.py
echo.

echo 4. TESTES DE AGENDAMENTOS E CONSULTAS
echo ------------------------------------
python test_appointments_consultations.py
echo.

echo **************************************************
echo *        TESTES DA API VeTech - FIM             *
echo **************************************************
echo.
echo Lembre-se de configurar os arquivos de teste com
echo credenciais e IDs validos conforme indicado em
echo TESTES_README.md antes de executar os testes.
echo.
pause 