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

    def test_authenticate_user_successfully(self, user_in_memory_repository):
        """
        Test authenticate user successfully.
        """

        repo = user_in_memory_repository

        plain_password = "StrongPassword123"
        user = User(
            username="testuser",
            hashed_password=hash_password(plain_password),
        )
        repo.save(user)

        use_case = AuthenticateUserUseCase(repository=repo)

        input_dto = AuthenticateUserInputDTO(
            username="testuser",
            password=plain_password,
        )

        authenticated_user = use_case.execute(input_dto)

        assert authenticated_user is not None
        assert authenticated_user.username == "testuser"

    def test_authenticate_user_with_invalid_username_raises_error(
        self, user_in_memory_repository
    ):
        """
        Test authenticate user with invalid username.
        """

        repo = user_in_memory_repository
        use_case = AuthenticateUserUseCase(repository=repo)

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
        self, user_in_memory_repository
    ):
        """
        Test authenticate user with invalid password.
        """

        repo = user_in_memory_repository

        plain_password = "StrongPassword123"
        user = User(
            username="testuser",
            hashed_password=hash_password(plain_password),
        )
        repo.save(user)

        use_case = AuthenticateUserUseCase(repository=repo)

        input_dto = AuthenticateUserInputDTO(
            username="testuser",
            password="WeakPassword",
        )

        with pytest.raises(
            InvalidPasswordError,
            match="Invalid username or password",
        ):
            use_case.execute(input_dto)
