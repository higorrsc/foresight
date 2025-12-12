from copy import deepcopy
from uuid import uuid4

import pytest

from src.identity_access_management.application.use_cases.permission import (
    InsufficientPermissionError,
)
from src.identity_access_management.application.use_cases.user import UserNotFoundError
from src.identity_access_management.application.use_cases.user.queries import (
    GetUserByIdUseCase,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities.user import User
from src.shared_kernel.application._shared.use_cases.queries import (
    GetByIdRequestInputDTO,
)
from tests.fakes.in_memory_repository import UserInMemoryRepository


@pytest.fixture
def user_repo():
    """
    Fixture that represents an in-memory repository for testing purposes.
    """

    return UserInMemoryRepository()


@pytest.fixture
def get_user_by_id_use_case(user_repo):
    """
    Fixture that represents a GetUserByIdUseCase for testing purposes.
    """

    return GetUserByIdUseCase(repository=user_repo)


class TestGetUserByIdUseCase:
    """
    Test suite for the GetUserByIdUseCase.
    """

    def test_admin_can_get_user_by_id(
        self,
        get_user_by_id_use_case,
        user_repo,
        admin_actor: User,
        guest_actor: User,
    ):
        """
        Test if admin can get user by id.
        """

        admin_actor.permissions.add(AppPermission.USER_READ)
        user_repo.save(deepcopy(admin_actor))
        user_repo.save(deepcopy(guest_actor))

        input_dto = GetByIdRequestInputDTO(
            actor=admin_actor,
            id=guest_actor.id,
        )

        result_user = get_user_by_id_use_case.execute(input_dto)

        assert result_user is not None
        assert result_user.id == guest_actor.id
        assert result_user.username == guest_actor.username

    def test_get_user_without_permission_raises_error(
        self,
        get_user_by_id_use_case,
        user_repo,
        guest_actor: User,
    ):
        """
        Test if get user without permission raises error.
        """

        user_repo.save(deepcopy(guest_actor))

        input_dto = GetByIdRequestInputDTO(
            actor=guest_actor,
            id=guest_actor.id,
        )

        with pytest.raises(
            InsufficientPermissionError,
            match="User does not have permission",
        ):
            get_user_by_id_use_case.execute(input_dto)

    def test_get_non_existent_user_raises_error(
        self,
        get_user_by_id_use_case,
        user_repo,
        admin_actor: User,
    ):
        """
        Testa que buscar um ID inexistente levanta UserNotFoundError.
        """
        admin_actor.permissions.add(AppPermission.USER_READ)
        user_repo.save(deepcopy(admin_actor))

        input_dto = GetByIdRequestInputDTO(
            actor=admin_actor,
            id=uuid4(),
        )

        with pytest.raises(
            UserNotFoundError,
            match="not found in this tenant",
        ):
            get_user_by_id_use_case.execute(input_dto)

    def test_get_user_from_other_tenant_raises_error(
        self,
        get_user_by_id_use_case,
        user_repo,
        admin_actor: User,
    ):
        """
        Test if getting a user from another tenant raises an error.
        """

        admin_actor.permissions.add(AppPermission.USER_READ)
        user_repo.save(deepcopy(admin_actor))

        other_tenant_user = User(
            username="other_tenant_user",
            hashed_password="johnDoeNew",
            tenant_id=uuid4(),
        )
        user_repo.save(other_tenant_user)

        input_dto = GetByIdRequestInputDTO(
            actor=admin_actor,
            id=other_tenant_user.id,
        )

        with pytest.raises(
            UserNotFoundError,
            match="not found in this tenant",
        ):
            get_user_by_id_use_case.execute(input_dto)
