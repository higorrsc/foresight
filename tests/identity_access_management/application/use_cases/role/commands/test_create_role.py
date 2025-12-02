import pytest

from src.identity_access_management.application.use_cases.role import InvalidRoleError
from src.identity_access_management.application.use_cases.role.commands import (
    CreateRoleInputDTO,
    CreateRoleOutputDTO,
    CreateRoleUseCase,
)
from tests.fakes import RoleInMemoryRepository


class TestCreateRoleUseCase:
    """
    Test the CreateRoleUseCase.
    """

    def test_create_role_with_valid_data(self, admin_actor):
        """
        Test the creation of a role with valid data.
        """

        repository = RoleInMemoryRepository()
        use_case = CreateRoleUseCase(repository)
        output = use_case.execute(
            CreateRoleInputDTO(
                actor=admin_actor,
                name="Test Role",
                description="Test Description",
            )
        )

        assert output.id is not None
        assert isinstance(output, CreateRoleOutputDTO)

    def test_create_role_with_empty_name(self, admin_actor):
        """
        Test the creation of a role with invalid data.
        """

        repository = RoleInMemoryRepository()
        use_case = CreateRoleUseCase(repository)
        with pytest.raises(
            InvalidRoleError,
            match="Invalid input data: Role name is required.",
        ):
            use_case.execute(
                CreateRoleInputDTO(
                    actor=admin_actor,
                    name="",
                    description="Test Description",
                )
            )

    def test_create_role_with_long_name(self, admin_actor):
        """
        Test the creation of a role with invalid data.
        """

        repository = RoleInMemoryRepository()
        use_case = CreateRoleUseCase(repository)
        with pytest.raises(
            InvalidRoleError,
            match="Role name must be at most 100 characters long.",
        ):
            use_case.execute(
                CreateRoleInputDTO(
                    actor=admin_actor,
                    name="A" * 101,
                    description="Test Description",
                )
            )

    def test_create_role_without_description(self, admin_actor):
        """
        Test the creation of a role without description.
        """

        repository = RoleInMemoryRepository()
        use_case = CreateRoleUseCase(repository)
        output = use_case.execute(
            CreateRoleInputDTO(
                actor=admin_actor,
                name="Test Role",
            )
        )

        assert output.id is not None
        assert isinstance(output, CreateRoleOutputDTO)
