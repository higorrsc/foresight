import pytest

from src.identity_access_management.application.use_cases.role import InvalidRoleError
from src.identity_access_management.application.use_cases.user import (
    InvalidUserError,
    UsernameAlreadyExistsError,
)
from src.identity_access_management.application.use_cases.user.commands import (
    CreateUserInputDTO,
    CreateUserUseCase,
)
from src.identity_access_management.domain.entities import Role, User
from tests.fakes import RoleInMemoryRepository, UserInMemoryRepository


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

    @pytest.fixture
    def role_in_memory_repository(self):
        """
        Fixture that represents a role repository.
        """

        repo = RoleInMemoryRepository()
        repo.save(Role(name="guest", description=""))

        return repo

    @pytest.fixture
    def empty_role_in_memory_repository(self):
        """
        Fixture that represents an empty role repository.
        """

        return RoleInMemoryRepository()

    def test_create_user_with_valid_data(
        self,
        user_in_memory_repository,
        role_in_memory_repository,
    ):
        """
        Test create user with valid data.
        """

        repo = user_in_memory_repository
        use_case = CreateUserUseCase(
            user_in_memory_repository,
            role_in_memory_repository,
        )

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
        self,
        user_in_memory_repository,
        role_in_memory_repository,
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

        use_case = CreateUserUseCase(
            user_in_memory_repository,
            role_in_memory_repository,
        )

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
        self,
        user_in_memory_repository,
        role_in_memory_repository,
    ):
        """
        Test create user with invalid domain data.
        """

        use_case = CreateUserUseCase(
            user_in_memory_repository,
            role_in_memory_repository,
        )

        input_dto = CreateUserInputDTO(
            username="",
            password="anypassword",
        )

        with pytest.raises(
            InvalidUserError,
            match="Invalid user data: Username is required.",
        ):
            use_case.execute(input_dto)

    def test_create_user_with_invalid_role_raises_error(
        self,
        user_in_memory_repository,
        role_in_memory_repository,
    ):
        """
        Test create user with invalid role.
        """

        use_case = CreateUserUseCase(
            user_in_memory_repository,
            role_in_memory_repository,
        )
        input_dto = CreateUserInputDTO(
            username="testuser",
            password="StrongPassword123",
            roles=["invalid_role"],
        )

        with pytest.raises(
            InvalidRoleError,
            match="Role 'invalid_role' does not exist.",
        ):
            use_case.execute(input_dto)

    def test_create_user_with_without_role_and_try_to_assign_guest_roles_raises_error(
        self,
        user_in_memory_repository,
        empty_role_in_memory_repository,
    ):
        """
        Test create user with valid data.
        """

        use_case = CreateUserUseCase(
            user_in_memory_repository,
            empty_role_in_memory_repository,
        )

        input_dto = CreateUserInputDTO(
            username="testuser",
            password="StrongPassword123",
        )

        with pytest.raises(
            RuntimeError,
            match="Default role 'guest' not found.",
        ):
            use_case.execute(input_dto)
