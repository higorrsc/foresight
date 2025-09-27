from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.infrastructure.config.settings import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)  # type: ignore

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
