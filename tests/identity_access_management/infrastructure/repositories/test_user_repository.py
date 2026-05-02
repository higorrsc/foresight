from src.identity_access_management.domain.entities import User
from src.identity_access_management.domain.entities.user import hash_password


class TestUserRepository:
    """
    Test suite for UserRepository.
    """

    def test_save_and_get_by_id(
        self,
        user_sqlalchemy_repo,
        default_tenant_id,
    ):
        """
        Test saving a user and retrieving it by ID.
        """

        user = User(
            username="testuser",
            hashed_password=hash_password("password123"),
            tenant_id=default_tenant_id,
        )
        saved_user = user_sqlalchemy_repo.save(user)

        assert saved_user is not None
        assert saved_user.id == user.id

        found_user = user_sqlalchemy_repo.get_by_id(
            entity_id=user.id,
            tenant_id=default_tenant_id,
        )
        assert found_user is not None
        assert found_user.username == "testuser"

    def test_get_by_username_found(
        self,
        user_sqlalchemy_repo,
        default_tenant_id,
    ):
        """
        Test retrieving a user by username when it exists.
        """

        user = User(
            username="findme",
            hashed_password=hash_password("password123"),
            tenant_id=default_tenant_id,
        )
        user_sqlalchemy_repo.save(user)

        found_user = user_sqlalchemy_repo.get_by_username(
            username="findme",
            tenant_id=default_tenant_id,
        )

        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.username == "findme"

    def test_get_by_username_not_found(
        self,
        user_sqlalchemy_repo,
        default_tenant_id,
    ):
        """
        Test retrieving a user by username when it does not exist.
        """
        found_user = user_sqlalchemy_repo.get_by_username(
            "nosuchuser",
            tenant_id=default_tenant_id,
        )
        assert found_user is None
