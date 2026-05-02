from src.core.application.dto import PaginatedResponseDTO
from src.core.application.use_cases.queries import ListRequestInputDTO
from src.shared_kernel.application.use_cases.organizational_unit.queries import (
    ListOrganizationalUnitUseCase,
)
from src.shared_kernel.domain.entities import OrganizationalUnit
from tests.fakes.in_memory_repository import OrganizationalUnitInMemoryRepository


class TestListOrganizationalUnit:
    """
    Test the ListOrganizationalUnit use case.
    """

    def test_list_organizational_units(self, admin_actor):
        """
        Test listing organizational units.
        """

        repository = OrganizationalUnitInMemoryRepository()
        use_case = ListOrganizationalUnitUseCase(repository)

        unit1 = OrganizationalUnit(
            description="Unit 1",
            code="U1",
            tenant_id=admin_actor.tenant_id,
        )
        unit2 = OrganizationalUnit(
            description="Unit 2",
            code="U2",
            tenant_id=admin_actor.tenant_id,
        )

        repository.save(unit1)
        repository.save(unit2)

        units: PaginatedResponseDTO[OrganizationalUnit] = use_case.execute(
            ListRequestInputDTO(actor=admin_actor)
        )

        assert len(units.data) == 2
        assert units.data[0].id is not None
        assert units.data[0].description == "Unit 1"
        assert units.data[1].id is not None
        assert units.data[1].description == "Unit 2"

    def test_empty_list_organizational_unit(self, admin_actor):
        """
        Test listing organizational units when there are no units.
        """

        repository = OrganizationalUnitInMemoryRepository()
        use_case = ListOrganizationalUnitUseCase(repository)

        units: PaginatedResponseDTO[OrganizationalUnit] = use_case.execute(
            ListRequestInputDTO(actor=admin_actor)
        )

        assert len(units.data) == 0
