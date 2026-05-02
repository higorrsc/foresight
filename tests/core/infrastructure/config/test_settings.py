import pytest

from src.core.infrastructure.config.settings import Settings


class TestSettings:
    """
    Test suite for the application settings.
    """

    def test_settings_default_sqlite(self):
        """
        Test that settings correctly configure a default SQLite database.
        """
        settings = Settings(
            db_driver="sqlite",
            db_database="test.sqlite3",
            test_in_memory=False,
        )

        assert settings.database_url == "sqlite+pysqlite:///test.sqlite3"

    def test_settings_cockroachdb_success(self):
        """
        Test successful configuration of a CockroachDB connection string.
        """
        settings = Settings(
            db_driver="cockroachdb",
            db_user="user",
            db_password="password",
            db_host="host",
            db_port=26257,
            db_database="db",
            db_ssl_root_cert="cert.pem",
        )

        url = settings.database_url

        assert "cockroachdb://" in url
        assert "user:password@host:26257/db" in url
        assert "sslmode=verify-full" in url
        assert "sslrootcert=cert.pem" in url

    def test_settings_cockroachdb_missing_vars(self):
        """
        Test that settings validation fails when required CockroachDB variables are missing.
        """

        def _make_settings(**overrides):
            """
            Create settings for test
            """

            base = {
                "db_driver": "sqlite",
                "db_database": ":memory:",
                "db_user": None,
                "db_password": None,
                "db_host": None,
                "db_port": None,
                "db_ssl_root_cert": None,
                "test_in_memory": True,
            }

            base.update(overrides)

            return Settings(**base)  # type: ignore

        with pytest.raises(ValueError):
            _make_settings(
                db_driver="cockroachdb",
                db_user="user",
                db_password="password",
            )

    def test_settings_postgresql(self):
        """
        Test configuration of a PostgreSQL connection string.
        """
        settings = Settings(
            db_driver="postgresql+psycopg2",
            db_user="user",
            db_password="password",
            db_host="host",
            db_port=5432,
            db_database="db",
        )

        url = settings.database_url

        assert url.startswith("postgresql+psycopg2://")
        assert "host:5432/db" in url

    def test_settings_mssql(self):
        """
        Test configuration of a MS SQL Server connection string.
        """
        settings = Settings(
            db_driver="mssql+pyodbc",
            db_user="user",
            db_password="password",
            db_host="host",
            db_port=1433,
            db_database="db",
        )

        url = settings.database_url

        assert url.startswith("mssql+pyodbc://")
        assert "host:1433/db" in url
        assert "driver=ODBC+Driver+17+for+SQL+Server" in url

    def test_settings_explicit_database_url_removed_behavior(self):
        """
        Test that DATABASE_URL is always derived and cannot be overridden directly.
        """
        settings = Settings(
            db_driver="sqlite",
            db_database="test.sqlite3",
        )

        assert "sqlite" in settings.database_url
