from src.core.application.dto import PaginatedResponseDTO
from src.core.application.use_cases.queries import ListRequestInputDTO
from src.shared_kernel.application.use_cases.area.queries import ListAreaUseCase
from src.shared_kernel.domain.entities import Area
from tests.fakes import AreaInMemoryRepository


class TestListArea:
    """
    Test the ListArea use case.
    """

    def test_list_areas(self, admin_actor):
        """
        Test listing areas.
        """

        repository = AreaInMemoryRepository()
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

        areas: PaginatedResponseDTO[Area] = use_case.execute(
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

        repository = AreaInMemoryRepository()
        use_case = ListAreaUseCase(repository)

        areas: PaginatedResponseDTO[Area] = use_case.execute(
            ListRequestInputDTO(actor=admin_actor)
        )

        assert len(areas.data) == 0
