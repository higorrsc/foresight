from uuid import UUID

import pytest

from src.core.application._shared.use_cases import GetByIdRequestInputDTO
from src.core.application.use_cases.area import AreaNotFoundError, GetAreaByIdUseCase
from src.core.domain.entities import Area
from src.core.infrastructure.repositories._shared import InMemoryRepository


class TestGetAreaByIdUseCase:
    """
    Test suite for the GetAreaByIdUseCase.
    """

    def test_get_area_by_id_with_valid_id(self):
        """
        Test getting an area by a valid ID.
        """

        repository = InMemoryRepository[Area]()
        use_case = GetAreaByIdUseCase(repository)

        area = Area(description="Test Area")
        repository.save(area)

        retrieved_area = use_case.execute(GetByIdRequestInputDTO(id=area.id))

        assert retrieved_area.id == area.id
        assert retrieved_area.description == area.description

    def test_get_area_by_id_with_non_existent_id(self):
        """
        Test getting an area by a non-existent ID.
        """

        repository = InMemoryRepository[Area]()
        use_case = GetAreaByIdUseCase(repository)

        non_existent_id: UUID = UUID("123e4567-e89b-12d3-a456-426614174000")

        with pytest.raises(AreaNotFoundError, match="Area with given ID not found."):
            use_case.execute(GetByIdRequestInputDTO(id=non_existent_id))
