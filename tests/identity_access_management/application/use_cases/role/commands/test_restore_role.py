from uuid import uuid4

import pytest

from src.identity_access_management.application.use_cases.role import RoleNotFoundError
from src.identity_access_management.application.use_cases.role.commands import (
    DeleteRoleUseCase,
    RestoreRoleUseCase,
)
from src.identity_access_management.domain.entities import Role
from src.shared_kernel.application._shared.use_cases.commands import (
    DeleteRequestInputDTO,
    RestoreRequestInputDTO,
)
from tests.fakes import RoleInMemoryRepository, UserInMemoryRepository


class TestRestoreRoleUseCase:
    """
    Test the RestoreRoleUseCase.
    """

    @pytest.fixture
    def role_in_memory_repository(self):
        """
        Fixture that represents an in-memory repository for testing purposes.
        """

        return RoleInMemoryRepository()

    @pytest.fixture
    def user_in_memory_repository(self):
        """
        Fixture that represents an in-memory repository for testing purposes.
        """

        return UserInMemoryRepository()

    def test_restore_role(
        self,
        role_in_memory_repository,
        user_in_memory_repository,
        admin_actor,
    ):
        """
        Test deleting an existing role.
        """

        role_repo = role_in_memory_repository
        user_repo = user_in_memory_repository

        delete_use_case = DeleteRoleUseCase(
            role_repo,
            user_repo,
        )

        role_to_delete = Role(
            name="Role to Delete",
            description="Description",
            tenant_id=admin_actor.tenant_id,
        )
        role_repo.save(role_to_delete)

        delete_use_case.execute(
            DeleteRequestInputDTO(
                id=role_to_delete.id,
                actor=admin_actor,
            )
        )

        found_role = role_repo.get_by_id(
            role_to_delete.id,
            admin_actor.tenant_id,
        )
        assert found_role.is_active is False
        assert found_role.deleted_at is not None

        # Restore the role
        restore_use_case = RestoreRoleUseCase(role_repo)
        restore_use_case.execute(
            RestoreRequestInputDTO(
                id=role_to_delete.id,
                actor=admin_actor,
            )
        )

        found_role = role_repo.get_by_id(
            role_to_delete.id,
            admin_actor.tenant_id,
        )
        assert found_role.is_active is True
        assert found_role.deleted_at is None

    def test_restore_non_existent_role_raises_error(
        self,
        role_in_memory_repository,
        admin_actor,
    ):
        """
        Test deleting a non-existent role raises RoleNotFoundError.
        """

        role_repo = role_in_memory_repository

        use_case = RestoreRoleUseCase(role_repo)

        non_existent_id = uuid4()
        input_dto = RestoreRequestInputDTO(
            id=non_existent_id,
            actor=admin_actor,
        )

        with pytest.raises(
            RoleNotFoundError,
            match="Role to restore not found in this tenant.",
        ):
            use_case.execute(input_dto)
