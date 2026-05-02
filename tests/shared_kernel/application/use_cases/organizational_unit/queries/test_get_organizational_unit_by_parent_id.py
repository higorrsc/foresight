from uuid import uuid4

import pytest

from src.shared_kernel.application.use_cases.organizational_unit.queries import (
    GetOrganizationalUnitByParentIdInputDTO,
    GetOrganizationalUnitByParentIdUseCase,
)
from src.shared_kernel.domain.entities import OrganizationalUnit
from tests.fakes import OrganizationalUnitInMemoryRepository


@pytest.fixture
def repository():
    return OrganizationalUnitInMemoryRepository()


@pytest.fixture
def use_case(repository):
    return GetOrganizationalUnitByParentIdUseCase(repository)


def test_get_organizational_unit_by_parent_id_success(
    use_case, repository, admin_actor
):
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

    repository.save(unit1)
    repository.save(unit2)
    repository.save(unit3)

    input_dto = GetOrganizationalUnitByParentIdInputDTO(
        actor=admin_actor,
        parent_id=parent_id,
    )

    result = use_case.execute(input_dto)

    assert len(result) == 2
    assert any(r.id == unit1.id for r in result)
    assert any(r.id == unit2.id for r in result)
    assert all(r.is_active is True for r in result)


def test_get_organizational_unit_by_parent_id_empty(use_case, repository, admin_actor):
    input_dto = GetOrganizationalUnitByParentIdInputDTO(
        actor=admin_actor,
        parent_id=uuid4(),
    )

    result = use_case.execute(input_dto)

    assert result == []
