from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.shared_kernel.infrastructure.config.settings import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)  # type: ignore

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
