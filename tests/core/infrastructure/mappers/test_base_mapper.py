from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from src.core.infrastructure.mappers.base_mapper import BaseMapper


@dataclass
class DummyEntity:
    """
    A dummy entity for testing auditing field mapping.
    """

    created_by: str | None = None
    created_at: datetime | None = None
    updated_by: str | None = None
    updated_at: datetime | None = None
    is_active: bool = True
    deleted_at: datetime | None = None


class DummyModel:
    """
    A dummy model for testing auditing field mapping.
    """

    def __init__(self):
        self.created_by: str | None = None
        self.created_at: datetime | None = None
        self.updated_by: str | None = None
        self.updated_at: datetime | None = None
        self.is_active: bool = True
        self.deleted_at: datetime | None = None


class TestBaseMapper:
    """
    Test suite for the BaseMapper.
    """

    def test_map_auditing_fields_to_model(self):
        """
        Test mapping of auditing fields from an entity to a model.
        """
        entity = DummyEntity(
            created_by=str(uuid4()),
            created_at=datetime.now(UTC),
            updated_by=str(uuid4()),
            updated_at=datetime.now(UTC),
            is_active=False,
            deleted_at=datetime.now(UTC),
        )
        model = DummyModel()

        BaseMapper.map_auditing_fields_to_model(entity, model)

        assert model.created_by == entity.created_by
        assert model.created_at == entity.created_at
        assert model.updated_by == entity.updated_by
        assert model.updated_at == entity.updated_at
        assert model.is_active == entity.is_active
        assert model.deleted_at == entity.deleted_at

    def test_map_auditing_fields_to_entity(self):
        """
        Test mapping of auditing fields from a model to an entity.
        """
        model = DummyModel()
        model.created_by = str(uuid4())
        model.created_at = datetime.now(UTC)
        model.updated_by = str(uuid4())
        model.updated_at = datetime.now(UTC)
        model.is_active = False
        model.deleted_at = datetime.now(UTC)

        entity = DummyEntity()

        BaseMapper.map_auditing_fields_to_entity(model, entity)

        assert entity.created_by == model.created_by
        assert entity.created_at == model.created_at
        assert entity.updated_by == model.updated_by
        assert entity.updated_at == model.updated_at
        assert entity.is_active == model.is_active
        assert entity.deleted_at == model.deleted_at

    def test_map_auditing_fields_partial(self):
        """
        Test mapping of auditing fields when some fields are missing in the target object.
        """

        @dataclass
        class PartialEntity:
            created_by: str | None = None
            created_at: datetime | None = None

        class PartialModel:
            def __init__(self):
                self.created_by = None
                self.created_at = None
                self.updated_by = None

        entity = PartialEntity(created_by="user1", created_at=datetime.now(UTC))
        model = PartialModel()

        BaseMapper.map_auditing_fields_to_model(entity, model)

        assert model.created_by == "user1"
        assert model.created_at == entity.created_at
        assert model.updated_by is None

        model.created_by = "user2"  # type: ignore
        model.updated_by = "user3"  # type: ignore
        entity = PartialEntity()

        BaseMapper.map_auditing_fields_to_entity(model, entity)

        assert entity.created_by == "user2"
        # entity does not have updated_by, so it shouldn't
        # be set (and it's not in PartialEntity anyway)
        assert not hasattr(entity, "updated_by")
