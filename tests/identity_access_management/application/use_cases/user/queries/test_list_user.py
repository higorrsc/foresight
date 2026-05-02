from copy import deepcopy
from uuid import uuid4

import pytest

from src.core.application.use_cases.queries import ListRequestInputDTO
from src.identity_access_management.application.use_cases.permission import (
    InsufficientPermissionError,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities.user import User


class TestListUserUseCase:
    """
    Test suite for the ListUserUseCase.
    """

    def test_list_users_with_permission(
        self,
        list_user_use_case,
        user_in_memory_repo,
        admin_actor: User,
        guest_actor: User,
    ):
        """
        Test list users with permission.
        """
        admin_actor.permissions.add(AppPermission.USER_READ)

        user_in_memory_repo.save(deepcopy(admin_actor))
        user_in_memory_repo.save(deepcopy(guest_actor))

        other_tenant_user = User(
            username="other_tenant_user",
            hashed_password="pw",
            tenant_id=uuid4(),
        )
        user_in_memory_repo.save(other_tenant_user)

        input_dto = ListRequestInputDTO(actor=admin_actor)
        result = list_user_use_case.execute(input_dto)

        assert result.meta.total_items == 2
        assert result.data[0].username == admin_actor.username
        assert result.data[1].username == guest_actor.username

    def test_list_users_without_permission_raises_error(
        self,
        list_user_use_case,
        guest_actor: User,
    ):
        """
        Test list users without permission raises error.
        """
        input_dto = ListRequestInputDTO(actor=guest_actor)

        with pytest.raises(
            InsufficientPermissionError,
            match="User does not have permission",
        ):
            list_user_use_case.execute(input_dto)
