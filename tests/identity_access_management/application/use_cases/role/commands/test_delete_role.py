from uuid import uuid4

import pytest

from src.identity_access_management.application.use_cases.role import RoleNotFoundError
from src.identity_access_management.application.use_cases.role.commands import (
    DeleteRoleUseCase,
)
from src.identity_access_management.domain.entities import Role
from src.shared_kernel.application._shared.use_cases.commands import (
    DeleteRequestInputDTO,
)
from tests.fakes import RoleInMemoryRepository


class TestDeleteRoleUseCase:
    """
    Test the DeleteRoleUseCase.
    """

    @pytest.fixture
    def role_in_memory_repository(self):
        """
        Fixture that represents an in-memory repository for testing purposes.
        """

        return RoleInMemoryRepository()

    def test_delete_existing_role(self, role_in_memory_repository, admin_actor):
        """
        Test deleting an existing role.
        """

        repo = role_in_memory_repository
        use_case = DeleteRoleUseCase(repository=repo)

        role_to_delete = Role(
            name="Role to Delete",
            description="Description",
            tenant_id=admin_actor.tenant_id,
        )
        repo.save(role_to_delete)

        input_dto = DeleteRequestInputDTO(
            id=role_to_delete.id,
            actor=admin_actor,
        )
        use_case.execute(input_dto)

        found_role = repo.get_by_id(
            role_to_delete.id,
            admin_actor.tenant_id,
        )
        assert found_role is None

    def test_delete_non_existent_role_raises_error(
        self, role_in_memory_repository, admin_actor
    ):
        """
        Test deleting a non-existent role raises RoleNotFoundError.
        """

        repo = role_in_memory_repository
        use_case = DeleteRoleUseCase(repository=repo)

        non_existent_id = uuid4()
        input_dto = DeleteRequestInputDTO(
            id=non_existent_id,
            actor=admin_actor,
        )

        with pytest.raises(
            RoleNotFoundError,
            match="Role with given ID not found.",
        ):
            use_case.execute(input_dto)
