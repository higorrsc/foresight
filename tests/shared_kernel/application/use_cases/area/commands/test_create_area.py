import pytest

from src.shared_kernel.application._shared.use_cases.commands import (
    CreateDescribedEntityInputDTO,
    CreateDescribedEntityOutputDTO,
)
from src.shared_kernel.application.use_cases.area import InvalidAreaError
from src.shared_kernel.application.use_cases.area.commands import CreateAreaUseCase
from src.shared_kernel.domain.entities.area import Area
from src.shared_kernel.infrastructure.repositories._shared import InMemoryRepository


class TestCreateArea:
    """
    Test the CreateAreaUseCase.
    """

    def test_create_area_with_valid_data(self, admin_actor):
        """
        Test the creation of an area with valid data.
        """

        repository = InMemoryRepository[Area]()
        use_case = CreateAreaUseCase(repository)
        output = use_case.execute(
            CreateDescribedEntityInputDTO(
                actor=admin_actor,
                description="Test Area",
            )
        )

        assert output.id is not None
        assert isinstance(output, CreateDescribedEntityOutputDTO)

    def test_create_area_with_invalid_data(self, admin_actor):
        """
        Test the creation of an area with invalid data.
        """

        repository = InMemoryRepository[Area]()
        use_case = CreateAreaUseCase(repository)

        with pytest.raises(
            InvalidAreaError,
            match="Invalid input data: Description must be a non-empty string.",
        ) as exc_info:
            use_case.execute(
                CreateDescribedEntityInputDTO(
                    actor=admin_actor,
                    description="",
                )
            )

        assert "Description must be a non-empty string." in str(exc_info.value)
