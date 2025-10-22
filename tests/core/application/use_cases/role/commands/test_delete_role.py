from uuid import uuid4

import pytest

from src.core.application._shared.use_cases.commands import DeleteRequestInputDTO
from src.core.application.use_cases.role import RoleNotFoundError
from src.core.application.use_cases.role.commands import DeleteRoleUseCase
from src.core.domain.entities import Role
from src.core.infrastructure.repositories._shared import InMemoryRepository


class TestDeleteRoleUseCase:
    """
    Test the DeleteRoleUseCase.
    """

    @pytest.fixture
    def role_in_memory_repository(self):
        """
        Fixture that represents an in-memory repository for testing purposes.
        """

        return InMemoryRepository[Role]()

    def test_delete_existing_role(self, role_in_memory_repository):
        """
        Test deleting an existing role.
        """

        repo = role_in_memory_repository
        use_case = DeleteRoleUseCase(repository=repo)

        role_to_delete = Role(name="Role to Delete", description="Description")
        repo.save(role_to_delete)

        input_dto = DeleteRequestInputDTO(id=role_to_delete.id)
        use_case.execute(input_dto)

        assert repo.get_by_id(role_to_delete.id) is None

    def test_delete_non_existent_role_raises_error(self, role_in_memory_repository):
        """
        Test deleting a non-existent role raises RoleNotFoundError.
        """

        repo = role_in_memory_repository
        use_case = DeleteRoleUseCase(repository=repo)

        non_existent_id = uuid4()
        input_dto = DeleteRequestInputDTO(id=non_existent_id)

        with pytest.raises(
            RoleNotFoundError,
            match="Role with given ID not found.",
        ):
            use_case.execute(input_dto)
