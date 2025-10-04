import pytest

from src.core.application.use_cases.user import (
    InvalidUserError,
    UpdateUserProfileUseCase,
    UserProfileRequestDTO,
)
from src.core.domain.entities import User, hash_password
from tests.core.fakes import UserInMemoryRepository


class TestUpdateUserProfile:
    """
    Test suite for the UpdateUserProfileUseCase.
    """

    @pytest.fixture
    def user_in_memory_repository(self):
        """
        Fixture that represents an in-memory repository for testing purposes.
        """

        return UserInMemoryRepository()

    def test_update_user_profile_successfully(self, user_in_memory_repository):
        """
        Test update user profile successfully.
        """

        user = User(
            username="testuser",
            hashed_password=hash_password("foresight"),
        )
        user_in_memory_repository.save(user)

        input_dto = UserProfileRequestDTO(
            user_id=user.id,
            first_name="John",
            last_name="Doe",
            email="john.doe@email.com",
            is_active=True,
        )

        use_case = UpdateUserProfileUseCase(repository=user_in_memory_repository)
        use_case.execute(input_dto)

        output = user_in_memory_repository.get_by_id(user.id)

        assert output is not None
        assert output.username == user.username
        assert output.first_name == "John"
        assert output.last_name == "Doe"
        assert output.email == "john.doe@email.com"
        assert output.is_active is True

    def test_update_user_profile_with_invalid_email_raises_error(
        self,
        user_in_memory_repository,
    ):
        """
        Test update user profile with invalid email.
        """

        user = User(
            username="testuser",
            hashed_password=hash_password("foresight"),
        )
        user_in_memory_repository.save(user)

        input_dto = UserProfileRequestDTO(
            user_id=user.id,
            first_name="John",
            last_name="Doe",
            email="john.doe#email.com",
            is_active=True,
        )
        use_case = UpdateUserProfileUseCase(user_in_memory_repository)

        with pytest.raises(
            InvalidUserError,
            match="Invalid user data: An email address must have an @-sign.",
        ):
            use_case.execute(input_dto)
