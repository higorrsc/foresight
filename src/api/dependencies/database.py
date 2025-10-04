from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.infrastructure.config.database import SessionLocal
from src.core.infrastructure.repositories import (
    AreaRepository,
    RoleRepository,
    UserRepository,
)


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
    session: Session = Depends(get_db_session),
) -> AreaRepository:
    """
    Return an AreaRepository instance with database session.
    """

    return AreaRepository(session)


def get_user_repository(
    session: Session = Depends(get_db_session),
) -> UserRepository:
    """
    Return an UserRepository instance with database session.
    """

    return UserRepository(session)


def get_role_repository(
    session: Session = Depends(get_db_session),
) -> RoleRepository:
    """
    Return an RoleRepository instance with database session.
    """

    return RoleRepository(session)
