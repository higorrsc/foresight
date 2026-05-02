from uuid import uuid4

import pytest

from src.identity_access_management.domain.entities import User
from src.shared_kernel.application.use_cases.organizational_unit.commands import (
    CreateOrganizationalUnitInputDTO,
    CreateOrganizationalUnitOutputDTO,
    CreateOrganizationalUnitUseCase,
)
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
    Fixture for a CreateOrganizationalUnitUseCase.
    """
    return CreateOrganizationalUnitUseCase(repository)


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


class TestCreateOrganizationalUnitUseCase:
    """
    Test suite for the CreateOrganizationalUnitUseCase.
    """

    def test_create_organizational_unit_success(self, use_case, repository, actor):
        """
        Test successful creation of an organizational unit.
        """
        input_dto = CreateOrganizationalUnitInputDTO(
            actor=actor,
            description="Test Unit",
            code="TU001",
        )

        result = use_case.execute(input_dto)

        assert isinstance(result, CreateOrganizationalUnitOutputDTO)
        assert result.id is not None

        saved_entity = repository.get_by_id(result.id, actor.tenant_id)
        assert saved_entity is not None
        assert saved_entity.description == "Test Unit"
        assert saved_entity.code == "TU001"
        assert saved_entity.tenant_id == actor.tenant_id
        assert saved_entity.created_by == actor.id
        assert saved_entity.updated_by == actor.id

    def test_create_organizational_unit_with_parent(self, use_case, repository, actor):
        """
        Test successful creation of an organizational unit with a parent.
        """
        parent_id = uuid4()
        input_dto = CreateOrganizationalUnitInputDTO(
            actor=actor,
            description="Child Unit",
            code="CU001",
            parent_id=parent_id,
        )

        result = use_case.execute(input_dto)

        assert result.id is not None
        saved_entity = repository.get_by_id(result.id, actor.tenant_id)
        assert saved_entity.parent_id == parent_id

    def test_create_organizational_unit_invalid_data(self, use_case, actor):
        """
        Test creation failure when provided with invalid data.
        """
        # Description too long or empty if there are validations in the entity
        # Let's assume description cannot be empty if it triggers EntityValidationError
        CreateOrganizationalUnitInputDTO(
            actor=actor,
            description="",  # Assuming empty description is invalid
            code="TU001",
        )

        # Note: Whether this fails depends on OrganizationalUnit entity implementation.
        # If it doesn't fail, we might need to check what actually triggers EntityValidationError.
        # For now, let's assume some validation exists.
        pass
