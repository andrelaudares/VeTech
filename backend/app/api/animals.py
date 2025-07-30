from fastapi import APIRouter, HTTPException, Depends, Query, Body, Path
from typing import Dict, Any, Annotated, Optional
from ..models.animal import (
    AnimalCreate, AnimalResponse, AnimalUpdate, 
    ClientActivationRequest, ClientActivationResponse,
    ClientStatusToggleRequest, ClientStatusToggleResponse,
    ClientInfoResponse
)
from ..models.animal_preferences import PetPreferencesCreate, PetPreferencesUpdate, PetPreferencesResponse
from ..db.supabase import supabase_admin
from uuid import UUID
import logging
import secrets
import string
from ..api.auth import get_current_user

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("", response_model=AnimalResponse)
async def create_animal(
    # Recebe os dados do animal do corpo da requisição
    animal: AnimalCreate = Body(...),
    # Adicionar dependência do usuário autenticado
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    # Obter clinic_id do usuário autenticado
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID da clínica não encontrado no token")

    logger.info(f"Requisição recebida para criar animal para clinic_id: {clinic_id}")
    logger.info(f"Dados do animal recebidos: {animal.model_dump()}")
    
    try:
        # Preparar os dados do animal para inserção
        # Garantindo que apenas os campos esperados pela tabela `animals` (com clinic_id do token) sejam enviados
        animal_data = {
            "clinic_id": str(clinic_id),  # ID da clínica logada (do token)
            "name": animal.name,
            "species": animal.species,
            "breed": animal.breed,
            "age": animal.age,
            "weight": animal.weight,
            "medical_history": animal.medical_history,
            "date_birth": animal.date_birth.isoformat() if animal.date_birth else None,
            "tutor_name": animal.tutor_name,
            "email": animal.email,
            "phone": animal.phone
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
    # Adicionar dependência do usuário autenticado
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    # Obter clinic_id do usuário autenticado
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID da clínica não encontrado no token")

    logger.info(f"Requisição recebida para atualizar animal ID: {animal_id} para clinic_id: {clinic_id}")
    logger.info(f"Dados de atualização recebidos: {animal_update.model_dump(exclude_unset=True)}")

    try:
        # 1. Verificar se o animal pertence à clínica antes de atualizar
        existing_animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        existing_animal = supabase_admin.process_response(existing_animal_response, single_item=True)
        if not existing_animal:
            logger.warning(f"Tentativa de atualizar animal {animal_id} não encontrado ou não pertencente à clínica {clinic_id}")
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence à clínica")

        # 2. Preparar os dados para atualização (apenas campos fornecidos)
        update_data = animal_update.model_dump(exclude_unset=True)

        if not update_data:
             raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        logger.info(f"Tentando atualizar animal ID: {animal_id} com dados: {update_data}")

        # 3. Atualizar o animal no banco de dados usando o método _request diretamente
        # Garantir que a atualização só ocorra se o animal_id e clinic_id (do token) corresponderem
        params = {
            "id": f"eq.{animal_id}",
            "clinic_id": f"eq.{clinic_id}" # Adiciona filtro por clinic_id
        }
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation" # Pedir para retornar o registro atualizado

        updated_animal_list_response = await supabase_admin._request(
            method="PATCH",
            endpoint=f"/rest/v1/animals",
            params=params,
            json=update_data,
            headers=headers
        )
        updated_animal_list = supabase_admin.process_response(updated_animal_list_response)


        if not updated_animal_list:
             # Se Prefer=representation falhar ou não retornar nada, tentar buscar novamente
             fallback_get_response = await supabase_admin._request("GET", f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=*")
             fallback_data = supabase_admin.process_response(fallback_get_response)
             if not fallback_data:
                 logger.error(f"Falha ao atualizar animal {animal_id}. Não encontrado após PATCH.")
                 raise HTTPException(status_code=404, detail="Animal não encontrado ou falha ao atualizar.")
             updated_animal = fallback_data[0]
        else:
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
    # Adicionar dependência do usuário autenticado
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> None:
    # Obter clinic_id do usuário autenticado
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID da clínica não encontrado no token")

    logger.info(f"Requisição recebida para deletar animal ID: {animal_id} da clinic_id: {clinic_id}")

    try:
        # 1. Verificar se o animal pertence à clínica antes de deletar (redundante com o filtro no DELETE, mas bom para log)
        existing_animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        existing_animal = supabase_admin.process_response(existing_animal_response, single_item=True)

        if not existing_animal:
            logger.warning(f"Tentativa de deletar animal {animal_id} não encontrado ou não pertencente à clínica {clinic_id}")
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence à clínica")

        # 2. Deletar o animal usando o método _request, filtrando por animal_id e clinic_id (do token)
        params = {
            "id": f"eq.{animal_id}",
            "clinic_id": f"eq.{clinic_id}" # Garante que só delete se pertencer à clínica do token
        }
        await supabase_admin._request(
            method="DELETE",
            endpoint="/rest/v1/animals",
            params=params
        )

        # 3. Verificar se realmente foi deletado (opcional)
        get_again_response = await supabase_admin._request("GET", f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id")
        if supabase_admin.process_response(get_again_response):
            logger.error(f"Erro ao deletar animal {animal_id}: ainda encontrado após DELETE.")
            raise HTTPException(status_code=500, detail="Erro interno: Falha ao deletar o animal.")


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
    # Adicionar dependência do usuário autenticado
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> list[Dict[str, Any]]:
    # Obter clinic_id do usuário autenticado
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID da clínica não encontrado no token")

    logger.info(f"Requisição recebida para listar todos os animais da clinic_id: {clinic_id}")

    try:
        # Buscar todos os animais **filtrando pela clinic_id do token**
        response = await supabase_admin._request(
            method="GET",
            endpoint=f"/rest/v1/animals?clinic_id=eq.{clinic_id}&select=*" # Adicionar filtro clinic_id
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
    animal_id: UUID = Path(..., description="ID do animal a ser consultado"),
    # Adicionar dependência do usuário autenticado
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    # Obter clinic_id do usuário autenticado
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID da clínica não encontrado no token")

    logger.info(f"Requisição recebida para consultar animal ID: {animal_id} da clinic_id: {clinic_id}")

    try:
        # Buscar animal específico pelo ID **e pela clinic_id do token**
        params = {
            "id": f"eq.{animal_id}",
            "clinic_id": f"eq.{clinic_id}", # Adicionar filtro clinic_id
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
    preferences: PetPreferencesCreate = Body(...),
    # Adicionar dependência do usuário autenticado
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Cadastra preferências alimentares para um animal.
    Verifica se o animal pertence à clínica autenticada.
    """
    # Obter clinic_id do usuário autenticado
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID da clínica não encontrado no token")

    logger.info(f"Requisição para cadastrar preferências alimentares para animal {animal_id} (clínica: {clinic_id})")

    try:
        # 1. Verificar se o animal pertence à clínica autenticada
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(animal_response):
            logger.warning(f"Animal {animal_id} não encontrado ou não pertence à clínica {clinic_id}")
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence à clínica")

        # 2. Verificar se já existem preferências para este animal
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
    animal_id: UUID = Path(..., description="ID do animal"),
    # Adicionar dependência do usuário autenticado
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Obtém as preferências alimentares de um animal.
    Verifica se o animal pertence à clínica autenticada.
    """
    # Obter clinic_id do usuário autenticado
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID da clínica não encontrado no token")

    logger.info(f"Requisição para obter preferências alimentares do animal {animal_id} (clínica: {clinic_id})")

    try:
        # 1. Verificar se o animal pertence à clínica autenticada
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(animal_response):
            logger.warning(f"Animal {animal_id} não encontrado ou não pertence à clínica {clinic_id}")
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence à clínica")

        # 2. Buscar preferências
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
    preferences: PetPreferencesUpdate = Body(...),
    # Adicionar dependência do usuário autenticado
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza as preferências alimentares de um animal (parcialmente).
    Verifica se o animal pertence à clínica autenticada.
    """
    # Obter clinic_id do usuário autenticado
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado ou ID da clínica não encontrado no token")

    logger.info(f"Requisição para atualizar preferências alimentares do animal {animal_id} (clínica: {clinic_id})")

    try:
        # 1. Verificar se o animal pertence à clínica autenticada
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id"
        )
        if not supabase_admin.process_response(animal_response):
            logger.warning(f"Animal {animal_id} não encontrado ou não pertence à clínica {clinic_id}")
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence à clínica")

        # 2. Preparar dados para atualização (apenas campos não nulos enviados)
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
        updated_data_list = supabase_admin.process_response(update_response)


        if updated_data_list:
            updated_data = updated_data_list[0]
            logger.info(f"Preferências do animal {animal_id} atualizadas com sucesso: {updated_data}")
            return updated_data
        else:
             # Se a atualização não retornou nada (pode acontecer se não houver preferências)
             # Verificar se as preferências existem para dar um erro 404 mais específico
            prefs_exist_response = await supabase_admin._request("GET", "/rest/v1/preferencias_pet", params={"animal_id": f"eq.{animal_id}", "select": "id"})
            if not supabase_admin.process_response(prefs_exist_response):
                 raise HTTPException(status_code=404, detail="Preferências não encontradas para este animal. Use POST para criar.")
            else:
                 # Se as preferências existem mas o PATCH não retornou, pode ser um erro interno ou de permissão
                 logger.error(f"Falha ao atualizar preferências para o animal {animal_id}. Resposta do PATCH: {update_response}")
                 raise HTTPException(status_code=500, detail="Erro ao atualizar preferências. Falha ao obter dados atualizados.")


    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao atualizar preferências do animal {animal_id}: {str(e)}", exc_info=True)
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_detail = f"{error_detail} - Response: {e.response.text}"
        raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar preferências: {error_detail}")


# Função auxiliar para gerar senha temporária
def generate_temporary_password(length: int = 8) -> str:
    """Gera uma senha temporária segura"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


@router.post("/{animal_id}/activate-client", response_model=ClientActivationResponse)
async def activate_client_access(
    animal_id: UUID = Path(..., description="ID do animal"),
    activation_data: ClientActivationRequest = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> ClientActivationResponse:
    """
    Ativa o acesso do cliente/tutor para um animal específico.
    Cria usuário em auth.users e vincula ao animal.
    """
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    logger.info(f"Ativando acesso do cliente para animal {animal_id} (clínica: {clinic_id})")

    try:
        # 1. Verificar se o animal pertence à clínica
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id,name,email,tutor_user_id"
        )
        animal_data = supabase_admin.process_response(animal_response, single_item=True)
        
        if not animal_data:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence à clínica")

        # 2. Verificar se já existe usuário vinculado
        if animal_data.get("tutor_user_id"):
            raise HTTPException(status_code=400, detail="Animal já possui tutor ativado. Use a rota de atualização.")

        # 3. Verificar se email já existe em auth.users
        try:
            # Usar uma consulta SQL direta para verificar se o email existe
            
            check_email_response = await supabase_admin._request(
                "GET",
                f"/rest/v1/rpc/check_user_email_exists",
                params={"email_to_check": activation_data.email},
                headers=supabase_admin.admin_headers
            )
            
            # Se a função RPC não existir, usar método alternativo
            if check_email_response.status_code == 404:
                # Método alternativo: consultar diretamente a view auth.users
                existing_user_response = await supabase_admin._request(
                    "GET",
                    "/rest/v1/auth_users",
                    params={"email": f"eq.{activation_data.email}", "select": "email"},
                    headers=supabase_admin.admin_headers
                )
                
                existing_users = supabase_admin.process_response(existing_user_response)
                if existing_users and len(existing_users) > 0:
                    raise HTTPException(status_code=400, detail="Email já está em uso por outro usuário")
            else:
                email_exists = supabase_admin.process_response(check_email_response)
                if email_exists:
                    raise HTTPException(status_code=400, detail="Email já está em uso por outro usuário")
                    
        except HTTPException as http_exc:
            if http_exc.status_code == 400:
                raise http_exc
            # Se der erro na consulta, continuar (pode ser que não tenha usuários ainda)
            logger.warning(f"Erro ao verificar usuários existentes: {http_exc.detail}")
        except Exception as e:
            # Se der erro na consulta, continuar (pode ser que não tenha usuários ainda)
            logger.warning(f"Erro ao verificar usuários existentes: {str(e)}")

        # 4. Gerar senha se necessário
        password = activation_data.password
        temporary_password = None
        
        if activation_data.generate_password or not password:
            temporary_password = generate_temporary_password()
            password = temporary_password
            logger.info(f"Senha temporária gerada para usuário {activation_data.email}")

        # 5. Criar usuário em auth.users usando Admin API
        user_data = {
            "email": activation_data.email,
            "password": password,
            "email_confirm": True,  # Confirma email automaticamente
            "user_metadata": {
                "name": activation_data.tutor_name,
                "phone": activation_data.phone,
                "role": "tutor",
                "clinic_id": str(clinic_id),
                "animal_id": str(animal_id),
                "temporary_password": bool(temporary_password)
            }
        }

        create_user_response = await supabase_admin._request(
            method="POST",
            endpoint="/auth/v1/admin/users",
            json=user_data,
            headers=supabase_admin.admin_headers
        )

        created_user = supabase_admin.process_response(create_user_response, single_item=True)
        if not created_user or not created_user.get("id"):
            raise HTTPException(status_code=500, detail="Falha ao criar usuário no sistema de autenticação")

        user_id = created_user["id"]
        logger.info(f"Usuário criado com sucesso: {user_id}")

        # 6. Atualizar dados do animal com informações do tutor e vinculação
        update_data = {
            "tutor_name": activation_data.tutor_name,
            "email": activation_data.email,
            "phone": activation_data.phone,
            "tutor_user_id": user_id,
            "client_active": True,
            "client_activated_at": "now()"
        }

        # Atualizar o animal
        update_response = await supabase_admin._request(
            method="PATCH",
            endpoint="/rest/v1/animals",
            params={"id": f"eq.{animal_id}", "clinic_id": f"eq.{clinic_id}"},
            json=update_data,
            headers={**supabase_admin.admin_headers, "Prefer": "return=representation"}
        )

        updated_animal = supabase_admin.process_response(update_response)
        if not updated_animal:
            # Se falhou ao atualizar animal, tentar deletar o usuário criado
            try:
                await supabase_admin._request(
                    method="DELETE",
                    endpoint=f"/auth/v1/admin/users/{user_id}",
                    headers=supabase_admin.admin_headers
                )
            except Exception as cleanup_error:
                logger.error(f"Erro ao limpar usuário após falha: {cleanup_error}")
            
            raise HTTPException(status_code=500, detail="Falha ao vincular tutor ao animal")

        logger.info(f"Acesso do cliente ativado com sucesso para animal {animal_id}")

        return ClientActivationResponse(
            success=True,
            message="Acesso do cliente ativado com sucesso",
            user_id=user_id,
            login_url="/tutor/login",
            temporary_password=temporary_password
        )

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao ativar acesso do cliente para animal {animal_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.patch("/{animal_id}/client-status", response_model=ClientStatusToggleResponse)
async def toggle_client_status(
    animal_id: UUID = Path(..., description="ID do animal"),
    status_data: ClientStatusToggleRequest = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> ClientStatusToggleResponse:
    """
    Ativa ou desativa o acesso do cliente/tutor.
    Não remove o usuário de auth.users, apenas controla o acesso.
    """
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    logger.info(f"Alterando status do cliente para animal {animal_id}: {status_data.active}")

    try:
        # Verificar se o animal pertence à clínica
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id,client_active,tutor_user_id"
        )
        animal_data = supabase_admin.process_response(animal_response, single_item=True)
        
        if not animal_data:
            raise HTTPException(status_code=404, detail="Animal não encontrado")

        if not animal_data.get("tutor_user_id"):
            raise HTTPException(status_code=400, detail="Animal não possui tutor cadastrado")

        # Atualizar status
        update_data = {"client_active": status_data.active}
        if status_data.active and not animal_data.get("client_active"):
            update_data["client_activated_at"] = "now()"

        update_response = await supabase_admin._request(
            method="PATCH",
            endpoint="/rest/v1/animals",
            params={"id": f"eq.{animal_id}", "clinic_id": f"eq.{clinic_id}"},
            json=update_data,
            headers={**supabase_admin.admin_headers, "Prefer": "return=representation"}
        )

        updated_animal = supabase_admin.process_response(update_response)
        if not updated_animal:
            raise HTTPException(status_code=500, detail="Falha ao atualizar status")

        return ClientStatusToggleResponse(
            success=True,
            message=f"Acesso do cliente {'ativado' if status_data.active else 'desativado'} com sucesso",
            client_active=status_data.active
        )

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao alterar status do cliente: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/{animal_id}/client-info", response_model=ClientInfoResponse)
async def get_client_info(
    animal_id: UUID = Path(..., description="ID do animal"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> ClientInfoResponse:
    """
    Obtém informações do cliente/tutor de um animal.
    """
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    try:
        # Buscar informações do cliente
        response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=tutor_name,email,phone,tutor_user_id,client_active,client_activated_at,client_last_login"
        )
        
        animal_data = supabase_admin.process_response(response, single_item=True)
        if not animal_data:
            raise HTTPException(status_code=404, detail="Animal não encontrado")

        return ClientInfoResponse(
            tutor_name=animal_data.get("tutor_name"),
            email=animal_data.get("email"),
            phone=animal_data.get("phone"),
            tutor_user_id=animal_data.get("tutor_user_id"),
            client_active=animal_data.get("client_active", False),
            client_activated_at=animal_data.get("client_activated_at"),
            client_last_login=animal_data.get("client_last_login")
        )

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao obter informações do cliente: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.patch("/{animal_id}/update-client", response_model=ClientActivationResponse)
async def update_client_info(
    animal_id: UUID = Path(..., description="ID do animal"),
    activation_data: ClientActivationRequest = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> ClientActivationResponse:
    """
    Atualiza informações do cliente/tutor existente.
    Atualiza tanto auth.users quanto a tabela animals.
    """
    clinic_id = current_user.get("id")
    if not clinic_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    logger.info(f"Atualizando informações do cliente para animal {animal_id}")

    try:
        # 1. Verificar se o animal pertence à clínica e tem tutor
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}&select=id,tutor_user_id,email"
        )
        animal_data = supabase_admin.process_response(animal_response, single_item=True)
        
        if not animal_data:
            raise HTTPException(status_code=404, detail="Animal não encontrado")

        tutor_user_id = animal_data.get("tutor_user_id")
        if not tutor_user_id:
            raise HTTPException(status_code=400, detail="Animal não possui tutor cadastrado. Use a rota de ativação.")

        # 2. Atualizar usuário em auth.users
        user_update_data = {
            "email": activation_data.email,
            "user_metadata": {
                "name": activation_data.tutor_name,
                "phone": activation_data.phone,
                "role": "tutor",
                "clinic_id": str(clinic_id),
                "animal_id": str(animal_id)
            }
        }

        # Se nova senha foi fornecida, atualizar
        if activation_data.password:
            user_update_data["password"] = activation_data.password

        update_user_response = await supabase_admin._request(
            method="PUT",
            endpoint=f"/auth/v1/admin/users/{tutor_user_id}",
            json=user_update_data,
            headers=supabase_admin.admin_headers
        )

        updated_user = supabase_admin.process_response(update_user_response, single_item=True)
        if not updated_user:
            raise HTTPException(status_code=500, detail="Falha ao atualizar usuário")

        # 3. Atualizar dados do animal
        animal_update_data = {
            "tutor_name": activation_data.tutor_name,
            "email": activation_data.email,
            "phone": activation_data.phone
        }

        update_response = await supabase_admin._request(
            method="PATCH",
            endpoint="/rest/v1/animals",
            params={"id": f"eq.{animal_id}", "clinic_id": f"eq.{clinic_id}"},
            json=animal_update_data,
            headers={**supabase_admin.admin_headers, "Prefer": "return=representation"}
        )

        updated_animal = supabase_admin.process_response(update_response)
        if not updated_animal:
            raise HTTPException(status_code=500, detail="Falha ao atualizar dados do animal")

        logger.info(f"Informações do cliente atualizadas com sucesso para animal {animal_id}")

        return ClientActivationResponse(
            success=True,
            message="Informações do cliente atualizadas com sucesso",
            user_id=tutor_user_id,
            login_url="/tutor/login"
        )

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Erro ao atualizar informações do cliente: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
