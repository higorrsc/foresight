import os
from typing import Any, Generator

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool, Pool, StaticPool

from src.api.dependencies.database import get_db_session
from src.api.main import app
from src.identity_access_management.domain.entities import User as UserEntity
from src.identity_access_management.infrastructure.mappers import UserMapper
from src.identity_access_management.infrastructure.models import UserModel
from src.shared_kernel.infrastructure.config import Base
from src.shared_kernel.infrastructure.db import seed_initial_data

# Imports needed for new data fixtures
from src.tenant_management.infrastructure.models import TenantModel

# --- ENVIRONMENT VARIABLE LOGIC ---

# 1. Load the .env file into OS environment variables
load_dotenv()

# 2. Read the environment variable. Default is 'true' (use in-memory).
USE_IN_MEMORY_DB = os.getenv("TEST_IN_MEMORY", "true").lower() in ("true", "1", "t")

DB_FILE_PATH = "test.sqlite3"  # Name of the physical test file
CONNECT_ARGS = {"check_same_thread": False}
POOLCLASS: type[Pool] = NullPool  # Default pool for files

if USE_IN_MEMORY_DB:
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    # StaticPool is ESSENTIAL for :memory: to work with TestClient
    POOLCLASS = StaticPool
    print("\n--- Running tests with IN-MEMORY database (from .env) ---")
else:
    SQLALCHEMY_DATABASE_URL = f"sqlite:///./{DB_FILE_PATH}"
    print(f"\n--- Running tests with FILE database ({DB_FILE_PATH}) (from .env) ---")

# --- END OF LOGIC ---

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=CONNECT_ARGS,
    poolclass=POOLCLASS,  # Use the dynamic poolclass
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="session")
def setup_database():
    """
    Creates the database tables once per test session.
    If using a file, deletes it at the end.
    """

    Base.metadata.create_all(bind=engine)
    yield
    # Only delete the file if we are not using in-memory
    if not USE_IN_MEMORY_DB:
        os.remove(DB_FILE_PATH)


@pytest.fixture(scope="function")
def db_session_for_test(setup_database) -> Generator[Session, None, None]:
    """
    Creates ONE transaction for each test, seeds data, flushes,
    and rolls back at the end.
    """

    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Use nested transactions (savepoints) for isolation
    # nested_transaction = session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    # Clear data from previous tests WITHIN the transaction
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())

    # Run the unified seeding WITHIN the transaction
    seed_initial_data(session)

    # Flush INSERTS to the DB (within the transaction)
    session.flush()

    yield session  # The test runs here, seeing the seeded data

    # Rollback everything at the end
    transaction.rollback()
    session.close()
    # nested_transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session_for_test: Session) -> Generator[TestClient, Any, Any]:
    """
    Creates a TestClient for each test, using the correct test session.
    """

    def override_get_db_session_for_test() -> Generator[Session, None, None]:
        yield db_session_for_test

    app.dependency_overrides[get_db_session] = override_get_db_session_for_test
    yield TestClient(app)
    app.dependency_overrides.clear()


# --- NEW DATA FIXTURES ---
@pytest.fixture(scope="function")
def default_tenant(db_session_for_test: Session) -> TenantModel:
    """
    Provides the default 'System Tenant' (TenantModel) created by seeding.
    """

    tenant = (
        db_session_for_test.query(TenantModel).filter_by(name="System Tenant").first()
    )
    assert tenant is not None, "Seeding of 'System Tenant' failed."
    return tenant


@pytest.fixture(scope="function")
def admin_user_model(
    db_session_for_test: Session,
    default_tenant: TenantModel,
) -> UserModel:
    """
    Provides the 'admin' UserModel created by seeding.
    """

    user = (
        db_session_for_test.query(UserModel)
        .filter_by(username="admin", tenant_id=default_tenant.id)
        .first()
    )
    assert user is not None, "Seeding of 'admin' user failed."
    return user


@pytest.fixture(scope="function")
def guest_user_model(
    db_session_for_test: Session,
    default_tenant: TenantModel,
) -> UserModel:
    """
    Provides the 'guest' UserModel created by seeding.
    """

    user = (
        db_session_for_test.query(UserModel)
        .filter_by(username="guest", tenant_id=default_tenant.id)
        .first()
    )

    assert user is not None, "Seeding of 'guest' user failed."
    return user


@pytest.fixture(scope="function")
def admin_actor(admin_user_model: UserModel) -> UserEntity:
    """
    Returns the 'admin' User (Domain Entity) to be used as an actor in use cases.
    """

    return UserMapper.to_entity(admin_user_model)


@pytest.fixture(scope="function")
def guest_actor(guest_user_model: UserModel) -> UserEntity:
    """
    Returns the 'guest' User (Domain Entity) to be used as an actor in use cases.
    """

    return UserMapper.to_entity(guest_user_model)


@pytest.fixture(scope="function")
def admin_token(client: TestClient) -> str:
    """
    Logs in as 'admin' and returns an access token.
    """

    response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "foresight_admin"},
    )
    assert response.status_code == 200, f"Failed to get admin token: {response.json()}"
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def guest_token(client: TestClient) -> str:
    """
    Logs in as 'guest' and returns an access token.
    """

    response = client.post(
        "/auth/token",
        data={"username": "guest", "password": "foresight_guest"},
    )
    assert response.status_code == 200, f"Failed to get guest token: {response.json()}"
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def default_tenant_id(default_tenant: TenantModel) -> str:
    """
    Returns the tenant ID to be used.
    """

    return str(default_tenant.id)
