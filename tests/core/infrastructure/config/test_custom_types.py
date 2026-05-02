import uuid
from unittest.mock import MagicMock

from src.core.infrastructure.config.custom_types import GUIDType


class TestGUIDType:
    def test_load_dialect_impl(self):
        guid_type = GUIDType()

        # Test Postgres
        dialect_pg = MagicMock()
        dialect_pg.name = "postgresql"
        guid_type.load_dialect_impl(dialect_pg)
        assert dialect_pg.type_descriptor.called

        # Test MSSQL
        dialect_mssql = MagicMock()
        dialect_mssql.name = "mssql"
        guid_type.load_dialect_impl(dialect_mssql)
        assert dialect_mssql.type_descriptor.called

        # Test Default (SQLite)
        dialect_sqlite = MagicMock()
        dialect_sqlite.name = "sqlite"
        guid_type.load_dialect_impl(dialect_sqlite)
        assert dialect_sqlite.type_descriptor.called

    def test_process_bind_param(self):
        guid_type = GUIDType()
        value = uuid.uuid4()

        # Test Postgres
        dialect_pg = MagicMock()
        dialect_pg.name = "postgresql"
        assert guid_type.process_bind_param(value, dialect_pg) == value

        # Test SQLite
        dialect_sqlite = MagicMock()
        dialect_sqlite.name = "sqlite"
        assert guid_type.process_bind_param(value, dialect_sqlite) == str(value)
        assert guid_type.process_bind_param(None, dialect_sqlite) is None

    def test_process_result_value(self):
        guid_type = GUIDType()
        value_uuid = uuid.uuid4()
        value_str = str(value_uuid)

        # Test Postgres
        dialect_pg = MagicMock()
        dialect_pg.name = "postgresql"
        assert guid_type.process_result_value(value_uuid, dialect_pg) == value_uuid

        # Test SQLite
        dialect_sqlite = MagicMock()
        dialect_sqlite.name = "sqlite"
        assert guid_type.process_result_value(value_str, dialect_sqlite) == value_uuid
        assert guid_type.process_result_value(None, dialect_sqlite) is None
        assert guid_type.process_result_value("invalid-uuid", dialect_sqlite) is None
        assert guid_type.process_result_value(value_uuid, dialect_sqlite) == value_uuid
