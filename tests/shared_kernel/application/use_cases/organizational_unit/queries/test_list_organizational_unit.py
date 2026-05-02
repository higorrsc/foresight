from src.core.application.dto import PaginatedResponseDTO
from src.core.application.use_cases.queries import ListRequestInputDTO
from src.shared_kernel.domain.entities import OrganizationalUnit


class TestListOrganizationalUnit:
    """
    Test the ListOrganizationalUnit use case.
    """

    def test_list_organizational_units(
        self,
        admin_actor,
        organizational_unit_in_memory_repo,
        list_organizational_unit_use_case,
    ):
        """
        Test listing organizational units.
        """

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

        organizational_unit_in_memory_repo.save(unit1)
        organizational_unit_in_memory_repo.save(unit2)

        units: PaginatedResponseDTO[OrganizationalUnit] = (
            list_organizational_unit_use_case.execute(
                ListRequestInputDTO(actor=admin_actor)
            )
        )

        assert len(units.data) == 2
        assert units.data[0].id is not None
        assert units.data[0].description == "Unit 1"
        assert units.data[1].id is not None
        assert units.data[1].description == "Unit 2"

    def test_empty_list_organizational_unit(
        self, admin_actor, list_organizational_unit_use_case
    ):
        """
        Test listing organizational units when there are no units.
        """

        units: PaginatedResponseDTO[OrganizationalUnit] = (
            list_organizational_unit_use_case.execute(
                ListRequestInputDTO(actor=admin_actor)
            )
        )

        assert len(units.data) == 0
