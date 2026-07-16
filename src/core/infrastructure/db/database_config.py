from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseConfig:
    """
    Database configuration.
    """

    driver: str
    user: str | None
    password: str | None
    host: str | None
    port: int | None
    database: str
    ssl_root_cert: str | None = None
    test_in_memory: bool = False
