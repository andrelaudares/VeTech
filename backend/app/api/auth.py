from fastapi import APIRouter, HTTPException, Body, Depends, Header
from pydantic import EmailStr
from typing import Dict, Any, Optional
import httpx
import jwt
from datetime import datetime

from ..models.user import UserCreate, UserResponse, ClinicProfileUpdate
from ..db.supabase import supabase_admin

router = APIRouter()

async def get_current_user(authorization: str = Header(...)) -> Dict[str, Any]:
    """
    Dependência para obter o usuário atual a partir do token JWT.
    """
    try:
        # Formato esperado: "Bearer [token]"
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token inválido")
        
        token = authorization.replace("Bearer ", "")
        
        # Verificar o token com o Supabase
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{supabase_admin.url}/auth/v1/user",
                headers={
                    **supabase_admin.headers,
                    "Authorization": f"Bearer {token}"
                }
            )
            response.raise_for_status()
            user_data = response.json()
            
            return {
                "id": user_data.get("id"),
                "email": user_data.get("email"),
                "user_metadata": user_data.get("user_metadata", {})
            }
    
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    except Exception as e:
        print(f"Erro ao verificar token: {str(e)}")
        raise HTTPException(status_code=401, detail="Falha na autenticação")

@router.post("/register", response_model=UserResponse)
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
        else:
            print("Erro: Estrutura da resposta de autenticação inesperada")
            print(f"Chaves em auth_user: {list(auth_user.keys())}")
        
        if not user_id:
            print("Erro: Não foi possível obter o ID do usuário")
            raise HTTPException(
                status_code=500,
                detail="Erro ao criar perfil: ID de usuário não encontrado"
            )
        
        # Agora vamos inserir os dados na tabela profiles manualmente
        try:
            # Dados para a tabela profiles
            clinics_data = {
                "id": user_id,  # Usar o ID do usuário autenticado
                "email": user.email,
                "name": user.name,
                "phone": user.phone,
                "password": user.password  # Adicionando a senha, pois a coluna existe na tabela profiles
            }
            
            print(f"Tentando inserir dados na tabela clinics: {clinics_data}")
            
            # Inserir dados na tabela profiles
            profile_result = await supabase_admin._request(
                "POST", 
                "/rest/v1/clinics", 
                json=clinics_data
            )
            
            print(f"Perfil criado com sucesso: {profile_result}")
            
        except Exception as profile_error:
            print(f"Erro ao criar perfil: {str(profile_error)}")
            # Mesmo se falhar a criação do perfil, o usuário já foi criado na autenticação
            # então retornamos os dados do usuário
        
        # Retornar a resposta
        return {
            "id": user_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "created_at": auth_user.get("created_at")
        }
    
    except Exception as e:
        print(f"Erro ao criar usuário: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
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
            user = auth_response.get("user", {})
            
            # Incluir o token de acesso na resposta
            return {
                "id": user.get("id", ""),
                "name": user.get("user_metadata", {}).get("name", ""),
                "email": user.get("email", ""),
                "phone": user.get("user_metadata", {}).get("phone", ""),
                "access_token": auth_response.get("access_token", ""),
                "refresh_token": auth_response.get("refresh_token", ""),
                "expires_at": auth_response.get("expires_at", ""),
                "message": "Login bem-sucedido"
            }
    
    except Exception as e:
        print(f"Erro ao fazer login: {str(e)}")
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
    try:
        # Obtém o ID do usuário atual
        user_id = current_user.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        # Busca os dados da clínica na tabela clinics
        response = await supabase_admin._request(
            "GET",
            f"/rest/v1/clinics?id=eq.{user_id}&select=*",
            headers={"Prefer": "return=representation"}
        )
        
        # Verifica se obteve os dados
        clinic_data = response.get("data", [])
        if not clinic_data or len(clinic_data) == 0:
            raise HTTPException(status_code=404, detail="Perfil de clínica não encontrado")
        
        # Retorna os dados da clínica (primeiro item da lista)
        clinic = clinic_data[0]
        return {
            "id": clinic.get("id"),
            "name": clinic.get("name"),
            "email": clinic.get("email"),
            "phone": clinic.get("phone"),
            "subscription_tier": clinic.get("subscription_tier", "basic"),
            "max_clients": clinic.get("max_clients", 50),
            "created_at": clinic.get("created_at"),
            "updated_at": clinic.get("updated_at")
        }
    
    except Exception as e:
        print(f"Erro ao buscar perfil da clínica: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao buscar dados do perfil")

@router.put("/clinic/profile")
async def update_clinic_profile(
    profile_update: ClinicProfileUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza os dados de perfil da clínica atualmente logada.
    """
    try:
        # Obtém o ID do usuário atual
        user_id = current_user.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        # Prepara os dados para atualização (apenas campos não nulos)
        update_data = {}
        if profile_update.name is not None:
            update_data["name"] = profile_update.name
        if profile_update.phone is not None:
            update_data["phone"] = profile_update.phone
        
        # Se não há dados para atualizar, retorna erro
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")
        
        # Adiciona timestamp de atualização
        update_data["updated_at"] = datetime.now().isoformat()
        
        try:
            # Atualiza os dados na tabela clinics
            response = await supabase_admin._request(
                "PATCH",
                f"/rest/v1/clinics?id=eq.{user_id}",
                json=update_data,
                headers={"Prefer": "return=representation"}
            )
            
            # Busca os dados atualizados
            updated_response = await supabase_admin._request(
                "GET",
                f"/rest/v1/clinics?id=eq.{user_id}&select=*",
                headers={"Prefer": "return=representation"}
            )
            
            # Verifica se obteve os dados
            updated_data = updated_response.get("data", [])
            if not updated_data or len(updated_data) == 0:
                raise HTTPException(status_code=404, detail="Perfil de clínica não encontrado após atualização")
            
            # Retorna os dados atualizados
            clinic = updated_data[0]
            return {
                "id": clinic.get("id"),
                "name": clinic.get("name"),
                "email": clinic.get("email"),
                "phone": clinic.get("phone"),
                "subscription_tier": clinic.get("subscription_tier", "basic"),
                "max_clients": clinic.get("max_clients", 50),
                "created_at": clinic.get("created_at"),
                "updated_at": clinic.get("updated_at"),
                "message": "Perfil atualizado com sucesso"
            }
        except Exception as supabase_error:
            print(f"Erro na comunicação com Supabase: {str(supabase_error)}")
            raise HTTPException(status_code=500, detail="Erro na comunicação com o banco de dados")
    
    except Exception as e:
        print(f"Erro ao atualizar perfil da clínica: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar dados do perfil")

# Adicione outras rotas aqui, como para gerenciamento de perfil