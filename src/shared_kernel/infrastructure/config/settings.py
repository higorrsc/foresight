from typing import Optional

from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    """
    Load and validate environment variables.
    """

    DB_DRIVER: str = "sqlite"
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_DATABASE: str = "./db.sqlite3"

    DB_SSL_ROOT_CERT: Optional[str] = None

    DATABASE_URL: Optional[str] = None

    SECRET_KEY: str = "default_secret_key_if_not_in_env_file"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    AUTH_PROVIDER: str = "local"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> str:
        """
        Build DATABASE_URL from environment variables.
        """

        if isinstance(v, str):
            return v

        values = info.data
        driver = values.get("DB_DRIVER")

        if driver == "sqlite":
            database_path = values.get("DB_DATABASE")
            if values.get("DB_DRIVER") == "sqlite" and database_path:
                return f"sqlite:///{database_path}"

        if driver == "cockroachdb":
            user = values.get("DB_USER")
            password = values.get("DB_PASSWORD")
            host = values.get("DB_HOST")
            port = values.get("DB_PORT")
            database = values.get("DB_DATABASE")
            cert_path = values.get("DB_SSL_ROOT_CERT")

            if not all([user, password, host, port, database, cert_path]):
                raise ValueError("For CockroachDB, all variables DB_* must be set.")

            return f"cockroachdb://{user}:{password}@{host}:{port}/{database}?sslmode=verify-full&sslrootcert={cert_path}"

        return str(
            URL.create(
                drivername=values.get("DB_DRIVER", "postgresql"),
                username=values.get("DB_USER"),
                password=values.get("DB_PASSWORD"),
                host=values.get("DB_HOST"),
                port=values.get("DB_PORT"),
                database=values.get("DB_DATABASE"),
            )
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
