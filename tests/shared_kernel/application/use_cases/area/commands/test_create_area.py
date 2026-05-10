import pytest

from src.core.application.use_cases.commands import (
    CreateDescribedEntityInputDTO,
    CreateDescribedEntityOutputDTO,
)
from src.shared_kernel.domain.exceptions import InvalidAreaError


class TestCreateArea:
    """
    Test the CreateAreaUseCase.
    """

    async def test_create_area_with_valid_data(self, admin_actor, create_area_use_case):
        """
        Test the creation of an area with valid data.
        """

        output = await create_area_use_case.execute(
            CreateDescribedEntityInputDTO(
                actor=admin_actor,
                description="Test Area",
            )
        )

        assert output.id is not None
        assert isinstance(output, CreateDescribedEntityOutputDTO)

    async def test_create_area_with_invalid_data(
        self,
        admin_actor,
        create_area_use_case,
    ):
        """
        Test the creation of an area with invalid data.
        """

        with pytest.raises(
            InvalidAreaError,
            match="Invalid input data: Description must be a non-empty string.",
        ) as exc_info:
            await create_area_use_case.execute(
                CreateDescribedEntityInputDTO(
                    actor=admin_actor,
                    description="",
                )
            )

        assert "Description must be a non-empty string." in str(exc_info.value)
