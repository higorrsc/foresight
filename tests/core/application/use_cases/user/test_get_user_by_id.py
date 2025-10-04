import uuid

import pytest

from src.core.application._shared.use_cases import GetByIdRequestInputDTO
from src.core.application.use_cases.user import GetUserByIdUseCase, UserNotFoundError
from src.core.domain.entities import User
from tests.core.fakes import UserInMemoryRepository


class TestGetUserByIdUseCase:
    """
    Test suite for the GetUserByIdUseCase.
    """

    @pytest.fixture
    def user_in_memory_repository(self):
        """
        Fixture that represents an in-memory repository for testing purposes.
        """

        return UserInMemoryRepository()

    def test_get_user_by_id(self, user_in_memory_repository):
        """
        Test get user by id.
        """

        new_user = User(
            username="testuser",
            hashed_password="anyhash",
        )

        repo = user_in_memory_repository
        repo.save(new_user)

        input_dto = GetByIdRequestInputDTO(new_user.id)
        use_case = GetUserByIdUseCase(repository=repo)
        output = use_case.execute(input_dto)

        assert output is not None
        assert output.id == new_user.id
        assert output.username == new_user.username

    def test_get_user_by_id_with_invalid_id(self, user_in_memory_repository):
        """
        Test get user by id with invalid id.
        """

        new_user = User(
            username="testuser",
            hashed_password="anyhash",
        )

        repo = user_in_memory_repository
        repo.save(new_user)

        input_dto = GetByIdRequestInputDTO(uuid.uuid4())
        use_case = GetUserByIdUseCase(repository=repo)

        with pytest.raises(
            UserNotFoundError,
            match="User with given ID not found.",
        ):
            use_case.execute(input_dto)
