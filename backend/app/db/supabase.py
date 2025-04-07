import httpx
from ..core.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_KEY

class SupabaseClient:
    def __init__(self, use_service_key=False):
        self.url = SUPABASE_URL
        self.key = SUPABASE_SERVICE_KEY if use_service_key else SUPABASE_KEY
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"  # Isso garante que o Supabase retorne os dados inseridos
        }
        print(f"Inicializando SupabaseClient com URL: {self.url}")

    async def _request(self, method, endpoint, json=None, params=None):
        url = f"{self.url}{endpoint}"
        print(f"Fazendo requisição {method} para {url}")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method,
                    url,
                    headers=self.headers,
                    json=json,
                    params=params
                )
                response.raise_for_status()  # Isso vai levantar uma exceção para códigos de erro HTTP
                return response.json()
            except httpx.HTTPError as e:
                print(f"Erro na requisição HTTP: {str(e)}")
                if hasattr(e, 'response') and e.response is not None:
                    print(f"Resposta de erro: {e.response.text}")
                raise
            except Exception as e:
                print(f"Erro inesperado: {str(e)}")
                raise

    async def register_user(self, email, password, user_data=None):
        """
        Registra um novo usuário usando a API de autenticação do Supabase
        
        Args:
            email (str): Email do usuário
            password (str): Senha do usuário
            user_data (dict, opcional): Dados adicionais do usuário
            
        Returns:
            dict: Dados do usuário registrado
        """
        try:
            # Endpoint para registro de usuário
            url = f"{self.url}/auth/v1/signup"
            
            # Dados para o registro
            data = {
                "email": email,
                "password": password,
                "data": user_data
            }
            
            print(f"Registrando usuário com email: {email}")
            
            # Fazer a requisição POST para registro
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=data
                )
                response.raise_for_status()
                
                # Retornar os dados do usuário
                user = response.json()
                return user
                
        except httpx.HTTPError as e:
            print(f"Erro ao registrar usuário: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Resposta de erro: {e.response.text}")
            raise
        except Exception as e:
            print(f"Erro inesperado ao registrar usuário: {str(e)}")
            raise

    async def insert(self, table, data):
        try:
            print(f"Inserindo na tabela {table}: {data}")
            result = await self._request("POST", f"/rest/v1/{table}", json=data)
            if isinstance(result, list):
                return result[0] if result else None
            return result
        except Exception as e:
            print(f"Erro ao inserir dados na tabela {table}: {str(e)}")
            raise

    async def select(self, table, columns="*", filters=None):
        params = {"select": columns}
        if filters:
            for key, value in filters.items():
                params[key] = value
        return await self._request("GET", f"/rest/v1/{table}", params=params)

    async def get_by_eq(self, table, column, value, select="*"):
        params = {
            "select": select,
            f"{column}": f"eq.{value}"
        }
        return await self._request("GET", f"/rest/v1/{table}", params=params)
        
    async def list_tables(self):
        """Lista todas as tabelas disponíveis no banco de dados."""
        try:
            # A API REST do Supabase não tem um endpoint para listar tabelas
            # Vamos tentar consultar informações das tabelas conhecidas
            result = {}
            
            # Verifica se a tabela 'users' existe
            try:
                users = await self._request("GET", "/rest/v1/users?limit=1", params=None)
                result["users"] = "Existe"
            except Exception:
                result["users"] = "Não existe"
                
            # Verifica se a tabela 'profiles' existe
            try:
                profiles = await self._request("GET", "/rest/v1/profiles?limit=1", params=None)
                result["profiles"] = "Existe"
            except Exception:
                result["profiles"] = "Não existe"
                
            return result
        except Exception as e:
            print(f"Erro ao listar tabelas: {str(e)}")
            return {"erro": str(e)}

# Instância do cliente para uso em toda a aplicação
supabase_client = SupabaseClient()
supabase_admin = SupabaseClient(use_service_key=True) 