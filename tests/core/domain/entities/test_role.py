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


class TestUpdateRole:
    """
    Test suite for updating the description of the Role entity.
    """

    def test_update_role_name(self):
        """
        Test updating the name of the Role entity.
        """

        role = Role(name="test_role", description="Test Role")
        new_name = "updated_role"
        role.update_role(new_name=new_name)

        assert role.name == new_name

    def test_update_role_description(self):
        """
        Test updating the description of the Role entity.
        """

        role = Role(name="test_role", description="Initial Description")
        new_description = "Updated Description"
        role.update_role(new_name="test_role", new_description=new_description)

        assert role.description == new_description

    def test_update_role_with_empty_name_raises_value_error(self):
        """
        Test that updating the Role with an empty name raises a EntityValidationError.
        """

        role = Role(name="test_role", description="Test Role")

        with pytest.raises(
            EntityValidationError,
            match="Role name is required.",
        ):
            role.update_role(new_name="")

    def test_update_role_with_long_name_raises_value_error(self):
        """
        Test that updating the Role with a name longer
        than 100 characters raises a EntityValidationError.
        """

        role = Role(name="test_role", description="Test Role")
        long_name = "A" * 101  # 101 characters long

        with pytest.raises(
            EntityValidationError,
            match="Role name must be at most 100 characters long.",
        ):
            role.update_role(new_name=long_name)

    def test_update_role_with_empty_description(self):
        """
        Test that updating the Role with an empty description raises a EntityValidationError.
        """

        role = Role(name="test_role", description="Test Role")
        role.update_role(new_name="test_role", new_description="")

        assert role.description == ""
