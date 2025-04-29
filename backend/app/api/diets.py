from fastapi import APIRouter, HTTPException, Depends, Path
from typing import Dict, Any, List, Optional
from uuid import UUID

from ..models.diet import (
    DietCreate, DietUpdate, DietResponse,
    DietOptionCreate, DietOptionUpdate, DietOptionResponse,
    DietFoodCreate, DietFoodUpdate, DietFoodResponse,
    RestrictedFoodCreate, RestrictedFoodUpdate, RestrictedFoodResponse,
    SnackCreate, SnackUpdate, SnackResponse
)
from ..db.supabase import supabase_admin
from ..api.auth import get_current_user

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
            "clinic_id": clinic_id,
            "tipo": diet.tipo,
            "objetivo": diet.objetivo,
            "observacoes": diet.observacoes,
            "data_inicio": diet.data_inicio.isoformat(),
            "data_fim": diet.data_fim.isoformat() if diet.data_fim else None,
            "status": diet.status
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
            
        # Adicionar lista vazia de opções de dieta
        created_diet["opcoes_dieta"] = []
        
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
        
        # Para cada dieta, buscar as opções de dieta
        for diet in diets:
            diet_id = diet.get("id")
            options_response = await supabase_admin._request(
                "GET",
                f"/rest/v1/opcoes_dieta?dieta_id=eq.{diet_id}"
            )
            
            options = supabase_admin.process_response(options_response)
            diet["opcoes_dieta"] = options if options else []
            
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
        
        # Buscar opções de dieta
        options_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/opcoes_dieta?dieta_id=eq.{diet_id}"
        )
        
        options = supabase_admin.process_response(options_response)
        diet["opcoes_dieta"] = options if options else []
        
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
            
        # Buscar opções de dieta
        options_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/opcoes_dieta?dieta_id=eq.{diet_id}"
        )
        
        updated_diet["opcoes_dieta"] = supabase_admin.process_response(options_response)
        
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
            
        # Remover opções de dieta associadas
        await supabase_admin._request(
            "DELETE",
            f"/rest/v1/opcoes_dieta?dieta_id=eq.{diet_id}"
        )
        
        # Remover a dieta
        await supabase_admin._request(
            "DELETE",
            f"/rest/v1/dietas?id=eq.{diet_id}"
        )
        
        return {"message": "Dieta removida com sucesso"}
        
    except Exception as e:
        print(f"Erro ao remover dieta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao remover dieta: {str(e)}")

# Rotas para Opções de Dieta
@router.post("/diets/{diet_id}/options", response_model=DietOptionResponse)
async def create_diet_option(
    diet_id: UUID,
    option: DietOptionCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Cria uma opção de dieta para uma dieta existente.
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
            
        # Criar a opção de dieta
        option_data = {
            "dieta_id": str(diet_id),
            "nome": option.nome,
            "valor_mensal_estimado": option.valor_mensal_estimado,
            "calorias_totais_dia": option.calorias_totais_dia,
            "porcao_refeicao": option.porcao_refeicao,
            "refeicoes_por_dia": option.refeicoes_por_dia,
            "indicacao": option.indicacao
        }
        
        option_response = await supabase_admin._request(
            "POST",
            "/rest/v1/opcoes_dieta",
            json=option_data
        )
        
        created_option = supabase_admin.process_response(option_response, single_item=True)
        if not created_option:
            raise HTTPException(status_code=500, detail="Erro ao criar opção de dieta")
            
        return created_option
        
    except Exception as e:
        print(f"Erro ao criar opção de dieta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar opção de dieta: {str(e)}")

@router.put("/diet-options/{option_id}", response_model=DietOptionResponse)
async def update_diet_option(
    option_id: UUID,
    option_update: DietOptionUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza uma opção de dieta existente.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se a opção de dieta existe
        option_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/opcoes_dieta?id=eq.{option_id}"
        )
        
        option_data = supabase_admin.process_response(option_response)
        if not option_data:
            raise HTTPException(status_code=404, detail="Opção de dieta não encontrada")
            
        # Verificar se a dieta pertence à clínica
        diet_id = option_data[0].get("dieta_id") if isinstance(option_data, list) else option_data.get("dieta_id")
        diet_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?id=eq.{diet_id}&clinic_id=eq.{clinic_id}"
        )
        
        diet_data = supabase_admin.process_response(diet_response)
        if not diet_data:
            raise HTTPException(status_code=403, detail="Acesso negado: dieta não pertence a esta clínica")
            
        # Preparar dados para atualização
        update_data = option_update.dict(exclude_unset=True)
        
        # Atualizar a opção de dieta
        updated_response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/opcoes_dieta?id=eq.{option_id}",
            json=update_data
        )
        
        # Buscar a opção atualizada
        result_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/opcoes_dieta?id=eq.{option_id}"
        )
        
        updated_option = supabase_admin.process_response(result_response, single_item=True)
        if not updated_option:
            raise HTTPException(status_code=404, detail="Opção de dieta não encontrada após atualização")
            
        return updated_option
        
    except Exception as e:
        print(f"Erro ao atualizar opção de dieta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar opção de dieta: {str(e)}")

@router.delete("/diet-options/{option_id}", status_code=204)
async def delete_diet_option(
    option_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> None:
    """
    Remove uma opção de dieta.
    """
    try:
        # Verificar autenticação
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se a opção existe
        option_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/opcoes_dieta?id=eq.{option_id}"
        )
        
        options = supabase_admin.process_response(option_response)
        if not options:
            raise HTTPException(status_code=404, detail="Opção de dieta não encontrada")
            
        # Verificar se a dieta associada pertence à clínica
        diet_id = options[0].get("dieta_id")
        diet_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?id=eq.{diet_id}&clinic_id=eq.{clinic_id}"
        )
        
        diets = supabase_admin.process_response(diet_response)
        if not diets:
            raise HTTPException(status_code=403, detail="Acesso negado a esta opção de dieta")
            
        # Remover a opção de dieta (e alimentos associados, se o cascade estiver configurado no DB)
        await supabase_admin._request(
            "DELETE",
            f"/rest/v1/opcoes_dieta?id=eq.{option_id}"
        )
        return None # FastAPI retornará 204 No Content automaticamente
        
    except Exception as e:
        print(f"Erro ao remover opção de dieta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao remover opção de dieta: {str(e)}")

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
            "nome": food.nome,
            "motivo": food.motivo
        }
        
        foods_response = await supabase_admin._request(
            "POST",
            "/rest/v1/alimentos_evitar",
            json=food_data
        )
        
        foods = supabase_admin.process_response(foods_response, single_item=True)
        if not foods:
            raise HTTPException(status_code=500, detail="Erro ao criar registro de alimento a evitar")
            
        return foods
        
    except Exception as e:
        print(f"Erro ao criar alimento a evitar: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar alimento a evitar: {str(e)}")

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

@router.put("/restricted-foods/{food_id}", response_model=RestrictedFoodResponse)
async def update_restricted_food(
    food_id: UUID,
    food_update: RestrictedFoodUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza um registro de alimento a ser evitado.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o alimento restrito existe
        food_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/alimentos_evitar?id=eq.{food_id}"
        )
        
        food_data = supabase_admin.process_response(food_response)
        if not food_data:
            raise HTTPException(status_code=404, detail="Alimento restrito não encontrado")
            
        # Verificar se o animal pertence à clínica
        animal_id = food_data[0].get("animal_id") if isinstance(food_data, list) else food_data.get("animal_id")
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}"
        )
        
        animal_data = supabase_admin.process_response(animal_response)
        if not animal_data:
            raise HTTPException(status_code=403, detail="Acesso negado: animal não pertence a esta clínica")
            
        # Preparar dados para atualização
        update_data = food_update.dict(exclude_unset=True)
        
        # Atualizar o alimento restrito
        updated_response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/alimentos_evitar?id=eq.{food_id}",
            json=update_data
        )
        
        # Buscar o alimento atualizado
        result_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/alimentos_evitar?id=eq.{food_id}"
        )
        
        updated_food = supabase_admin.process_response(result_response, single_item=True)
        if not updated_food:
            raise HTTPException(status_code=404, detail="Alimento restrito não encontrado após atualização")
            
        return updated_food
        
    except Exception as e:
        print(f"Erro ao atualizar alimento restrito: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar alimento restrito: {str(e)}")

@router.delete("/restricted-foods/{food_id}", status_code=204)
async def delete_restricted_food(
    food_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> None:
    """
    Remove um alimento restrito.
    """
    try:
        # Verificar autenticação
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o alimento existe
        food_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/alimentos_evitar?id=eq.{food_id}"
        )
        
        foods = supabase_admin.process_response(food_response)
        if not foods:
            raise HTTPException(status_code=404, detail="Alimento restrito não encontrado")
            
        # Verificar se o animal pertence à clínica
        animal_id = foods[0].get("animal_id")
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}"
        )
        
        animals = supabase_admin.process_response(animal_response)
        if not animals:
            raise HTTPException(status_code=403, detail="Acesso negado a este alimento restrito")
            
        # Remover o alimento restrito
        await supabase_admin._request(
            "DELETE",
            f"/rest/v1/alimentos_evitar?id=eq.{food_id}"
        )
        return None
        
    except Exception as e:
        print(f"Erro ao remover alimento restrito: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao remover alimento restrito: {str(e)}")

# Rotas para Snacks
@router.post("/animals/{animal_id}/snacks", response_model=SnackResponse)
async def create_snack(
    animal_id: UUID,
    snack: SnackCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Cria um registro de lanche entre refeições para um animal.
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
        
        # Criar o lanche
        snack_data = {
            "animal_id": str(animal_id),
            "clinic_id": clinic_id,
            "nome": snack.nome,
            "frequencia_semanal": snack.frequencia_semanal,
            "quantidade": snack.quantidade,
            "observacoes": snack.observacoes
        }
        
        # Adicionando cabeçalho Prefer para retornar representação
        headers = supabase_admin.admin_headers.copy()
        headers["Prefer"] = "return=representation"
        
        snack_response = await supabase_admin._request(
            "POST",
            "/rest/v1/snacks_entre_refeicoes",
            json=snack_data,
            headers=headers
        )
        
        created_snack = supabase_admin.process_response(snack_response, single_item=True)
        if not created_snack:
            raise HTTPException(status_code=500, detail="Erro ao criar registro de lanche")
            
        return created_snack
        
    except Exception as e:
        print(f"Erro ao criar lanche: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar lanche: {str(e)}")

@router.get("/animals/{animal_id}/snacks", response_model=List[SnackResponse])
async def list_snacks(
    animal_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Lista todos os snacks permitidos para um animal.
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
            
        # Buscar snacks do animal
        snacks_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/snacks_entre_refeicoes?animal_id=eq.{animal_id}"
        )
        
        snacks = supabase_admin.process_response(snacks_response)
        return snacks
        
    except Exception as e:
        print(f"Erro ao listar snacks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar snacks: {str(e)}")

@router.put("/snacks/{snack_id}", response_model=SnackResponse)
async def update_snack(
    snack_id: UUID,
    snack_update: SnackUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza um registro de lanche entre refeições.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o lanche existe
        snack_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/snacks_entre_refeicoes?id=eq.{snack_id}"
        )
        
        snack_data = supabase_admin.process_response(snack_response)
        if not snack_data:
            raise HTTPException(status_code=404, detail="Lanche não encontrado")
            
        # Verificar se o animal pertence à clínica
        animal_id = snack_data[0].get("animal_id") if isinstance(snack_data, list) else snack_data.get("animal_id")
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}"
        )
        
        animal_data = supabase_admin.process_response(animal_response)
        if not animal_data:
            raise HTTPException(status_code=403, detail="Acesso negado: animal não pertence a esta clínica")
            
        # Preparar dados para atualização
        update_data = snack_update.dict(exclude_unset=True)
        
        # Atualizar o lanche
        updated_response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/snacks_entre_refeicoes?id=eq.{snack_id}",
            json=update_data
        )
        
        # Buscar o lanche atualizado
        result_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/snacks_entre_refeicoes?id=eq.{snack_id}"
        )
        
        updated_snack = supabase_admin.process_response(result_response, single_item=True)
        if not updated_snack:
            raise HTTPException(status_code=404, detail="Lanche não encontrado após atualização")
            
        return updated_snack
        
    except Exception as e:
        print(f"Erro ao atualizar lanche: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar lanche: {str(e)}")

@router.delete("/snacks/{snack_id}", status_code=204)
async def delete_snack(
    snack_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> None:
    """
    Remove um snack.
    """
    try:
        # Verificar autenticação
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o snack existe
        snack_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/snacks_entre_refeicoes?id=eq.{snack_id}"
        )
        
        snacks = supabase_admin.process_response(snack_response)
        if not snacks:
            raise HTTPException(status_code=404, detail="Snack não encontrado")
            
        # Verificar se o animal pertence à clínica
        animal_id = snacks[0].get("animal_id")
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}"
        )
        
        animals = supabase_admin.process_response(animal_response)
        if not animals:
            raise HTTPException(status_code=403, detail="Acesso negado a este snack")
            
        # Remover o snack
        await supabase_admin._request(
            "DELETE",
            f"/rest/v1/snacks_entre_refeicoes?id=eq.{snack_id}"
        )
        return None
        
    except Exception as e:
        print(f"Erro ao remover snack: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao remover snack: {str(e)}")

# Rotas para Alimentos da Dieta
@router.post("/diet-options/{option_id}/foods", response_model=DietFoodResponse)
async def create_diet_food(
    option_id: UUID,
    food: DietFoodCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Adiciona um alimento a uma opção de dieta.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se a opção de dieta existe
        option_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/opcoes_dieta?id=eq.{option_id}"
        )
        
        option_data = supabase_admin.process_response(option_response)
        if not option_data:
            raise HTTPException(status_code=404, detail="Opção de dieta não encontrada")
            
        # Verificar se a dieta pertence à clínica
        diet_id = option_data[0].get("dieta_id") if isinstance(option_data, list) else option_data.get("dieta_id")
        diet_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?id=eq.{diet_id}"
        )
        
        diet_data = supabase_admin.process_response(diet_response)
        if not diet_data:
            raise HTTPException(status_code=404, detail="Dieta não encontrada")
            
        diet = diet_data[0] if isinstance(diet_data, list) else diet_data
        if diet.get("clinic_id") != clinic_id:
            raise HTTPException(status_code=403, detail="Acesso negado: dieta não pertence a esta clínica")
            
        # Criar o alimento
        food_data = {
            "opcao_dieta_id": str(option_id),
            "nome": food.nome,
            "tipo": food.tipo,
            "quantidade": food.quantidade,
            "calorias": food.calorias,
            "horario": food.horario
        }
        
        food_response = await supabase_admin._request(
            "POST",
            "/rest/v1/alimentos_dieta",
            json=food_data
        )
        
        created_food = supabase_admin.process_response(food_response, single_item=True)
        if not created_food:
            raise HTTPException(status_code=500, detail="Erro ao adicionar alimento à dieta")
            
        return created_food
        
    except Exception as e:
        print(f"Erro ao adicionar alimento à dieta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar alimento à dieta: {str(e)}")

@router.get("/diet-options/{option_id}/foods", response_model=List[DietFoodResponse])
async def list_diet_foods(
    option_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Lista todos os alimentos de uma opção de dieta.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se a opção de dieta existe
        option_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/opcoes_dieta?id=eq.{option_id}"
        )
        
        options = supabase_admin.process_response(option_response)
        if not options:
            raise HTTPException(status_code=404, detail="Opção de dieta não encontrada")
            
        # Verificar se a dieta associada pertence à clínica
        diet_id = options[0].get("dieta_id")
        diet_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?id=eq.{diet_id}&clinic_id=eq.{clinic_id}"
        )
        
        diets = supabase_admin.process_response(diet_response)
        if not diets:
            raise HTTPException(status_code=404, detail="Dieta não encontrada ou não pertence a esta clínica")
            
        # Buscar alimentos da opção de dieta
        foods_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/alimentos_dieta?opcao_dieta_id=eq.{option_id}"
        )
        
        foods = supabase_admin.process_response(foods_response)
        return foods
        
    except Exception as e:
        print(f"Erro ao listar alimentos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar alimentos: {str(e)}")

@router.put("/diet-foods/{food_id}", response_model=DietFoodResponse)
async def update_diet_food(
    food_id: UUID,
    food_update: DietFoodUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Atualiza um alimento de uma opção de dieta.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o alimento existe
        food_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/alimentos_dieta?id=eq.{food_id}"
        )
        
        food_data = supabase_admin.process_response(food_response)
        if not food_data:
            raise HTTPException(status_code=404, detail="Alimento não encontrado")
            
        # Verificar se a opção de dieta pertence à clínica
        option_id = food_data[0].get("opcao_dieta_id") if isinstance(food_data, list) else food_data.get("opcao_dieta_id")
        option_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/opcoes_dieta?id=eq.{option_id}"
        )
        
        option_data = supabase_admin.process_response(option_response)
        if not option_data:
            raise HTTPException(status_code=404, detail="Opção de dieta não encontrada")
            
        diet_id = option_data[0].get("dieta_id") if isinstance(option_data, list) else option_data.get("dieta_id")
        diet_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?id=eq.{diet_id}&clinic_id=eq.{clinic_id}"
        )
        
        diet_data = supabase_admin.process_response(diet_response)
        if not diet_data:
            raise HTTPException(status_code=403, detail="Acesso negado: dieta não pertence a esta clínica")
            
        # Preparar dados para atualização
        update_data = food_update.dict(exclude_unset=True)
        
        # Atualizar o alimento
        updated_response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/alimentos_dieta?id=eq.{food_id}",
            json=update_data
        )
        
        # Buscar o alimento atualizado
        result_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/alimentos_dieta?id=eq.{food_id}"
        )
        
        updated_food = supabase_admin.process_response(result_response, single_item=True)
        if not updated_food:
            raise HTTPException(status_code=404, detail="Alimento não encontrado após atualização")
            
        return updated_food
        
    except Exception as e:
        print(f"Erro ao atualizar alimento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar alimento: {str(e)}")

@router.delete("/diet-foods/{food_id}", status_code=204)
async def delete_diet_food(
    food_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> None:
    """
    Remove um alimento de uma opção de dieta.
    """
    try:
        # Verificar autenticação
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o alimento existe
        food_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/alimentos_dieta?id=eq.{food_id}"
        )
        
        foods = supabase_admin.process_response(food_response)
        if not foods:
            raise HTTPException(status_code=404, detail="Alimento não encontrado")
            
        # Verificar se a opção de dieta pertence à clínica (via dieta)
        option_id = foods[0].get("opcao_dieta_id")
        option_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/opcoes_dieta?id=eq.{option_id}"
        )
        
        options = supabase_admin.process_response(option_response)
        if not options:
            raise HTTPException(status_code=404, detail="Opção de dieta não encontrada")
            
        diet_id = options[0].get("dieta_id")
        diet_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?id=eq.{diet_id}&clinic_id=eq.{clinic_id}"
        )
        
        diets = supabase_admin.process_response(diet_response)
        if not diets:
            raise HTTPException(status_code=403, detail="Acesso negado a este alimento")
            
        # Remover o alimento
        await supabase_admin._request(
            "DELETE",
            f"/rest/v1/alimentos_dieta?id=eq.{food_id}"
        )
        return None
        
    except Exception as e:
        print(f"Erro ao remover alimento da dieta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao remover alimento da dieta: {str(e)}") 