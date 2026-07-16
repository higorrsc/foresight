import pytest

from src.core.domain import EntityValidationError
from src.identity_access_management.domain.entities import Permission


class TestCreatePermissionEntity:
    """
    Test suite for the Permission entity.
    """

    def test_create_permission_with_valid_data(self):
        """
        Test create a permission with valid data.
        """

        permission = Permission(
            codename="test_permission",
            description="Test Permission",
        )

        assert permission.codename == "test_permission"
        assert permission.description == "Test Permission"
        assert permission.id is not None

    def test_codename_is_required(self):
        """
        Test that creating a Permission without a codename raises a ValueError.
        """

        with pytest.raises(
            EntityValidationError,
            match="Permission codename is required.",
        ):
            Permission(
                codename="",
                description="Test Permission",
            )

    def test_codename_cannot_be_longer_than_100_characters(self):
        """
        Test that creating a Permission with a codename longer
        than 100 characters raises a ValueError.
        """
        long_codename = "A" * 101  # 101 characters long
        with pytest.raises(
            EntityValidationError,
            match="Permission codename must be at most 100 characters long.",
        ):
            Permission(
                codename=long_codename,
                description="Test Permission",
            )

    def test_description_is_required(self):
        """
        Test that creating a Permission without a description raises a ValueError.
        """

        with pytest.raises(
            EntityValidationError,
            match="Permission description is required.",
        ):
            Permission(
                codename="test_permission",
                description="",
            )

    def test_description_cannot_be_longer_than_200_characters(self):
        """
        Test that creating a Permission with a description longer
        than 200 characters raises a ValueError.
        """
        long_description = "A" * 201  # 201 characters long
        with pytest.raises(
            EntityValidationError,
            match="Permission description must be at most 200 characters long.",
        ):
            Permission(
                codename="test_permission",
                description=long_description,
            )


class TestUpdatePermission:
    """
    Test suite for updating the codename and description of the Permission entity.
    """

    def test_update_permission_codename(self):
        """
        Test updating the codename of the Permission entity.
        """

        permission = Permission(
            codename="test_permission",
            description="Test Permission",
        )
        new_codename = "updated_permission"
        permission.update_permission(new_codename=new_codename)

        assert permission.codename == new_codename

    def test_update_permission_description(self):
        """
        Test updating the description of the Permission entity.
        """

        permission = Permission(
            codename="test_permission",
            description="Test Permission",
        )
        new_description = "Updated Permission"
        permission.update_permission(new_description=new_description)

        assert permission.description == new_description

    def test_update_permission_with_long_codename_raises_value_error(self):
        """
        Test that updating the Permission with a long codename
        raises a EntityValidationError
        """

        permission = Permission(
            codename="test_permission",
            description="Test Permission",
        )

        long_codename = "A" * 101  # 101 characters long
        with pytest.raises(
            EntityValidationError,
            match="Permission codename must be at most 100 characters long.",
        ):
            permission.update_permission(new_codename=long_codename)
