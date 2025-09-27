import pytest

from src.core.domain._shared.exceptions import EntityValidationError
from src.core.domain.entities import User, hash_password


class TestUserEntity:
    """
    Test suite for the User entity.
    """

    def test_user_creation_with_valid_data(self):
        """
        Test create a user with valid data.
        """

        hashed_pwd = hash_password("umaSenhaForte123")
        user = User(
            username="testuser",
            hashed_password=hashed_pwd,
        )

        assert user.username == "testuser"
        assert user.hashed_password is not None
        assert user.hashed_password != "umaSenhaForte123"

    def test_password_hashing_is_consistent(self):
        """
        Test that the password hashing algorithm is consistent.
        """

        password = "minhaSenhaSuperSecreta"
        hashed_pwd = hash_password(password)

        user = User(username="testuser", hashed_password=hashed_pwd)

        assert user.verify_password(password) is True
        assert user.verify_password("senhaErrada") is False

    def test_verify_password_with_correct_and_incorrect_password(self):
        """
        Test the verify_password method with correct and incorrect passwords.
        """

        password = "password123"
        hashed_pwd = hash_password(password)
        user = User(username="anotheruser", hashed_password=hashed_pwd)

        assert user.verify_password("password123") is True
        assert user.verify_password("Password123") is False
        assert user.verify_password("wrongpassword") is False

    def test_create_user_with_empty_username_raises_value_error(self):
        """
        Test that creating a user with an empty username raises a EntityValidationError.
        """

        with pytest.raises(EntityValidationError, match="Username is required"):
            User(username="", hashed_password="some_hash")

    def test_users_with_same_id_are_equal(self):
        """
        Test that two users with the same ID are considered equal.
        """
        user1 = User(username="user1", hashed_password="hash1")
        user2 = User(username="user2", hashed_password="hash2", id=user1.id)

        assert user1 == user2

    def test_users_with_different_ids_are_not_equal(self):
        """
        Test that two users with different IDs are not considered equal.
        """

        user1 = User(username="user1", hashed_password="hash1")
        user2 = User(username="user2", hashed_password="hash2")

        assert user1 != user2
