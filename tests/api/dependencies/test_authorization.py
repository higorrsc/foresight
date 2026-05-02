from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from src.api.dependencies.authorization import PermissionChecker, RoleChecker
from src.identity_access_management.domain.entities import User


@pytest.fixture
def mock_user():
    """
    Fixture for a mock user.
    """
    return Mock(spec=User)


class TestAuthorizationDependencies:
    """
    Test suite for authorization dependencies.
    """

    def test_role_checker_success(self, mock_user):
        """
        Test role checker with a user who has the required role.
        """
        mock_user.has_role.side_effect = lambda role: role == "admin"
        checker = RoleChecker(allowed_roles=["admin", "editor"])

        # Should not raise any exception
        checker(mock_user)
        mock_user.has_role.assert_any_call("admin")

    def test_role_checker_failure(self, mock_user):
        """
        Test role checker with a user who does not have the required role.
        """
        mock_user.has_role.return_value = False
        checker = RoleChecker(allowed_roles=["admin"])

        with pytest.raises(HTTPException) as excinfo:
            checker(mock_user)

        assert excinfo.value.status_code == 403
        assert "Operation not permitted" in excinfo.value.detail

    def test_permission_checker_success(self, mock_user):
        """
        Test permission checker with a user who has the required permission.
        """
        mock_user.permissions = {"user:create", "user:read"}
        checker = PermissionChecker(required_permissions=["user:create"])

        # Should not raise any exception
        checker(mock_user)

    def test_permission_checker_failure(self, mock_user):
        """
        Test permission checker with a user who does not have the required permission.
        """
        mock_user.permissions = {"user:read"}
        checker = PermissionChecker(required_permissions=["user:create"])

        with pytest.raises(HTTPException) as excinfo:
            checker(mock_user)

        assert excinfo.value.status_code == 403
        assert "Operation not permitted" in excinfo.value.detail

    def test_permission_checker_empty_permissions(self, mock_user):
        """
        Test permission checker with a user who has no permissions.
        """
        mock_user.permissions = None
        checker = PermissionChecker(required_permissions=["user:create"])

        with pytest.raises(HTTPException) as excinfo:
            checker(mock_user)

        assert excinfo.value.status_code == 403
