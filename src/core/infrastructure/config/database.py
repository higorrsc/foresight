from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .settings import settings

SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)  # type: ignore

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
