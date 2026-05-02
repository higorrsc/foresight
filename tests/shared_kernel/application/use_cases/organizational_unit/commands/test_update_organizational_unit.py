from uuid import uuid4

import pytest

from src.identity_access_management.domain.entities import User
from src.shared_kernel.application.use_cases.organizational_unit.commands import (
    UpdateOrganizationalUnitInputDTO,
    UpdateOrganizationalUnitOutputDTO,
    UpdateOrganizationalUnitUseCase,
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
    Fixture for an UpdateOrganizationalUnitUseCase.
    """
    return UpdateOrganizationalUnitUseCase(repository)


@pytest.fixture
def actor():
    """
    Fixture for a mock actor (User).
    """
    return User(
        id=uuid4(),
        username="test_user",
        email="test@example.com",
        hashed_password="hashed_password",
        tenant_id=uuid4(),
    )


class TestUpdateOrganizationalUnitUseCase:
    """
    Test suite for the UpdateOrganizationalUnitUseCase.
    """

    def test_update_organizational_unit_success(self, use_case, repository, actor):
        """
        Test successful update of an organizational unit.
        """
        # Setup: Create an existing organizational unit
        entity_id = uuid4()
        original_entity = OrganizationalUnit(
            id=entity_id,
            tenant_id=actor.tenant_id,
            description="Original Description",
            code="ORIG",
            created_by=actor.id,
            updated_by=actor.id,
        )
        repository.save(original_entity)

        input_dto = UpdateOrganizationalUnitInputDTO(
            actor=actor,
            id=entity_id,
            description="Updated Description",
            code="UPDATED",
            parent_id=None,
        )

        result = use_case.execute(input_dto)

        assert isinstance(result, UpdateOrganizationalUnitOutputDTO)
        assert result.id == entity_id
        assert result.description == "Updated Description"

        saved_entity = repository.get_by_id(entity_id, actor.tenant_id)
        assert saved_entity is not None
        assert saved_entity.description == "Updated Description"
        assert saved_entity.code == "UPDATED"
        assert saved_entity.updated_by == actor.id

    def test_update_organizational_unit_not_found(self, use_case, actor):
        """
        Test that updating a non-existent organizational unit raises an error.
        """
        input_dto = UpdateOrganizationalUnitInputDTO(
            actor=actor,
            id=uuid4(),
            description="Updated Description",
            code="UPDATED",
        )

        with pytest.raises(OrganizationalUnitNotFoundError):
            use_case.execute(input_dto)
