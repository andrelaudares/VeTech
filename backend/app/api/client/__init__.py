from fastapi import APIRouter
from .appointments import router as appointments_router
from .appointment_requests import router as appointment_requests_router
from .consultations import router as consultations_router
from .profile import router as profile_router

client_router = APIRouter()

# Incluir rotas específicas do cliente/tutor
client_router.include_router(profile_router, prefix="/profile", tags=["client-profile"])
client_router.include_router(appointments_router, prefix="/appointments", tags=["client-appointments"])
client_router.include_router(appointment_requests_router, prefix="/appointment-requests", tags=["client-appointment-requests"])
client_router.include_router(consultations_router, prefix="/consultations", tags=["client-consultations"])