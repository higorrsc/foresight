import ssl

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .settings import settings

SQLALCHEMY_DATABASE_URL = settings.database_url

db_connect_args: dict = {}

if settings.db_driver == "cockroachdb+asyncpg" and getattr(
    settings, "ssl_root_cert", None
):
    ssl_context = ssl.create_default_context(cafile=settings.db_ssl_root_cert)
    ssl_context.check_hostname = True
    db_connect_args["ssl"] = ssl_context

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=db_connect_args,
)  # type: ignore

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
