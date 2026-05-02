from uuid import uuid4

import pytest

from src.core.application.use_cases.commands.generic_restore import (
    RestoreRequestInputDTO,
)
from src.identity_access_management.application.use_cases.permission import (
    InsufficientPermissionError,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities import User
from src.shared_kernel.application.use_cases.organizational_unit.commands import (
    RestoreOrganizationalUnitUseCase,
)
from src.shared_kernel.application.use_cases.organizational_unit.exceptions import (
    OrganizationalUnitNotFoundError,
)
from src.shared_kernel.domain.entities import OrganizationalUnit
from tests.fakes.in_memory_repository import OrganizationalUnitInMemoryRepository


@pytest.fixture
def repository():
    return OrganizationalUnitInMemoryRepository()


@pytest.fixture
def use_case(repository):
    return RestoreOrganizationalUnitUseCase(repository)


@pytest.fixture
def actor():
    return User(
        id=uuid4(),
        username="test_user",
        email="test@example.com",
        hashed_password="hashed_password",
        tenant_id=uuid4(),
        permissions=[AppPermission.ORGANIZATIONAL_UNIT_DELETE],  # type: ignore
    )


def test_restore_organizational_unit_success(use_case, repository, actor):
    entity_id = uuid4()
    entity = OrganizationalUnit(
        id=entity_id,
        tenant_id=actor.tenant_id,
        description="Test Unit",
        code="TU001",
        created_by=actor.id,
        updated_by=actor.id,
    )
    entity.soft_delete()
    repository.save(entity)

    assert entity.deleted_at is not None

    input_dto = RestoreRequestInputDTO(
        actor=actor,
        id=entity_id,
    )

    use_case.execute(input_dto)

    saved_entity = repository.get_by_id(entity_id, actor.tenant_id)
    assert saved_entity is not None
    assert saved_entity.deleted_at is None
    assert saved_entity.updated_by == actor.id


def test_restore_organizational_unit_insufficient_permission(
    use_case, repository, actor
):
    actor_no_perm = User(
        id=uuid4(),
        username="no_perm",
        email="no_perm@example.com",
        hashed_password="hashed_password",
        tenant_id=actor.tenant_id,
        permissions=[],  # type: ignore
    )

    input_dto = RestoreRequestInputDTO(
        actor=actor_no_perm,
        id=uuid4(),
    )

    with pytest.raises(InsufficientPermissionError):
        use_case.execute(input_dto)


def test_restore_organizational_unit_not_found(use_case, actor):
    input_dto = RestoreRequestInputDTO(
        actor=actor,
        id=uuid4(),
    )

    with pytest.raises(OrganizationalUnitNotFoundError):
        use_case.execute(input_dto)
