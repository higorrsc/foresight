from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from src.api.v1.routers.identity_access_management import (
    auth_router,
    permission_router,
    role_router,
    user_router,
)
from src.api.v1.routers.planning import scenario_router
from src.api.v1.routers.shared_kernel import (
    area_router,
    organizational_unit_router,
)
from src.api.v1.routers.tenant_management import plan_router, tenant_router
from src.core.infrastructure.config import AsyncSessionLocal
from src.core.infrastructure.logging import get_logger, setup_logging
from src.scripts import seed_initial_data

# Initialize logging configuration
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    """
    Application lifespan.
    """

    logger.info("Starting the application...")
    async with AsyncSessionLocal() as db_session:
        try:
            # Se o seu script de seed for síncrono, terá de o adaptar ou
            # usar db_session.run_sync() se for estritamente necessário.
            # O ideal é tornar o seed_initial_data também assíncrono.
            await seed_initial_data(db_session)  # type: ignore
            await db_session.commit()
        except Exception as e:
            await db_session.rollback()
            logger.error(f"Seeding error: {e}")

    yield  # A aplicação fica em execução aqui

    # Código a ser executado QUANDO a aplicação for encerrada
    logger.info("Shutting down application...")


app = FastAPI(
    title="Foresight API (v1 & Legacy)",
    description="API para simulação orçamentária e projeção de gastos/custos. Supports v1 and legacy (deprecated) endpoints.",
    version="1.1.0",
    lifespan=lifespan,
)


@app.get("/")
def read_root():
    """
    Root of the API.
    """

    return {"message": "Bem-vindo à Foresight API!"}


# Legacy (deprecated) endpoints
app.include_router(auth_router, deprecated=True)
app.include_router(permission_router, deprecated=True)
app.include_router(plan_router, deprecated=True)
app.include_router(tenant_router, deprecated=True)
app.include_router(user_router, deprecated=True)
app.include_router(role_router, deprecated=True)
app.include_router(area_router, deprecated=True)
app.include_router(scenario_router, deprecated=True)
app.include_router(organizational_unit_router, deprecated=True)

# API v1 endpoints
v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(auth_router)
v1_router.include_router(permission_router)
v1_router.include_router(plan_router)
v1_router.include_router(tenant_router)
v1_router.include_router(user_router)
v1_router.include_router(role_router)
v1_router.include_router(area_router)
v1_router.include_router(scenario_router)
v1_router.include_router(organizational_unit_router)

app.include_router(v1_router)
