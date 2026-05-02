from functools import cached_property
from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.infrastructure.db import DatabaseConfig
from src.core.infrastructure.db.builders import BUILDERS


class Settings(BaseSettings):
    """
    Load and validate environment variables.
    """

    # =========================
    # DB ENV VARS
    # =========================

    db_driver: Literal[
        "sqlite",
        "postgresql+psycopg2",
        "mssql+pyodbc",
        "cockroachdb",
    ] = "sqlite"

    db_user: str | None = Field(default=None, validate_default=True)
    db_password: str | None = Field(default=None, validate_default=True)
    db_host: str | None = Field(default=None, validate_default=True)
    db_port: int | None = Field(default=None, validate_default=True)
    db_database: str = "./foresight.sqlite3"
    db_ssl_root_cert: str | None = Field(default=None, validate_default=True)

    test_in_memory: bool = True

    # =========================
    # AUTH
    # =========================

    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    auth_provider: str = "local"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # =========================
    # VALIDATION
    # =========================

    @model_validator(mode="after")
    def validate_environment(self) -> "Settings":
        """
        Validate environment variables.
        """

        if self.db_driver == "sqlite":
            if not self.db_database:
                raise ValueError("SQLite requires DB_DATABASE")

        if self.db_driver == "cockroachdb":
            required = [
                self.db_host,
                self.db_port,
                self.db_database,
                self.db_user,
                self.db_password,
                self.db_ssl_root_cert,
            ]
            if not all(required):
                raise ValueError(
                    f"{self.db_driver} requires DB_HOST, DB_PORT, DB_DATABASE"
                )

        if self.db_driver in {
            "postgresql+psycopg2",
            "mssql+pyodbc",
        }:
            required = [
                self.db_host,
                self.db_port,
                self.db_database,
            ]
            if not all(required):
                raise ValueError(
                    f"{self.db_driver} requires DB_HOST, DB_PORT, DB_DATABASE"
                )

        return self

    # =========================
    # BUILD DATABASE CONFIG DTO
    # =========================

    @cached_property
    def database_config(self) -> DatabaseConfig:
        """
        Database configuration.
        """

        return DatabaseConfig(
            driver=self.db_driver,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_database,
            ssl_root_cert=self.db_ssl_root_cert,
            test_in_memory=self.test_in_memory,
        )

    # =========================
    # DATABASE URL
    # =========================

    @cached_property
    def database_url(self) -> str:
        """
        Database URL.
        """

        builder = BUILDERS.get(self.db_driver)

        if not builder:
            raise ValueError(f"Unsupported DB_DRIVER: {self.db_driver}")

        return builder(self.database_config)


settings = Settings()
