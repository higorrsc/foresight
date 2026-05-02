from uuid import uuid4

import pytest

from src.core.application.use_cases.commands.generic_delete import DeleteRequestInputDTO
from src.identity_access_management.application.use_cases.permission import (
    InsufficientPermissionError,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities import User
from src.shared_kernel.application.use_cases.organizational_unit.commands import (
    DeleteOrganizationalUnitUseCase,
)
from src.shared_kernel.application.use_cases.organizational_unit.exceptions import (
    OrganizationalUnitNotFoundError,
)
from src.shared_kernel.domain.entities import OrganizationalUnit
from tests.fakes.in_memory_repository import OrganizationalUnitInMemoryRepository


@pytest.fixture
def repository():
    """
    Fixture for an OrganizationalUnitInMemoryRepository.
    """
    return OrganizationalUnitInMemoryRepository()


@pytest.fixture
def use_case(repository):
    """
    Fixture for a DeleteOrganizationalUnitUseCase.
    """
    return DeleteOrganizationalUnitUseCase(repository)


@pytest.fixture
def actor():
    """
    Fixture for a mock actor (User) with delete permissions.
    """
    return User(
        id=uuid4(),
        username="test_user",
        email="test@example.com",
        hashed_password="hashed_password",
        tenant_id=uuid4(),
        permissions=[AppPermission.ORGANIZATIONAL_UNIT_DELETE],  # type: ignore
    )


class TestDeleteOrganizationalUnitUseCase:
    """
    Test suite for the DeleteOrganizationalUnitUseCase.
    """

    def test_delete_organizational_unit_success(self, use_case, repository, actor):
        """
        Test successful deletion (soft delete) of an organizational unit.
        """
        entity_id = uuid4()
        entity = OrganizationalUnit(
            id=entity_id,
            tenant_id=actor.tenant_id,
            description="Test Unit",
            code="TU001",
            created_by=actor.id,
            updated_by=actor.id,
        )
        repository.save(entity)

        input_dto = DeleteRequestInputDTO(
            actor=actor,
            id=entity_id,
        )

        use_case.execute(input_dto)

        saved_entity = repository.get_by_id(entity_id, actor.tenant_id)
        assert saved_entity is not None
        assert saved_entity.deleted_at is not None
        assert saved_entity.updated_by == actor.id

    def test_delete_organizational_unit_insufficient_permission(
        self, use_case, repository, actor
    ):
        """
        Test that deletion fails when the actor has insufficient permissions.
        """
        actor_no_perm = User(
            id=uuid4(),
            username="no_perm",
            email="no_perm@example.com",
            hashed_password="hashed_password",
            tenant_id=actor.tenant_id,
            permissions=[],  # type: ignore
        )

        input_dto = DeleteRequestInputDTO(
            actor=actor_no_perm,
            id=uuid4(),
        )

        with pytest.raises(InsufficientPermissionError):
            use_case.execute(input_dto)

    def test_delete_organizational_unit_not_found(self, use_case, actor):
        """
        Test that deletion fails when the organizational unit is not found.
        """
        input_dto = DeleteRequestInputDTO(
            actor=actor,
            id=uuid4(),
        )

        with pytest.raises(OrganizationalUnitNotFoundError):
            use_case.execute(input_dto)
