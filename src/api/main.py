from fastapi import FastAPI

from src.api.routers import area_router
from src.core.infrastructure.config.database import Base, engine
from src.core.infrastructure.models import AreaModel

Base.metadata.create_all(bind=engine)
AreaModel.metadata.create_all(bind=engine)


app = FastAPI(
    title="Foresight API",
    description="API para simulação orçamentária e projeção de gastos/custos.",
    version="1.0.0",
)

app.include_router(area_router.router)


@app.get("/")
def read_root():
    """
    Root of the API.
    """

    return {"message": "Bem-vindo à Foresight API!"}
