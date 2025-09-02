"""
Rotas de consultas específicas para clientes/tutores
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel
from ..auth import get_current_user
from ...db.supabase import supabase_admin as supabase
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/debug/user-info")
async def debug_user_info(current_user: dict = Depends(get_current_user)):
    """
    Endpoint de debug para verificar informações do usuário logado
    """
    try:
        # Buscar informações do usuário na tabela animals
        animals_result = await supabase.select(
            "animals", 
            columns="*",
            filters={"tutor_user_id": f"eq.{current_user['id']}"}
        )
        
        # Buscar informações do usuário na tabela auth.users via email
        auth_user_info = None
        if current_user.get('email'):
            try:
                # Verificar se existe na tabela animals por email
                animals_by_email = await supabase.select(
                    "animals", 
                    columns="*",
                    filters={"email": f"eq.{current_user['email']}"}
                )
            except Exception as e:
                animals_by_email = None
        
        return {
            "current_user_from_jwt": current_user,
            "animals_by_tutor_user_id": animals_result,
            "animals_by_email": animals_by_email if 'animals_by_email' in locals() else None,
            "debug_info": {
                "user_id_exists_in_animals": len(animals_result) > 0 if animals_result else False,
                "total_animals_found": len(animals_result) if animals_result else 0
            }
        }
    except Exception as e:
        logger.error(f"Erro no debug: {str(e)}")
        return {
            "error": str(e),
            "current_user_from_jwt": current_user
        }

class ConsultationResponse(BaseModel):
    """Modelo de resposta para consultas do cliente"""
    id: str
    animal_id: str
    animal_name: str
    clinic_name: Optional[str] = None
    date: str
    description: str
    created_at: str
    updated_at: str

class ConsultationSummary(BaseModel):
    """Modelo de resumo de consultas"""
    total_consultations: int
    recent_consultations: List[ConsultationResponse]
    animals_with_consultations: int
    last_consultation_date: Optional[str] = None

@router.get("/", response_model=List[ConsultationResponse])
async def get_client_consultations(
    current_user: dict = Depends(get_current_user),
    animal_id: Optional[int] = Query(None, description="Filtrar por animal específico"),
    date_from: Optional[date] = Query(None, description="Data inicial"),
    date_to: Optional[date] = Query(None, description="Data final"),
    limit: int = Query(50, description="Limite de resultados")
):
    """
    Lista todas as consultas dos animais do cliente/tutor
    """
    try:
        # Log de debug para identificar o usuário
        logger.info(f"Buscando consultas para usuário: {current_user['id']} - Email: {current_user.get('email', 'N/A')}")
        
        # Primeiro, buscar os animais do tutor
        # Para tutores, o current_user['id'] é o user_id do Supabase Auth
        # Precisamos buscar pelos animais que têm tutor_user_id igual ao current_user['id']
        animals_result = await supabase.select(
            "animals", 
            columns="id,name",
            filters={"tutor_user_id": f"eq.{current_user['id']}"}
        )
        
        logger.info(f"Animais encontrados: {len(animals_result) if animals_result else 0}")
        if animals_result:
            logger.info(f"IDs dos animais: {[animal['id'] for animal in animals_result]}")
        
        if not animals_result:
            return []
        
        # Extrair IDs dos animais
        animal_ids = [animal["id"] for animal in animals_result]
        
        # Construir filtros para consultas
        filters = {}
        
        # Filtrar por animal específico se fornecido
        if animal_id:
            if animal_id not in animal_ids:
                return []  # Animal não pertence ao tutor
            filters["animal_id"] = f"eq.{animal_id}"
        else:
            # Filtrar por todos os animais do tutor
            if len(animal_ids) == 1:
                filters["animal_id"] = f"eq.{animal_ids[0]}"
            else:
                filters["animal_id"] = f"in.({','.join(map(str, animal_ids))})"
        
        # Filtros de data
        if date_from:
            filters["date"] = f"gte.{date_from.isoformat()}"
            
        if date_to:
            if "date" in filters:
                # Combinar filtros de data (precisa usar AND)
                filters["date"] = f"gte.{date_from.isoformat()}"
                filters["date"] = f"lte.{date_to.isoformat()}"
            else:
                filters["date"] = f"lte.{date_to.isoformat()}"
        
        # Buscar consultas com informações da clínica
        consultations_result = await supabase.select(
            "consultations",
            columns="id,animal_id,date,description,created_at,updated_at,clinic_id",
            filters=filters
        )
        
        if not consultations_result:
            return []
        
        # Buscar informações das clínicas
        clinic_ids = list(set([c["clinic_id"] for c in consultations_result if c.get("clinic_id")]))
        clinics_map = {}
        
        if clinic_ids:
            clinics_result = await supabase.select(
                "clinics",
                columns="id,name",
                filters={"id": f"in.({','.join(clinic_ids)})"}  
            )
            if clinics_result:
                clinics_map = {clinic["id"]: clinic["name"] for clinic in clinics_result}
        
        # Criar mapa de animais para facilitar o lookup
        animals_map = {animal["id"]: animal["name"] for animal in animals_result}
        
        # Formatar resposta
        consultations = []
        for consultation in consultations_result:
            animal_name = animals_map.get(consultation["animal_id"], "Animal não encontrado")
            clinic_name = clinics_map.get(consultation.get("clinic_id"), None)
            
            consultations.append(ConsultationResponse(
                id=consultation["id"],
                animal_id=consultation["animal_id"],
                animal_name=animal_name,
                clinic_name=clinic_name,
                date=consultation["date"],
                description=consultation["description"],
                created_at=consultation["created_at"],
                updated_at=consultation["updated_at"]
            ))
        
        return consultations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consultas: {str(e)}")

@router.get("/{consultation_id}", response_model=ConsultationResponse)
async def get_consultation_details(
    consultation_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtém detalhes de uma consulta específica
    """
    try:
        # Buscar a consulta específica
        consultation_result = await supabase.select(
            "consultations",
            columns="id,animal_id,date,description,created_at,updated_at,clinic_id",
            filters={"id": f"eq.{consultation_id}"}
        )
        
        if not consultation_result:
            raise HTTPException(status_code=404, detail="Consulta não encontrada")
        
        consultation = consultation_result[0] if isinstance(consultation_result, list) else consultation_result
        
        # Verificar se o animal da consulta pertence ao tutor
        animal_result = await supabase.get_by_eq(
            "animals",
            "id",
            consultation["animal_id"]
        )
        
        if not animal_result:
            raise HTTPException(status_code=404, detail="Animal não encontrado")
        
        animal = animal_result[0] if isinstance(animal_result, list) else animal_result
        
        # Verificar se o animal pertence ao tutor atual
        if animal["tutor_user_id"] != current_user["id"]:
            raise HTTPException(status_code=404, detail="Consulta não encontrada")
        
        # Buscar informações da clínica se disponível
        clinic_name = None
        if consultation.get("clinic_id"):
            clinic_result = await supabase.get_by_eq(
                "clinics",
                "id",
                consultation["clinic_id"]
            )
            if clinic_result:
                clinic = clinic_result[0] if isinstance(clinic_result, list) else clinic_result
                clinic_name = clinic.get("name")
        
        return ConsultationResponse(
            id=consultation["id"],
            animal_id=consultation["animal_id"],
            animal_name=animal["name"],
            clinic_name=clinic_name,
            date=consultation["date"],
            description=consultation["description"],
            created_at=consultation["created_at"],
            updated_at=consultation["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consulta: {str(e)}")

@router.get("/animal/{animal_id}", response_model=List[ConsultationResponse])
async def get_animal_consultations(
    animal_id: str,
    current_user: dict = Depends(get_current_user),
    limit: int = Query(20, description="Limite de resultados")
):
    """
    Lista consultas de um animal específico
    """
    try:
        # Verificar se o animal pertence ao tutor
        animal_result = await supabase.get_by_eq(
            "animals",
            "id",
            animal_id
        )
        
        if not animal_result:
            raise HTTPException(status_code=404, detail="Animal não encontrado")
        
        animal = animal_result[0] if isinstance(animal_result, list) else animal_result
        
        # Verificar se o animal pertence ao tutor atual
        if animal["tutor_user_id"] != current_user["id"]:
            raise HTTPException(status_code=404, detail="Animal não encontrado")
        
        # Buscar consultas do animal
        consultations_result = await supabase.select(
            "consultations",
            columns="id,animal_id,date,description,created_at,updated_at,clinic_id",
            filters={"animal_id": f"eq.{animal_id}"}
        )
        
        if not consultations_result:
            return []
        
        # Buscar informações das clínicas
        clinic_ids = list(set([c["clinic_id"] for c in consultations_result if c.get("clinic_id")]))
        clinics_map = {}
        
        if clinic_ids:
            clinics_result = await supabase.select(
                "clinics",
                columns="id,name",
                filters={"id": f"in.({','.join(clinic_ids)})"}
            )
            if clinics_result:
                clinics_map = {clinic["id"]: clinic["name"] for clinic in clinics_result}
        
        # Formatar resposta
        consultations = []
        for consultation in consultations_result:
            clinic_name = clinics_map.get(consultation.get("clinic_id"), None)
            
            consultations.append(ConsultationResponse(
                id=consultation["id"],
                animal_id=consultation["animal_id"],
                animal_name=animal["name"],
                clinic_name=clinic_name,
                date=consultation["date"],
                description=consultation["description"],
                created_at=consultation["created_at"],
                updated_at=consultation["updated_at"]
            ))
        
        # Ordenar por data (mais recentes primeiro)
        consultations.sort(key=lambda x: x.date, reverse=True)
        
        # Aplicar limite
        return consultations[:limit]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consultas do animal: {str(e)}")

@router.get("/summary/overview", response_model=ConsultationSummary)
async def get_consultations_summary(
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna um resumo das consultas do cliente
    """
    try:
        # Primeiro, buscar os animais do tutor
        # Para tutores, o current_user['id'] é o user_id do Supabase Auth
        # Precisamos buscar pelos animais que têm tutor_user_id igual ao current_user['id']
        animals_result = await supabase.select(
            "animals", 
            columns="id,name",
            filters={"tutor_user_id": f"eq.{current_user['id']}"}
        )
        
        if not animals_result:
            return ConsultationSummary(
                total_consultations=0,
                recent_consultations=[],
                animals_with_consultations=0,
                last_consultation_date=None
            )
        
        # Extrair IDs dos animais
        animal_ids = [animal["id"] for animal in animals_result]
        animals_map = {animal["id"]: animal["name"] for animal in animals_result}
        
        # Buscar todas as consultas dos animais do tutor
        filters = {}
        if len(animal_ids) == 1:
            filters["animal_id"] = f"eq.{animal_ids[0]}"
        else:
            filters["animal_id"] = f"in.({','.join(map(str, animal_ids))})"
        
        consultations_result = await supabase.select(
            "consultations",
            columns="id,animal_id,date,description,created_at,updated_at,clinic_id",
            filters=filters
        )
        
        if not consultations_result:
            return ConsultationSummary(
                total_consultations=0,
                recent_consultations=[],
                animals_with_consultations=0,
                last_consultation_date=None
            )
        
        # Buscar informações das clínicas
        clinic_ids = list(set([c["clinic_id"] for c in consultations_result if c.get("clinic_id")]))
        clinics_map = {}
        
        if clinic_ids:
            clinics_result = await supabase.select(
                "clinics",
                columns="id,name",
                filters={"id": f"in.({','.join(clinic_ids)})"}
            )
            if clinics_result:
                clinics_map = {clinic["id"]: clinic["name"] for clinic in clinics_result}
        
        # Ordenar consultas por data (mais recentes primeiro)
        consultations_result.sort(key=lambda x: x["date"], reverse=True)
        
        # Pegar as 5 consultas mais recentes
        recent_consultations_data = consultations_result[:5]
        
        # Formatar consultas recentes
        recent_consultations = []
        for consultation in recent_consultations_data:
            animal_name = animals_map.get(consultation["animal_id"], "Animal não encontrado")
            clinic_name = clinics_map.get(consultation.get("clinic_id"), None)
            
            recent_consultations.append(ConsultationResponse(
                    id=consultation["id"],
                    animal_id=consultation["animal_id"],
                    animal_name=animal_name,
                    clinic_name=clinic_name,
                    date=consultation["date"],
                    description=consultation["description"],
                    created_at=consultation["created_at"],
                    updated_at=consultation["updated_at"]
                ))
        
        # Contar animais únicos com consultas
        unique_animals = len(set(consultation["animal_id"] for consultation in consultations_result))
        
        # Última consulta
        last_consultation_date = consultations_result[0]["date"] if consultations_result else None
        
        return ConsultationSummary(
            total_consultations=len(consultations_result),
            recent_consultations=recent_consultations,
            animals_with_consultations=unique_animals,
            last_consultation_date=last_consultation_date
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar resumo: {str(e)}")