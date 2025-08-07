from fastapi import APIRouter, HTTPException, Depends, Query, Body, Path
from typing import Dict, Any, List, Optional
from ..models.consultation import ConsultationCreate, ConsultationResponse, ConsultationUpdate
from ..db.supabase import supabase_admin
from uuid import UUID
from datetime import datetime
import logging
from ..api.auth import get_current_user

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("", response_model=ConsultationResponse)
async def create_consultation(
    consultation: ConsultationCreate = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID da clínica não encontrado no token")

    logger.info(f"Requisição recebida para criar consulta para clinic_id: {clinic_id}")
    logger.info(f"Dados da consulta recebidos: {consultation.model_dump()}")

    try:
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{consultation.animal_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(animal_response):
            logger.warning(f"Animal {consultation.animal_id} não encontrado ou não pertence à clínica {clinic_id}")
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence à clínica")

        consultation_data = {
            "clinic_id": str(clinic_id),
            "animal_id": str(consultation.animal_id),
            "description": consultation.description,
            "date": consultation.date.isoformat() if consultation.date else datetime.utcnow().isoformat()
        }

        logger.info(f"Tentando inserir consulta na tabela 'consultations' com dados: {consultation_data}")

        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"
        response = await supabase_admin._request(
            "POST",
            "/rest/v1/consultations",
            json=consultation_data,
            headers=headers
        )
        created_consultation = supabase_admin.process_response(response, single_item=True)

        if created_consultation:
            logger.info(f"Consulta criada com sucesso: {created_consultation}")
            return created_consultation
        else:
            logger.error(f"Resposta inesperada ao inserir consulta: {response}")
            raise HTTPException(status_code=500, detail="Resposta inesperada do Supabase.")

    except HTTPException as http_exc:
        logger.error(f"Erro HTTP: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao criar consulta: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("", response_model=List[ConsultationResponse])
async def get_consultations(
    animal_id: Optional[UUID] = Query(None, description="Filtrar consultas por ID do animal"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID da clínica não encontrado no token")

    logger.info(f"Requisição para listar consultas da clinic_id: {clinic_id}, animal_id: {animal_id}")
    try:
        query = f"/rest/v1/consultations?clinic_id=eq.{clinic_id}&select=*"
        if animal_id:
            query += f"&animal_id=eq.{animal_id}"
        query += "&order=date.desc"

        response = await supabase_admin._request("GET", query)
        consultations = supabase_admin.process_response(response)

        logger.info(f"Consultas encontradas: {len(consultations)}")
        return consultations
    except Exception as e:
        logger.error(f"Erro ao buscar consultas: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.patch("/{consultation_id}", response_model=ConsultationResponse)
async def update_consultation(
    consultation_id: UUID = Path(..., description="ID da consulta a ser atualizada"),
    consultation_update: ConsultationUpdate = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    logger.info(f"Atualizando consulta ID: {consultation_id}")
    logger.info(f"Dados: {consultation_update.model_dump(exclude_unset=True)}")

    try:
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        check_query = f"/rest/v1/consultations?id=eq.{consultation_id}&clinic_id=eq.{clinic_id}&select=id"
        check_response = await supabase_admin._request("GET", check_query)
        existing_consultation = supabase_admin.process_response(check_response)

        if not existing_consultation:
            logger.warning(f"Consulta {consultation_id} não encontrada ou não pertence à clínica {clinic_id}")
            raise HTTPException(status_code=404, detail="Consulta não encontrada ou não pertence à clínica")

        update_data = consultation_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado para atualizar")

        if 'date' in update_data and isinstance(update_data['date'], datetime):
            update_data['date'] = update_data['date'].isoformat()

        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"
        update_response = await supabase_admin._request(
            method="PATCH",
            endpoint=f"/rest/v1/consultations?id=eq.{consultation_id}&clinic_id=eq.{clinic_id}",
            json=update_data,
            headers=headers
        )

        updated_data = supabase_admin.process_response(update_response)

        if not updated_data:
            fallback_get = await supabase_admin._request("GET", f"/rest/v1/consultations?id=eq.{consultation_id}&clinic_id=eq.{clinic_id}&select=*")
            fallback_data = supabase_admin.process_response(fallback_get)
            if not fallback_data:
                 logger.error(f"Erro ao atualizar consulta {consultation_id}: não encontrada após PATCH.")
                 raise HTTPException(status_code=500, detail="Falha ao atualizar consulta ou buscar dados atualizados.")
            updated_data = fallback_data

        logger.info(f"Consulta {consultation_id} atualizada com sucesso.")
        return updated_data[0]

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao atualizar consulta {consultation_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/{consultation_id}", status_code=204)
async def delete_consultation(
    consultation_id: UUID = Path(..., description="ID da consulta a ser deletada"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> None:
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID da clínica não encontrado no token")

    logger.info(f"Deletando consulta ID: {consultation_id} da clinic_id: {clinic_id}")

    try:
        check_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/consultations?id=eq.{consultation_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(check_response):
            raise HTTPException(status_code=404, detail="Consulta não encontrada ou não pertence à clínica")

        params = {"id": f"eq.{consultation_id}", "clinic_id": f"eq.{clinic_id}"}
        await supabase_admin._request(
            method="DELETE",
            endpoint="/rest/v1/consultations",
            params=params
        )
        logger.info(f"Consulta {consultation_id} deletada.")
        return None

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao deletar consulta {consultation_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/tutor/{tutor_id}", response_model=List[ConsultationResponse])
async def get_tutor_consultations(
    tutor_id: int = Path(..., description="ID do tutor"),
    animal_id: Optional[UUID] = Query(None, description="Filtrar por animal específico"),
    limit: Optional[int] = Query(10, description="Número máximo de consultas"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Lista consultas dos animais de um tutor específico.
    Endpoint para área do tutor visualizar histórico de consultas.
    """
    user_id = current_user.get("id")
    user_type = current_user.get("user_type", "clinic")
    
    # Verificar se o usuário atual é o próprio tutor ou uma clínica
    if user_type == "tutor" and user_id != tutor_id:
        raise HTTPException(status_code=403, detail="Acesso negado: você só pode ver suas próprias consultas")
    
    logger.info(f"Listando consultas para tutor_id: {tutor_id}, animal_id: {animal_id}")

    try:
        # Primeiro, buscar os animais do tutor
        animals_query = f"/rest/v1/animals?tutor_user_id=eq.{tutor_id}&select=id,name,species,breed"
        animals_response = await supabase_admin._request("GET", animals_query)
        animals_data = supabase_admin.process_response(animals_response)
        
        if not animals_data:
            logger.info(f"Nenhum animal encontrado para tutor_id: {tutor_id}")
            return []
        
        # Filtrar por animal específico se fornecido
        if animal_id:
            animals_data = [animal for animal in animals_data if animal["id"] == str(animal_id)]
            if not animals_data:
                logger.info(f"Animal {animal_id} não encontrado para tutor_id: {tutor_id}")
                return []
        
        # Extrair IDs dos animais
        animal_ids = [animal["id"] for animal in animals_data]
        animal_names = {animal["id"]: animal["name"] for animal in animals_data}
        
        # Buscar consultas dos animais do tutor
        consultations_query = f"/rest/v1/consultations?animal_id=in.({','.join(animal_ids)})"
        consultations_query += "&order=date.desc"
        
        if limit:
            consultations_query += f"&limit={limit}"
        
        logger.debug(f"Executando query de consultas: {consultations_query}")
        
        consultations_response = await supabase_admin._request("GET", consultations_query)
        consultations_data = supabase_admin.process_response(consultations_response)
        
        # Enriquecer dados com informações dos animais
        for consultation in consultations_data:
            animal_id = consultation.get("animal_id")
            if animal_id in animal_names:
                consultation["animal_name"] = animal_names[animal_id]
        
        logger.info(f"Encontradas {len(consultations_data)} consultas para tutor_id: {tutor_id}")
        return consultations_data
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao buscar consultas do tutor {tutor_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consultas do tutor: {str(e)}")

@router.get("/tutor/{tutor_id}/animal/{animal_id}", response_model=List[ConsultationResponse])
async def get_tutor_animal_consultations(
    tutor_id: int = Path(..., description="ID do tutor"),
    animal_id: UUID = Path(..., description="ID do animal"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Lista consultas de um animal específico do tutor.
    Endpoint detalhado para histórico de um animal.
    """
    user_id = current_user.get("id")
    user_type = current_user.get("user_type", "clinic")
    
    # Verificar se o usuário atual é o próprio tutor ou uma clínica
    if user_type == "tutor" and user_id != tutor_id:
        raise HTTPException(status_code=403, detail="Acesso negado: você só pode ver consultas de seus próprios animais")
    
    logger.info(f"Listando consultas para tutor_id: {tutor_id}, animal_id: {animal_id}")

    try:
        # Verificar se o animal pertence ao tutor
        animal_query = f"/rest/v1/animals?id=eq.{animal_id}&tutor_user_id=eq.{tutor_id}&select=id,name,species,breed"
        animal_response = await supabase_admin._request("GET", animal_query)
        animal_data = supabase_admin.process_response(animal_response)
        
        if not animal_data:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence ao tutor")
        
        animal_info = animal_data[0]
        
        # Buscar consultas do animal
        consultations_query = f"/rest/v1/consultations?animal_id=eq.{animal_id}&order=date.desc"
        consultations_response = await supabase_admin._request("GET", consultations_query)
        consultations_data = supabase_admin.process_response(consultations_response)
        
        # Enriquecer dados com informações do animal
        for consultation in consultations_data:
            consultation["animal_name"] = animal_info["name"]
            consultation["animal_species"] = animal_info["species"]
            consultation["animal_breed"] = animal_info["breed"]
        
        logger.info(f"Encontradas {len(consultations_data)} consultas para animal {animal_id}")
        return consultations_data
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao buscar consultas do animal {animal_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consultas do animal: {str(e)}")

@router.get("/tutor/{tutor_id}/summary")
async def get_tutor_consultations_summary(
    tutor_id: int = Path(..., description="ID do tutor"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Retorna um resumo das consultas do tutor.
    Inclui estatísticas e últimas consultas.
    """
    user_id = current_user.get("id")
    user_type = current_user.get("user_type", "clinic")
    
    # Verificar se o usuário atual é o próprio tutor ou uma clínica
    if user_type == "tutor" and user_id != tutor_id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    logger.info(f"Gerando resumo de consultas para tutor_id: {tutor_id}")

    try:
        # Buscar animais do tutor
        animals_query = f"/rest/v1/animals?tutor_user_id=eq.{tutor_id}&select=id,name,species"
        animals_response = await supabase_admin._request("GET", animals_query)
        animals_data = supabase_admin.process_response(animals_response)
        
        if not animals_data:
            return {
                "total_animals": 0,
                "total_consultations": 0,
                "recent_consultations": [],
                "animals_summary": []
            }
        
        animal_ids = [animal["id"] for animal in animals_data]
        
        # Buscar todas as consultas dos animais
        consultations_query = f"/rest/v1/consultations?animal_id=in.({','.join(animal_ids)})"
        consultations_response = await supabase_admin._request("GET", consultations_query)
        consultations_data = supabase_admin.process_response(consultations_response)
        
        # Buscar últimas 5 consultas
        recent_query = f"/rest/v1/consultations?animal_id=in.({','.join(animal_ids)})"
        recent_query += "&order=date.desc&limit=5"
        recent_response = await supabase_admin._request("GET", recent_query)
        recent_consultations = supabase_admin.process_response(recent_response)
        
        # Criar mapa de nomes dos animais
        animal_names = {animal["id"]: animal["name"] for animal in animals_data}
        
        # Enriquecer consultas recentes
        for consultation in recent_consultations:
            animal_id = consultation.get("animal_id")
            if animal_id in animal_names:
                consultation["animal_name"] = animal_names[animal_id]
        
        # Calcular estatísticas por animal
        animals_summary = []
        for animal in animals_data:
            animal_consultations = [c for c in consultations_data if c["animal_id"] == animal["id"]]
            animals_summary.append({
                "animal_id": animal["id"],
                "animal_name": animal["name"],
                "species": animal["species"],
                "total_consultations": len(animal_consultations),
                "last_consultation": max([c["date"] for c in animal_consultations]) if animal_consultations else None
            })
        
        summary = {
            "total_animals": len(animals_data),
            "total_consultations": len(consultations_data),
            "recent_consultations": recent_consultations,
            "animals_summary": animals_summary
        }
        
        logger.info(f"Resumo gerado para tutor_id: {tutor_id}")
        return summary
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao gerar resumo para tutor {tutor_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao gerar resumo: {str(e)}")