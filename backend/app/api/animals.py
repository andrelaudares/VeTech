from fastapi import APIRouter, HTTPException, Depends, Query, Body
from typing import Dict, Any, Annotated
from ..models.animal import AnimalCreate, AnimalResponse
from ..db.supabase import supabase_admin
from uuid import UUID
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("", response_model=AnimalResponse)
async def create_animal(
    # Recebe os dados do animal do corpo da requisição
    animal: AnimalCreate = Body(...), 
    # Recebe clinics_id como parâmetro de query obrigatório
    clinics_id: UUID = Query(..., description="ID da clínica que está cadastrando o animal")
) -> Dict[str, Any]:
    logger.info(f"Requisição recebida para criar animal para clinic_id: {clinics_id}")
    logger.info(f"Dados do animal recebidos: {animal.model_dump()}")
    
    try:
        # Preparar os dados do animal para inserção
        # Garantindo que apenas os campos esperados pela tabela `animals` (com clinics_id) sejam enviados
        animal_data = {
            "clinics_id": str(clinics_id),  # ID da clínica logada
            "name": animal.name,
            "species": animal.species,
            "breed": animal.breed,
            "age": animal.age,
            "weight": animal.weight,
            "medical_history": animal.medical_history
        }
        
        logger.info(f"Tentando inserir animal na tabela 'animals' com dados: {animal_data}")
        
        # Inserir o animal no banco de dados usando o método insert
        try:
            # A função insert já lida com a requisição POST para /rest/v1/animals
            created_animal = await supabase_admin.insert("animals", data=animal_data)
            
            # O método insert retorna uma lista, pegamos o primeiro elemento
            if isinstance(created_animal, list) and created_animal:
                 logger.info(f"Animal criado com sucesso no Supabase: {created_animal[0]}")
                 return created_animal[0] # Retorna o dicionário do animal criado
            elif isinstance(created_animal, dict): # Caso retorne dict diretamente
                 logger.info(f"Animal criado com sucesso no Supabase: {created_animal}")
                 return created_animal
            else:
                logger.error(f"Resposta inesperada do Supabase ao inserir animal: {created_animal}")
                raise HTTPException(
                    status_code=500,
                    detail="Resposta inesperada do Supabase após inserção."
                )

        except HTTPException as http_exc:
             # Se o erro já for HTTPException (ex: vindo do _request dentro do insert), repassa
             logger.error(f"Erro HTTP durante a chamada Supabase: Status={http_exc.status_code}, Detalhe={http_exc.detail}")
             raise http_exc
        except Exception as supabase_error:
            # Captura outros erros da chamada ao Supabase
            logger.error(f"Erro na chamada Supabase 'insert': {supabase_error}", exc_info=True)
            # Tenta extrair detalhes do erro, se possível
            error_detail = str(supabase_error)
            if hasattr(supabase_error, 'response') and supabase_error.response is not None:
                 error_detail = f"{error_detail} - Response: {supabase_error.response.text}"
            raise HTTPException(
                status_code=500,
                detail=f"Erro interno ao tentar inserir animal no banco: {error_detail}"
            )
            
    except Exception as e:
        # Captura erros gerais antes da chamada ao Supabase (ex: preparação de dados)
        logger.error(f"Erro geral em create_animal antes da chamada Supabase: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno no servidor: {str(e)}"
        )
