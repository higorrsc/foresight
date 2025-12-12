from copy import deepcopy
from uuid import uuid4

import pytest

from src.identity_access_management.application.use_cases.permission import (
    InsufficientPermissionError,
)
from src.identity_access_management.application.use_cases.user.queries import (
    ListUserUseCase,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities.user import User
from src.shared_kernel.application._shared.use_cases.queries import ListRequestInputDTO
from tests.fakes import UserInMemoryRepository


@pytest.fixture
def user_repo():
    """
    Fixture that represents an in-memory repository for testing purposes.
    """

    return UserInMemoryRepository()


@pytest.fixture
def list_user_use_case(user_repo):
    """
    Fixture that represents a ListUserUseCase for testing purposes.
    """

    return ListUserUseCase(repository=user_repo)


class TestListUserUseCase:
    """
    Test suite for the ListUserUseCase.
    """

    def test_list_users_with_permission(
        self,
        list_user_use_case,
        user_repo,
        admin_actor: User,
        guest_actor: User,
    ):
        """
        Test list users with permission.
        """
        admin_actor.permissions.add(AppPermission.USER_READ)

        user_repo.save(deepcopy(admin_actor))
        user_repo.save(deepcopy(guest_actor))

        other_tenant_user = User(
            username="other_tenant_user",
            hashed_password="pw",
            tenant_id=uuid4(),
        )
        user_repo.save(other_tenant_user)

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
