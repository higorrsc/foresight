import pytest

from src.core.domain._shared.exceptions import EntityValidationError
from src.core.domain.entities.role import Role
from src.core.infrastructure.repositories._shared.in_memory_repository import (
    InMemoryRepository,
)


class TestUpdateRoleUseCase:
    """
    Test suite for the UpdateRoleUseCase.
    """

    @pytest.fixture
    def role_in_memory_repository(self):
        """
        Fixture that represents an in-memory repository for testing purposes.
        """

        return InMemoryRepository[Role]()

    def test_update_role(self, role_in_memory_repository):
        """
        Test update role.
        """

        repo = role_in_memory_repository
        role = Role(name="Test", description="Test role")
        repo.save(role)

        role.update_role(new_name="Updated", new_description="Updated role")
        repo.update(role)
        assert role.name == "Updated"
        assert role.description == "Updated role"

    def test_update_role_with_invalid_name(self, role_in_memory_repository):
        """
        Test update role with invalid name.
        """

        repo = role_in_memory_repository
        role = Role(name="Test", description="Test role")
        repo.save(role)

        with pytest.raises(
            EntityValidationError,
            match="Role name is required.",
        ):
            role.update_role(new_name="")
