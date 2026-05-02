from unittest.mock import Mock, patch
from uuid import uuid4

import pytest

from src.identity_access_management.application.use_cases.role import RoleNotFoundError
from src.identity_access_management.application.use_cases.user import (
    UsernameAlreadyExistsError,
)
from src.identity_access_management.application.use_cases.user.commands import (
    CreateUserInputDTO,
    CreateUserOutputDTO,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities import Role, User


class TestCreateUserUseCase:
    """
    Test suite for the CreateUserUseCase.
    """

    def test_create_user_success(
        self, create_user_use_case_mocked, mock_user_repository, mock_role_repository
    ):
        """
        Test successful user creation.
        """
        actor = Mock(spec=User)
        actor.permissions = {AppPermission.USER_CREATE}
        actor.tenant_id = uuid4()
        actor.id = uuid4()

        input_dto = CreateUserInputDTO(
            actor=actor, username="newuser", password="password123", roles=["admin"]
        )

        mock_user_repository.get_by_username_global.return_value = None
        mock_role_repository.get_by_name.return_value = Mock(spec=Role, name="admin")

        with patch(
            "src.identity_access_management.application.use_cases.user.commands.create_user.hash_password",
            return_value="hashed_pwd",
        ):
            result = create_user_use_case_mocked.execute(input_dto)

        assert isinstance(result, CreateUserOutputDTO)
        assert result.username == "newuser"
        mock_user_repository.save.assert_called_once()

    def test_create_user_no_permission(self, create_user_use_case_mocked):
        """
        Test user creation fails when actor lacks permission.
        """
        actor = Mock(spec=User)
        actor.permissions = set()

        input_dto = CreateUserInputDTO(
            actor=actor, username="newuser", password="password123"
        )

        with pytest.raises(PermissionError) as excinfo:
            create_user_use_case_mocked.execute(input_dto)

        assert "User does not have permission" in str(excinfo.value)

    def test_create_user_username_exists(
        self, create_user_use_case_mocked, mock_user_repository
    ):
        """
        Test user creation fails when username already exists globally.
        """
        actor = Mock(spec=User)
        actor.permissions = {AppPermission.USER_CREATE}

        input_dto = CreateUserInputDTO(
            actor=actor, username="existinguser", password="password123"
        )

        mock_user_repository.get_by_username_global.return_value = Mock(spec=User)

        with pytest.raises(UsernameAlreadyExistsError):
            create_user_use_case_mocked.execute(input_dto)

    def test_create_user_role_not_found(
        self, create_user_use_case_mocked, mock_user_repository, mock_role_repository
    ):
        """
        Test user creation fails when a specified role is not found.
        """
        actor = Mock(spec=User)
        actor.permissions = {AppPermission.USER_CREATE}
        actor.tenant_id = uuid4()

        input_dto = CreateUserInputDTO(
            actor=actor,
            username="newuser",
            password="password123",
            roles=["nonexistent"],
        )

        mock_user_repository.get_by_username_global.return_value = None
        mock_role_repository.get_by_name.return_value = None

        with pytest.raises(RoleNotFoundError):
            create_user_use_case_mocked.execute(input_dto)

    def test_create_user_default_guest_role(
        self, create_user_use_case_mocked, mock_user_repository, mock_role_repository
    ):
        """
        Test user creation with default 'guest' role when no roles are specified.
        """
        actor = Mock(spec=User)
        actor.permissions = {AppPermission.USER_CREATE}
        actor.tenant_id = uuid4()
        actor.id = uuid4()

        input_dto = CreateUserInputDTO(
            actor=actor, username="newuser", password="password123", roles=[]
        )

        mock_user_repository.get_by_username_global.return_value = None
        guest_role = Mock(spec=Role)
        guest_role.name = "guest"
        mock_role_repository.get_by_name.return_value = guest_role

        with patch(
            "src.identity_access_management.application.use_cases.user.commands.create_user.hash_password",
            return_value="hashed_pwd",
        ):
            create_user_use_case_mocked.execute(input_dto)

        mock_role_repository.get_by_name.assert_called_with("guest", actor.tenant_id)
