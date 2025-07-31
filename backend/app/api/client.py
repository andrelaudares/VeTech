"""
Rotas de API para clientes (tutores)
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
import logging

from ..models.client import ClientProfileUpdate, AnimalUpdate
from ..db.supabase import supabase_admin
from .auth import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/profile")
async def get_client_profile(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Obtém os dados de perfil do cliente (tutor) atualmente logado.
    """
    try:
        user_id = current_user.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Buscar dados do tutor na tabela animals
        query = f"/rest/v1/animals?tutor_user_id=eq.{user_id}&select=tutor_name,email,phone,tutor_user_id"
        response_data = await supabase_admin._request("GET", query)
        animals_data = supabase_admin.process_response(response_data)

        if not animals_data:
            raise HTTPException(status_code=404, detail="Perfil de cliente não encontrado")

        # Pegar os dados do primeiro animal (todos devem ter os mesmos dados do tutor)
        client_data = animals_data[0]
        
        return {
            "id": client_data.get("tutor_user_id"),
            "name": client_data.get("tutor_name"),
            "email": client_data.get("email"),
            "phone": client_data.get("phone")
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar perfil do cliente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar dados do perfil")

@router.put("/profile")
async def update_client_profile(
    profile_update: ClientProfileUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza os dados de perfil do cliente (tutor) atualmente logado.
    """
    try:
        user_id = current_user.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        update_data = profile_update.model_dump(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        # Mapear campos do modelo para campos da tabela
        db_update_data = {}
        if "tutor_name" in update_data:
            db_update_data["tutor_name"] = update_data["tutor_name"]
        if "phone" in update_data:
            db_update_data["phone"] = update_data["phone"]

        if not db_update_data:
            raise HTTPException(status_code=400, detail="Nenhum campo válido para atualização")

        # Atualizar todos os registros do tutor na tabela animals
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"

        patch_response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/animals?tutor_user_id=eq.{user_id}",
            json=db_update_data,
            headers=headers
        )

        updated_animals = supabase_admin.process_response(patch_response)

        if not updated_animals:
            raise HTTPException(status_code=500, detail="Erro ao atualizar perfil")

        # Retornar dados atualizados do primeiro animal
        updated_client = updated_animals[0]
        
        return {
            "id": updated_client.get("tutor_user_id"),
            "name": updated_client.get("tutor_name"),
            "email": updated_client.get("email"),
            "phone": updated_client.get("phone"),
            "message": "Perfil atualizado com sucesso"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar perfil do cliente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar dados do perfil")

@router.get("/animals")
async def get_client_animals(current_user: Dict[str, Any] = Depends(get_current_user)) -> List[Dict[str, Any]]:
    """
    Obtém todos os animais do cliente (tutor) atualmente logado.
    """
    try:
        user_id = current_user.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Buscar todos os animais do tutor
        query = f"/rest/v1/animals?tutor_user_id=eq.{user_id}&select=id,name,species,breed,weight,age,medical_history,created_at,updated_at"
        response_data = await supabase_admin._request("GET", query)
        animals_data = supabase_admin.process_response(response_data)

        return animals_data or []

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar animais do cliente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar animais")

@router.get("/animals/{animal_id}")
async def get_animal_details(
    animal_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Obtém detalhes de um animal específico do cliente.
    """
    try:
        user_id = current_user.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Buscar animal específico do tutor
        query = f"/rest/v1/animals?id=eq.{animal_id}&tutor_user_id=eq.{user_id}&select=*"
        response_data = await supabase_admin._request("GET", query)
        animals_data = supabase_admin.process_response(response_data)

        if not animals_data:
            raise HTTPException(status_code=404, detail="Animal não encontrado")

        return animals_data[0]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar detalhes do animal: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar detalhes do animal")

@router.put("/animals/{animal_id}")
async def update_animal(
    animal_id: str,
    animal_update: AnimalUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza dados de um animal específico do cliente.
    """
    try:
        user_id = current_user.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        update_data = animal_update.model_dump(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        # Verificar se o animal pertence ao tutor
        check_query = f"/rest/v1/animals?id=eq.{animal_id}&tutor_user_id=eq.{user_id}&select=id"
        check_response = await supabase_admin._request("GET", check_query)
        if not supabase_admin.process_response(check_response):
            raise HTTPException(status_code=404, detail="Animal não encontrado")

        # Atualizar o animal
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"

        patch_response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/animals?id=eq.{animal_id}&tutor_user_id=eq.{user_id}",
            json=update_data,
            headers=headers
        )

        updated_animals = supabase_admin.process_response(patch_response)

        if not updated_animals:
            raise HTTPException(status_code=500, detail="Erro ao atualizar animal")

        return {
            **updated_animals[0],
            "message": "Animal atualizado com sucesso"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar animal: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar animal")

@router.get("/appointments")
async def get_client_appointments(current_user: Dict[str, Any] = Depends(get_current_user)) -> List[Dict[str, Any]]:
    """
    Obtém todos os agendamentos dos animais do cliente.
    """
    try:
        user_id = current_user.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Buscar agendamentos através dos animais do tutor
        # Primeiro, buscar IDs dos animais do tutor
        animals_query = f"/rest/v1/animals?tutor_user_id=eq.{user_id}&select=id"
        animals_response = await supabase_admin._request("GET", animals_query)
        animals_data = supabase_admin.process_response(animals_response)

        if not animals_data:
            return []

        animal_ids = [animal["id"] for animal in animals_data]
        
        # Buscar agendamentos para esses animais
        appointments = []
        for animal_id in animal_ids:
            appointments_query = f"/rest/v1/appointments?animal_id=eq.{animal_id}&select=*"
            appointments_response = await supabase_admin._request("GET", appointments_query)
            animal_appointments = supabase_admin.process_response(appointments_response)
            if animal_appointments:
                appointments.extend(animal_appointments)

        return appointments

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar agendamentos do cliente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar agendamentos")

@router.get("/animal")
async def get_my_animal(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Obtém os dados do animal principal do cliente (tutor) atualmente logado.
    Retorna o primeiro animal encontrado para o tutor.
    """
    try:
        user_id = current_user.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Buscar o primeiro animal do tutor
        query = f"/rest/v1/animals?tutor_user_id=eq.{user_id}&select=*&limit=1"
        response_data = await supabase_admin._request("GET", query)
        animals_data = supabase_admin.process_response(response_data)

        if not animals_data:
            raise HTTPException(status_code=404, detail="Nenhum animal encontrado para este tutor")

        return animals_data[0]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar animal do cliente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar animal")

@router.patch("/animal")
async def update_my_animal(
    animal_update: AnimalUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza os dados do animal principal do cliente (tutor) atualmente logado.
    """
    try:
        user_id = current_user.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        update_data = animal_update.model_dump(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        # Buscar o primeiro animal do tutor para obter o ID
        query = f"/rest/v1/animals?tutor_user_id=eq.{user_id}&select=id&limit=1"
        response_data = await supabase_admin._request("GET", query)
        animals_data = supabase_admin.process_response(response_data)

        if not animals_data:
            raise HTTPException(status_code=404, detail="Nenhum animal encontrado para este tutor")

        animal_id = animals_data[0]["id"]

        # Atualizar o animal
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"

        patch_response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/animals?id=eq.{animal_id}&tutor_user_id=eq.{user_id}",
            json=update_data,
            headers=headers
        )

        updated_animals = supabase_admin.process_response(patch_response)

        if not updated_animals:
            raise HTTPException(status_code=500, detail="Erro ao atualizar animal")

        return {
            **updated_animals[0],
            "message": "Animal atualizado com sucesso"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar animal: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar animal")