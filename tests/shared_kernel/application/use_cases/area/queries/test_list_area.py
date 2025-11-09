from src.shared_kernel.application._shared.use_cases.queries import (
    ListRequestInputDTO,
    ListResponseOutputDTO,
)
from src.shared_kernel.application.use_cases.area.queries import ListAreaUseCase
from src.shared_kernel.domain.entities import Area
from src.shared_kernel.infrastructure.repositories._shared import InMemoryRepository


class TestListArea:
    """
    Test the ListArea use case.
    """

    def test_list_areas(self, admin_actor):
        """
        Test listing areas.
        """

        repository = InMemoryRepository[Area]()
        use_case = ListAreaUseCase(repository)

        area1 = Area(
            description="Area 1",
            tenant_id=admin_actor.tenant_id,
        )
        area2 = Area(
            description="Area 2",
            tenant_id=admin_actor.tenant_id,
        )

        repository.save(area1)
        repository.save(area2)

        areas: ListResponseOutputDTO[Area] = use_case.execute(
            ListRequestInputDTO(actor=admin_actor)
        )

        assert len(areas.data) == 2
        assert areas.data[0].id is not None
        assert areas.data[0].description == "Area 1"
        assert areas.data[1].id is not None
        assert areas.data[1].description == "Area 2"

    def test_empty_list_area(self, admin_actor):
        """
        Test listing areas when there are no areas.
        """

        repository = InMemoryRepository[Area]()
        use_case = ListAreaUseCase(repository)

        areas: ListResponseOutputDTO[Area] = use_case.execute(
            ListRequestInputDTO(actor=admin_actor)
        )

        assert len(areas.data) == 0
