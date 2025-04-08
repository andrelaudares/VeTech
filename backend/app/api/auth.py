from fastapi import APIRouter, HTTPException, Body
from pydantic import EmailStr
from typing import Dict, Any
import httpx

from ..models.user import UserCreate, UserResponse
from ..db.supabase import supabase_admin

router = APIRouter()

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
            
            return {
                "id": user.get("id", ""),
                "name": user.get("user_metadata", {}).get("name", ""),
                "email": user.get("email", ""),
                "phone": user.get("user_metadata", {}).get("phone", ""),
                "message": "Login bem-sucedido"
            }
    
    except Exception as e:
        print(f"Erro ao fazer login: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas"
        )