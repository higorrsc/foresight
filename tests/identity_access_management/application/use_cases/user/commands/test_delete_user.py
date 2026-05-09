from copy import deepcopy
from uuid import uuid4

import pytest

from src.core.application.use_cases.commands import DeleteRequestInputDTO
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities.user import User
from src.identity_access_management.domain.exceptions import (
    InsufficientPermissionError,
    InvalidUserError,
    UserNotFoundError,
)


class TestDeleteUserUseCase:
    """
    Test suite for the DeleteUserUseCase.
    """

    async def test_admin_can_delete_other_user(
        self,
        delete_user_use_case,
        user_in_memory_repo,
        admin_actor: User,
        guest_actor: User,
    ):
        """
        Test if an admin can delete another user.
        """

        admin_actor.permissions.add(AppPermission.USER_DELETE)
        await user_in_memory_repo.save(deepcopy(admin_actor))
        await user_in_memory_repo.save(deepcopy(guest_actor))

        input_dto = DeleteRequestInputDTO(actor=admin_actor, id=guest_actor.id)

        await delete_user_use_case.execute(input_dto)

        deleted_user = await user_in_memory_repo.get_by_id(
            guest_actor.id, admin_actor.tenant_id
        )
        assert deleted_user is not None
        assert deleted_user.is_active is False
        assert deleted_user.deleted_at is not None
        assert deleted_user.updated_by == admin_actor.id

    async def test_user_cannot_delete_without_permission(
        self,
        delete_user_use_case,
        user_in_memory_repo,
        admin_actor: User,
        guest_actor: User,
    ):
        """
        Test if a user without permission cannot delete another user.
        """
        await user_in_memory_repo.save(deepcopy(admin_actor))
        await user_in_memory_repo.save(deepcopy(guest_actor))

        input_dto = DeleteRequestInputDTO(actor=guest_actor, id=admin_actor.id)

        with pytest.raises(
            InsufficientPermissionError,
            match="User does not have permission",
        ):
            await delete_user_use_case.execute(input_dto)

    async def test_user_cannot_delete_self(
        self,
        delete_user_use_case,
        user_in_memory_repo,
        admin_actor: User,
    ):
        """
        Test if a user cannot delete themselves.
        """
        admin_actor.permissions.add(AppPermission.USER_DELETE)
        await user_in_memory_repo.save(deepcopy(admin_actor))

        input_dto = DeleteRequestInputDTO(actor=admin_actor, id=admin_actor.id)

        with pytest.raises(
            InvalidUserError,
            match="User cannot delete their own account",
        ):
            await delete_user_use_case.execute(input_dto)

    async def test_delete_non_existent_user_raises_error(
        self,
        delete_user_use_case,
        user_in_memory_repo,
        admin_actor: User,
    ):
        """
        Test if deleting a non-existent user raises an error.
        """
        admin_actor.permissions.add(AppPermission.USER_DELETE)
        await user_in_memory_repo.save(deepcopy(admin_actor))

        input_dto = DeleteRequestInputDTO(actor=admin_actor, id=uuid4())

        with pytest.raises(
            UserNotFoundError,
            match="User to delete not found",
        ):
            await delete_user_use_case.execute(input_dto)
