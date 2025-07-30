from fastapi import APIRouter
from .auth import router as auth_router
from .animals import router as animals_router
from .appointments import router as appointments_router
from .consultations import router as consultations_router
from .diets import router as diets_router
from .activities import router as activities_router
from .gamification import router as gamification_router
from .dashboard import router as dashboard_router
from .client import router as client_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(animals_router, prefix="/animals", tags=["animals"])
api_router.include_router(appointments_router, prefix="/appointments", tags=["appointments"])
api_router.include_router(consultations_router, prefix="/consultations", tags=["consultations"])
api_router.include_router(diets_router, tags=["diets"])
api_router.include_router(activities_router, prefix="", tags=["activities"])
api_router.include_router(gamification_router, prefix="", tags=["gamification"])
api_router.include_router(dashboard_router, prefix="", tags=["dashboard"])
api_router.include_router(client_router, prefix="/client", tags=["client"])