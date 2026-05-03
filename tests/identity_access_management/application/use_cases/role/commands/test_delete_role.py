from uuid import uuid4

import pytest

from src.core.application.use_cases.commands import DeleteRequestInputDTO
from src.identity_access_management.domain.entities import Role
from src.identity_access_management.domain.entities.user import hash_password
from src.identity_access_management.domain.exceptions import (
    RoleDeletionIntegrityError,
    RoleNotFoundError,
)


class TestDeleteRoleUseCase:
    """
    Test the DeleteRoleUseCase.
    """

    def test_delete_existing_role_without_associated_users(
        self,
        role_in_memory_repo,
        user_in_memory_repo,
        delete_role_use_case_iam,
        admin_actor,
    ):
        """
        Test deleting an existing role.
        """

        role_to_delete = Role(
            name="Role to Delete",
            description="Description",
            tenant_id=admin_actor.tenant_id,
        )
        role_in_memory_repo.save(role_to_delete)

        input_dto = DeleteRequestInputDTO(
            id=role_to_delete.id,
            actor=admin_actor,
        )

        delete_role_use_case_iam.execute(input_dto)

        found_role = role_in_memory_repo.get_by_id(
            role_to_delete.id,
            admin_actor.tenant_id,
        )
        assert found_role.is_active is False
        assert found_role.deleted_at is not None

    def test_delete_non_existent_role_raises_error(
        self,
        delete_role_use_case_iam,
        admin_actor,
    ):
        """
        Test deleting a non-existent role raises RoleNotFoundError.
        """

        non_existent_id = uuid4()
        input_dto = DeleteRequestInputDTO(
            id=non_existent_id,
            actor=admin_actor,
        )

        with pytest.raises(
            RoleNotFoundError,
            match=f"Role with ID '{non_existent_id}' not found.",
        ):
            delete_role_use_case_iam.execute(input_dto)

    def test_delete_role_with_associated_user_raises_error(
        self,
        role_in_memory_repo,
        user_in_memory_repo,
        delete_role_use_case_iam,
        admin_actor,
    ):
        """
        Test deleting a role with associated users raises RoleDeletionIntegrityError.
        """

        role_to_delete = Role(
            name="deletable_role",
            description="Description",
            tenant_id=admin_actor.tenant_id,
        )
        role_in_memory_repo.save(role_to_delete)

        from src.identity_access_management.domain.entities.user import User

        user_associated = User(
            username="user_associated",
            hashed_password=hash_password("password123"),
            tenant_id=admin_actor.tenant_id,
            roles={role_to_delete.id},  # type: ignore
        )
        user_in_memory_repo.save(user_associated)

        users_count = user_in_memory_repo.count_users_by_role(role_to_delete.id)
        assert users_count == 1

        with pytest.raises(
            RoleDeletionIntegrityError,
            match=(
                f"Cannot delete role '{role_to_delete.name}' "
                f"because it is assigned to {users_count} users."
            ),
        ):
            delete_role_use_case_iam.execute(
                DeleteRequestInputDTO(
                    id=role_to_delete.id,
                    actor=admin_actor,
                )
            )
