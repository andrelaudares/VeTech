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
        
        # Os dados de profiles são gerenciados automaticamente pelo Supabase quando 
        # usamos a função auth.users() e temos uma trigger RLS configurada
        
        # Retornar a resposta
        return {
            "id": auth_user.get("id", ""),
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