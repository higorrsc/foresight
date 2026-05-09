from copy import deepcopy
from uuid import uuid4

import pytest

from src.core.application.use_cases.queries import GetByIdRequestInputDTO
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities.user import User
from src.identity_access_management.domain.exceptions import (
    InsufficientPermissionError,
    UserNotFoundError,
)


class TestGetUserByIdUseCase:
    """
    Test suite for the GetUserByIdUseCase.
    """

    async def test_admin_can_get_user_by_id(
        self,
        get_user_by_id_use_case,
        user_in_memory_repo,
        admin_actor: User,
        guest_actor: User,
    ):
        """
        Test if admin can get user by id.
        """

        admin_actor.permissions.add(AppPermission.USER_READ)
        await user_in_memory_repo.save(deepcopy(admin_actor))
        await user_in_memory_repo.save(deepcopy(guest_actor))

        input_dto = GetByIdRequestInputDTO(
            actor=admin_actor,
            id=guest_actor.id,
        )

        result_user = await get_user_by_id_use_case.execute(input_dto)

        assert result_user is not None
        assert result_user.id == guest_actor.id
        assert result_user.username == guest_actor.username

    async def test_get_user_without_permission_raises_error(
        self,
        get_user_by_id_use_case,
        user_in_memory_repo,
        guest_actor: User,
    ):
        """
        Test if get user without permission raises error.
        """

        await user_in_memory_repo.save(deepcopy(guest_actor))

        input_dto = GetByIdRequestInputDTO(
            actor=guest_actor,
            id=guest_actor.id,
        )

        with pytest.raises(
            InsufficientPermissionError,
            match="User does not have permission",
        ):
            await get_user_by_id_use_case.execute(input_dto)

    async def test_get_non_existent_user_raises_error(
        self,
        get_user_by_id_use_case,
        user_in_memory_repo,
        admin_actor: User,
    ):
        """
        Testa que buscar um ID inexistente levanta UserNotFoundError.
        """
        admin_actor.permissions.add(AppPermission.USER_READ)
        await user_in_memory_repo.save(deepcopy(admin_actor))

        input_dto = GetByIdRequestInputDTO(
            actor=admin_actor,
            id=uuid4(),
        )

        with pytest.raises(
            UserNotFoundError,
            match="not found in this tenant",
        ):
            await get_user_by_id_use_case.execute(input_dto)

    async def test_get_user_from_other_tenant_raises_error(
        self,
        get_user_by_id_use_case,
        user_in_memory_repo,
        admin_actor: User,
    ):
        """
        Test if getting a user from another tenant raises an error.
        """

        admin_actor.permissions.add(AppPermission.USER_READ)
        await user_in_memory_repo.save(deepcopy(admin_actor))

        other_tenant_user = User(
            username="other_tenant_user",
            hashed_password="johnDoeNew",
            tenant_id=uuid4(),
        )
        await user_in_memory_repo.save(other_tenant_user)

        input_dto = GetByIdRequestInputDTO(
            actor=admin_actor,
            id=other_tenant_user.id,
        )

        with pytest.raises(
            UserNotFoundError,
            match="not found in this tenant",
        ):
            await get_user_by_id_use_case.execute(input_dto)
