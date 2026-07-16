from copy import deepcopy

import pytest

from src.identity_access_management.application.use_cases.user.commands import (
    SetUserPermissionsInputDTO,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities import Permission, User
from src.identity_access_management.domain.exceptions import (
    InsufficientPermissionError,
    PermissionNotFoundError,
)


class TestSetUserPermissionsUseCase:
    """
    Test suite for the SetUserPermissionsUseCase.
    """

    async def test_admin_can_set_permissions_for_user(
        self,
        set_user_permissions_use_case,
        user_in_memory_repo,
        permission_in_memory_repo,
        admin_actor: User,
        guest_actor: User,
    ):
        """
        Test if an admin can set permissions for a user.
        """
        admin_actor.permissions.add(AppPermission.USER_SET_PERMISSIONS)

        await permission_in_memory_repo.save(
            Permission(
                codename="admin:editor",
                description="Editor permission",
            )
        )

        await user_in_memory_repo.save(deepcopy(admin_actor))
        await user_in_memory_repo.save(deepcopy(guest_actor))

        input_dto = SetUserPermissionsInputDTO(
            actor=admin_actor,
            user_id_to_update=guest_actor.id,
            permissions_codes=["admin:editor"],
        )

        await set_user_permissions_use_case.execute(input_dto)

        updated_guest = await user_in_memory_repo.get_by_id(
            guest_actor.id, admin_actor.tenant_id
        )
        assert updated_guest.permissions == {"admin:editor"}
        assert updated_guest.updated_by == admin_actor.id

    async def test_guest_cannot_set_permissions(
        self,
        set_user_permissions_use_case,
        user_in_memory_repo,
        guest_actor: User,
    ):
        """
        Test if a guest user cannot set permissions.
        """
        await user_in_memory_repo.save(deepcopy(guest_actor))  # Não tem a permissão

        input_dto = SetUserPermissionsInputDTO(
            actor=guest_actor,
            user_id_to_update=guest_actor.id,
            permissions_codes=["admin"],
        )

        with pytest.raises(
            InsufficientPermissionError,
            match="User does not have permission",
        ):
            await set_user_permissions_use_case.execute(input_dto)

    async def test_set_non_existent_permission_raises_error(
        self,
        set_user_permissions_use_case,
        user_in_memory_repo,
        admin_actor: User,
    ):
        """
        Test if setting a non-existent permission raises an error.
        """

        admin_actor.permissions.add(AppPermission.USER_SET_PERMISSIONS)
        await user_in_memory_repo.save(deepcopy(admin_actor))

        input_dto = SetUserPermissionsInputDTO(
            actor=admin_actor,
            user_id_to_update=admin_actor.id,
            permissions_codes=["fake_permission"],
        )

        with pytest.raises(
            PermissionNotFoundError,
            match="Permission 'fake_permission' not found.",
        ):
            await set_user_permissions_use_case.execute(input_dto)
