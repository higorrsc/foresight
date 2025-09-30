import pytest

from src.core.application.use_cases.role import (
    CreateRoleInputDTO,
    CreateRoleOutputDTO,
    CreateRoleUseCase,
)
from src.core.application.use_cases.role.exceptions import InvalidRoleError
from src.core.domain.entities import Role
from src.core.infrastructure.repositories._shared import InMemoryRepository


class TestCreateRoleUseCase:
    """
    Test the CreateRoleUseCase.
    """

    def test_create_role_with_valid_data(self):
        """
        Test the creation of a role with valid data.
        """

        repository = InMemoryRepository[Role]()
        use_case = CreateRoleUseCase(repository)
        output = use_case.execute(
            CreateRoleInputDTO(
                "Test Role",
                "Test Description",
            )
        )

        assert output.id is not None
        assert isinstance(output, CreateRoleOutputDTO)

    def test_create_role_with_empty_name(self):
        """
        Test the creation of a role with invalid data.
        """

        repository = InMemoryRepository[Role]()
        use_case = CreateRoleUseCase(repository)
        with pytest.raises(
            InvalidRoleError,
            match="Invalid input data: Role name is required.",
        ):
            use_case.execute(
                CreateRoleInputDTO(
                    "",
                    "Test Description",
                )
            )

    def test_create_role_with_long_name(self):
        """
        Test the creation of a role with invalid data.
        """

        repository = InMemoryRepository[Role]()
        use_case = CreateRoleUseCase(repository)
        with pytest.raises(
            InvalidRoleError,
            match="Role name must be at most 100 characters long.",
        ):
            use_case.execute(
                CreateRoleInputDTO(
                    "A" * 101,
                    "Test Description",
                )
            )

    def test_create_role_without_description(self):
        """
        Test the creation of a role without description.
        """

        repository = InMemoryRepository[Role]()
        use_case = CreateRoleUseCase(repository)
        output = use_case.execute(CreateRoleInputDTO("Test Role"))

        assert output.id is not None
        assert isinstance(output, CreateRoleOutputDTO)
