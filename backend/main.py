import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import API_V1_STR
from app.api import api_router

# Criar aplicação FastAPI
app = FastAPI(
    title="FinanceAI API",
    description="API para autenticação básica do FinanceAI",
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
    return {"message": "Bem-vindo à API do FinanceAI"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 