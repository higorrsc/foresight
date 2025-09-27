import pytest

from src.core.application.use_cases.user import (
    CreateUserInputDTO,
    CreateUserUseCase,
    InvalidUserError,
    UsernameAlreadyExistsError,
)
from src.core.domain.entities import User
from src.core.tests.fakes import UserInMemoryRepository


class TestCreateUserUseCase:
    """
    Test suite for the CreateUserUseCase.
    """

    @pytest.fixture
    def user_in_memory_repository(self):
        """
        Fixture that represents an in-memory repository for testing purposes.
        """

        return UserInMemoryRepository()

    def test_create_user_with_valid_data(self, user_in_memory_repository):
        """
        Test create user with valid data.
        """

        repo = user_in_memory_repository
        use_case = CreateUserUseCase(repository=repo)

        input_dto = CreateUserInputDTO(
            username="testuser",
            password="StrongPassword123",
        )

        output_dto = use_case.execute(input_dto)

        assert output_dto is not None
        assert output_dto.username == "testuser"

        saved_user = repo.get_by_id(output_dto.id)
        assert saved_user is not None
        assert saved_user.username == "testuser"
        assert saved_user.verify_password("StrongPassword123")

    def test_create_user_with_existing_username_raises_error(
        self, user_in_memory_repository
    ):
        """
        Test create user with existing username.
        """

        repo = user_in_memory_repository

        existing_user = User(
            username="existinguser",
            hashed_password="somehash",
        )
        repo.save(existing_user)

        use_case = CreateUserUseCase(repository=repo)

        input_dto = CreateUserInputDTO(
            username="existinguser",
            password="anypassword",
        )

        with pytest.raises(
            UsernameAlreadyExistsError,
            match="Username 'existinguser' already exists.",
        ):
            use_case.execute(input_dto)

    def test_create_user_with_invalid_domain_data_raises_error(
        self, user_in_memory_repository
    ):
        """
        Testa que a exceção de validação do domínio é corretamente propagada.
        """
        repo = user_in_memory_repository
        use_case = CreateUserUseCase(repository=repo)

        input_dto = CreateUserInputDTO(
            username="",
            password="anypassword",
        )

        with pytest.raises(
            InvalidUserError,
            match="Invalid user data: Username is required.",
        ):
            use_case.execute(input_dto)
