import pytest

from src.identity_access_management.application.use_cases.user import (
    InvalidPasswordError,
    UserNotFoundError,
)
from src.identity_access_management.application.use_cases.user.commands import (
    AuthenticateUserInputDTO,
    AuthenticateUserUseCase,
)
from src.identity_access_management.domain.entities import User
from src.identity_access_management.domain.entities.user import hash_password
from tests.fakes.in_memory_repository import UserInMemoryRepository


class TestAuthenticateUserUseCase:
    """
    Test suite for the AuthenticateUserUseCase.
    """

    @pytest.fixture
    def user_in_memory_repository(self):
        """
        Fixture that represents an in-memory repository for testing purposes.
        """

        return UserInMemoryRepository()

    def test_authenticate_user_successfully(
        self,
        user_in_memory_repository,
    ):
        """
        Test authenticate user successfully.
        """

        plain_password = "StrongPassword123"
        user = User(
            username="testuser",
            hashed_password=hash_password(plain_password),
        )
        user_in_memory_repository.save(user)

        use_case = AuthenticateUserUseCase(repository=user_in_memory_repository)

        input_dto = AuthenticateUserInputDTO(
            username="testuser",
            password=plain_password,
        )

        authenticated_user = use_case.execute(input_dto)

        assert authenticated_user is not None
        assert authenticated_user.username == "testuser"

    def test_authenticate_user_with_invalid_username_raises_error(
        self,
        user_in_memory_repository,
    ):
        """
        Test authenticate user with invalid username.
        """

        use_case = AuthenticateUserUseCase(repository=user_in_memory_repository)

        input_dto = AuthenticateUserInputDTO(
            username="nonexistentuser",
            password="anypassword",
        )

        with pytest.raises(
            UserNotFoundError,
            match="Invalid username or password",
        ):
            use_case.execute(input_dto)

    def test_authenticate_user_with_invalid_password_raises_error(
        self,
        user_in_memory_repository,
    ):
        """
        Test authenticate user with invalid password.
        """

        plain_password = "StrongPassword123"
        user = User(
            username="testuser",
            hashed_password=hash_password(plain_password),
        )
        user_in_memory_repository.save(user)

        use_case = AuthenticateUserUseCase(repository=user_in_memory_repository)

        input_dto = AuthenticateUserInputDTO(
            username="testuser",
            password="WeakPassword",
        )

        with pytest.raises(
            InvalidPasswordError,
            match="Invalid username or password",
        ):
            use_case.execute(input_dto)

    def test_authenticate_inactive_user_raises_error(
        self,
        user_in_memory_repository,
    ):
        """
        Test authenticate inactive user.
        """

        user = User(
            username="inactive_user",
            hashed_password=hash_password("password123"),
            is_active=False,
        )
        user_in_memory_repository.save(user)

        input_dto = AuthenticateUserInputDTO(
            username="inactive_user",
            password="password123",
        )

        use_case = AuthenticateUserUseCase(repository=user_in_memory_repository)

        with pytest.raises(
            UserNotFoundError,
            match="User account is inactive.",
        ):
            use_case.execute(input_dto)
