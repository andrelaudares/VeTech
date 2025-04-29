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
    animal_update: AnimalUpdate = Body(...)
) -> Dict[str, Any]:
    logger.info(f"Requisição recebida para atualizar animal ID: {animal_id}")
    logger.info(f"Dados de atualização recebidos: {animal_update.model_dump(exclude_unset=True)}")

    try:
        # Preparar os dados para atualização (apenas campos fornecidos)
        update_data = animal_update.model_dump(exclude_unset=True)

        if not update_data:
             raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        logger.info(f"Tentando atualizar animal ID: {animal_id} com dados: {update_data}")

        # Atualizar o animal no banco de dados usando o método _request diretamente
        # O método `update` do Supabase requer filtros e dados
        params = {
            "id": f"eq.{animal_id}"
        }
        updated_animal_list = await supabase_admin._request(
            method="PATCH",
            endpoint=f"/rest/v1/animals",
            params=params,
            json=update_data
        )

        if not updated_animal_list:
            logger.error(f"Falha ao atualizar animal {animal_id}. Resposta vazia do Supabase ou animal não encontrado.")
            raise HTTPException(status_code=404, detail="Animal não encontrado ou falha ao atualizar.")

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
) -> list[Dict[str, Any]]:
    logger.info(f"Requisição recebida para listar todos os animais")

    try:
        # Buscar todos os animais sem filtro de clínica
        response = await supabase_admin._request(
            method="GET",
            endpoint="/rest/v1/animals"
        )

        # A resposta direta do _request pode ser a lista ou um dict {'data': [...]}
        # Vamos garantir que retornamos a lista
        animals_list = []
        if isinstance(response, list):
            animals_list = response
        elif isinstance(response, dict) and 'data' in response and isinstance(response['data'], list):
            # Caso comum onde Supabase retorna {'data': [...]}
            animals_list = response['data']
        # Adicione outras verificações se a estrutura da resposta puder variar mais

        if not animals_list:
            logger.info(f"Nenhum animal encontrado no banco de dados.")
            return []

        logger.info(f"Encontrados {len(animals_list)} animais.")
        return animals_list # Retorna a lista diretamente

    except Exception as e:
        logger.error(f"Erro ao buscar animais: {e}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_detail = f"{error_detail} - Response: {e.response.text}"
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno no servidor ao buscar animais: {error_detail}"
        )

@router.get("/{animal_id}", response_model=AnimalResponse)
async def get_animal(
    animal_id: UUID = Path(..., description="ID do animal a ser consultado")
) -> Dict[str, Any]:
    logger.info(f"Requisição recebida para consultar animal ID: {animal_id}")

    try:
        # Buscar animal específico pelo ID
        params = {
            "id": f"eq.{animal_id}",
            "select": "*" # Garante que todos os campos sejam retornados
        }

        # Obter animal usando o método _request
        response = await supabase_admin._request(
            method="GET",
            endpoint="/rest/v1/animals",
            params=params
        )

        # Verificar a estrutura da resposta e extrair o animal
        animal_data = None
        if isinstance(response, list) and len(response) > 0:
             # Caso _request retorne a lista diretamente
            animal_data = response[0]
        elif isinstance(response, dict) and 'data' in response and isinstance(response['data'], list):
            # Caso comum onde Supabase retorna {'data': [...]}
            animal_list = response['data']
            if animal_list: # Verifica se a lista não está vazia
                animal_data = animal_list[0]

        if animal_data:
            logger.info(f"Animal {animal_id} encontrado: {animal_data}")
            return animal_data # Retorna o dicionário do animal
        else:
            logger.warning(f"Animal {animal_id} não encontrado ou resposta inesperada: {response}")
            raise HTTPException(status_code=404, detail="Animal não encontrado")

    except HTTPException as http_exc:
        # Se já for um erro HTTP (como o 404 acima), apenas relança
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
    preferences: PetPreferencesCreate = Body(...)
) -> Dict[str, Any]:
    """
    Cadastra preferências alimentares para um animal
    """
    logger.info(f"Requisição para cadastrar preferências alimentares para animal {animal_id}")

    try:
        # Verificar se já existem preferências para este animal
        existing_preferences_response = await supabase_admin._request(
            method="GET",
            endpoint="/rest/v1/preferencias_pet",
            params={"animal_id": f"eq.{animal_id}", "select": "id"} # Busca apenas o ID para verificar existência
        )

        # Tratar a resposta para verificar se a lista de preferências está realmente vazia
        preferences_exist = False
        if isinstance(existing_preferences_response, list) and len(existing_preferences_response) > 0:
            preferences_exist = True
        elif isinstance(existing_preferences_response, dict) and 'data' in existing_preferences_response and isinstance(existing_preferences_response['data'], list) and len(existing_preferences_response['data']) > 0:
            preferences_exist = True

        if preferences_exist:
            logger.warning(f"Já existem preferências para o animal {animal_id}")
            raise HTTPException(
                status_code=400,
                detail="Já existem preferências cadastradas para este animal. Use o endpoint PUT ou PATCH para atualizar."
            )

        # Preparar dados para inserção
        preferences_data = {
            "animal_id": str(animal_id),
            "gosta_de": preferences.gosta_de,
            "nao_gosta_de": preferences.nao_gosta_de
        }

        # Inserir preferências
        # A função insert agora retorna o objeto criado ou lança exceção
        created_preferences = await supabase_admin.insert(
            table="preferencias_pet",
            data=preferences_data
        )

        # A função insert do supabase_admin agora deve retornar o dict diretamente ou lançar erro
        if isinstance(created_preferences, dict):
            logger.info(f"Preferências criadas com sucesso: {created_preferences}")
            return created_preferences
        else:
             # Se chegou aqui, algo inesperado aconteceu no insert
            logger.error(f"Resposta inesperada do Supabase ao inserir preferências: {created_preferences}")
            raise HTTPException(status_code=500, detail="Resposta inesperada do Supabase ao criar preferências.")

    except HTTPException as http_exc:
        # Repassa exceções HTTP conhecidas (como 400 ou 404)
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao cadastrar preferências para animal {animal_id}: {str(e)}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_detail = f"{error_detail} - Response: {e.response.text}"
        raise HTTPException(status_code=500, detail=f"Erro interno ao cadastrar preferências: {error_detail}")

@router.get("/{animal_id}/preferences", response_model=PetPreferencesResponse)
async def get_animal_preferences(
    animal_id: UUID = Path(..., description="ID do animal")
) -> Dict[str, Any]:
    """
    Obtém as preferências alimentares de um animal
    """
    logger.info(f"Requisição para obter preferências alimentares do animal {animal_id}")

    try:
        # Buscar preferências
        response = await supabase_admin._request(
            method="GET",
            endpoint="/rest/v1/preferencias_pet",
            params={"animal_id": f"eq.{animal_id}", "select": "*"}
        )

        # Tratar a resposta
        preferences_data = None
        if isinstance(response, list) and len(response) > 0:
            preferences_data = response[0]
        elif isinstance(response, dict) and 'data' in response and isinstance(response['data'], list) and len(response['data']) > 0:
             preferences_data = response['data'][0]

        if preferences_data:
            logger.info(f"Preferências encontradas para animal {animal_id}: {preferences_data}")
            return preferences_data
        else:
            logger.warning(f"Preferências não encontradas para o animal {animal_id}. Resposta: {response}")
            raise HTTPException(status_code=404, detail="Preferências não encontradas para este animal")

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao obter preferências do animal {animal_id}: {str(e)}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_detail = f"{error_detail} - Response: {e.response.text}"
        raise HTTPException(status_code=500, detail=f"Erro interno ao obter preferências: {error_detail}")

@router.patch("/{animal_id}/preferences", response_model=PetPreferencesResponse)
async def update_animal_preferences(
    animal_id: UUID = Path(..., description="ID do animal"),
    preferences: PetPreferencesUpdate = Body(...)
) -> Dict[str, Any]:
    """
    Atualiza as preferências alimentares de um animal (parcialmente)
    """
    logger.info(f"Requisição para atualizar preferências alimentares do animal {animal_id}")

    try:
        # Preparar dados para atualização (apenas campos não nulos enviados)
        preferences_data = preferences.model_dump(exclude_unset=True)
        if not preferences_data:
            logger.info(f"Nenhum dado fornecido para atualização de preferências do animal {animal_id}")
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        # Verificar se existem preferências para atualizar
        # Não precisamos buscar antes com PATCH, ele falhará se não encontrar (ou não fará nada)

        # Atualizar preferências usando PATCH
        # O método _request com PATCH/POST/PUT no Supabase costuma retornar os dados alterados em uma lista
        update_response = await supabase_admin._request(
            method="PATCH",
            endpoint="/rest/v1/preferencias_pet",
            params={"animal_id": f"eq.{animal_id}"}, # Filtro
            json=preferences_data # Dados a atualizar
        )

        # Tratar a resposta do PATCH
        updated_data = None
        if isinstance(update_response, list) and len(update_response) > 0:
            updated_data = update_response[0]
        elif isinstance(update_response, dict) and 'data' in update_response and isinstance(update_response['data'], list) and len(update_response['data']) > 0:
             updated_data = update_response['data'][0]

        if updated_data:
            logger.info(f"Preferências do animal {animal_id} atualizadas com sucesso: {updated_data}")
            return updated_data
        else:
             # Isso pode ocorrer se o animal_id não existir na tabela de preferências
            logger.warning(f"Falha ao atualizar preferências para o animal {animal_id}. Preferências podem não existir. Resposta: {update_response}")
            # Verificar se o animal existe na tabela 'animals' para dar um erro mais preciso
            animal_exists_response = await supabase_admin._request("GET", "/rest/v1/animals", params={"id": f"eq.{animal_id}", "select": "id"})
            animal_exists = (isinstance(animal_exists_response, list) and len(animal_exists_response) > 0) or \
                            (isinstance(animal_exists_response, dict) and 'data' in animal_exists_response and len(animal_exists_response.get('data', [])) > 0)
            if not animal_exists:
                 raise HTTPException(status_code=404, detail=f"Animal com ID {animal_id} não encontrado.")
            else:
                raise HTTPException(status_code=404, detail="Preferências não encontradas para este animal. Use POST para criar.")

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao atualizar preferências do animal {animal_id}: {str(e)}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_detail = f"{error_detail} - Response: {e.response.text}"
        raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar preferências: {error_detail}")
