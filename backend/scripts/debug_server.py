from app.api import api_router
from fastapi import FastAPI
import uvicorn

# Criar uma instância simples do FastAPI
app = FastAPI(title="Debug API")

# Registrar as rotas
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "API de debug funcionando!"}

# Listar todas as rotas registradas
print("Rotas disponíveis:")
for route in app.routes:
    print(f"{route.methods} {route.path}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000) 