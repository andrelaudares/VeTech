import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do Supabase
SUPABASE_URL = "https://ltaawmkfczzqjikdojxe.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")

print(f"URL do Supabase: {SUPABASE_URL}")
print(f"Chave do Supabase está presente: {'Sim' if SUPABASE_KEY else 'Não'}")
print(f"Chave de serviço do Supabase está presente: {'Sim' if SUPABASE_SERVICE_KEY else 'Não'}")

# Configurações da API
API_V1_STR = "/api/v1"

# Configurações da OpenAI (não imprimir chaves)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Configurações do Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")