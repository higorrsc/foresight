from datetime import datetime
from uuid import uuid4

import pytest

from src.core.application._shared.use_cases.commands import RestoreRequestInputDTO
from src.core.application.use_cases.user import UserNotFoundError
from src.core.application.use_cases.user.commands import RestoreUserUseCase
from src.core.domain.entities import User
from tests.core.fakes import UserInMemoryRepository


class TestRestoreUserUseCase:
    """
    Test suite for the RestoreUserUseCase.
    """

    @pytest.fixture
    def user_in_memory_repository(self):
        """
        Fixture that represents an in-memory repository for testing purposes.
        """

        return UserInMemoryRepository()

    def test_restore_existing_user(self, user_in_memory_repository):
        """
        Test restore existing user.
        """

        repo = user_in_memory_repository

        user_to_restore = User(
            username="toberestored",
            hashed_password="anyhash",
        )
        user_to_restore.is_active = False
        user_to_restore.deleted_at = datetime.now()
        repo.save(user_to_restore)

        use_case = RestoreUserUseCase(repository=repo)

        input_dto = RestoreRequestInputDTO(id=user_to_restore.id)

        use_case.execute(input_dto)

        found_user = repo.get_by_id(user_to_restore.id)
        assert found_user is not None
        assert found_user.deleted_at is None
        assert found_user.is_active is True

    def test_restore_non_existent_user_raises_error(self, user_in_memory_repository):
        """
        Test restore non-existent user.
        """

        repo = user_in_memory_repository
        use_case = RestoreUserUseCase(repository=repo)

        non_existent_id = uuid4()
        input_dto = RestoreRequestInputDTO(id=non_existent_id)

        with pytest.raises(
            UserNotFoundError,
            match="User with given ID not found.",
        ):
            use_case.execute(input_dto)
