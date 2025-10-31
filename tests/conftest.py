import os
from typing import Generator

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool, StaticPool

from src.api.dependencies.database import get_db_session
from src.api.main import app
from src.shared_kernel.infrastructure.config import Base
from src.shared_kernel.infrastructure.db import (
    seed_app_permissions,
    seed_initial_roles,
    seed_initial_users,
)

load_dotenv()

USE_IN_MEMORY_DB = os.getenv("TEST_IN_MEMORY", "true").lower() in ("true", "1", "t")
DB_FILE_PATH = "test.sqlite3"

SQLALCHEMY_DATABASE_URL = (
    "sqlite:///:memory:" if USE_IN_MEMORY_DB else f"sqlite:///./{DB_FILE_PATH}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else NullPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="session")
def setup_database():
    """
    Create database for tests
    """

    Base.metadata.create_all(bind=engine)
    yield

    if not USE_IN_MEMORY_DB:
        os.remove("test.sqlite3")


@pytest.fixture(scope="function")
def db_session_for_test(setup_database) -> Generator[Session, None, None]:
    """
    Creates ONE transaction for each test, seeds data, and rolls back at the end.
    """

    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())

    seed_initial_roles(session)
    session.flush()
    seed_app_permissions(session)
    session.flush()
    seed_initial_users(session)
    session.flush()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session_for_test: Session) -> Generator[TestClient, None, None]:
    """
    Create client for each test.
    """

    def override_get_db_session_for_test() -> Generator[Session, None, None]:
        yield db_session_for_test

    app.dependency_overrides[get_db_session] = override_get_db_session_for_test

    yield TestClient(app)

    app.dependency_overrides.clear()
