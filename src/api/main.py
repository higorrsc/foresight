from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routers import area_router, auth_router, role_router, user_router
from src.core.infrastructure.config.database import Base, SessionLocal, engine
from src.core.infrastructure.db import (
    seed_app_permissions,
    seed_initial_roles,
    seed_initial_users,
)
from src.core.infrastructure.models import AreaModel

Base.metadata.create_all(bind=engine)
AreaModel.metadata.create_all(bind=engine)


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

app.include_router(auth_router.router)
app.include_router(user_router.public_router)
app.include_router(user_router.protected_router)
app.include_router(role_router.router)
app.include_router(area_router.router)


@app.get("/")
def read_root():
    """
    Root of the API.
    """

    return {"message": "Bem-vindo à Foresight API!"}
