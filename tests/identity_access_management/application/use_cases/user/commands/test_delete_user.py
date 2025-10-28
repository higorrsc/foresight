from uuid import uuid4

import pytest

from src.identity_access_management.application.use_cases.user import UserNotFoundError
from src.identity_access_management.application.use_cases.user.commands import (
    DeleteUserUseCase,
)
from src.identity_access_management.domain.entities import User
from src.shared_kernel.application._shared.use_cases.commands import (
    DeleteRequestInputDTO,
)
from tests.fakes.in_memory_repository import UserInMemoryRepository


class TestDeleteUserUseCase:
    """
    Test suite for the DeleteUserUseCase.
    """

    @pytest.fixture
    def user_in_memory_repository(self):
        """
        Fixture that represents an in-memory repository for testing purposes.
        """

        return UserInMemoryRepository()

    def test_delete_existing_user(self, user_in_memory_repository):
        """
        Test delete existing user.
        """

        repo = user_in_memory_repository

        user_to_delete = User(
            username="tobedeleted",
            hashed_password="anyhash",
        )
        repo.save(user_to_delete)

        use_case = DeleteUserUseCase(repository=repo)

        input_dto = DeleteRequestInputDTO(id=user_to_delete.id)

        use_case.execute(input_dto)

        found_user = repo.get_by_id(user_to_delete.id)
        assert found_user is not None
        assert found_user.deleted_at is not None
        assert found_user.is_active is False

    def test_delete_non_existent_user_raises_error(self, user_in_memory_repository):
        """
        Test delete non-existent user.
        """

        repo = user_in_memory_repository
        use_case = DeleteUserUseCase(repository=repo)

        non_existent_id = uuid4()
        input_dto = DeleteRequestInputDTO(id=non_existent_id)

        with pytest.raises(
            UserNotFoundError,
            match="User with given ID not found.",
        ):
            use_case.execute(input_dto)
