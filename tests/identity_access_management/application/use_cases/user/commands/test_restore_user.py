from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.identity_access_management.application.use_cases.user import UserNotFoundError
from src.identity_access_management.application.use_cases.user.commands import (
    RestoreUserUseCase,
)
from src.identity_access_management.application.use_cases.user.exceptions import (
    InsufficientPermissionError,
    InvalidUserError,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities.user import User
from src.shared_kernel.application._shared.use_cases.commands import (
    RestoreRequestInputDTO,
)
from tests.fakes.in_memory_repository import UserInMemoryRepository


@pytest.fixture
def user_repo():
    """
    Fixture that represents an in-memory repository for testing purposes.
    """

    return UserInMemoryRepository()


@pytest.fixture
def restore_user_use_case(user_repo):
    """
    Fixture that represents a RestoreUserUseCase for testing purposes.
    """

    return RestoreUserUseCase(repository=user_repo)


class TestRestoreUserUseCase:
    """
    Test suite for the RestoreUserUseCase.
    """

    def test_admin_can_restore_other_user(
        self,
        restore_user_use_case,
        user_repo,
        admin_actor: User,
        guest_actor: User,
    ):
        """
        Test if an admin can restore another user.
        """

        admin_actor.permissions.add(AppPermission.USER_DELETE)
        user_repo.save(deepcopy(admin_actor))
        guest_actor.is_active = False
        guest_actor.deleted_at = datetime.now(timezone.utc)
        user_repo.save(deepcopy(guest_actor))

        input_dto = RestoreRequestInputDTO(actor=admin_actor, id=guest_actor.id)

        restore_user_use_case.execute(input_dto)

        restored_user = user_repo.get_by_id(guest_actor.id, admin_actor.tenant_id)
        assert restored_user is not None
        assert restored_user.is_active is True
        assert restored_user.deleted_at is None
        assert restored_user.updated_by == admin_actor.id

    def test_user_cannot_restore_without_permission(
        self,
        restore_user_use_case,
        user_repo,
        guest_actor: User,
        admin_actor: User,
    ):
        """
        Test if a user without permission cannot restore another user.
        """

        admin_actor.is_active = False
        admin_actor.deleted_at = datetime.now(timezone.utc)
        user_repo.save(deepcopy(admin_actor))
        user_repo.save(deepcopy(guest_actor))

        input_dto = RestoreRequestInputDTO(actor=guest_actor, id=admin_actor.id)

        with pytest.raises(
            InsufficientPermissionError,
            match="User does not have permission",
        ):
            restore_user_use_case.execute(input_dto)

    def test_user_cannot_restore_self(
        self,
        restore_user_use_case,
        user_repo,
        admin_actor: User,
    ):
        """
        Test if a user cannot restore themselves.
        """
        admin_actor.permissions.add(AppPermission.USER_DELETE)
        user_repo.save(deepcopy(admin_actor))

        input_dto = RestoreRequestInputDTO(actor=admin_actor, id=admin_actor.id)

        with pytest.raises(
            InvalidUserError,
            match="User cannot restore their own account",
        ):
            restore_user_use_case.execute(input_dto)

    def test_restore_non_existent_user_raises_error(
        self,
        restore_user_use_case,
        user_repo,
        admin_actor: User,
    ):
        """
        Test if deleting a non-existent user raises an error.
        """
        admin_actor.permissions.add(AppPermission.USER_DELETE)
        user_repo.save(deepcopy(admin_actor))

        input_dto = RestoreRequestInputDTO(actor=admin_actor, id=uuid4())

        with pytest.raises(
            UserNotFoundError,
            match="User to restore not found",
        ):
            restore_user_use_case.execute(input_dto)
