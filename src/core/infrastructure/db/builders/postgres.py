"""
Postgres URL builder.
"""

from sqlalchemy import URL

from src.core.infrastructure.db import DatabaseConfig


def build_postgres_url(config: DatabaseConfig) -> str:
    """
    Build Postgres URL from environment variables.
    """

    return str(
        URL.create(
            drivername=config.driver,
            username=config.user,
            password=config.password,
            host=config.host,
            port=config.port,
            database=config.database,
        )
    )
