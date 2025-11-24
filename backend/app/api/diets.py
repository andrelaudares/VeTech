from fastapi import APIRouter, HTTPException, Depends, Path
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging

from ..models.diet import (
    DietCreate, DietUpdate, DietResponse,
    RestrictedFoodCreate, RestrictedFoodUpdate, RestrictedFoodResponse,
    DietProgressCreate, DietProgressUpdate, DietProgressResponse,
    AlimentoBaseCreate, AlimentoBaseUpdate, AlimentoBaseResponse
)
from ..db.supabase import supabase_admin
from ..api.auth import get_current_user

# Configuração básica de logging para este módulo
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Rotas para Dietas
@router.post("/animals/{animal_id}/diets", response_model=DietResponse)
async def create_diet(
    animal_id: UUID,
    diet: DietCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Cria um plano de dieta para um animal.
    """
    try:
        # Verificar se o animal pertence à clínica
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Verificar se o animal existe e pertence à clínica
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}"
        )
        
        animal_data = supabase_admin.process_response(animal_response)
        if not animal_data:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")
        
        # Criar a dieta
        diet_data = {
            "animal_id": str(animal_id),
            "clinic_id": current_user["clinic_id"],
            "nome": diet.nome,
            "tipo": diet.tipo,
            "objetivo": diet.objetivo,
            "data_inicio": diet.data_inicio.isoformat(),
            "data_fim": diet.data_fim.isoformat() if diet.data_fim else None,
            "status": diet.status,
            "refeicoes_por_dia": diet.refeicoes_por_dia,
            "calorias_totais_dia": diet.calorias_totais_dia,
            "valor_mensal_estimado": diet.valor_mensal_estimado,
            "alimento_id": diet.alimento_id,
            "quantidade_gramas": diet.quantidade_gramas,
            "horario": diet.horario
        }
        
        # Adicionando cabeçalho Prefer para retornar representação
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"
        
        diet_response = await supabase_admin._request(
            "POST",
            "/rest/v1/dietas",
            json=diet_data,
            headers=headers
        )
        
        created_diet = supabase_admin.process_response(diet_response, single_item=True)
        if not created_diet:
            raise HTTPException(status_code=500, detail="Erro ao criar dieta: dados não retornados")
        
        return created_diet
        
    except Exception as e:
        print(f"Erro ao criar dieta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar dieta: {str(e)}")

@router.get("/animals/{animal_id}/diets", response_model=List[DietResponse])
async def list_diets(
    animal_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Lista todas as dietas de um animal.
    """
    try:
        # Verificar se o animal pertence à clínica
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o animal existe e pertence à clínica
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}"
        )
        
        animal_data = supabase_admin.process_response(animal_response)
        if not animal_data:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")
            
        # Buscar dietas do animal
        diets_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?animal_id=eq.{animal_id}&clinic_id=eq.{clinic_id}"
        )
        
        diets = supabase_admin.process_response(diets_response)
        if not diets:
            # Se não houver dietas, retornar uma lista vazia
            return []
        
        return diets
        
    except Exception as e:
        print(f"Erro ao listar dietas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar dietas: {str(e)}")

@router.get("/diets/{diet_id}", response_model=DietResponse)
async def get_diet(
    diet_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Obtém detalhes de uma dieta específica.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Buscar a dieta
        diet_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?id=eq.{diet_id}&clinic_id=eq.{clinic_id}"
        )
        
        diets = supabase_admin.process_response(diet_response)
        if not diets:
            raise HTTPException(status_code=404, detail="Dieta não encontrada ou não pertence a esta clínica")
            
        diet = diets[0]
        return diet
        
    except Exception as e:
        print(f"Erro ao obter dieta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter dieta: {str(e)}")

@router.put("/diets/{diet_id}", response_model=DietResponse)
async def update_diet(
    diet_id: UUID,
    diet_update: DietUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza uma dieta existente.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se a dieta existe e pertence à clínica
        diet_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?id=eq.{diet_id}&clinic_id=eq.{clinic_id}"
        )
        
        diets = supabase_admin.process_response(diet_response)
        if not diets:
            raise HTTPException(status_code=404, detail="Dieta não encontrada ou não pertence a esta clínica")
            
        # Preparar dados para atualização (apenas campos não nulos)
        update_data = {}
        for field, value in diet_update.dict(exclude_unset=True).items():
            if value is not None:
                if field == 'data_inicio' or field == 'data_fim':
                    update_data[field] = value.isoformat()
                else:
                    update_data[field] = value
        
        # Se não há dados para atualizar, retornar erro
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")
        
        # Adicionando cabeçalho Prefer para retornar representação
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"
        
        # Atualizar a dieta
        updated_response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/dietas?id=eq.{diet_id}",
            json=update_data,
            headers=headers
        )
        
        # Se a resposta contiver dados, use-os diretamente
        updated_diet = supabase_admin.process_response(updated_response, single_item=True)
        
        # Se não houver dados retornados, buscar a dieta atualizada
        if not updated_diet:
            updated_diet_response = await supabase_admin._request(
                "GET",
                f"/rest/v1/dietas?id=eq.{diet_id}"
            )
            
            updated_diet = supabase_admin.process_response(updated_diet_response, single_item=True)
            if not updated_diet:
                raise HTTPException(status_code=404, detail="Dieta não encontrada após atualização")
        
        return updated_diet
        
    except Exception as e:
        print(f"Erro ao atualizar dieta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar dieta: {str(e)}")

@router.delete("/diets/{diet_id}")
async def delete_diet(
    diet_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Remove uma dieta do sistema.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se a dieta existe e pertence à clínica
        diet_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?id=eq.{diet_id}&clinic_id=eq.{clinic_id}"
        )
        
        diets = supabase_admin.process_response(diet_response)
        if not diets:
            raise HTTPException(status_code=404, detail="Dieta não encontrada ou não pertence a esta clínica")
            
        # Remover a dieta
        await supabase_admin._request(
            "DELETE",
            f"/rest/v1/dietas?id=eq.{diet_id}"
        )
        
        return {"message": "Dieta removida com sucesso"}
        
    except Exception as e:
        print(f"Erro ao remover dieta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao remover dieta: {str(e)}")

# Fim das rotas de dietas





# Rotas para Alimentos a Evitar
@router.post("/animals/{animal_id}/restricted-foods", response_model=RestrictedFoodResponse)
async def create_restricted_food(
    animal_id: UUID,
    food: RestrictedFoodCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Adiciona um alimento à lista de alimentos restritos para um animal.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o animal existe e pertence à clínica
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}"
        )
        
        animals = supabase_admin.process_response(animal_response)
        if not animals:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")
        
        # Criar alimento restrito
        food_data = {
            "animal_id": str(animal_id),
            "clinic_id": str(clinic_id),
            "nome": food.nome,
            "motivo": food.motivo
        }
        
        # Adicionando cabeçalho Prefer para retornar representação
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"
        
        try:
            # Primeiro, tente com 'name'
            foods_response = await supabase_admin._request(
                "POST",
                "/rest/v1/alimentos_evitar",
                json=food_data,
                headers=headers
            )
            
            foods = supabase_admin.process_response(foods_response, single_item=True)
            if not foods:
                # Verificar se a resposta contém erro específico do Supabase (ex: violação de constraint)
                error_detail = supabase_admin.extract_error_detail(foods_response)
                error_msg = f"Erro ao criar registro de alimento a evitar: resposta vazia ou inválida do Supabase. {error_detail}"
                logger.error(error_msg) # Usar logger para detalhes
                raise HTTPException(status_code=500, detail="Erro ao criar registro de alimento a evitar.")
                
        except Exception as post_error:
            # Log detalhado do erro original
            logger.error(f"Erro ao tentar inserir em alimentos_evitar: {str(post_error)}", exc_info=True)
            # Tentar extrair mais detalhes se for um erro HTTP do Supabase
            detail = str(post_error)
            if hasattr(post_error, 'response') and hasattr(post_error.response, 'text'):
                 detail = f"{detail} - Supabase Response: {post_error.response.text}"

            raise HTTPException(status_code=500, detail=f"Erro interno ao criar alimento a evitar: {detail}")
            
        logger.info(f"Alimento a evitar criado com sucesso: {foods}") # Usar logger
        return foods
        
    except HTTPException as http_exc: # Capturar HTTPException explicitamente para repassar
        raise http_exc
    except Exception as e:
        # Log detalhado do erro
        logger.error(f"Erro inesperado em create_restricted_food: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor ao criar alimento a evitar: {str(e)}")

@router.get("/animals/{animal_id}/restricted-foods", response_model=List[RestrictedFoodResponse])
async def list_restricted_foods(
    animal_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Lista todos os alimentos que o pet deve evitar.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o animal existe e pertence à clínica
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}"
        )
        
        animals = supabase_admin.process_response(animal_response)
        if not animals:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")
            
        # Buscar alimentos a evitar
        foods_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/alimentos_evitar?animal_id=eq.{animal_id}"
        )
        
        foods = supabase_admin.process_response(foods_response)
        return foods
        
    except Exception as e:
        print(f"Erro ao listar alimentos a evitar: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar alimentos a evitar: {str(e)}")

@router.put("/animals/{animal_id}/restricted-foods/{food_id}", response_model=RestrictedFoodResponse)
async def update_restricted_food(
    animal_id: UUID,
    food_id: UUID,
    food: RestrictedFoodUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza um alimento na lista de alimentos restritos para um animal.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o animal existe e pertence à clínica
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}"
        )
        
        animals = supabase_admin.process_response(animal_response)
        if not animals:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")
            
        # Verificar se o alimento existe e pertence ao animal
        food_response = await supabase_admin._request(
            "GET", 
            f"/rest/v1/alimentos_evitar?id=eq.{food_id}&animal_id=eq.{animal_id}"
        )
        
        existing_food = supabase_admin.process_response(food_response)
        if not existing_food:
            raise HTTPException(
                status_code=404, 
                detail="Alimento restrito não encontrado ou não pertence a este animal"
            )
            
        # Atualizar o alimento
        food_data = {}
        if food.nome is not None:
            food_data["nome"] = food.nome
        if food.motivo is not None:
            food_data["motivo"] = food.motivo
            
        if not food_data:
            raise HTTPException(
                status_code=400, 
                detail="Nenhum dado fornecido para atualização"
            )
            
        # Adicionando cabeçalho Prefer para retornar representação
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"
        
        food_response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/alimentos_evitar?id=eq.{food_id}",
            json=food_data,
            headers=headers
        )
        
        foods = supabase_admin.process_response(food_response, single_item=True)
        if not foods:
            raise HTTPException(
                status_code=500, 
                detail="Erro ao atualizar registro de alimento a evitar"
            )
            
        return foods
        
    except Exception as e:
        print(f"Erro ao atualizar alimento a evitar: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao atualizar alimento a evitar: {str(e)}"
        )

@router.delete("/animals/{animal_id}/restricted-foods/{food_id}", response_model=RestrictedFoodResponse)
async def delete_restricted_food(
    animal_id: UUID,
    food_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Remove um alimento da lista de alimentos restritos para um animal.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o animal existe e pertence à clínica
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}"
        )
        
        animals = supabase_admin.process_response(animal_response)
        if not animals:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")
            
        # Verificar se o alimento existe e pertence ao animal
        food_response = await supabase_admin._request(
            "GET", 
            f"/rest/v1/alimentos_evitar?id=eq.{food_id}&animal_id=eq.{animal_id}"
        )
        
        existing_food = supabase_admin.process_response(food_response)
        if not existing_food:
            raise HTTPException(
                status_code=404, 
                detail="Alimento restrito não encontrado ou não pertence a este animal"
            )
            
        # Adicionando cabeçalho Prefer para retornar representação
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"
        
        # Excluir o alimento
        food_response = await supabase_admin._request(
            "DELETE",
            f"/rest/v1/alimentos_evitar?id=eq.{food_id}",
            headers=headers
        )
        
        if not food_response:
            # Verificar se o alimento ainda existe após a tentativa de exclusão
            check_response = await supabase_admin._request(
                "GET",
                f"/rest/v1/alimentos_evitar?id=eq.{food_id}",
                headers=supabase_admin.admin_headers
            )
            
            if supabase_admin.process_response(check_response):
                raise HTTPException(
                    status_code=500, 
                    detail="Falha ao excluir o alimento restrito"
                )
        
        # Retornar os dados do alimento que foi excluído
        return existing_food[0]
        
    except Exception as e:
        print(f"Erro ao excluir alimento a evitar: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao excluir alimento a evitar: {str(e)}"
        )

# Rotas para Alimentos Base
# CRUD para Alimentos Base
@router.post("/alimentos-base", response_model=AlimentoBaseResponse, status_code=201)
async def create_alimento_base(
    alimento: AlimentoBaseCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Cria um novo alimento base.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o usuário tem permissão (apenas administradores ou agentes de IA)
        user_role = current_user.get("role")
        if user_role not in ["admin", "ai_agent"]:
            raise HTTPException(status_code=403, detail="Sem permissão para criar alimentos base")
            
        # Preparar dados para criação
        alimento_data = alimento.dict()
        
        # Adicionando cabeçalho Prefer para retornar representação
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"
        
        # Criar o alimento base
        alimento_response = await supabase_admin._request(
            "POST",
            "/rest/v1/alimentos_base",
            json=alimento_data,
            headers=headers
        )
        
        created_alimento = supabase_admin.process_response(alimento_response, single_item=True)
        if not created_alimento:
            raise HTTPException(status_code=500, detail="Erro ao criar alimento base: dados não retornados")
        
        return created_alimento
        
    except Exception as e:
        print(f"Erro ao criar alimento base: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar alimento base: {str(e)}")

@router.get("/alimentos-base", response_model=List[AlimentoBaseResponse])
async def get_alimentos_base(
    nome: Optional[str] = None,
    tipo: Optional[str] = None,
    especie_destino: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Lista todos os alimentos base disponíveis para dietas.
    Permite filtrar por nome, tipo e espécie destino.
    """
    try:
        # Verificar se o usuário está autenticado
        # Guardar contra current_user None/malformado para evitar 500
        if not isinstance(current_user, dict):
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Construir a query com os filtros
        query = "/rest/v1/alimentos_base?"
        filters = []
        
        if nome:
            filters.append(f"nome=ilike.%{nome}%")
        if tipo:
            filters.append(f"tipo=eq.{tipo}")
        if especie_destino:
            filters.append(f"especie_destino=eq.{especie_destino}")
            
        if filters:
            query += "&".join(filters)
            
        # Adicionar ordenação
        if query.endswith("?"):
            query += "order=nome.asc"
        else:
            query += "&order=nome.asc"
        
        # Buscar os alimentos base
        alimentos_response = await supabase_admin._request(
            "GET",
            query
        )
        
        alimentos_data = supabase_admin.process_response(alimentos_response)
        return alimentos_data or []
        
    except Exception as e:
        print(f"Erro ao listar alimentos base: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar alimentos base: {str(e)}")

@router.get("/alimentos-base/tipos", response_model=List[str])
async def get_alimentos_tipos(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[str]:
    """
    Obtém a lista de tipos de alimentos disponíveis.
    """
    try:
        # Verificar se o usuário está autenticado
        if not isinstance(current_user, dict):
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Buscar tipos distintos
        tipos_response = await supabase_admin._request(
            "GET",
            "/rest/v1/alimentos_base?select=tipo&distinct=true"
        )
        
        tipos_data = supabase_admin.process_response(tipos_response)
        if not tipos_data:
            return []
            
        # Extrair apenas os valores de tipo
        tipos = [item.get("tipo") for item in tipos_data if item.get("tipo")]
        return tipos
        
    except Exception as e:
        print(f"Erro ao obter tipos de alimentos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter tipos de alimentos: {str(e)}")

@router.get("/alimentos-base/especies", response_model=List[str])
async def get_alimentos_especies(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[str]:
    """
    Obtém a lista de espécies destino disponíveis nos alimentos.
    """
    try:
        # Verificar se o usuário está autenticado
        if not isinstance(current_user, dict):
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Buscar espécies distintas
        especies_response = await supabase_admin._request(
            "GET",
            "/rest/v1/alimentos_base?select=especie_destino&distinct=true"
        )
        
        especies_data = supabase_admin.process_response(especies_response)
        if not especies_data:
            return []
            
        # Extrair apenas os valores de espécie
        especies = [item.get("especie_destino") for item in especies_data if item.get("especie_destino")]
        return especies
        
    except Exception as e:
        print(f"Erro ao obter espécies de alimentos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter espécies de alimentos: {str(e)}")

@router.get("/alimentos-base/{alimento_id}", response_model=AlimentoBaseResponse)
async def get_alimento_base(
    alimento_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Obtém detalhes de um alimento base específico.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Buscar o alimento base
        alimento_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/alimentos_base?alimento_id=eq.{alimento_id}"
        )
        
        alimento_data = supabase_admin.process_response(alimento_response)
        if not alimento_data:
            raise HTTPException(status_code=404, detail="Alimento base não encontrado")
            
        return alimento_data[0]
        
    except Exception as e:
        print(f"Erro ao obter alimento base: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter alimento base: {str(e)}")

@router.put("/alimentos-base/{alimento_id}", response_model=AlimentoBaseResponse)
async def update_alimento_base(
    alimento_id: int,
    alimento: AlimentoBaseUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza um alimento base existente.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o usuário tem permissão (apenas administradores ou agentes de IA)
        user_role = current_user.get("role")
        if user_role not in ["admin", "ai_agent"]:
            raise HTTPException(status_code=403, detail="Sem permissão para atualizar alimentos base")
            
        # Verificar se o alimento base existe
        alimento_check = await supabase_admin._request(
            "GET",
            f"/rest/v1/alimentos_base?alimento_id=eq.{alimento_id}"
        )
        
        existing_alimento = supabase_admin.process_response(alimento_check)
        if not existing_alimento:
            raise HTTPException(status_code=404, detail="Alimento base não encontrado")
            
        # Preparar dados para atualização
        update_data = {k: v for k, v in alimento.dict().items() if v is not None}
        
        # Adicionando cabeçalho Prefer para retornar representação
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"
        
        # Atualizar o alimento base
        alimento_response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/alimentos_base?alimento_id=eq.{alimento_id}",
            json=update_data,
            headers=headers
        )
        
        updated_alimento = supabase_admin.process_response(alimento_response, single_item=True)
        if not updated_alimento:
            # Verificar se o registro ainda existe após a tentativa de atualização
            check_response = await supabase_admin._request(
                "GET",
                f"/rest/v1/alimentos_base?alimento_id=eq.{alimento_id}"
            )
            
            updated_alimento = supabase_admin.process_response(check_response, single_item=True)
            if not updated_alimento:
                raise HTTPException(status_code=500, detail="Erro ao atualizar alimento base")
                
        return updated_alimento
        
    except Exception as e:
        print(f"Erro ao atualizar alimento base: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar alimento base: {str(e)}")

@router.delete("/alimentos-base/{alimento_id}", response_model=AlimentoBaseResponse)
async def delete_alimento_base(
    alimento_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Remove um alimento base existente.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o usuário tem permissão (apenas administradores ou agentes de IA)
        user_role = current_user.get("role")
        if user_role not in ["admin", "ai_agent"]:
            raise HTTPException(status_code=403, detail="Sem permissão para excluir alimentos base")
            
        # Verificar se o alimento base existe
        alimento_check = await supabase_admin._request(
            "GET",
            f"/rest/v1/alimentos_base?alimento_id=eq.{alimento_id}"
        )
        
        existing_alimento = supabase_admin.process_response(alimento_check)
        if not existing_alimento:
            raise HTTPException(status_code=404, detail="Alimento base não encontrado")
            
        # Excluir o alimento base
        headers = supabase_admin.admin_headers.copy()
        
        alimento_response = await supabase_admin._request(
            "DELETE",
            f"/rest/v1/alimentos_base?alimento_id=eq.{alimento_id}",
            headers=headers
        )
        
        if not alimento_response:
            # Verificar se o registro ainda existe após a tentativa de exclusão
            check_response = await supabase_admin._request(
                "GET",
                f"/rest/v1/alimentos_base?alimento_id=eq.{alimento_id}"
            )
            
            if supabase_admin.process_response(check_response):
                raise HTTPException(status_code=500, detail="Falha ao excluir o alimento base")
        
        # Retornar os dados do alimento que foi excluído
        return existing_alimento[0]
        
    except Exception as e:
        print(f"Erro ao excluir alimento base: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao excluir alimento base: {str(e)}")


# Rota para atualizar informações de dieta no animal
@router.put("/animals/{animal_id}/dieta-atual", response_model=Dict[str, Any])
async def update_animal_dieta(
    animal_id: UUID,
    dieta_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza as informações de dieta atual no registro do animal.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o animal existe e pertence à clínica
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}"
        )
        
        animal_data = supabase_admin.process_response(animal_response)
        if not animal_data:
            raise HTTPException(status_code=404, detail="Animal não encontrado")
            
        # Preparar dados para atualização
        update_data = {}
        if "dieta_atual_id" in dieta_data:
            update_data["dieta_atual_id"] = dieta_data["dieta_atual_id"]
        if "dieta_atual_nome" in dieta_data:
            update_data["dieta_atual_nome"] = dieta_data["dieta_atual_nome"]
        if "dieta_atual_status" in dieta_data:
            update_data["dieta_atual_status"] = dieta_data["dieta_atual_status"]
        if "dieta_atual_data_inicio" in dieta_data:
            update_data["dieta_atual_data_inicio"] = dieta_data["dieta_atual_data_inicio"]
        if "dieta_atual_data_fim" in dieta_data:
            update_data["dieta_atual_data_fim"] = dieta_data["dieta_atual_data_fim"]
            
        # Atualizar o animal
        update_response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/animals?id=eq.{animal_id}",
            json=update_data
        )
        
        # Verificar se a atualização foi bem-sucedida
        if update_response.status_code not in (200, 201, 204):
            raise HTTPException(
                status_code=update_response.status_code,
                detail=f"Erro ao atualizar informações de dieta: {update_response.text}"
            )
            
        # Buscar o animal atualizado
        updated_animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}"
        )
        
        updated_animal_data = supabase_admin.process_response(updated_animal_response)
        if not updated_animal_data:
            raise HTTPException(status_code=404, detail="Animal não encontrado após atualização")
            
        return updated_animal_data[0]
        
    except Exception as e:
        print(f"Erro ao atualizar informações de dieta no animal: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar informações de dieta: {str(e)}")

# Rotas para Progresso da Dieta
@router.post("/diets/{diet_id}/progress", response_model=DietProgressResponse)
async def create_diet_progress(
    diet_id: UUID,
    progress: DietProgressCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Registra o progresso de uma dieta.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Verificar se a dieta existe e pertence à clínica
        diet_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?id=eq.{diet_id}&clinic_id=eq.{clinic_id}"
        )
        
        diet_data = supabase_admin.process_response(diet_response)
        if not diet_data:
            raise HTTPException(status_code=404, detail="Dieta não encontrada ou não pertence a esta clínica")
        
        # Criar o registro de progresso
        progress_data = {
            "animal_id": progress.animal_id,
            "dieta_id": progress.dieta_id,
            "opcao_dieta_id": progress.opcao_dieta_id,
            "data": progress.data.isoformat(),
            "refeicao_completa": progress.refeicao_completa,
            "horario_realizado": progress.horario_realizado.isoformat() if progress.horario_realizado else None,
            "quantidade_consumida": progress.quantidade_consumida,
            "observacoes_tutor": progress.observacoes_tutor,
            "pontos_ganhos": progress.pontos_ganhos
        }
        
        # Adicionando cabeçalho Prefer para retornar representação
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"
        
        progress_response = await supabase_admin._request(
            "POST",
            "/rest/v1/dieta_progresso",
            json=progress_data,
            headers=headers
        )
        
        created_progress = supabase_admin.process_response(progress_response, single_item=True)
        if not created_progress:
            raise HTTPException(status_code=500, detail="Erro ao registrar progresso: dados não retornados")
        
        return created_progress
        
    except Exception as e:
        print(f"Erro ao registrar progresso da dieta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao registrar progresso da dieta: {str(e)}")

@router.get("/diets/{diet_id}/progress", response_model=List[DietProgressResponse])
async def list_diet_progress(
    diet_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Lista todos os registros de progresso de uma dieta.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se a dieta existe e pertence à clínica
        diet_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?id=eq.{diet_id}&clinic_id=eq.{clinic_id}"
        )
        
        diet_data = supabase_admin.process_response(diet_response)
        if not diet_data:
            raise HTTPException(status_code=404, detail="Dieta não encontrada ou não pertence a esta clínica")
        
        # Buscar os registros de progresso
        progress_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dieta_progresso?dieta_id=eq.{diet_id}&order=data.desc"
        )
        
        progress_data = supabase_admin.process_response(progress_response)
        return progress_data
        
    except Exception as e:
        print(f"Erro ao listar progresso da dieta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar progresso da dieta: {str(e)}")

@router.put("/diet-progress/{progress_id}", response_model=DietProgressResponse)
async def update_diet_progress(
    progress_id: UUID,
    progress: DietProgressUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza um registro de progresso de dieta.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o registro de progresso existe
        progress_check = await supabase_admin._request(
            "GET",
            f"/rest/v1/dieta_progresso?id=eq.{progress_id}"
        )
        
        existing_progress = supabase_admin.process_response(progress_check)
        if not existing_progress:
            raise HTTPException(status_code=404, detail="Registro de progresso não encontrado")
            
        # Verificar se a dieta associada pertence à clínica
        diet_id = existing_progress[0]["dieta_id"]
        diet_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?id=eq.{diet_id}&clinic_id=eq.{clinic_id}"
        )
        
        diet_data = supabase_admin.process_response(diet_response)
        if not diet_data:
            raise HTTPException(status_code=403, detail="Sem permissão para atualizar este registro de progresso")
            
        # Preparar dados para atualização
        update_data = {}
        if progress.data is not None:
            update_data["data"] = progress.data.isoformat()
        if progress.refeicao_completa is not None:
            update_data["refeicao_completa"] = progress.refeicao_completa
        if progress.horario_realizado is not None:
            update_data["horario_realizado"] = progress.horario_realizado
        if progress.quantidade_consumida is not None:
            update_data["quantidade_consumida"] = progress.quantidade_consumida
        if progress.observacoes_tutor is not None:
            update_data["observacoes_tutor"] = progress.observacoes_tutor
        if progress.pontos_ganhos is not None:
            update_data["pontos_ganhos"] = progress.pontos_ganhos
            
        # Atualizar o registro de progresso
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"
        
        progress_response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/dieta_progresso?id=eq.{progress_id}",
            json=update_data,
            headers=headers
        )
        
        updated_progress = supabase_admin.process_response(progress_response, single_item=True)
        if not updated_progress:
            # Verificar se o registro ainda existe após a tentativa de atualização
            check_response = await supabase_admin._request(
                "GET",
                f"/rest/v1/dieta_progresso?id=eq.{progress_id}"
            )
            
            updated_progress = supabase_admin.process_response(check_response, single_item=True)
            if not updated_progress:
                raise HTTPException(status_code=500, detail="Erro ao atualizar registro de progresso")
                
        return updated_progress
        
    except Exception as e:
        print(f"Erro ao atualizar progresso da dieta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar progresso da dieta: {str(e)}")

@router.delete("/diet-progress/{progress_id}", response_model=DietProgressResponse)
async def delete_diet_progress(
    progress_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Remove um registro de progresso de dieta.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o registro de progresso existe
        progress_check = await supabase_admin._request(
            "GET",
            f"/rest/v1/dieta_progresso?id=eq.{progress_id}"
        )
        
        existing_progress = supabase_admin.process_response(progress_check)
        if not existing_progress:
            raise HTTPException(status_code=404, detail="Registro de progresso não encontrado")
            
        # Verificar se a dieta associada pertence à clínica
        diet_id = existing_progress[0]["dieta_id"]
        diet_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?id=eq.{diet_id}&clinic_id=eq.{clinic_id}"
        )
        
        diet_data = supabase_admin.process_response(diet_response)
        if not diet_data:
            raise HTTPException(status_code=403, detail="Sem permissão para excluir este registro de progresso")
            
        # Excluir o registro de progresso
        headers = supabase_admin.admin_headers.copy()
        
        progress_response = await supabase_admin._request(
            "DELETE",
            f"/rest/v1/dieta_progresso?id=eq.{progress_id}",
            headers=headers
        )
        
        if not progress_response:
            # Verificar se o registro ainda existe após a tentativa de exclusão
            check_response = await supabase_admin._request(
                "GET",
                f"/rest/v1/dieta_progresso?id=eq.{progress_id}"
            )
            
            if supabase_admin.process_response(check_response):
                raise HTTPException(status_code=500, detail="Falha ao excluir o registro de progresso")
        
        # Retornar os dados do registro que foi excluído
        return existing_progress[0]
        
    except Exception as e:
        print(f"Erro ao excluir progresso da dieta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao excluir progresso da dieta: {str(e)}")