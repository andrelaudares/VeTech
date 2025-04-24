from fastapi import APIRouter, HTTPException, Depends, Query, Body, Path
from typing import Dict, Any, Annotated, Optional
from ..models.animal import AnimalCreate, AnimalResponse, AnimalUpdate
from ..models.animal_preferences import PetPreferencesCreate, PetPreferencesUpdate, PetPreferencesResponse
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
    clinic_id: UUID = Query(..., description="ID da clínica que está cadastrando o animal")
) -> Dict[str, Any]:
    logger.info(f"Requisição recebida para criar animal para clinic_id: {clinic_id}")
    logger.info(f"Dados do animal recebidos: {animal.model_dump()}")
    
    try:
        # Preparar os dados do animal para inserção
        # Garantindo que apenas os campos esperados pela tabela `animals` (com clinics_id) sejam enviados
        animal_data = {
            "clinic_id": str(clinic_id),  # ID da clínica logada
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

@router.patch("/{animal_id}", response_model=AnimalResponse)
async def update_animal(
    animal_id: UUID = Path(..., description="ID do animal a ser atualizado"),
    animal_update: AnimalUpdate = Body(...),
    clinic_id: UUID = Query(..., description="ID da clínica proprietária do animal")
) -> Dict[str, Any]:
    logger.info(f"Requisição recebida para atualizar animal ID: {animal_id} para clinic_id: {clinic_id}")
    logger.info(f"Dados de atualização recebidos: {animal_update.model_dump(exclude_unset=True)}")

    try:
        # Verifica se o animal pertence à clínica
        existing_animal = await supabase_admin.get_by_eq(
            table="animals",
            column="id",
            value=str(animal_id),
            select="id, clinic_id"
        )
        if not existing_animal or str(existing_animal[0]['clinic_id']) != str(clinic_id):
            logger.warning(f"Animal {animal_id} não encontrado ou não pertence à clínica {clinic_id}")
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence à clínica")

        # Preparar os dados para atualização (apenas campos fornecidos)
        update_data = animal_update.model_dump(exclude_unset=True)

        if not update_data:
             raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        logger.info(f"Tentando atualizar animal ID: {animal_id} com dados: {update_data}")

        # Atualizar o animal no banco de dados usando o método _request diretamente
        # O método `update` do Supabase requer filtros e dados
        params = {
            "id": f"eq.{animal_id}",
            "clinic_id": f"eq.{clinic_id}" # Garante que só atualize se pertencer à clínica
        }
        updated_animal_list = await supabase_admin._request(
            method="PATCH",
            endpoint=f"/rest/v1/animals",
            params=params,
            json=update_data
        )

        if not updated_animal_list:
            logger.error(f"Falha ao atualizar animal {animal_id}. Resposta vazia do Supabase.")
            raise HTTPException(status_code=404, detail="Falha ao atualizar o animal. Animal não encontrado ou erro interno.")

        # A resposta de PATCH geralmente retorna uma lista com o objeto atualizado
        updated_animal = updated_animal_list[0]
        logger.info(f"Animal {animal_id} atualizado com sucesso: {updated_animal}")
        return updated_animal

    except HTTPException as http_exc:
        logger.error(f"Erro HTTP ao atualizar animal {animal_id}: Status={http_exc.status_code}, Detalhe={http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Erro geral ao atualizar animal {animal_id}: {e}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
             error_detail = f"{error_detail} - Response: {e.response.text}"
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno no servidor ao atualizar animal: {error_detail}"
        )

@router.delete("/{animal_id}", status_code=204)
async def delete_animal(
    animal_id: UUID = Path(..., description="ID do animal a ser deletado"),
    clinic_id: UUID = Query(..., description="ID da clínica proprietária do animal")
) -> None:
    logger.info(f"Requisição recebida para deletar animal ID: {animal_id} da clinic_id: {clinic_id}")

    try:
        # Verificar se o animal pertence à clínica antes de deletar (opcional, mas bom para segurança)
        existing_animal = await supabase_admin.get_by_eq(
            table="animals",
            column="id",
            value=str(animal_id),
            select="id, clinic_id"
        )
        if not existing_animal or str(existing_animal[0]['clinic_id']) != str(clinic_id):
            logger.warning(f"Tentativa de deletar animal {animal_id} não encontrado ou não pertencente à clínica {clinic_id}")
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence à clínica")

        # Deletar o animal usando o método _request
        params = {
            "id": f"eq.{animal_id}",
            "clinic_id": f"eq.{clinic_id}" # Garante que só delete se pertencer à clínica
        }
        await supabase_admin._request(
            method="DELETE",
            endpoint="/rest/v1/animals",
            params=params
        )
        # DELETE não retorna conteúdo, então apenas logamos sucesso
        logger.info(f"Animal {animal_id} deletado com sucesso da clínica {clinic_id}")
        return None # Retorna None para indicar sucesso com status 204 No Content

    except HTTPException as http_exc:
        logger.error(f"Erro HTTP ao deletar animal {animal_id}: Status={http_exc.status_code}, Detalhe={http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Erro geral ao deletar animal {animal_id}: {e}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
             error_detail = f"{error_detail} - Response: {e.response.text}"
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno no servidor ao deletar animal: {error_detail}"
        )

@router.get("", response_model=list[AnimalResponse])
async def list_animals(
    clinic_id: UUID = Query(..., description="ID da clínica proprietária dos animais")
) -> list[Dict[str, Any]]:
    logger.info(f"Requisição recebida para listar animais da clinic_id: {clinic_id}")
    
    try:
        # Buscar todos os animais associados à clínica
        params = {"clinic_id": f"eq.{clinic_id}"}
        
        # Obter animais usando o método _request
        animals = await supabase_admin._request(
            method="GET",
            endpoint="/rest/v1/animals",
            params=params
        )
        
        if not animals:
            logger.info(f"Nenhum animal encontrado para a clínica {clinic_id}")
            return []
            
        logger.info(f"Encontrados {len(animals)} animais para a clínica {clinic_id}")
        return animals
        
    except Exception as e:
        logger.error(f"Erro ao buscar animais da clínica {clinic_id}: {e}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_detail = f"{error_detail} - Response: {e.response.text}"
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno no servidor ao buscar animais: {error_detail}"
        )

@router.get("/{animal_id}", response_model=AnimalResponse)
async def get_animal(
    animal_id: UUID = Path(..., description="ID do animal a ser consultado"),
    clinic_id: UUID = Query(..., description="ID da clínica proprietária do animal")
) -> Dict[str, Any]:
    logger.info(f"Requisição recebida para consultar animal ID: {animal_id} da clinic_id: {clinic_id}")
    
    try:
        # Buscar animal específico associado à clínica
        params = {
            "id": f"eq.{animal_id}",
            "clinic_id": f"eq.{clinic_id}"
        }
        
        # Obter animal usando o método _request
        animal_result = await supabase_admin._request(
            method="GET",
            endpoint="/rest/v1/animals",
            params=params
        )
        
        if not animal_result or len(animal_result) == 0:
            logger.warning(f"Animal {animal_id} não encontrado ou não pertence à clínica {clinic_id}")
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence à clínica")
            
        logger.info(f"Animal {animal_id} encontrado: {animal_result[0]}")
        return animal_result[0]
        
    except HTTPException as http_exc:
        logger.error(f"Erro HTTP ao consultar animal {animal_id}: Status={http_exc.status_code}, Detalhe={http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao consultar animal {animal_id}: {e}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_detail = f"{error_detail} - Response: {e.response.text}"
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno no servidor ao consultar animal: {error_detail}"
        )

@router.post("/{animal_id}/preferences", response_model=PetPreferencesResponse)
async def create_animal_preferences(
    animal_id: UUID = Path(..., description="ID do animal"),
    preferences: PetPreferencesCreate = Body(...),
    clinic_id: UUID = Query(..., description="ID da clínica proprietária do animal")
) -> Dict[str, Any]:
    """
    Cadastra preferências alimentares para um animal
    """
    logger.info(f"Requisição para cadastrar preferências alimentares para animal {animal_id}")
    
    try:
        # Verificar se o animal existe e pertence à clínica
        existing_animal = await supabase_admin.get_by_eq(
            table="animals",
            column="id",
            value=str(animal_id),
            select="id, clinic_id"
        )
        if not existing_animal or str(existing_animal[0]['clinic_id']) != str(clinic_id):
            logger.warning(f"Animal {animal_id} não encontrado ou não pertence à clínica {clinic_id}")
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence à clínica")
        
        # Verificar se já existem preferências para este animal
        existing_preferences = await supabase_admin._request(
            method="GET",
            endpoint="/rest/v1/preferencias_pet",
            params={"animal_id": f"eq.{animal_id}"}
        )
        
        if existing_preferences and len(existing_preferences) > 0:
            logger.warning(f"Já existem preferências para o animal {animal_id}")
            raise HTTPException(
                status_code=400, 
                detail="Já existem preferências cadastradas para este animal. Use o endpoint PUT para atualizar."
            )
        
        # Preparar dados para inserção
        preferences_data = {
            "animal_id": str(animal_id),
            "gosta_de": preferences.gosta_de,
            "nao_gosta_de": preferences.nao_gosta_de
        }
        
        # Inserir preferências
        created_preferences = await supabase_admin.insert(
            table="preferencias_pet",
            data=preferences_data
        )
        
        if isinstance(created_preferences, list) and created_preferences:
            logger.info(f"Preferências criadas com sucesso: {created_preferences[0]}")
            return created_preferences[0]
        elif isinstance(created_preferences, dict):
            logger.info(f"Preferências criadas com sucesso: {created_preferences}")
            return created_preferences
        else:
            logger.error(f"Resposta inesperada ao inserir preferências: {created_preferences}")
            raise HTTPException(status_code=500, detail="Resposta inesperada do Supabase.")
            
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao cadastrar preferências: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/{animal_id}/preferences", response_model=PetPreferencesResponse)
async def get_animal_preferences(
    animal_id: UUID = Path(..., description="ID do animal"),
    clinic_id: UUID = Query(..., description="ID da clínica proprietária do animal")
) -> Dict[str, Any]:
    """
    Obtém as preferências alimentares de um animal
    """
    logger.info(f"Requisição para obter preferências alimentares do animal {animal_id}")
    
    try:
        # Verificar se o animal existe e pertence à clínica
        existing_animal = await supabase_admin.get_by_eq(
            table="animals",
            column="id",
            value=str(animal_id),
            select="id, clinic_id"
        )
        if not existing_animal or str(existing_animal[0]['clinic_id']) != str(clinic_id):
            logger.warning(f"Animal {animal_id} não encontrado ou não pertence à clínica {clinic_id}")
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence à clínica")
        
        # Buscar preferências
        preferences = await supabase_admin._request(
            method="GET",
            endpoint="/rest/v1/preferencias_pet",
            params={"animal_id": f"eq.{animal_id}"}
        )
        
        if not preferences or len(preferences) == 0:
            logger.warning(f"Preferências não encontradas para o animal {animal_id}")
            raise HTTPException(status_code=404, detail="Preferências não encontradas para este animal")
        
        logger.info(f"Preferências encontradas: {preferences[0]}")
        return preferences[0]
            
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao obter preferências: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/{animal_id}/preferences", response_model=PetPreferencesResponse)
async def update_animal_preferences(
    animal_id: UUID = Path(..., description="ID do animal"),
    preferences: PetPreferencesUpdate = Body(...),
    clinic_id: UUID = Query(..., description="ID da clínica proprietária do animal")
) -> Dict[str, Any]:
    """
    Atualiza as preferências alimentares de um animal
    """
    logger.info(f"Requisição para atualizar preferências alimentares do animal {animal_id}")
    
    try:
        # Verificar se o animal existe e pertence à clínica
        existing_animal = await supabase_admin.get_by_eq(
            table="animals",
            column="id",
            value=str(animal_id),
            select="id, clinic_id"
        )
        if not existing_animal or str(existing_animal[0]['clinic_id']) != str(clinic_id):
            logger.warning(f"Animal {animal_id} não encontrado ou não pertence à clínica {clinic_id}")
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence à clínica")
        
        # Buscar preferências existentes
        existing_preferences = await supabase_admin._request(
            method="GET",
            endpoint="/rest/v1/preferencias_pet",
            params={"animal_id": f"eq.{animal_id}"}
        )
        
        if not existing_preferences or len(existing_preferences) == 0:
            logger.warning(f"Preferências não encontradas para o animal {animal_id}")
            raise HTTPException(
                status_code=404, 
                detail="Preferências não encontradas. Use o endpoint POST para criar."
            )
        
        # Preparar dados para atualização
        preferences_data = preferences.model_dump(exclude_unset=True)
        if not preferences_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")
        
        # Atualizar preferências
        updated_preferences = await supabase_admin._request(
            method="PATCH",
            endpoint="/rest/v1/preferencias_pet",
            params={"animal_id": f"eq.{animal_id}"},
            json=preferences_data
        )
        
        # Buscar dados atualizados
        result = await supabase_admin._request(
            method="GET",
            endpoint="/rest/v1/preferencias_pet",
            params={"animal_id": f"eq.{animal_id}"}
        )
        
        logger.info(f"Preferências atualizadas: {result[0]}")
        return result[0]
            
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao atualizar preferências: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
