import pytest

from src.core.application.use_cases.commands import (
    UpdateDescribedEntityInputDTO,
    UpdateDescribedEntityOutputDTO,
)
from src.shared_kernel.application.use_cases.area import InvalidAreaError
from src.shared_kernel.application.use_cases.area.commands import UpdateAreaUseCase
from src.shared_kernel.domain.entities import Area
from tests.fakes import AreaInMemoryRepository


class TestUpdateArea:
    """
    Test suite for the UpdateAreaUseCase use case.
    """

    def test_update_area_with_valid_data(self, admin_actor):
        """
        Test updating an area with valid data.
        """

        repository = AreaInMemoryRepository()
        use_case = UpdateAreaUseCase(repository)

        area = Area(
            description="Initial Description",
            tenant_id=admin_actor.tenant_id,
        )
        repository.save(area)

        output: UpdateDescribedEntityOutputDTO = use_case.execute(
            UpdateDescribedEntityInputDTO(
                id=area.id,
                description="Updated Description",
                actor=admin_actor,
            )
        )

        assert output.id == area.id
        assert output.description == "Updated Description"

    def test_update_area_with_invalid_data_empty_description(self, admin_actor):
        """
        Test updating an area with invalid data.
        """

        repository = AreaInMemoryRepository()
        use_case = UpdateAreaUseCase(repository)

        area = Area(
            description="Initial Description",
            tenant_id=admin_actor.tenant_id,
        )
        repository.save(area)

        with pytest.raises(
            InvalidAreaError,
            match="Invalid input data: Description must be a non-empty string.",
        ):
            use_case.execute(
                UpdateDescribedEntityInputDTO(
                    id=area.id,
                    description="",  # Invalid description
                    actor=admin_actor,
                )
            )

    def test_update_area_with_invalid_data_long_description(self, admin_actor):
        """
        Test updating an area with invalid data.
        """

        repository = AreaInMemoryRepository()
        use_case = UpdateAreaUseCase(repository)

        area = Area(
            description="Initial Description",
            tenant_id=admin_actor.tenant_id,
        )
        repository.save(area)

        with pytest.raises(
            InvalidAreaError,
            match=(
                "Invalid input data: Description must be at most 100 characters long."
            ),
        ):
            use_case.execute(
                UpdateDescribedEntityInputDTO(
                    id=area.id,
                    description="a" * 200,  # Invalid description
                    actor=admin_actor,
                )
            )
