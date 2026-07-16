from copy import deepcopy

import pytest

from src.identity_access_management.application.use_cases.user.commands import (
    UserProfileInputDTO,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities.user import User
from src.identity_access_management.domain.exceptions import (
    InsufficientPermissionError,
)


class TestUpdateUserProfileUseCase:
    """
    Test suite for the UpdateUserProfileUseCase.
    """

    async def test_user_can_update_own_profile(
        self,
        update_user_profile_use_case,
        user_in_memory_repo,
        guest_actor: User,
    ):
        """
        Test if a user can update their own profile.
        """

        await user_in_memory_repo.save(deepcopy(guest_actor))

        input_dto = UserProfileInputDTO(
            actor=guest_actor,
            user_id_to_update=guest_actor.id,
            first_name="Guesty",
        )

        await update_user_profile_use_case.execute(input_dto)

        updated_user = await user_in_memory_repo.get_by_id(
            guest_actor.id, guest_actor.tenant_id
        )
        assert updated_user.first_name == "Guesty"
        assert updated_user.updated_by == guest_actor.id

    async def test_admin_can_update_other_user_profile(
        self,
        update_user_profile_use_case,
        user_in_memory_repo,
        admin_actor: User,
        guest_actor: User,
    ):
        """
        Test if an admin can update the profile of another user.
        """

        admin_actor.permissions.add(AppPermission.USER_UPDATE)

        await user_in_memory_repo.save(deepcopy(admin_actor))
        await user_in_memory_repo.save(deepcopy(guest_actor))

        input_dto = UserProfileInputDTO(
            actor=admin_actor,
            user_id_to_update=guest_actor.id,
            last_name="McGuest",
        )

        await update_user_profile_use_case.execute(input_dto)

        updated_guest = await user_in_memory_repo.get_by_id(
            guest_actor.id, admin_actor.tenant_id
        )
        assert updated_guest.last_name == "McGuest"
        assert updated_guest.updated_by == admin_actor.id

    async def test_user_cannot_update_other_user_profile(
        self,
        update_user_profile_use_case,
        user_in_memory_repo,
        admin_actor: User,
        guest_actor: User,
    ):
        """
        Test if a user cannot update the profile of another user.
        """

        await user_in_memory_repo.save(deepcopy(admin_actor))
        await user_in_memory_repo.save(deepcopy(guest_actor))

        input_dto = UserProfileInputDTO(
            actor=guest_actor,
            user_id_to_update=admin_actor.id,
            first_name="Hacker",
        )

        with pytest.raises(
            InsufficientPermissionError,
            match="User does not have permission to update another user's profile.",
        ):
            await update_user_profile_use_case.execute(input_dto)
