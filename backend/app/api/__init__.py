from fastapi import APIRouter
from .auth import router as auth_router
from .animals import router as animals_router
from .appointments import router as appointments_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(animals_router, prefix="/animals", tags=["animals"])
api_router.include_router(appointments_router, prefix="/appointments", tags=["appointments"]) 