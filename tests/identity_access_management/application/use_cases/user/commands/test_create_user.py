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
    CreateUserUseCase,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities import Role, User


@pytest.fixture
def mock_user_repo():
    return Mock()


@pytest.fixture
def mock_role_repo():
    return Mock()


@pytest.fixture
def use_case(mock_user_repo, mock_role_repo):
    return CreateUserUseCase(mock_user_repo, mock_role_repo)


def test_create_user_success(use_case, mock_user_repo, mock_role_repo):
    actor = Mock(spec=User)
    actor.permissions = {AppPermission.USER_CREATE}
    actor.tenant_id = uuid4()
    actor.id = uuid4()

    input_dto = CreateUserInputDTO(
        actor=actor, username="newuser", password="password123", roles=["admin"]
    )

    mock_user_repo.get_by_username_global.return_value = None
    mock_role_repo.get_by_name.return_value = Mock(spec=Role, name="admin")

    with patch(
        "src.identity_access_management.application.use_cases.user.commands.create_user.hash_password",
        return_value="hashed_pwd",
    ):
        result = use_case.execute(input_dto)

    assert isinstance(result, CreateUserOutputDTO)
    assert result.username == "newuser"
    mock_user_repo.save.assert_called_once()


def test_create_user_no_permission(use_case):
    actor = Mock(spec=User)
    actor.permissions = set()

    input_dto = CreateUserInputDTO(
        actor=actor, username="newuser", password="password123"
    )

    with pytest.raises(PermissionError) as excinfo:
        use_case.execute(input_dto)

    assert "User does not have permission" in str(excinfo.value)


def test_create_user_username_exists(use_case, mock_user_repo):
    actor = Mock(spec=User)
    actor.permissions = {AppPermission.USER_CREATE}

    input_dto = CreateUserInputDTO(
        actor=actor, username="existinguser", password="password123"
    )

    mock_user_repo.get_by_username_global.return_value = Mock(spec=User)

    with pytest.raises(UsernameAlreadyExistsError):
        use_case.execute(input_dto)


def test_create_user_role_not_found(use_case, mock_user_repo, mock_role_repo):
    actor = Mock(spec=User)
    actor.permissions = {AppPermission.USER_CREATE}
    actor.tenant_id = uuid4()

    input_dto = CreateUserInputDTO(
        actor=actor, username="newuser", password="password123", roles=["nonexistent"]
    )

    mock_user_repo.get_by_username_global.return_value = None
    mock_role_repo.get_by_name.return_value = None

    with pytest.raises(RoleNotFoundError):
        use_case.execute(input_dto)


def test_create_user_default_guest_role(use_case, mock_user_repo, mock_role_repo):
    actor = Mock(spec=User)
    actor.permissions = {AppPermission.USER_CREATE}
    actor.tenant_id = uuid4()
    actor.id = uuid4()

    input_dto = CreateUserInputDTO(
        actor=actor, username="newuser", password="password123", roles=[]
    )

    mock_user_repo.get_by_username_global.return_value = None
    guest_role = Mock(spec=Role)
    guest_role.name = "guest"
    mock_role_repo.get_by_name.return_value = guest_role

    with patch(
        "src.identity_access_management.application.use_cases.user.commands.create_user.hash_password",
        return_value="hashed_pwd",
    ):
        use_case.execute(input_dto)

    mock_role_repo.get_by_name.assert_called_with("guest", actor.tenant_id)
