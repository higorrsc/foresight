import pytest

from src.core.application._shared.use_cases import ListRequestInputDTO
from src.core.application.use_cases.user import ListUserUseCase
from src.core.domain.entities import User
from tests.core.fakes import UserInMemoryRepository


class TestListUserUseCase:
    """
    Test suite for the ListUserUseCase.
    """

    @pytest.fixture
    def user_in_memory_repository(self):
        """
        Fixture that represents an in-memory repository for testing purposes.
        """

        return UserInMemoryRepository()

    def test_list_existing_user(self, user_in_memory_repository):
        """
        Test list existing user.
        """

        repo = user_in_memory_repository

        user_to_list = User(
            username="tobelisted",
            hashed_password="anyhash",
        )
        repo.save(user_to_list)

        another_user_to_list = User(
            username="tobelisted",
            hashed_password="anyhash",
        )
        repo.save(another_user_to_list)

        use_case = ListUserUseCase(repository=repo)

        input_dto = ListRequestInputDTO()

        output = use_case.execute(input_dto)

        assert output is not None
        assert len(output.data) == 2

    def test_list_non_existent_user_raises_error(self, user_in_memory_repository):
        """
        Test list non-existent user.
        """

        repo = user_in_memory_repository
        use_case = ListUserUseCase(repository=repo)

        input_dto = ListRequestInputDTO()

        output = use_case.execute(input_dto)
        assert output is not None
        assert len(output.data) == 0
