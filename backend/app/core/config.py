import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")

print(f"URL do Supabase: {SUPABASE_URL}")
print(f"Chave do Supabase está presente: {'Sim' if SUPABASE_KEY else 'Não'}")
print(f"Chave de serviço do Supabase está presente: {'Sim' if SUPABASE_SERVICE_KEY else 'Não'}")

# Configurações da API
API_V1_STR = "/api" 