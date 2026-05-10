from uuid import uuid4

import pytest

from src.core.application.use_cases.commands import (
    DeleteRequestInputDTO,
    RestoreRequestInputDTO,
)
from src.identity_access_management.application.use_cases.role.commands import (
    DeleteRoleUseCase,
    RestoreRoleUseCase,
)
from src.identity_access_management.domain.entities import Role
from src.identity_access_management.domain.exceptions import RoleNotFoundError


class TestRestoreRoleUseCase:
    """
    Test the RestoreRoleUseCase.
    """

    async def test_restore_role(
        self,
        role_in_memory_repo,
        user_in_memory_repo,
        admin_actor,
    ):
        """
        Test deleting an existing role.
        """

        delete_use_case = DeleteRoleUseCase(
            role_in_memory_repo,
            user_in_memory_repo,
        )

        role_to_delete = Role(
            name="Role to Delete",
            description="Description",
            tenant_id=admin_actor.tenant_id,
        )
        await role_in_memory_repo.save(role_to_delete)

        await delete_use_case.execute(
            DeleteRequestInputDTO(
                id=role_to_delete.id,
                actor=admin_actor,
            )
        )

        found_role = await role_in_memory_repo.get_by_id(
            role_to_delete.id,
            admin_actor.tenant_id,
        )
        assert found_role.is_active is False
        assert found_role.deleted_at is not None

        # Restore the role
        restore_use_case = RestoreRoleUseCase(role_in_memory_repo)
        await restore_use_case.execute(
            RestoreRequestInputDTO(
                id=role_to_delete.id,
                actor=admin_actor,
            )
        )

        found_role = await role_in_memory_repo.get_by_id(
            role_to_delete.id,
            admin_actor.tenant_id,
        )
        assert found_role.is_active is True
        assert found_role.deleted_at is None

    async def test_restore_non_existent_role_raises_error(
        self,
        role_in_memory_repo,
        admin_actor,
    ):
        """
        Test deleting a non-existent role raises RoleNotFoundError.
        """

        use_case = RestoreRoleUseCase(role_in_memory_repo)

        non_existent_id = uuid4()
        input_dto = RestoreRequestInputDTO(
            id=non_existent_id,
            actor=admin_actor,
        )

        with pytest.raises(
            RoleNotFoundError,
            match="Role to restore not found in this tenant.",
        ):
            await use_case.execute(input_dto)
