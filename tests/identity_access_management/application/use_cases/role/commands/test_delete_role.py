from uuid import uuid4

import pytest

from src.identity_access_management.application.use_cases.role import RoleNotFoundError
from src.identity_access_management.application.use_cases.role.commands import (
    DeleteRoleUseCase,
)
from src.identity_access_management.application.use_cases.role.exceptions import (
    RoleDeletionIntegrityError,
)
from src.identity_access_management.domain.entities import Role
from src.identity_access_management.domain.entities.user import User, hash_password
from src.shared_kernel.application._shared.use_cases.commands import (
    DeleteRequestInputDTO,
)
from tests.fakes import RoleInMemoryRepository, UserInMemoryRepository


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

    @pytest.fixture
    def user_in_memory_repository(self):
        """
        Fixture that represents an in-memory repository for testing purposes.
        """

        return UserInMemoryRepository()

    def test_delete_existing_role_without_associated_users(
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

        use_case = DeleteRoleUseCase(
            role_repo,
            user_repo,
        )

        role_to_delete = Role(
            name="Role to Delete",
            description="Description",
            tenant_id=admin_actor.tenant_id,
        )
        role_repo.save(role_to_delete)

        input_dto = DeleteRequestInputDTO(
            id=role_to_delete.id,
            actor=admin_actor,
        )

        use_case.execute(input_dto)

        found_role = role_repo.get_by_id(
            role_to_delete.id,
            admin_actor.tenant_id,
        )
        assert found_role.is_active is False
        assert found_role.deleted_at is not None

    def test_delete_non_existent_role_raises_error(
        self,
        role_in_memory_repository,
        user_in_memory_repository,
        admin_actor,
    ):
        """
        Test deleting a non-existent role raises RoleNotFoundError.
        """

        role_repo = role_in_memory_repository
        user_repo = user_in_memory_repository

        use_case = DeleteRoleUseCase(
            role_repo,
            user_repo,
        )

        non_existent_id = uuid4()
        input_dto = DeleteRequestInputDTO(
            id=non_existent_id,
            actor=admin_actor,
        )

        with pytest.raises(
            RoleNotFoundError,
            match=f"Role with ID '{non_existent_id}' not found.",
        ):
            use_case.execute(input_dto)

    def test_delete_role_with_associated_user_raises_error(
        self,
        role_in_memory_repository,
        user_in_memory_repository,
        admin_actor,
    ):
        """
        Test deleting a role with associated users raises RoleDeletionIntegrityError.
        """

        role_repo = role_in_memory_repository
        user_repo = user_in_memory_repository

        use_case = DeleteRoleUseCase(
            role_repo,
            user_repo,
        )

        role_to_delete = Role(
            name="deletable_role",
            description="Description",
            tenant_id=admin_actor.tenant_id,
        )
        role_repo.save(role_to_delete)

        user_associated = User(
            username="user_associated",
            hashed_password=hash_password("password123"),
            tenant_id=admin_actor.tenant_id,
            roles={role_to_delete.id},  # type: ignore
        )
        user_repo.save(user_associated)

        users_count = user_repo.count_users_by_role(role_to_delete.id)
        assert users_count == 1

        with pytest.raises(
            RoleDeletionIntegrityError,
            match=(
                f"Cannot delete role '{role_to_delete.name}' "
                f"because it is assigned to {users_count} users."
            ),
        ):
            use_case.execute(
                DeleteRequestInputDTO(
                    id=role_to_delete.id,
                    actor=admin_actor,
                )
            )
