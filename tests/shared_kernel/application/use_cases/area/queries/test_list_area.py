from src.core.application.dto import PaginatedResponseDTO
from src.core.application.use_cases.queries import ListRequestInputDTO
from src.shared_kernel.domain.entities import Area


class TestListArea:
    """
    Test the ListArea use case.
    """

    def test_list_areas(self, admin_actor, area_in_memory_repo, list_area_use_case):
        """
        Test listing areas.
        """

        area1 = Area(
            description="Area 1",
            tenant_id=admin_actor.tenant_id,
        )
        area2 = Area(
            description="Area 2",
            tenant_id=admin_actor.tenant_id,
        )

        area_in_memory_repo.save(area1)
        area_in_memory_repo.save(area2)

        areas: PaginatedResponseDTO[Area] = list_area_use_case.execute(
            ListRequestInputDTO(actor=admin_actor)
        )

        assert len(areas.data) == 2
        assert areas.data[0].id is not None
        assert areas.data[0].description == "Area 1"
        assert areas.data[1].id is not None
        assert areas.data[1].description == "Area 2"

    def test_empty_list_area(self, admin_actor, list_area_use_case):
        """
        Test listing areas when there are no areas.
        """

        areas: PaginatedResponseDTO[Area] = list_area_use_case.execute(
            ListRequestInputDTO(actor=admin_actor)
        )

        assert len(areas.data) == 0
