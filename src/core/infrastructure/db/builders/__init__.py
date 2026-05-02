from .cockroach import build_cockroach_url
from .mssql import build_mssql_url
from .postgres import build_postgres_url
from .sqlite import build_sqlite_url

BUILDERS = {
    "sqlite": build_sqlite_url,
    "postgresql+psycopg2": build_postgres_url,
    "mssql+pyodbc": build_mssql_url,
    "cockroachdb": build_cockroach_url,
}

__all__ = [
    "BUILDERS",
    "build_cockroach_url",
    "build_mssql_url",
    "build_postgres_url",
    "build_sqlite_url",
]
