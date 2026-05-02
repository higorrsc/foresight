from uuid import uuid4

import pytest

from src.core.application.use_cases.queries.generic_get_by_id import (
    GetByIdRequestInputDTO,
)
from src.identity_access_management.application.use_cases.permission import (
    InsufficientPermissionError,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities import User
from src.shared_kernel.application.use_cases.organizational_unit.exceptions import (
    OrganizationalUnitNotFoundError,
)
from src.shared_kernel.application.use_cases.organizational_unit.queries import (
    GetOrganizationalUnitByIdUseCase,
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
    Fixture for a GetOrganizationalUnitByIdUseCase.
    """
    return GetOrganizationalUnitByIdUseCase(repository)


@pytest.fixture
def actor():
    """
    Fixture for a mock actor (User) with read permissions.
    """
    return User(
        id=uuid4(),
        username="test_user",
        email="test@example.com",
        hashed_password="hashed_password",
        tenant_id=uuid4(),
        permissions=[AppPermission.ORGANIZATIONAL_UNIT_READ],  # type: ignore
    )


class TestGetOrganizationalUnitByIdUseCase:
    """
    Test suite for the GetOrganizationalUnitByIdUseCase.
    """

    def test_get_organizational_unit_by_id_success(self, use_case, repository, actor):
        """
        Test successful retrieval of an organizational unit by its ID.
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

        input_dto = GetByIdRequestInputDTO(
            actor=actor,
            id=entity_id,
        )

        result = use_case.execute(input_dto)

        assert result == entity
        assert result.id == entity_id

    def test_get_organizational_unit_by_id_insufficient_permission(
        self, use_case, actor
    ):
        """
        Test that retrieval fails when the actor has insufficient permissions.
        """
        actor_no_perm = User(
            id=uuid4(),
            username="no_perm",
            email="no_perm@example.com",
            hashed_password="hashed_password",
            tenant_id=actor.tenant_id,
            permissions=[],  # type: ignore
        )

        input_dto = GetByIdRequestInputDTO(
            actor=actor_no_perm,
            id=uuid4(),
        )

        with pytest.raises(InsufficientPermissionError):
            use_case.execute(input_dto)

    def test_get_organizational_unit_by_id_not_found(self, use_case, actor):
        """
        Test that retrieval fails when the organizational unit is not found.
        """
        input_dto = GetByIdRequestInputDTO(
            actor=actor,
            id=uuid4(),
        )

        with pytest.raises(OrganizationalUnitNotFoundError):
            use_case.execute(input_dto)
