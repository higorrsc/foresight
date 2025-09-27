import pytest

from src.core.application.use_cases.area import (
    InputUpdateAreaDTO,
    OutputUpdateAreaDTO,
    UpdateAreaUseCase,
)
from src.core.domain.entities import Area
from src.core.infrastructure.repositories._shared import InMemoryRepository


class TestUpdateArea:
    """
    Test suite for the UpdateAreaUseCase use case.
    """

    def test_update_area_with_valid_data(self):
        """
        Test updating an area with valid data.
        """

        repository = InMemoryRepository[Area]()
        use_case = UpdateAreaUseCase(repository)

        area = Area(description="Initial Description")
        repository.save(area)

        output: OutputUpdateAreaDTO = use_case.execute(
            InputUpdateAreaDTO(
                id=area.id,
                description="Updated Description",
            )
        )

        assert output.id == area.id
        assert output.description == "Updated Description"

    def test_update_area_with_invalid_data_empty_description(self):
        """
        Test updating an area with invalid data.
        """

        repository = InMemoryRepository[Area]()
        use_case = UpdateAreaUseCase(repository)

        area = Area(description="Initial Description")
        repository.save(area)

        with pytest.raises(
            ValueError,
            match="Invalid input data: Description must be a non-empty string.",
        ):
            use_case.execute(
                InputUpdateAreaDTO(
                    id=area.id,
                    description="",  # Invalid description
                )
            )

    def test_update_area_with_invalid_data_long_description(self):
        """
        Test updating an area with invalid data.
        """

        repository = InMemoryRepository[Area]()
        use_case = UpdateAreaUseCase(repository)

        area = Area(description="Initial Description")
        repository.save(area)

        with pytest.raises(
            ValueError,
            match="Invalid input data: Description must be at most 100 characters long.",
        ):
            use_case.execute(
                InputUpdateAreaDTO(
                    id=area.id,
                    description="a" * 200,  # Invalid description
                )
            )
