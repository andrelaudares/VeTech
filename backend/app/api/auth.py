from fastapi import APIRouter, HTTPException, Body, Depends, Header
from pydantic import EmailStr
from typing import Dict, Any, Optional
import httpx
import jwt
from datetime import datetime
import logging

from ..models.user import UserCreate, UserResponse, ClinicProfileUpdate
from ..db.supabase import supabase_admin

router = APIRouter()

logger = logging.getLogger(__name__)

async def get_current_user(authorization: str = Header(...)) -> Dict[str, Any]:
    """
    Dependência para obter o usuário atual a partir do token JWT.
    """
    logger.debug(f"Recebido header Authorization: {authorization}")
    try:
        # Formato esperado: "Bearer [token]"
        if not authorization or not authorization.startswith("Bearer "):
            logger.warning("Header de autorização ausente ou mal formatado.")
            raise HTTPException(status_code=401, detail="Token inválido ou ausente")
        
        token = authorization.split(" ")[1] # Mais robusto que replace
        logger.debug(f"Token extraído: {token}")
        
        # Headers para a requisição ao Supabase para validar o token do USUÁRIO
        # Garantir que APENAS o token do usuário seja usado para "Authorization"
        # e os outros headers necessários do supabase_admin (como apikey) sejam mantidos.
        request_headers = supabase_admin.headers.copy() # Copia os headers base (apikey, etc.)
        request_headers["Authorization"] = f"Bearer {token}" # Define/Sobrescreve o Authorization com o token do usuário

        logger.debug(f"Enviando requisição para Supabase /auth/v1/user com headers: {request_headers}")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{supabase_admin.url}/auth/v1/user",
                headers=request_headers
            )
            logger.debug(f"Resposta do Supabase /auth/v1/user: Status {response.status_code}, Conteúdo: {response.text}")
            response.raise_for_status() # Levanta exceção para 4xx/5xx
            user_data = response.json()
            
            # Verificar se user_data contém as informações esperadas
            if not user_data or not user_data.get("id"):
                logger.error(f"Resposta inesperada do Supabase /auth/v1/user: {user_data}")
                raise HTTPException(status_code=500, detail="Resposta inesperada do serviço de autenticação")
            
            return {
                "id": user_data.get("id"),
                "email": user_data.get("email"),
                "user_metadata": user_data.get("user_metadata", {})
            }
    
    except httpx.HTTPStatusError as exc:
        logger.error(f"Erro HTTP ao validar token com Supabase: {exc.response.status_code} - {exc.response.text}", exc_info=True)
        detail_message = "Falha na autenticação."
        if exc.response.status_code == 401:
            detail_message = "Token inválido ou expirado."
        elif exc.response.status_code == 403:
             # O JSON que você enviou ("arquivo-contexto") mostrava 403 de /auth/v1/user com bad_jwt
            detail_message = "Token JWT inválido (bad_jwt)."
        raise HTTPException(status_code=401, detail=detail_message) # Retorna 401 para o cliente

    except jwt.PyJWTError: # Embora a validação JWT local não pareça ser o caso aqui.
        logger.warning("Erro de decodificação JWT (PyJWTError)", exc_info=True)
        raise HTTPException(status_code=401, detail="Token JWT malformado.")
    
    except Exception as e:
        logger.error(f"Exceção não esperada em get_current_user: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno no servidor durante a autenticação")

@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(user: UserCreate) -> Dict[str, Any]:
    try:
        # Registrar o usuário na API de autenticação do Supabase
        print(f"Tentando registrar usuário com email: {user.email}")
        
        # Dados adicionais do usuário
        user_metadata = {
            "name": user.name,
            "phone": user.phone
        }
        
        # Registrar o usuário usando a API de autenticação
        auth_user = await supabase_admin.register_user(
            email=user.email,
            password=user.password,
            user_data=user_metadata
        )
        
        print(f"Usuário registrado com sucesso: {auth_user}")
        
        # Obter o ID do usuário recém-criado - corrigindo a obtenção do ID
        user_id = None
        if 'id' in auth_user:
            user_id = auth_user['id']
            print(f"ID do usuário extraído: {user_id}")
        elif 'user' in auth_user and 'id' in auth_user['user']:
            user_id = auth_user['user']['id']
            print(f"ID do usuário extraído de auth_user['user']: {user_id}")
        else:
            print("Erro: Estrutura da resposta de autenticação inesperada")
            print(f"Chaves em auth_user: {list(auth_user.keys())}")
            if 'user' in auth_user:
                print(f"Chaves em auth_user['user']: {list(auth_user['user'].keys()) if isinstance(auth_user['user'], dict) else 'user não é um dicionário'}")
        
        if not user_id:
            print("Erro: Não foi possível obter o ID do usuário")
            raise HTTPException(
                status_code=500,
                detail="Erro ao criar perfil: ID de usuário não encontrado"
            )
        
        # Agora vamos inserir os dados na tabela clinics
        try:
            # Verificar o tipo de subscription_tier
            subscription_tier = user.subscription_tier.lower()
            if subscription_tier not in ["basic", "premium", "enterprise"]:
                subscription_tier = "basic"
                
            # Ajustar para o caso do Supabase (primeira letra maiúscula)
            if subscription_tier == "basic":
                subscription_tier = "Basic"
            elif subscription_tier == "premium":
                subscription_tier = "Premium"
            elif subscription_tier == "enterprise":
                subscription_tier = "Enterprise"
            
            # Definir max_clients baseado no tier
            max_clients = 50  # valor padrão
            if subscription_tier == "Premium":
                max_clients = 100
            elif subscription_tier == "Enterprise":
                max_clients = 500

            # Criar timestamp para created_at e updated_at
            now = datetime.now().isoformat()

            # Dados para a tabela clinics
            clinics_data = {
                "id": user_id,
                "email": user.email,
                "name": user.name,
                "phone": user.phone,
                "subscription_tier": subscription_tier,
                "max_clients": max_clients,
                "password": user.password,  # Incluindo a senha pois o campo é NOT NULL
                "created_at": now,
                "updated_at": now
            }
            
            print(f"Tentando inserir dados na tabela clinics: {clinics_data}")
            
            # Usar o método insert do supabase_admin em vez do _request diretamente
            profile_result = await supabase_admin.insert("clinics", clinics_data)
            
            print(f"Perfil criado com sucesso: {profile_result}")
            
            # Retornar a resposta
            return {
                "id": user_id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "created_at": auth_user.get("created_at") or now
            }
            
        except Exception as profile_error:
            print(f"Erro ao criar perfil: {str(profile_error)}")
            
            # Se falhou a criação do perfil, tente dar mais detalhes sobre o erro
            error_detail = str(profile_error)
            
            # Se for um erro de comunicação com a API, tente obter mais detalhes
            if hasattr(profile_error, 'response'):
                error_detail += f" | Resposta: {profile_error.response.text}"
            
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao criar perfil na tabela clinics: {error_detail}"
            )
    
    except HTTPException:
        # Repassar as HTTPExceptions sem modificar
        raise
    except Exception as e:
        print(f"Erro ao criar usuário: {str(e)}")
        
        # Se for um erro de comunicação com a API, tente obter mais detalhes
        error_detail = str(e)
        if hasattr(e, 'response'):
            error_detail += f" | Resposta: {e.response.text}"
        
        raise HTTPException(
            status_code=500,
            detail=f"Erro durante o registro: {error_detail}"
        )

@router.post("/login")
async def login(email: EmailStr = Body(...), 
    password: str = Body(...)) -> Dict[str, Any]:
    try:
        # Endpoint para login
        url = f"{supabase_admin.url}/auth/v1/token?grant_type=password"
        
        # Dados para o login
        data = {
            "email": email,
            "password": password
        }
        
        print(f"Tentando fazer login para: {email}")
        
        # Fazer a requisição POST para login
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=supabase_admin.headers,
                json=data
            )
            response.raise_for_status()
            
            # Retornar os dados do usuário
            auth_response = response.json()
            print(f"Login bem-sucedido para: {email}")
            
            # Extrair dados do usuário
            user = auth_response.get("user", {})
            
            # Montar resposta no formato exato da documentação da API
            token = auth_response.get("access_token", "")
            if not token:
                print("ALERTA: Token não encontrado na resposta original!")
                # Tenta encontrar o token em outros campos possíveis
                token = auth_response.get("accessToken", auth_response.get("token", ""))
                
            result = {
                "access_token": token,
                "token_type": "bearer",
                "clinic": {
                    "id": user.get("id", ""),
                    "name": user.get("user_metadata", {}).get("name", ""),
                    "email": user.get("email", "")
                }
            }
            
            return result
    
    except Exception as e:
        # Adicionando log mais detalhado
        error_detail = f"Erro ao fazer login para o email {email}: {str(e)}"
        if isinstance(e, httpx.HTTPStatusError):
            # Se for um erro HTTP, logar o corpo da resposta se disponível
            error_detail += f" | Resposta do Supabase: {e.response.text}"
        print(error_detail)
        
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas"
        )

@router.post("/logout")
async def logout() -> Dict[str, str]:
    """
    Endpoint de logout. No momento, apenas retorna uma mensagem indicando
    que o cliente deve descartar o token.
    """
    # Futuramente, pode-se adicionar lógica para invalidar o token no servidor
    # (ex: adicionar a uma blacklist) se necessário.
    return {"message": "Logout bem-sucedido. Por favor, descarte o token no cliente."}

# Rotas de perfil da clínica
@router.get("/clinic/profile")
async def get_clinic_profile(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Obtém os dados de perfil da clínica atualmente logada.
    """
    logger.info(f"Tentando obter perfil para clinic_id: {current_user.get('id')}")
    try:
        user_id = current_user.get("id")
        if not user_id:
            logger.error("get_clinic_profile: ID do usuário não encontrado no token.")
            raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID não presente no token")

        # Busca os dados da clínica na tabela clinics usando _request e process_response
        # O select busca todos os campos relevantes conforme sprint1.md e schema
        query = f"/rest/v1/clinics?id=eq.{user_id}&select=id,name,email,phone,subscription_tier,max_clients,created_at,updated_at"
        
        # As chamadas de _request do supabase_admin devem usar a service_role_key implicitamente,
        # o que deve bypassar RLS para SELECT se configurado corretamente.
        response_data = await supabase_admin._request(
            "GET",
            query
            # Não precisa de headers{"Prefer": "return=representation"} para GET com select específico
        )

        clinic_list = supabase_admin.process_response(response_data)

        if not clinic_list:
            logger.warning(f"Perfil da clínica não encontrado para user_id: {user_id}. Resposta Supabase: {response_data}")
            raise HTTPException(status_code=404, detail="Perfil de clínica não encontrado")

        clinic = clinic_list[0]
        logger.info(f"Perfil da clínica encontrado para user_id: {user_id}")
        return {
            "id": clinic.get("id"),
            "name": clinic.get("name"),
            "email": clinic.get("email"),
            "phone": clinic.get("phone"),
            "subscription_tier": clinic.get("subscription_tier"), # Default já tratado pelo DB
            "max_clients": clinic.get("max_clients"), # Default já tratado pelo DB
            "created_at": clinic.get("created_at"),
            "updated_at": clinic.get("updated_at")
        }

    except HTTPException as http_exc:
        # Se já é uma HTTPException, apenas relança
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao buscar perfil da clínica para user_id {current_user.get('id')}: {str(e)}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'response') and hasattr(e.response, 'text'): # Verifica se e.response e e.response.text existem
            error_detail = f"{error_detail} - Response: {e.response.text}"
        raise HTTPException(status_code=500, detail=f"Erro interno ao buscar dados do perfil: {error_detail}")

@router.put("/clinic/profile")
async def update_clinic_profile(
    profile_update: ClinicProfileUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]: # A resposta deve ser consistente com sprint1.md
    """
    Atualiza os dados de perfil da clínica atualmente logada.
    """
    logger.info(f"Tentando atualizar perfil para clinic_id: {current_user.get('id')} com dados: {profile_update.model_dump(exclude_unset=True)}")
    try:
        user_id = current_user.get("id")
        if not user_id:
            logger.error("update_clinic_profile: ID do usuário não encontrado no token.")
            raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID não presente no token")

        update_data = profile_update.model_dump(exclude_unset=True)

        if not update_data:
            logger.info(f"Nenhum dado fornecido para atualização do perfil da clínica {user_id}")
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        # Adiciona timestamp de atualização
        update_data["updated_at"] = datetime.now().isoformat()

        # Primeiro, verificar se o perfil da clínica existe
        check_query = f"/rest/v1/clinics?id=eq.{user_id}&select=id"
        check_response_data = await supabase_admin._request("GET", check_query)
        if not supabase_admin.process_response(check_response_data):
            logger.warning(f"Tentativa de atualizar perfil não existente para user_id: {user_id}")
            raise HTTPException(status_code=404, detail="Perfil de clínica não encontrado para atualização")

        # Atualiza os dados na tabela clinics usando PATCH e Prefer: return=representation
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation" # Para obter o registro atualizado de volta

        patch_response_data = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/clinics?id=eq.{user_id}",
            json=update_data,
            headers=headers
        )

        updated_clinic_list = supabase_admin.process_response(patch_response_data)

        if not updated_clinic_list:
            logger.error(f"Falha ao atualizar perfil da clínica {user_id} ou dados não retornados. Resposta Supabase: {patch_response_data}")
            # Tentar buscar novamente como fallback, caso o Prefer não funcione como esperado ou a RLS interfira na leitura pós-escrita
            fallback_response_data = await supabase_admin._request("GET", f"/rest/v1/clinics?id=eq.{user_id}&select=id,name,email,phone,subscription_tier,max_clients,created_at,updated_at")
            fallback_clinic_list = supabase_admin.process_response(fallback_response_data)
            if not fallback_clinic_list:
                raise HTTPException(status_code=500, detail="Erro ao atualizar perfil: Falha ao buscar dados atualizados.")
            updated_clinic = fallback_clinic_list[0]
        else:
            updated_clinic = updated_clinic_list[0]

        logger.info(f"Perfil da clínica {user_id} atualizado com sucesso.")
        return {
            "id": updated_clinic.get("id"),
            "name": updated_clinic.get("name"),
            "email": updated_clinic.get("email"),
            "phone": updated_clinic.get("phone"),
            "subscription_tier": updated_clinic.get("subscription_tier"),
            "max_clients": updated_clinic.get("max_clients"),
            "created_at": updated_clinic.get("created_at"),
            "updated_at": updated_clinic.get("updated_at"),
            "message": "Perfil atualizado com sucesso" # Conforme sprint1.md
        }

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao atualizar perfil da clínica {current_user.get('id')}: {str(e)}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            error_detail = f"{error_detail} - Response: {e.response.text}"
        raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar dados do perfil: {error_detail}")

# Adicione outras rotas aqui, como para gerenciamento de perfil