from uuid import uuid4

import pytest

from src.core.domain import EntityValidationError
from src.core.domain.entities.described import DescribedEntity


class TestDescribedEntity:
    def test_described_entity_initialization(self):
        tenant_id = uuid4()
        entity_id = uuid4()
        description = "Valid description"

        class MyEntity(DescribedEntity):
            pass

        entity = MyEntity(id=entity_id, tenant_id=tenant_id, description=description)

        assert entity.id == entity_id
        assert entity.tenant_id == tenant_id
        assert entity.description == description

    def test_update_description(self):
        class MyEntity(DescribedEntity):
            pass

        entity = MyEntity(id=uuid4(), description="Old description")
        new_description = "New description"

        entity.update_description(new_description)

        assert entity.description == new_description

    def test_validate_empty_description(self):
        class MyEntity(DescribedEntity):
            pass

        with pytest.raises(EntityValidationError) as excinfo:
            MyEntity(id=uuid4(), description="")

        assert "Description must be a non-empty string." in str(excinfo.value)

    def test_validate_whitespace_description(self):
        class MyEntity(DescribedEntity):
            pass

        with pytest.raises(EntityValidationError) as excinfo:
            MyEntity(id=uuid4(), description="   ")

        assert "Description must be a non-empty string." in str(excinfo.value)

    def test_validate_too_long_description(self):
        class MyEntity(DescribedEntity):
            pass

        long_description = "a" * 101
        with pytest.raises(EntityValidationError) as excinfo:
            MyEntity(id=uuid4(), description=long_description)

        assert "Description must be at most 100 characters long." in str(excinfo.value)
