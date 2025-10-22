from uuid import uuid4

import pytest

from src.core.application.use_cases.user import InvalidPasswordError, UserNotFoundError
from src.core.application.use_cases.user.commands import (
    ChangePasswordInputDTO,
    ChangePasswordUseCase,
)
from src.core.domain.entities import User, hash_password
from tests.core.fakes import UserInMemoryRepository


class TestChangePasswordUseCase:
    """
    Test suite for the ChangePasswordUseCase.
    """

    @pytest.fixture
    def user_repo(self):
        """
        Fixture that represents a user repository.
        """

        return UserInMemoryRepository()

    def test_change_password_successfully(self, user_repo):
        """
        Test change password successfully.
        """

        old_password = "old_strong_password"
        user = User(
            username="testuser",
            hashed_password=hash_password(old_password),
        )
        user_repo.save(user)

        use_case = ChangePasswordUseCase(repository=user_repo)

        input_dto = ChangePasswordInputDTO(
            user_id=user.id,
            old_password=old_password,
            new_password="new_very_strong_password",
        )

        use_case.execute(input_dto)

        updated_user = user_repo.get_by_id(user.id)
        assert updated_user is not None
        assert updated_user.verify_password("new_very_strong_password") is True
        assert updated_user.verify_password(old_password) is False

    def test_change_password_for_non_existent_user_raises_error(self, user_repo):
        """
        Test that UserNotFoundError is raised when trying to change
        the password of a non-existent user.
        """

        use_case = ChangePasswordUseCase(repository=user_repo)

        input_dto = ChangePasswordInputDTO(
            user_id=uuid4(),
            old_password="any",
            new_password="any",
        )

        with pytest.raises(
            UserNotFoundError,
            match="User not found.",
        ):
            use_case.execute(input_dto)

    def test_change_password_with_incorrect_old_password_raises_error(self, user_repo):
        """
        Test that InvalidPasswordError is raised when trying to change
        the password with an incorrect old password.
        """

        user = User(
            username="testuser",
            hashed_password=hash_password("correct_old_password"),
        )
        user_repo.save(user)

        use_case = ChangePasswordUseCase(repository=user_repo)

        input_dto = ChangePasswordInputDTO(
            user_id=user.id,
            old_password="wrong_old_password",
            new_password="new_password",
        )

        with pytest.raises(
            InvalidPasswordError,
            match="Invalid old password.",
        ):
            use_case.execute(input_dto)

    def test_change_password_with_invalid_new_password_raises_error(self, user_repo):
        """
        Test change password with invalid new password.
        """

        old_password = "old_strong_password"
        user = User(
            username="testuser",
            hashed_password=hash_password(old_password),
        )
        user_repo.save(user)

        use_case = ChangePasswordUseCase(repository=user_repo)

        input_dto = ChangePasswordInputDTO(
            user_id=user.id,
            old_password=old_password,
            new_password="short",
        )

        with pytest.raises(
            ValueError,
            match="New password must be at least 8 characters long.",
        ):
            use_case.execute(input_dto)
