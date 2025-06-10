from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from datetime import datetime, date
import logging

from ..db.supabase import supabase_admin
from ..api.auth import get_current_user

# Configuração básica de logging para este módulo
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/dashboard/stats")
async def get_dashboard_stats(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Obtém estatísticas gerais para o dashboard.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        stats = {}

        # 1. Total de animais ativos
        animals_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/animals?clinic_id=eq.{clinic_id}&select=id"
        )
        animals_data = supabase_admin.process_response(animals_response)
        stats["animais_ativos"] = len(animals_data) if animals_data else 0

        # 2. Agendamentos de hoje (buscar todos e filtrar por data)
        appointments_today_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/appointments?clinic_id=eq.{clinic_id}&select=id,date"
        )
        appointments_all = supabase_admin.process_response(appointments_today_response)
        
        # Filtrar por data de hoje no Python
        today = date.today()
        appointments_today_data = []
        if appointments_all:
            for apt in appointments_all:
                apt_date = apt.get('date', '')
                if apt_date.startswith(today.isoformat()):
                    appointments_today_data.append(apt)
        
        stats["consultas_hoje"] = len(appointments_today_data) if appointments_today_data else 0

        # 3. Animais sem dietas
        if animals_data:
            animal_ids = [animal['id'] for animal in animals_data]
            
            # Buscar dietas existentes para esses animais
            diets_response = await supabase_admin._request(
                "GET",
                f"/rest/v1/dietas?animal_id=in.({','.join(animal_ids)})&select=animal_id"
            )
            diets_data = supabase_admin.process_response(diets_response)
            
            animals_with_diets = set()
            if diets_data:
                animals_with_diets = {diet['animal_id'] for diet in diets_data}
            
            animals_without_diets = len(animal_ids) - len(animals_with_diets)
            stats["animais_sem_dietas"] = animals_without_diets
        else:
            stats["animais_sem_dietas"] = 0

        # 4. Animais sem planos de atividade
        if animals_data:
            # Buscar planos de atividade existentes
            activity_plans_response = await supabase_admin._request(
                "GET",
                f"/rest/v1/planos_atividade?animal_id=in.({','.join(animal_ids)})&select=animal_id"
            )
            activity_plans_data = supabase_admin.process_response(activity_plans_response)
            
            animals_with_activities = set()
            if activity_plans_data:
                animals_with_activities = {plan['animal_id'] for plan in activity_plans_data}
            
            animals_without_activities = len(animal_ids) - len(animals_with_activities)
            stats["animais_sem_atividades"] = animals_without_activities
        else:
            stats["animais_sem_atividades"] = 0

        return stats

    except Exception as e:
        logger.error(f"Erro ao buscar estatísticas do dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar estatísticas: {str(e)}")

@router.get("/dashboard/appointments-today")
async def get_appointments_today(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Obtém agendamentos do dia atual.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        # Buscar todos os agendamentos e filtrar por data de hoje
        appointments_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/appointments?clinic_id=eq.{clinic_id}&order=start_time.asc&select=*"
        )
        
        appointments_all = supabase_admin.process_response(appointments_response)
        if not appointments_all:
            return []

        # Filtrar por data de hoje no Python
        today = date.today()
        appointments_today_data = []
        if appointments_all:
            for apt in appointments_all:
                apt_date = apt.get('date', '')
                if apt_date.startswith(today.isoformat()):
                    appointments_today_data.append(apt)

        if not appointments_today_data:
            return []

        # Para cada agendamento, buscar dados do animal
        enriched_appointments = []
        for appointment in appointments_today_data:
            animal_id = appointment.get('animal_id')
            if animal_id:
                # Buscar dados do animal (corrigir campo tutor_name)
                animal_response = await supabase_admin._request(
                    "GET",
                    f"/rest/v1/animals?id=eq.{animal_id}&select=name,tutor_name"
                )
                animal_data = supabase_admin.process_response(animal_response, single_item=True)
                
                enriched_appointment = {
                    "id": appointment.get('id'),
                    "animal_name": animal_data.get('name', 'N/A') if animal_data else 'N/A',
                    "owner_name": animal_data.get('tutor_name') if animal_data and animal_data.get('tutor_name') else 'Tutor não informado',
                    "time_scheduled": appointment.get('start_time'),  # Manter esse nome para compatibilidade com frontend
                    "status": appointment.get('status', 'agendado'),
                    "description": appointment.get('description', 'Consulta'),
                    "notes": appointment.get('description', '')
                }
                enriched_appointments.append(enriched_appointment)

        return enriched_appointments

    except Exception as e:
        logger.error(f"Erro ao buscar agendamentos de hoje: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar agendamentos: {str(e)}")

@router.get("/dashboard/alerts")
async def get_dashboard_alerts(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Obtém alertas importantes para o dashboard.
    """
    try:
        # Verificar se o usuário está autenticado
        clinic_id = current_user.get("id")
        if not clinic_id:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")

        alerts = []

        # 1. Verificar dietas prestes a expirar (próximos 7 dias)
        from datetime import timedelta
        next_week = (date.today() + timedelta(days=7)).isoformat()
        
        expiring_diets_response = await supabase_admin._request(
            "GET",
            f"/rest/v1/dietas?clinic_id=eq.{clinic_id}&data_fim=lte.{next_week}&data_fim=gte.{date.today().isoformat()}&select=id,data_fim"
        )
        expiring_diets_data = supabase_admin.process_response(expiring_diets_response)
        
        if expiring_diets_data:
            alerts.append({
                "type": "warning",
                "icon": "🔁",
                "message": f"{len(expiring_diets_data)} dieta(s) personalizada(s) expira(m) nos próximos 7 dias."
            })

        # 2. Verificar animais sem dietas
        stats_response = await get_dashboard_stats(current_user)
        animals_without_diets = stats_response.get("animais_sem_dietas", 0)
        
        if animals_without_diets > 0:
            alerts.append({
                "type": "info",
                "icon": "🍽️",
                "message": f"{animals_without_diets} animal(is) ainda não possui(em) plano de dieta."
            })

        # 3. Verificar animais sem atividades
        animals_without_activities = stats_response.get("animais_sem_atividades", 0)
        
        if animals_without_activities > 0:
            alerts.append({
                "type": "info",
                "icon": "🏃‍♂️",
                "message": f"{animals_without_activities} animal(is) ainda não possui(em) plano de atividades."
            })

        return alerts

    except Exception as e:
        logger.error(f"Erro ao buscar alertas do dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar alertas: {str(e)}") 