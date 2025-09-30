from fastapi import APIRouter
from .auth import router as auth_router
from .animals import router as animals_router
from .appointments import router as appointments_router
from .appointment_requests import router as appointment_requests_router
from .consultations import router as consultations_router
from .diets import router as diets_router
from .activities import router as activities_router
from .gamification import router as gamification_router
from .dashboard import router as dashboard_router
from .client import client_router
from .health_check import router as health_router
from .diets_ai import router as diets_ai_router

api_router = APIRouter()

# Rotas de autenticação
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

# Rotas da clínica (administrativas)
api_router.include_router(animals_router, prefix="/animals", tags=["animals"])
api_router.include_router(appointments_router, prefix="/appointments", tags=["appointments"])
api_router.include_router(appointment_requests_router, prefix="/appointment-requests", tags=["appointment-requests"])
api_router.include_router(consultations_router, prefix="/consultations", tags=["consultations"])

# Rotas específicas do cliente/tutor
api_router.include_router(client_router, prefix="/client", tags=["client"])

# Outras rotas
api_router.include_router(diets_router, tags=["diets"])
api_router.include_router(diets_ai_router, tags=["diets_ai"])
api_router.include_router(activities_router, prefix="", tags=["activities"])
api_router.include_router(gamification_router, prefix="", tags=["gamification"])
api_router.include_router(dashboard_router, prefix="", tags=["dashboard"])
api_router.include_router(health_router, tags=["health"])