from fastapi import FastAPI

from src.api.routers import area_router

app = FastAPI(
    title="Foresight API",
    description="API para simulação orçamentária e projeção de gastos/custos.",
    version="1.0.0",
)

app.include_router(area_router.router)


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à Foresight API!"}
