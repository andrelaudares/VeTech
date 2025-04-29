import os
import httpx
import json
from typing import Any, Dict, List, Optional
from ..core.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_KEY

class SupabaseClient:
    def __init__(self, url: str, key: str, service_key: Optional[str] = None):
        self.url = url
        self.key = key
        self.service_key = service_key
        self.headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }

        if service_key:
            self.admin_headers = {
                "apikey": service_key,
                "Authorization": f"Bearer {service_key}",
                "Content-Type": "application/json"
            }
        else:
            self.admin_headers = self.headers

    async def _request(self, method, endpoint, json=None, params=None, headers=None):
        """
        Método para fazer requisições para a API do Supabase
        """
        url = f"{self.url}{endpoint}"
        
        # Use os cabeçalhos fornecidos ou os padrão
        request_headers = headers or self.headers
        if endpoint.startswith("/auth/") and self.service_key:
            request_headers = self.admin_headers
            
        # Adicionar o header Prefer para retornar a representação
        if "Prefer" not in request_headers:
            request_headers["Prefer"] = "return=representation"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method,
                    url=url,
                    json=json,
                    params=params,
                    headers=request_headers,
                    timeout=30.0
                )
                
                try:
                    response.raise_for_status()
                    return {"data": response.json()}
                except httpx.HTTPStatusError as e:
                    error_detail = response.text
                    try:
                        error_json = response.json()
                        if 'error' in error_json:
                            error_detail = error_json.get('error', {}).get('message', error_detail)
                        elif 'msg' in error_json:
                            error_detail = error_json['msg']
                    except:
                        pass
                    
                    return {"error": f"HTTP Error: {e.response.status_code} - {error_detail}"}
        except Exception as e:
            return {"error": f"Erro inesperado: {str(e)}"}

    def process_response(self, response, single_item=False):
        """
        Processa a resposta do Supabase, lidando com diferentes formatos de resposta.
        
        Args:
            response (dict): A resposta obtida de _request
            single_item (bool): Se deve retornar apenas o primeiro item quando o resultado for uma lista
            
        Returns:
            dict/list: Os dados da resposta processados
            None: Se ocorrer um erro
        """
        if "error" in response:
            return None
            
        data = response.get("data", {})
        
        if single_item:
            if isinstance(data, list) and data:
                return data[0]
            elif isinstance(data, dict):
                return data
            else:
                return None
        else:
            return data

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
            print(f"Resultado da inserção: {result}")
            return self.process_response(result, single_item=True)
        except httpx.HTTPError as e:
            error_msg = f"Erro HTTP ao inserir dados na tabela {table}: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f" | Resposta: {e.response.text}"
            print(error_msg)
            raise
        except Exception as e:
            print(f"Erro ao inserir dados na tabela {table}: {str(e)}")
            raise

    async def select(self, table, columns="*", filters=None):
        params = {"select": columns}
        if filters:
            for key, value in filters.items():
                params[key] = value
        
        url = f"{self.url}/rest/v1/{table}"
        print(f"Fazendo consulta para URL: {url}")
        print(f"Parâmetros: {params}")
        
        result = await self._request("GET", f"/rest/v1/{table}", params=params)
        return self.process_response(result)

    async def get_by_eq(self, table, column, value, select="*"):
        params = {
            "select": select,
            f"{column}": f"eq.{value}"
        }
        result = await self._request("GET", f"/rest/v1/{table}", params=params)
        return self.process_response(result)
        
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
supabase_client = SupabaseClient(SUPABASE_URL, SUPABASE_KEY)
supabase_admin = SupabaseClient(SUPABASE_URL, SUPABASE_SERVICE_KEY) 