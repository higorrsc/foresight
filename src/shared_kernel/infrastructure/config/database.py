from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.shared_kernel.infrastructure.config.settings import settings
from src.shared_kernel.infrastructure.models._shared.mixins import SQLAlchemyBasicFields

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)  # type: ignore

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


class SQLAlchemyBase(Base, SQLAlchemyBasicFields):
    """
    Base class for all SQLAlchemy models.
    """

    __abstract__ = True
