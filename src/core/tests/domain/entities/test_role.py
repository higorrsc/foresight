import pytest

from src.core.domain._shared.exceptions import EntityValidationError
from src.core.domain.entities import Role


class TestCreteRole:
    """
    Test suite for the Role entity.
    """

    def test_create_role_with_valid_data(self):
        """
        Test create a role with valid data.
        """

        role = Role(name="test_role", description="Test Role")

        assert role.name == "test_role"
        assert role.description == "Test Role"
        assert role.id is not None

    def test_name_is_required(self):
        """
        Test that creating a Role without a name raises a ValueError.
        """

        with pytest.raises(
            EntityValidationError,
            match="Role name is required.",
        ):
            Role(name="", description="Test Role")

    def test_name_cannot_be_longer_than_100_characters(self):
        """
        Test that creating a Role with a name longer
        than 100 characters raises a ValueError.
        """
        long_name = "A" * 101  # 101 characters long
        with pytest.raises(
            EntityValidationError,
            match="Role name must be at most 100 characters long.",
        ):
            Role(name=long_name, description="Test Role")
