from src.core.application._shared.use_cases.queries import (
    ListRequestInputDTO,
    ListResponseOutputDTO,
)
from src.core.application.use_cases.area.queries import ListAreaUseCase
from src.core.domain.entities import Area
from src.core.infrastructure.repositories._shared import InMemoryRepository


class TestListArea:
    """
    Test the ListArea use case.
    """

    def test_list_areas(self):
        """
        Test listing areas.
        """

        repository = InMemoryRepository[Area]()
        use_case = ListAreaUseCase(repository)

        area1 = Area(description="Area 1")
        area2 = Area(description="Area 2")

        repository.save(area1)
        repository.save(area2)

        areas: ListResponseOutputDTO[Area] = use_case.execute(ListRequestInputDTO())

        assert len(areas.data) == 2
        assert areas.data[0].id is not None
        assert areas.data[0].description == "Area 1"
        assert areas.data[1].id is not None
        assert areas.data[1].description == "Area 2"

    def test_empty_list_area(self):
        """
        Test listing areas when there are no areas.
        """

        repository = InMemoryRepository[Area]()
        use_case = ListAreaUseCase(repository)

        areas: ListResponseOutputDTO[Area] = use_case.execute(ListRequestInputDTO())

        assert len(areas.data) == 0
