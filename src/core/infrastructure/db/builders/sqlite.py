"""
SQLite URL builder.
"""

from src.core.infrastructure.db import DatabaseConfig


def build_sqlite_url(config: DatabaseConfig) -> str:
    """
    Build SQLite URL from environment variables.
    """

    return f"sqlite+pysqlite:///{config.database}"
