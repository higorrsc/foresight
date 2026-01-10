import uuid

from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER as MSSQL_UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.types import CHAR, TypeDecorator


class GUID_Type(TypeDecorator):
    """
    Custom UUID type that adapts to the database dialect:
    - PostgreSQL: Uses the native UUID type
    - SQL Server: Uses the native UNIQUEIDENTIFIER type
    - SQLite and others: Uses CHAR(36)
    """

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        """
        Use the native PostgreSQL UUID type if we are in Postgres.
        Otherwise, use CHAR(36).
        """

        if dialect.name in ("postgresql", "cockroachdb"):
            return dialect.type_descriptor(PG_UUID(as_uuid=True))

        if dialect.name == "mssql":
            return dialect.type_descriptor(MSSQL_UUID())

        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        """
        Converts the Python UUID object to a string before saving.
        """

        if value is None:
            return value

        if dialect.name in ("postgresql", "mssql", "cockroachdb"):
            return value

        return str(value)

    def process_result_value(self, value, dialect):
        """
        Converts the string returned from the database to a Python UUID object.
        """

        if value is None:
            return value

        if dialect.name in ("postgresql", "mssql", "cockroachdb"):
            return value

        if not isinstance(value, uuid.UUID):
            try:
                return uuid.UUID(value)
            except (TypeError, ValueError):
                return None

        return value
