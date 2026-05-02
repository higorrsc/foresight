import pytest
from pydantic import ValidationError

from src.core.infrastructure.config.settings import Settings


class TestSettings:
    def test_settings_default_sqlite(self):
        settings = Settings(DB_DRIVER="sqlite", DB_DATABASE="test.sqlite3")
        assert settings.DATABASE_URL == "sqlite:///test.sqlite3"

    def test_settings_cockroachdb_success(self):
        settings = Settings(
            DB_DRIVER="cockroachdb",
            DB_USER="user",
            DB_PASSWORD="password",
            DB_HOST="host",
            DB_PORT=26257,
            DB_DATABASE="db",
            DB_SSL_ROOT_CERT="cert.pem",
        )
        assert "cockroachdb://user:password@host:26257/db" in settings.DATABASE_URL  # type: ignore
        assert "sslmode=verify-full" in settings.DATABASE_URL  # type: ignore
        assert "sslrootcert=cert.pem" in settings.DATABASE_URL  # type: ignore

    def test_settings_cockroachdb_missing_vars(self, monkeypatch):
        # Ensure environment is clean
        monkeypatch.delenv("DB_DRIVER", raising=False)
        monkeypatch.delenv("DB_USER", raising=False)
        monkeypatch.delenv("DB_PASSWORD", raising=False)
        monkeypatch.delenv("DB_HOST", raising=False)
        monkeypatch.delenv("DB_PORT", raising=False)
        monkeypatch.delenv("DB_DATABASE", raising=False)

        with pytest.raises(ValidationError):
            Settings(
                _env_file=None,  # type: ignore
                DB_DRIVER="cockroachdb",
                DB_USER="user",
                # missing others
            )

    def test_settings_postgresql(self):
        settings = Settings(
            _env_file=None,  # type: ignore
            DB_DRIVER="postgresql",
            DB_USER="user",
            DB_PASSWORD="password",
            DB_HOST="host",
            DB_PORT=5432,
            DB_DATABASE="db",
        )
        # SQLAlchemy URL masks password when stringified
        assert settings.DATABASE_URL == "postgresql://user:***@host:5432/db"

    def test_settings_explicit_database_url(self):
        url = "postgresql://other:pass@otherhost:5432/otherdb"
        settings = Settings(DATABASE_URL=url)
        assert settings.DATABASE_URL == url
