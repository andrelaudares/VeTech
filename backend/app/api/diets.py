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
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}",
            headers={"Prefer": "return=representation"}
        )
        
        animal_data = animal_response.get("data", [])
        if not animal_data:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")
        
        # Criar a dieta
        diet_data = {
            "pet_id": str(animal_id),
            "clinica_id": clinic_id,
            "tipo": diet.tipo,
            "objetivo": diet.objetivo,
            "peso_atual_pet": diet.peso_atual_pet,
            "idade_pet": diet.idade_pet,
            "raca_pet": diet.raca_pet,
            "tamanho_pet": diet.tamanho_pet,
            "observacoes": diet.observacoes,
            "data_inicio": diet.data_inicio.isoformat(),
            "data_fim": diet.data_fim.isoformat() if diet.data_fim else None,
            "status": diet.status
        }
        
        diet_response = await supabase_admin._request(
            "POST",
            "/rest/v1/dietas",
            json=diet_data,
            headers={"Prefer": "return=representation"}
        )
        
        created_diet = diet_response.get("data", [])[0] if diet_response.get("data") else {}
        if not created_diet:
            raise HTTPException(status_code=500, detail="Erro ao criar dieta")
            
        return {
            **created_diet,
            "opcoes_dieta": []
        }
        
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
            
        # Buscar dietas do animal
        diets_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?pet_id=eq.{animal_id}&clinica_id=eq.{clinic_id}",
            headers={"Prefer": "return=representation"}
        )
        
        diets = diets_response.get("data", [])
        
        # Para cada dieta, buscar as opções de dieta
        for diet in diets:
            diet_id = diet.get("id")
            options_response = await supabase_admin._request(
                "GET",
                f"/rest/v1/opcoes_dieta?dieta_id=eq.{diet_id}",
                headers={"Prefer": "return=representation"}
            )
            
            diet["opcoes_dieta"] = options_response.get("data", [])
            
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
            f"/rest/v1/dietas?id=eq.{diet_id}&clinica_id=eq.{clinic_id}",
            headers={"Prefer": "return=representation"}
        )
        
        diets = diet_response.get("data", [])
        if not diets:
            raise HTTPException(status_code=404, detail="Dieta não encontrada")
            
        diet = diets[0]
        
        # Buscar opções de dieta
        options_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/opcoes_dieta?dieta_id=eq.{diet_id}",
            headers={"Prefer": "return=representation"}
        )
        
        diet["opcoes_dieta"] = options_response.get("data", [])
        
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
            f"/rest/v1/dietas?id=eq.{diet_id}&clinica_id=eq.{clinic_id}",
            headers={"Prefer": "return=representation"}
        )
        
        diets = diet_response.get("data", [])
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
        
        # Atualizar a dieta
        updated_response = await supabase_admin._request(
            "PATCH",
            f"/rest/v1/dietas?id=eq.{diet_id}",
            json=update_data,
            headers={"Prefer": "return=representation"}
        )
        
        # Buscar a dieta atualizada
        updated_diet_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?id=eq.{diet_id}",
            headers={"Prefer": "return=representation"}
        )
        
        updated_diet = updated_diet_response.get("data", [])[0] if updated_diet_response.get("data") else {}
        if not updated_diet:
            raise HTTPException(status_code=404, detail="Dieta não encontrada após atualização")
            
        # Buscar opções de dieta
        options_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/opcoes_dieta?dieta_id=eq.{diet_id}",
            headers={"Prefer": "return=representation"}
        )
        
        updated_diet["opcoes_dieta"] = options_response.get("data", [])
        
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
            f"/rest/v1/dietas?id=eq.{diet_id}&clinica_id=eq.{clinic_id}",
            headers={"Prefer": "return=representation"}
        )
        
        diets = diet_response.get("data", [])
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
    Adiciona uma opção de dieta a um plano.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se a dieta existe e pertence à clínica
        diet_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?id=eq.{diet_id}&clinica_id=eq.{clinic_id}",
            headers={"Prefer": "return=representation"}
        )
        
        diets = diet_response.get("data", [])
        if not diets:
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
            json=option_data,
            headers={"Prefer": "return=representation"}
        )
        
        created_option = option_response.get("data", [])[0] if option_response.get("data") else {}
        if not created_option:
            raise HTTPException(status_code=500, detail="Erro ao criar opção de dieta")
            
        return created_option
        
    except Exception as e:
        print(f"Erro ao criar opção de dieta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar opção de dieta: {str(e)}")

# Rotas para Alimentos a Evitar
@router.post("/animals/{animal_id}/restricted-foods", response_model=RestrictedFoodResponse)
async def create_restricted_food(
    animal_id: UUID,
    food: RestrictedFoodCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Adiciona um alimento que o pet deve evitar.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o animal existe e pertence à clínica
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}",
            headers={"Prefer": "return=representation"}
        )
        
        animals = animal_response.get("data", [])
        if not animals:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")
            
        # Criar o alimento a evitar
        food_data = {
            "pet_id": str(animal_id),
            "nome": food.nome,
            "motivo": food.motivo
        }
        
        food_response = await supabase_admin._request(
            "POST",
            "/rest/v1/alimentos_evitar",
            json=food_data,
            headers={"Prefer": "return=representation"}
        )
        
        created_food = food_response.get("data", [])[0] if food_response.get("data") else {}
        if not created_food:
            raise HTTPException(status_code=500, detail="Erro ao adicionar alimento a evitar")
            
        return created_food
        
    except Exception as e:
        print(f"Erro ao adicionar alimento a evitar: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar alimento a evitar: {str(e)}")

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
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}",
            headers={"Prefer": "return=representation"}
        )
        
        animals = animal_response.get("data", [])
        if not animals:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")
            
        # Buscar alimentos a evitar
        foods_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/alimentos_evitar?pet_id=eq.{animal_id}",
            headers={"Prefer": "return=representation"}
        )
        
        foods = foods_response.get("data", [])
        return foods
        
    except Exception as e:
        print(f"Erro ao listar alimentos a evitar: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar alimentos a evitar: {str(e)}")

# Rotas para Snacks
@router.post("/animals/{animal_id}/snacks", response_model=SnackResponse)
async def create_snack(
    animal_id: UUID,
    snack: SnackCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Adiciona um snack permitido entre refeições.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o animal existe e pertence à clínica
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}",
            headers={"Prefer": "return=representation"}
        )
        
        animals = animal_response.get("data", [])
        if not animals:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")
            
        # Criar o snack
        snack_data = {
            "pet_id": str(animal_id),
            "nome": snack.nome,
            "frequencia_semanal": snack.frequencia_semanal,
            "quantidade": snack.quantidade,
            "observacoes": snack.observacoes
        }
        
        snack_response = await supabase_admin._request(
            "POST",
            "/rest/v1/snacks_entre_refeicoes",
            json=snack_data,
            headers={"Prefer": "return=representation"}
        )
        
        created_snack = snack_response.get("data", [])[0] if snack_response.get("data") else {}
        if not created_snack:
            raise HTTPException(status_code=500, detail="Erro ao adicionar snack")
            
        return created_snack
        
    except Exception as e:
        print(f"Erro ao adicionar snack: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar snack: {str(e)}")

@router.get("/animals/{animal_id}/snacks", response_model=List[SnackResponse])
async def list_snacks(
    animal_id: UUID,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Lista todos os snacks permitidos entre refeições.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
            
        # Verificar se o animal existe e pertence à clínica
        animal_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?id=eq.{animal_id}&clinic_id=eq.{clinic_id}",
            headers={"Prefer": "return=representation"}
        )
        
        animals = animal_response.get("data", [])
        if not animals:
            raise HTTPException(status_code=404, detail="Animal não encontrado ou não pertence a esta clínica")
            
        # Buscar snacks
        snacks_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/snacks_entre_refeicoes?pet_id=eq.{animal_id}",
            headers={"Prefer": "return=representation"}
        )
        
        snacks = snacks_response.get("data", [])
        return snacks
        
    except Exception as e:
        print(f"Erro ao listar snacks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar snacks: {str(e)}")

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
            f"/rest/v1/opcoes_dieta?id=eq.{option_id}",
            headers={"Prefer": "return=representation"}
        )
        
        options = option_response.get("data", [])
        if not options:
            raise HTTPException(status_code=404, detail="Opção de dieta não encontrada")
            
        # Verificar se a dieta associada pertence à clínica
        diet_id = options[0].get("dieta_id")
        diet_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?id=eq.{diet_id}&clinica_id=eq.{clinic_id}",
            headers={"Prefer": "return=representation"}
        )
        
        diets = diet_response.get("data", [])
        if not diets:
            raise HTTPException(status_code=403, detail="Acesso negado a esta opção de dieta")
            
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
            json=food_data,
            headers={"Prefer": "return=representation"}
        )
        
        created_food = food_response.get("data", [])[0] if food_response.get("data") else {}
        if not created_food:
            raise HTTPException(status_code=500, detail="Erro ao adicionar alimento")
            
        return created_food
        
    except Exception as e:
        print(f"Erro ao adicionar alimento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar alimento: {str(e)}")

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
            f"/rest/v1/opcoes_dieta?id=eq.{option_id}",
            headers={"Prefer": "return=representation"}
        )
        
        options = option_response.get("data", [])
        if not options:
            raise HTTPException(status_code=404, detail="Opção de dieta não encontrada")
            
        # Verificar se a dieta associada pertence à clínica
        diet_id = options[0].get("dieta_id")
        diet_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?id=eq.{diet_id}&clinica_id=eq.{clinic_id}",
            headers={"Prefer": "return=representation"}
        )
        
        diets = diet_response.get("data", [])
        if not diets:
            raise HTTPException(status_code=403, detail="Acesso negado a esta opção de dieta")
            
        # Buscar alimentos
        foods_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/alimentos_dieta?opcao_dieta_id=eq.{option_id}",
            headers={"Prefer": "return=representation"}
        )
        
        foods = foods_response.get("data", [])
        return foods
        
    except Exception as e:
        print(f"Erro ao listar alimentos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar alimentos: {str(e)}") 