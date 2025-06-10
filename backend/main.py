import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import API_V1_STR
from app.api import api_router

# Criar aplicação FastAPI
app = FastAPI(
    title="VeTech API",
    description="API para o sistema VeTech para clínicas veterinárias",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adicionar rotas da API
app.include_router(api_router, prefix=API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do VeTech"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True) 