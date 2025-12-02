from uuid import UUID

import pytest

from src.shared_kernel.application._shared.use_cases.queries import (
    GetByIdRequestInputDTO,
)
from src.shared_kernel.application.use_cases.area import AreaNotFoundError
from src.shared_kernel.application.use_cases.area.queries import GetAreaByIdUseCase
from src.shared_kernel.domain.entities import Area
from tests.fakes import AreaInMemoryRepository


class TestGetAreaByIdUseCase:
    """
    Test suite for the GetAreaByIdUseCase.
    """

    def test_get_area_by_id_with_valid_id(self, admin_actor):
        """
        Test getting an area by a valid ID.
        """

        repository = AreaInMemoryRepository()
        use_case = GetAreaByIdUseCase(repository)

        area = Area(description="Test Area", tenant_id=admin_actor.tenant_id)
        repository.save(area)

        retrieved_area = use_case.execute(
            GetByIdRequestInputDTO(
                id=area.id,
                actor=admin_actor,
            )
        )

        assert retrieved_area.id == area.id
        assert retrieved_area.description == area.description

    def test_get_area_by_id_with_non_existent_id(self, admin_actor):
        """
        Test getting an area by a non-existent ID.
        """

        repository = AreaInMemoryRepository()
        use_case = GetAreaByIdUseCase(repository)

        non_existent_id: UUID = UUID("123e4567-e89b-12d3-a456-426614174000")

        with pytest.raises(AreaNotFoundError, match="Area with given ID not found."):
            use_case.execute(
                GetByIdRequestInputDTO(
                    id=non_existent_id,
                    actor=admin_actor,
                )
            )
