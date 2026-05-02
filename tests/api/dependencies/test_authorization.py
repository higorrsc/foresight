import pytest
from fastapi import HTTPException

from src.api.dependencies.authorization import PermissionChecker, RoleChecker


class TestAuthorizationDependencies:
    """
    Test suite for authorization dependencies.
    """

    def test_role_checker_success(self, authorization_dependency_mock_user):
        """
        Test role checker with a user who has the required role.
        """
        authorization_dependency_mock_user.has_role.side_effect = (
            lambda role: role == "admin"
        )
        checker = RoleChecker(allowed_roles=["admin", "editor"])

        # Should not raise any exception
        checker(authorization_dependency_mock_user)
        authorization_dependency_mock_user.has_role.assert_any_call("admin")

    def test_role_checker_failure(self, authorization_dependency_mock_user):
        """
        Test role checker with a user who does not have the required role.
        """
        authorization_dependency_mock_user.has_role.return_value = False
        checker = RoleChecker(allowed_roles=["admin"])

        with pytest.raises(HTTPException) as excinfo:
            checker(authorization_dependency_mock_user)

        assert excinfo.value.status_code == 403
        assert "Operation not permitted" in excinfo.value.detail

    def test_permission_checker_success(self, authorization_dependency_mock_user):
        """
        Test permission checker with a user who has the required permission.
        """
        authorization_dependency_mock_user.permissions = {"user:create", "user:read"}
        checker = PermissionChecker(required_permissions=["user:create"])

        # Should not raise any exception
        checker(authorization_dependency_mock_user)

    def test_permission_checker_failure(self, authorization_dependency_mock_user):
        """
        Test permission checker with a user who does not have the required permission.
        """
        authorization_dependency_mock_user.permissions = {"user:read"}
        checker = PermissionChecker(required_permissions=["user:create"])

        with pytest.raises(HTTPException) as excinfo:
            checker(authorization_dependency_mock_user)

        assert excinfo.value.status_code == 403
        assert "Operation not permitted" in excinfo.value.detail

    def test_permission_checker_empty_permissions(
        self, authorization_dependency_mock_user
    ):
        """
        Test permission checker with a user who has no permissions.
        """
        authorization_dependency_mock_user.permissions = None
        checker = PermissionChecker(required_permissions=["user:create"])

        with pytest.raises(HTTPException) as excinfo:
            checker(authorization_dependency_mock_user)

        assert excinfo.value.status_code == 403
