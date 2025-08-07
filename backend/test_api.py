"""
Script de teste para verificar se a API está funcionando corretamente
"""
import asyncio
import sys
import os

# Adicionar o diretório do backend ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.supabase import supabase_admin

async def test_database_connection():
    """Testa a conexão com o banco de dados"""
    print("=== Teste de Conexão com o Banco de Dados ===")
    
    try:
        # Teste 1: Verificar se consegue acessar a tabela appointments
        print("1. Testando acesso à tabela appointments...")
        result = await supabase_admin._request("GET", "/rest/v1/appointments?limit=1")
        if "error" in result:
            print(f"❌ Erro ao acessar appointments: {result['error']}")
        else:
            print("✅ Acesso à tabela appointments OK")
            
        # Teste 2: Verificar se consegue acessar a tabela animals
        print("2. Testando acesso à tabela animals...")
        result = await supabase_admin._request("GET", "/rest/v1/animals?limit=1")
        if "error" in result:
            print(f"❌ Erro ao acessar animals: {result['error']}")
        else:
            print("✅ Acesso à tabela animals OK")
            
        # Teste 3: Verificar estrutura da tabela appointments
        print("3. Verificando estrutura da tabela appointments...")
        result = await supabase_admin._request("GET", "/rest/v1/appointments?select=id,clinic_id,animal_id,date,start_time,end_time,description,status,solicitado_por_cliente,status_solicitacao,observacoes_cliente&limit=1")
        if "error" in result:
            print(f"❌ Erro ao verificar estrutura: {result['error']}")
        else:
            print("✅ Estrutura da tabela appointments OK")
            
        # Teste 4: Verificar se há dados de teste
        print("4. Verificando dados de teste...")
        result = await supabase_admin._request("GET", "/rest/v1/appointments?solicitado_por_cliente=eq.true&limit=5")
        if "error" in result:
            print(f"❌ Erro ao buscar dados de teste: {result['error']}")
        else:
            data = result.get("data", [])
            print(f"✅ Encontrados {len(data)} agendamentos solicitados por clientes")
            
        print("\n=== Teste Concluído ===")
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    asyncio.run(test_database_connection())