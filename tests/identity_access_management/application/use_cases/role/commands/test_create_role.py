import pytest

from src.identity_access_management.application.use_cases.permission.exceptions import (
    PermissionNotFoundError,
)
from src.identity_access_management.application.use_cases.role import InvalidRoleError
from src.identity_access_management.application.use_cases.role.commands import (
    CreateRoleInputDTO,
    CreateRoleOutputDTO,
)
from src.identity_access_management.domain.entities.permission import Permission


class TestCreateRoleUseCase:
    """
    Test the CreateRoleUseCase.
    """

    def test_create_role_with_valid_data(
        self,
        admin_actor,
        create_role_use_case,
    ):
        """
        Test the creation of a role with valid data.
        """

        output = create_role_use_case.execute(
            CreateRoleInputDTO(
                actor=admin_actor,
                name="Test Role",
                description="Test Description",
            )
        )

        assert output.id is not None
        assert isinstance(output, CreateRoleOutputDTO)

    def test_create_role_with_empty_name(
        self,
        admin_actor,
        create_role_use_case,
    ):
        """
        Test the creation of a role with invalid data.
        """

        with pytest.raises(
            InvalidRoleError,
            match="Invalid input data: Role name is required.",
        ):
            create_role_use_case.execute(
                CreateRoleInputDTO(
                    actor=admin_actor,
                    name="",
                    description="Test Description",
                )
            )

    def test_create_role_with_long_name(
        self,
        admin_actor,
        create_role_use_case,
    ):
        """
        Test the creation of a role with invalid data.
        """

        with pytest.raises(
            InvalidRoleError,
            match="Role name must be at most 100 characters long.",
        ):
            create_role_use_case.execute(
                CreateRoleInputDTO(
                    actor=admin_actor,
                    name="A" * 101,
                    description="Test Description",
                )
            )

    def test_create_role_without_description(
        self,
        admin_actor,
        create_role_use_case,
    ):
        """
        Test the creation of a role without description.
        """

        output = create_role_use_case.execute(
            CreateRoleInputDTO(
                actor=admin_actor,
                name="Test Role",
            )
        )

        assert output.id is not None
        assert isinstance(output, CreateRoleOutputDTO)

    def test_create_role_with_valid_permission(
        self,
        admin_actor,
        permission_in_memory_repo,
        create_role_use_case,
    ):
        """
        Test the creation of a role with valid permission.
        """
        permission_in_memory_repo.save(
            Permission(codename="area:read", description="Read area")
        )
        permission_in_memory_repo.save(
            Permission(codename="area:create", description="Create area")
        )

        output = create_role_use_case.execute(
            CreateRoleInputDTO(
                actor=admin_actor,
                name="Test Role",
                permissions=[
                    "area:read",
                    "area:create",
                ],
            )
        )

        assert output.id is not None
        assert isinstance(output, CreateRoleOutputDTO)

    def test_create_role_with_invalid_permission(
        self,
        admin_actor,
        create_role_use_case,
    ):
        """
        Test the creation of a role with valid permission.
        """

        with pytest.raises(
            PermissionNotFoundError,
            match="Permission 'area:reader' not found.",
        ):
            create_role_use_case.execute(
                CreateRoleInputDTO(
                    actor=admin_actor,
                    name="Test Role",
                    permissions=["area:reader"],
                )
            )
