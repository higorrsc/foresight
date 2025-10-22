from uuid import uuid4

import pytest

from src.core.application.use_cases.role import InvalidRoleError, RoleNotFoundError
from src.core.application.use_cases.role.commands import (
    UpdateRoleRequestDTO,
    UpdateRoleUseCase,
)
from src.core.domain.entities import Role
from src.core.infrastructure.repositories._shared import InMemoryRepository


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
        use_case = UpdateRoleUseCase(repository=repo)

        role = Role(name="Test", description="Test role")
        repo.save(role)

        input_dto = UpdateRoleRequestDTO(
            id=role.id,
            name="Updated",
            description="Updated role",
        )

        output = use_case.execute(input_dto)

        assert output.name == "Updated"
        assert output.description == "Updated role"

    def test_update_role_with_invalid_name(self, role_in_memory_repository):
        """
        Test update role with invalid name.
        """

        repo = role_in_memory_repository
        use_case = UpdateRoleUseCase(repository=repo)

        role = Role(name="Test", description="Test role")
        repo.save(role)

        input_dto = UpdateRoleRequestDTO(
            id=role.id,
            name="a" * 101,
            description="Updated role",
        )

        with pytest.raises(
            InvalidRoleError,
            match="Role name must be at most 100 characters long.",
        ):
            use_case.execute(input_dto)

    def test_update_role_with_invalid_id(self, role_in_memory_repository):
        """ ""
        Test update role with invalid id.
        """

        repo = role_in_memory_repository
        use_case = UpdateRoleUseCase(repository=repo)

        role = Role(name="Test", description="Test role")
        repo.save(role)

        invalid_id = uuid4()

        input_dto = UpdateRoleRequestDTO(
            id=invalid_id,
            name="Updated",
            description="Updated role",
        )

        with pytest.raises(
            RoleNotFoundError,
            match=f"Role with id {invalid_id} not found.",
        ):
            use_case.execute(input_dto)
