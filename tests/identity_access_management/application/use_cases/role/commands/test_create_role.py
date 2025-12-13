import pytest

from src.identity_access_management.application.use_cases.permission.exceptions import (
    PermissionNotFoundError,
)
from src.identity_access_management.application.use_cases.role import InvalidRoleError
from src.identity_access_management.application.use_cases.role.commands import (
    CreateRoleInputDTO,
    CreateRoleOutputDTO,
    CreateRoleUseCase,
)
from src.identity_access_management.domain.entities.permission import Permission
from src.identity_access_management.domain.repositories import (
    IPermissionRepository,
    IRoleRepository,
)
from tests.fakes import PermissionInMemoryRepository, RoleInMemoryRepository


@pytest.fixture()
def role_repository() -> IRoleRepository:
    """
    Fixture that represents an in-memory repository for testing purposes.
    """

    return RoleInMemoryRepository()


@pytest.fixture()
def permission_repository() -> IPermissionRepository:
    """
    Fixture that represents an in-memory repository for testing purposes.
    """

    return PermissionInMemoryRepository(
        [
            Permission(codename="area:read", description="Read area"),
            Permission(codename="area:create", description="Create area"),
        ]
    )


class TestCreateRoleUseCase:
    """
    Test the CreateRoleUseCase.
    """

    def test_create_role_with_valid_data(
        self,
        admin_actor,
        role_repository,
        permission_repository,
    ):
        """
        Test the creation of a role with valid data.
        """

        use_case = CreateRoleUseCase(
            role_repository,
            permission_repository,
        )
        output = use_case.execute(
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
        role_repository,
        permission_repository,
    ):
        """
        Test the creation of a role with invalid data.
        """

        use_case = CreateRoleUseCase(
            role_repository,
            permission_repository,
        )
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

    def test_create_role_with_long_name(
        self,
        admin_actor,
        role_repository,
        permission_repository,
    ):
        """
        Test the creation of a role with invalid data.
        """

        use_case = CreateRoleUseCase(
            role_repository,
            permission_repository,
        )
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

    def test_create_role_without_description(
        self,
        admin_actor,
        role_repository,
        permission_repository,
    ):
        """
        Test the creation of a role without description.
        """

        use_case = CreateRoleUseCase(
            role_repository,
            permission_repository,
        )
        output = use_case.execute(
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
        role_repository,
        permission_repository,
    ):
        """
        Test the creation of a role with valid permission.
        """

        use_case = CreateRoleUseCase(
            role_repository,
            permission_repository,
        )
        output = use_case.execute(
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
        role_repository,
        permission_repository,
    ):
        """
        Test the creation of a role with valid permission.
        """

        use_case = CreateRoleUseCase(
            role_repository,
            permission_repository,
        )

        with pytest.raises(
            PermissionNotFoundError,
            match="Permission 'area:reader' not found.",
        ):
            use_case.execute(
                CreateRoleInputDTO(
                    actor=admin_actor,
                    name="Test Role",
                    permissions=["area:reader"],
                )
            )
