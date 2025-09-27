from typing import Generator

from fastapi import Depends

from src.core.infrastructure.config.database import SessionLocal
from src.core.infrastructure.repositories.area_repository import AreaRepository


def get_db_session() -> Generator:
    """
    Create a database session by request.
    """

    db = None

    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()


def get_area_repository(
    session: SessionLocal = Depends(get_db_session),
) -> AreaRepository:
    """
    Return an AreaRepository instance with database session.
    """

    return AreaRepository(session)
