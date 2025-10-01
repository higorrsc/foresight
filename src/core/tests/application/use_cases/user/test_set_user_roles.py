# src/core/tests/application/use_cases/user/test_set_user_roles.py
from uuid import uuid4

import pytest

from src.core.application.use_cases.user import SetUserRolesUseCase, UserNotFoundError
from src.core.application.use_cases.user.set_user_roles import SetUserRolesRequestDTO
from src.core.domain.entities.role import Role
from src.core.domain.entities.user import User
from src.core.tests.fakes.in_memory_user_repository import (
    RoleInMemoryRepository,
    UserInMemoryRepository,
)


class TestSetUserRolesUseCase:
    """
    Test suite for the SetUserRolesUseCase.
    """

    @pytest.fixture
    def user_repo(self):
        """
        Fixture that represents a user repository.
        """
        return UserInMemoryRepository()

    @pytest.fixture
    def role_repo(self):
        """
        Fixture that represents a role repository.
        """
        repo = RoleInMemoryRepository()
        repo.save(Role(name="admin", description=""))
        repo.save(Role(name="guest", description=""))
        repo.save(Role(name="editor", description=""))

        return repo

    def test_set_roles_for_existing_user(self, user_repo, role_repo):
        """
        Test setting roles for an existing user.
        """

        user = User(username="testuser", hashed_password="pw", roles={"guest"})
        user_repo.save(user)

        use_case = SetUserRolesUseCase(
            user_repository=user_repo,
            role_repository=role_repo,
        )

        input_dto = SetUserRolesRequestDTO(
            user_id=user.id,
            role_names=["admin", "editor"],
        )
        use_case.execute(input_dto)

        updated_user = user_repo.get_by_id(user.id)
        assert updated_user.roles == {"admin", "editor"}

    def test_clear_roles_from_user(self, user_repo, role_repo):
        """
        Test clearing roles from a user.
        """

        user = User(
            username="testuser",
            hashed_password="pw",
            roles={"admin", "guest"},
        )
        user_repo.save(user)

        use_case = SetUserRolesUseCase(
            user_repository=user_repo,
            role_repository=role_repo,
        )

        input_dto = SetUserRolesRequestDTO(
            user_id=user.id,
            role_names=[],
        )
        use_case.execute(input_dto)

        updated_user = user_repo.get_by_id(user.id)
        assert updated_user.roles == set()

    def test_set_roles_for_non_existent_user_raises_error(self, user_repo, role_repo):
        """
        Test setting roles for a non-existent user.
        """
        use_case = SetUserRolesUseCase(
            user_repository=user_repo, role_repository=role_repo
        )

        input_dto = SetUserRolesRequestDTO(
            user_id=uuid4(),
            role_names=["admin"],
        )

        with pytest.raises(
            UserNotFoundError,
            match=f"User with ID '{input_dto.user_id}' not found.",
        ):
            use_case.execute(input_dto)

    def test_set_non_existent_role_raises_error(self, user_repo, role_repo):
        """
        Test setting a non-existent role.
        """

        user = User(username="testuser", hashed_password="pw")
        user_repo.save(user)

        use_case = SetUserRolesUseCase(
            user_repository=user_repo,
            role_repository=role_repo,
        )

        input_dto = SetUserRolesRequestDTO(
            user_id=user.id,
            role_names=[
                "admin",
                "non_existent_role",
            ],
        )

        with pytest.raises(
            ValueError,
            match="Role 'non_existent_role' does not exist.",
        ):
            use_case.execute(input_dto)
