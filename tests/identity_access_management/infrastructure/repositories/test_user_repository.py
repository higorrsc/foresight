import pytest

from src.identity_access_management.domain.entities import User
from src.identity_access_management.domain.entities.user import hash_password
from src.identity_access_management.infrastructure.repositories import UserRepository


@pytest.fixture(scope="function")
def user_repository(db_session_for_test):
    """
    Create a UserRepository instance for testing.
    """

    return UserRepository(db_session_for_test)


class TestUserRepository:
    """
    Test suite for UserRepository.
    """

    def test_save_and_get_by_id(self, user_repository):
        """
        Test saving a user and retrieving it by ID.
        """

        user = User(
            username="testuser",
            hashed_password=hash_password("password123"),
        )
        saved_user = user_repository.save(user)

        assert saved_user is not None
        assert saved_user.id == user.id

        found_user = user_repository.get_by_id(user.id)
        assert found_user is not None
        assert found_user.username == "testuser"

    def test_get_by_username_found(self, user_repository):
        """
        Test retrieving a user by username when it exists.
        """

        user = User(
            username="findme",
            hashed_password=hash_password("password123"),
        )
        user_repository.save(user)

        found_user = user_repository.get_by_username("findme")

        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.username == "findme"

    def test_get_by_username_not_found(self, user_repository):
        """
        Test retrieving a user by username when it does not exist.
        """
        found_user = user_repository.get_by_username("nosuchuser")
        assert found_user is None
