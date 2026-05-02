"""
MS SQL Server URL builder.
"""

from sqlalchemy import URL

from src.core.infrastructure.db import DatabaseConfig


def build_mssql_url(config: DatabaseConfig) -> str:
    """
    Build MS SQL Server URL from environment variables.
    """

    return str(
        URL.create(
            drivername=config.driver,
            username=config.user,
            password=config.password,
            host=config.host,
            port=config.port,
            database=config.database,
            query={"driver": "ODBC Driver 17 for SQL Server"},
        )
    )
