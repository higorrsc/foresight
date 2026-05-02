"""
Cockroach URL builder.
"""

from src.core.infrastructure.db import DatabaseConfig


def build_cockroach_url(config: DatabaseConfig) -> str:
    """
    Build Cockroach URL from environment variables.
    """

    return (
        f"cockroachdb://{config.user}:{config.password}"
        f"@{config.host}:{config.port}/{config.database}"
        f"?sslmode=verify-full&sslrootcert={config.ssl_root_cert}"
    )
