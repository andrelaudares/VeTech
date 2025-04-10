import uvicorn

if __name__ == "__main__":
    print("Iniciando servidor FastAPI...")
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_level="debug"
    ) 