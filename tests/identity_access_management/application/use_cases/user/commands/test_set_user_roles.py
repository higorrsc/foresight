from copy import deepcopy

import pytest

from src.identity_access_management.application.use_cases.user.commands import (
    SetUserRolesInputDTO,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities import Role, User
from src.identity_access_management.domain.exceptions import (
    InsufficientPermissionError,
    RoleNotFoundError,
)


class TestSetUserRolesUseCase:
    """
    Test suite for the SetUserRolesUseCase.
    """

    def test_admin_can_set_roles_for_user(
        self,
        set_user_roles_use_case,
        user_in_memory_repo,
        role_in_memory_repo,
        admin_actor: User,
        guest_actor: User,
    ):
        """
        Test if an admin can set roles for a user.
        """
        admin_actor.permissions.add(AppPermission.USER_SET_ROLES)

        role_in_memory_repo.save(
            Role(
                name="editor",
                description="Editor role",
                tenant_id=admin_actor.tenant_id,
            )
        )

        user_in_memory_repo.save(deepcopy(admin_actor))
        user_in_memory_repo.save(deepcopy(guest_actor))

        input_dto = SetUserRolesInputDTO(
            actor=admin_actor,
            user_id_to_update=guest_actor.id,
            role_names=["editor"],
        )

        set_user_roles_use_case.execute(input_dto)

        updated_guest = user_in_memory_repo.get_by_id(
            guest_actor.id, admin_actor.tenant_id
        )
        assert updated_guest.roles == {"editor"}
        assert updated_guest.updated_by == admin_actor.id

    def test_guest_cannot_set_roles(
        self,
        set_user_roles_use_case,
        user_in_memory_repo,
        guest_actor: User,
    ):
        """
        Test if a guest user cannot set roles.
        """
        user_in_memory_repo.save(deepcopy(guest_actor))  # Não tem a permissão

        input_dto = SetUserRolesInputDTO(
            actor=guest_actor, user_id_to_update=guest_actor.id, role_names=["admin"]
        )

        with pytest.raises(
            InsufficientPermissionError,
            match="User does not have permission",
        ):
            set_user_roles_use_case.execute(input_dto)

    def test_set_non_existent_role_raises_error(
        self,
        set_user_roles_use_case,
        user_in_memory_repo,
        admin_actor: User,
    ):
        """
        Test if setting a non-existent role raises an error.
        """

        admin_actor.permissions.add(AppPermission.USER_SET_ROLES)
        user_in_memory_repo.save(deepcopy(admin_actor))

        input_dto = SetUserRolesInputDTO(
            actor=admin_actor,
            user_id_to_update=admin_actor.id,
            role_names=["fake_role"],
        )

        with pytest.raises(
            RoleNotFoundError,
            match="Role 'fake_role' not found.",
        ):
            set_user_roles_use_case.execute(input_dto)
