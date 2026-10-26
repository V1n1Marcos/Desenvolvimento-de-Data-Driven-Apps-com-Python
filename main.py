from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from models import InvalidItemIDException
from routes import router

app = FastAPI(
    title="API de Exercícios FastAPI",
    description="Aplicação desenvolvida para atender aos 12 exercícios propostos.",
    version="1.0.0",
)


# Exercício 10: Manipulador global para a exceção personalizada InvalidItemIDException
@app.exception_handler(InvalidItemIDException)
async def invalid_item_id_exception_handler(
    request: Request, exc: InvalidItemIDException
):
    return JSONResponse(status_code=400, content={"error": exc.message})


# Inclui as rotas definidas em routes.py
app.include_router(router)

# Exercício 1: Execução local 
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:main", host="127.0.0.1", port=8000, reload=True)