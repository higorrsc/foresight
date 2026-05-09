from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .settings import settings

SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)  # type: ignore

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
