from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routers.identity_access_management import (
    AuthRouter,
    RoleRouter,
    UserProtectedRouter,
    UserPublicRouter,
)
from src.api.routers.shared_kernel import AreaRouter
from src.shared_kernel.infrastructure.config import SessionLocal
from src.shared_kernel.infrastructure.db import (
    seed_app_permissions,
    seed_initial_roles,
    seed_initial_users,
)


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    """
    Application lifespan.
    """

    print("Starting the application...")
    db_session = SessionLocal()
    try:
        seed_initial_roles(db_session)
        db_session.flush()
        seed_app_permissions(db_session)
        db_session.flush()
        seed_initial_users(db_session)
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

app.include_router(AuthRouter)
app.include_router(UserPublicRouter)
app.include_router(UserProtectedRouter)
app.include_router(RoleRouter)
app.include_router(AreaRouter)


@app.get("/")
def read_root():
    """
    Root of the API.
    """

    return {"message": "Bem-vindo à Foresight API!"}
