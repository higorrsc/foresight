from copy import deepcopy

import pytest

from src.identity_access_management.application.use_cases.user import (
    InvalidPasswordError,
)
from src.identity_access_management.application.use_cases.user.commands import (
    ChangePasswordInputDTO,
    ChangePasswordUseCase,
)
from src.identity_access_management.application.use_cases.user.exceptions import (
    InsufficientPermissionError,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities.user import User, hash_password
from tests.fakes.in_memory_repository import UserInMemoryRepository


@pytest.fixture
def user_repo():
    """
    Fixture that represents a user repository.
    """

    return UserInMemoryRepository()


@pytest.fixture
def change_password_use_case(user_repo):
    """
    Fixture that represents a ChangePasswordUseCase.
    """

    return ChangePasswordUseCase(user_repo)


class TestChangePasswordUseCase:
    """
    Test suite for the ChangePasswordUseCase.
    """

    def test_user_can_change_own_password(
        self,
        change_password_use_case,
        user_repo,
        guest_actor: User,
    ):
        """
        Test if a user can change their own password.
        """

        guest_actor_with_hash = deepcopy(guest_actor)
        guest_actor_with_hash.hashed_password = hash_password("foresight_guest")
        user_repo.save(guest_actor_with_hash)

        input_dto = ChangePasswordInputDTO(
            actor=guest_actor_with_hash,
            user_id_to_change=guest_actor_with_hash.id,
            old_password="foresight_guest",
            new_password="new_strong_password_123",
        )

        change_password_use_case.execute(input_dto)

        updated_user = user_repo.get_by_id(guest_actor.id, guest_actor.tenant_id)
        assert updated_user.verify_password("new_strong_password_123") is True
        assert updated_user.updated_by == guest_actor.id

    def test_admin_can_change_other_user_password_without_old_password(
        self,
        change_password_use_case,
        user_repo,
        admin_actor: User,
        guest_actor: User,
    ):
        """
        Test if an admin can change the password of another user without providing
        the old password.
        """

        admin_actor.permissions.add(AppPermission.USER_CHANGE_PASSWORD)
        user_repo.save(deepcopy(admin_actor))
        user_repo.save(deepcopy(guest_actor))

        input_dto = ChangePasswordInputDTO(
            actor=admin_actor,
            user_id_to_change=guest_actor.id,
            old_password="--qualquer-coisa-irrelevante--",  # Admin não precisa de saber
            new_password="admin_reset_password",
        )

        change_password_use_case.execute(input_dto)

        updated_guest = user_repo.get_by_id(guest_actor.id, admin_actor.tenant_id)
        assert updated_guest.verify_password("admin_reset_password") is True
        assert updated_guest.updated_by == admin_actor.id

    def test_change_password_with_incorrect_old_password_raises_error(
        self,
        change_password_use_case,
        user_repo,
        guest_actor: User,
    ):
        """
        Test if changing the password with an incorrect old password raises an error.
        """

        guest_actor_with_hash = deepcopy(guest_actor)
        guest_actor_with_hash.hashed_password = hash_password("correct_old_password")
        user_repo.save(guest_actor_with_hash)

        input_dto = ChangePasswordInputDTO(
            actor=guest_actor_with_hash,
            user_id_to_change=guest_actor_with_hash.id,
            old_password="wrong_old_password",
            new_password="new_password",
        )

        with pytest.raises(InvalidPasswordError, match="Invalid old password."):
            change_password_use_case.execute(input_dto)

    def test_user_cannot_change_other_user_password(
        self,
        change_password_use_case,
        user_repo,
        guest_actor: User,
        admin_actor: User,
    ):
        """
        Testa que um utilizador comum não pode alterar a senha de outro.
        """
        user_repo.save(deepcopy(admin_actor))
        user_repo.save(deepcopy(guest_actor))  # guest_actor não tem a permissão

        input_dto = ChangePasswordInputDTO(
            actor=guest_actor,
            user_id_to_change=admin_actor.id,
            old_password="---",
            new_password="hacked_asdf",
        )

        with pytest.raises(
            InsufficientPermissionError,
            match="User does not have permission to change another user's password.",
        ):
            change_password_use_case.execute(input_dto)
