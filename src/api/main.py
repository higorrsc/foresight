from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routers.identity_access_management import (
    auth_router,
    permission_router,
    role_router,
    user_router,
)
from src.api.routers.planning import scenario_router
from src.api.routers.shared_kernel import (
    area_router,
    organizational_unit_router,
)
from src.api.routers.tenant_management import plan_router, tenant_router
from src.core.infrastructure.config import AsyncSessionLocal
from src.scripts import seed_initial_data


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    """
    Application lifespan.
    """

    print("Starting the application...")
    async with AsyncSessionLocal() as db_session:
        try:
            # Se o seu script de seed for síncrono, terá de o adaptar ou
            # usar db_session.run_sync() se for estritamente necessário.
            # O ideal é tornar o seed_initial_data também assíncrono.
            await seed_initial_data(db_session)
            await db_session.commit()
        except Exception as e:
            await db_session.rollback()
            print(f"Seeding error: {e}")

    yield  # A aplicação fica em execução aqui

    # Código a ser executado QUANDO a aplicação for encerrada
    print("Shutting down application...")


app = FastAPI(
    title="Foresight API",
    description="API para simulação orçamentária e projeção de gastos/custos.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def read_root():
    """
    Root of the API.
    """

    return {"message": "Bem-vindo à Foresight API!"}


app.include_router(auth_router)
app.include_router(permission_router)
app.include_router(plan_router)
app.include_router(tenant_router)
app.include_router(user_router)
app.include_router(role_router)
app.include_router(area_router)
app.include_router(scenario_router)
app.include_router(organizational_unit_router)
