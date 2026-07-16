import pytest

from src.identity_access_management.application.use_cases.user.commands import (
    AuthenticateUserInputDTO,
)
from src.identity_access_management.domain.entities import User
from src.identity_access_management.domain.entities.user import hash_password
from src.identity_access_management.domain.exceptions import (
    InvalidPasswordError,
    UserNotFoundError,
)


class TestAuthenticateUserUseCase:
    """
    Test suite for the AuthenticateUserUseCase.
    """

    async def test_authenticate_user_successfully(
        self,
        user_in_memory_repo,
        authenticate_user_use_case,
    ):
        """
        Test authenticate user successfully.
        """

        plain_password = "StrongPassword123"
        user = User(
            username="testuser",
            hashed_password=hash_password(plain_password),
        )
        await user_in_memory_repo.save(user)

        input_dto = AuthenticateUserInputDTO(
            username="testuser",
            password=plain_password,
        )

        authenticated_user = await authenticate_user_use_case.execute(input_dto)

        assert authenticated_user is not None
        assert authenticated_user.username == "testuser"

    async def test_authenticate_user_with_invalid_username_raises_error(
        self,
        authenticate_user_use_case,
    ):
        """
        Test authenticate user with invalid username.
        """

        input_dto = AuthenticateUserInputDTO(
            username="nonexistentuser",
            password="anypassword",
        )

        with pytest.raises(
            UserNotFoundError,
            match="Invalid username or password",
        ):
            await authenticate_user_use_case.execute(input_dto)

    async def test_authenticate_user_with_invalid_password_raises_error(
        self,
        user_in_memory_repo,
        authenticate_user_use_case,
    ):
        """
        Test authenticate user with invalid password.
        """

        plain_password = "StrongPassword123"
        user = User(
            username="testuser",
            hashed_password=hash_password(plain_password),
        )
        await user_in_memory_repo.save(user)

        input_dto = AuthenticateUserInputDTO(
            username="testuser",
            password="WeakPassword",
        )

        with pytest.raises(
            InvalidPasswordError,
            match="Invalid username or password",
        ):
            await authenticate_user_use_case.execute(input_dto)

    async def test_authenticate_inactive_user_raises_error(
        self,
        user_in_memory_repo,
        authenticate_user_use_case,
    ):
        """
        Test authenticate inactive user.
        """

        user = User(
            username="inactive_user",
            hashed_password=hash_password("password123"),
            is_active=False,
        )
        await user_in_memory_repo.save(user)

        input_dto = AuthenticateUserInputDTO(
            username="inactive_user",
            password="password123",
        )

        with pytest.raises(
            UserNotFoundError,
            match="User account is inactive.",
        ):
            await authenticate_user_use_case.execute(input_dto)
