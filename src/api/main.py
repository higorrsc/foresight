from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routers.identity_access_management import (
    AuthRouter,
    RoleRouter,
    UserRouter,
)
from src.api.routers.shared_kernel import AreaRouter
from src.api.routers.tenant_management import PlanRouter, TenantRouter
from src.shared_kernel.infrastructure.config import SessionLocal
from src.shared_kernel.infrastructure.db import seed_initial_data


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    """
    Application lifespan.
    """

    print("Starting the application...")
    db_session = SessionLocal()
    try:
        seed_initial_data(db_session)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(f"Seeding error: {e}")
    finally:
        db_session.close()

    yield  # A aplicação fica em execução aqui

    # Código a ser executado QUANDO a aplicação for encerrada
    print("A encerrar a aplicação...")


app = FastAPI(
    title="Foresight API",
    description="API para simulação orçamentária e projeção de gastos/custos.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(PlanRouter)
app.include_router(TenantRouter)
app.include_router(AuthRouter)
app.include_router(UserRouter)
app.include_router(RoleRouter)
app.include_router(AreaRouter)


@app.get("/")
def read_root():
    """
    Root of the API.
    """

    return {"message": "Bem-vindo à Foresight API!"}
