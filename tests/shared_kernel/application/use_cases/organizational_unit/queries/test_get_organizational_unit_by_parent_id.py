from uuid import uuid4

from src.shared_kernel.application.use_cases.organizational_unit.queries import (
    GetOrganizationalUnitByParentIdInputDTO,
)
from src.shared_kernel.domain.entities import OrganizationalUnit


class TestGetOrganizationalUnitByParentIdUseCase:
    """
    Test suite for the GetOrganizationalUnitByParentIdUseCase.
    """

    def test_get_organizational_unit_by_parent_id_success(
        self,
        get_organizational_unit_by_parent_id_use_case,
        organizational_unit_in_memory_repo,
        admin_actor,
    ):
        """
        Test successful retrieval of organizational units by their parent ID.
        """
        parent_id = uuid4()

        unit1 = OrganizationalUnit(
            id=uuid4(),
            tenant_id=admin_actor.tenant_id,
            description="Child Unit 1",
            code="CU001",
            parent_id=parent_id,
            created_by=admin_actor.id,
            updated_by=admin_actor.id,
        )
        unit2 = OrganizationalUnit(
            id=uuid4(),
            tenant_id=admin_actor.tenant_id,
            description="Child Unit 2",
            code="CU002",
            parent_id=parent_id,
            created_by=admin_actor.id,
            updated_by=admin_actor.id,
        )
        unit3 = OrganizationalUnit(
            id=uuid4(),
            tenant_id=admin_actor.tenant_id,
            description="Other Unit",
            code="OU001",
            parent_id=uuid4(),
            created_by=admin_actor.id,
            updated_by=admin_actor.id,
        )

        organizational_unit_in_memory_repo.save(unit1)
        organizational_unit_in_memory_repo.save(unit2)
        organizational_unit_in_memory_repo.save(unit3)

        input_dto = GetOrganizationalUnitByParentIdInputDTO(
            actor=admin_actor,
            parent_id=parent_id,
        )

        result = get_organizational_unit_by_parent_id_use_case.execute(input_dto)

        assert len(result) == 2
        assert any(r.id == unit1.id for r in result)
        assert any(r.id == unit2.id for r in result)
        assert all(r.is_active is True for r in result)

    def test_get_organizational_unit_by_parent_id_empty(
        self, get_organizational_unit_by_parent_id_use_case, admin_actor
    ):
        """
        Test that an empty list is returned when no organizational units have the given parent ID.
        """
        input_dto = GetOrganizationalUnitByParentIdInputDTO(
            actor=admin_actor,
            parent_id=uuid4(),
        )

        result = get_organizational_unit_by_parent_id_use_case.execute(input_dto)

        assert result == []
