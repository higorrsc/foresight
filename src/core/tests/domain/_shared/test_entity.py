from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.core.domain._shared import AbstractEntity


@dataclass(kw_only=True, eq=False)
class DummyEntity(AbstractEntity):
    """
    A dummy entity for testing purposes.
    """

    name: str

    def _validate(self):
        """
        Validate the entity.

        Raises:
            ValueError: If the entity is in an invalid state.
        """

        if not self.name:
            raise ValueError("Name cannot be empty")
        if not isinstance(self.name, str):
            raise ValueError("Name must be a string")
        if len(self.name) < 3:
            raise ValueError("Name must be at least 3 characters long")
        if len(self.name) > 255:
            raise ValueError("Name must be less than 255 characters long")


class TestAbstractEntity:
    """
    Test cases for the AbstractEntity class.
    """

    def test_entity_creation(self):
        """
        Test the creation of an entity.
        """

        entity = DummyEntity(name="Test Entity")
        assert entity.name == "Test Entity"
        assert isinstance(entity.id, UUID)
        assert isinstance(entity.created_at, datetime)
        assert isinstance(entity.updated_at, datetime)

    def test_entity_equality(self):
        """
        Test the equality of two entities.
        """

        entity1 = DummyEntity(name="Entity 1")
        entity2 = DummyEntity(name="Entity 2", id=entity1.id)  # ✅ id igual

        assert entity1 == entity2

    def test_entity_inequality(self):
        """
        Test the inequality of two entities.
        """

        entity1 = DummyEntity(name="Entity 1")
        entity2 = DummyEntity(name="Entity 2")  # ❌ id diferente

        assert entity1 != entity2

    def test_validate_empty_name(self):
        """
        Test the validation of an entity with an empty name.
        """

        try:
            DummyEntity(name="")
        except ValueError as e:
            assert str(e) == "Name cannot be empty"

    def test_validate_short_name(self):
        """
        Test the validation of an entity with a short name.
        """

        try:
            DummyEntity(name="ab")
        except ValueError as e:
            assert str(e) == "Name must be at least 3 characters long"

    def test_validate_long_name(self):
        """
        Test the validation of an entity with a long name.
        """

        try:
            DummyEntity(name="a" * 256)
        except ValueError as e:
            assert str(e) == "Name must be less than 255 characters long"

    def test_validate_non_string_name(self):
        """
        Test the validation of an entity with a non-string name.
        """

        try:
            DummyEntity(name=123)  # type: ignore
        except ValueError as e:
            assert str(e) == "Name must be a string"
