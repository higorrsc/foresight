from datetime import datetime
from uuid import uuid4

from src.shared_kernel.domain.entities import OrganizationalUnit
from src.shared_kernel.infrastructure.mappers.organizational_unit_mapper import (
    OrganizationalUnitMapper,
)
from src.shared_kernel.infrastructure.models import OrganizationalUnitModel


class TestOrganizationalUnitMapper:
    """
    Test suite for the OrganizationalUnitMapper.
    """

    def test_organizational_unit_to_model(self):
        """
        Test mapping of an OrganizationalUnit entity to an OrganizationalUnitModel.
        """
        tenant_id = uuid4()
        entity_id = uuid4()
        parent_id = uuid4()
        created_by = uuid4()
        created_at = datetime.now()

        entity = OrganizationalUnit(
            id=entity_id,
            tenant_id=tenant_id,
            code="OU001",
            description="Test Organizational Unit",
            parent_id=parent_id,
        )
        # Add auditing fields
        entity.created_at = created_at
        entity.created_by = created_by

        model = OrganizationalUnitMapper.to_model(entity)

        assert model.id == entity_id
        assert model.tenant_id == tenant_id
        assert model.code == "OU001"
        assert model.description == "Test Organizational Unit"
        assert model.parent_id == parent_id
        assert model.created_at == created_at
        assert model.created_by == created_by

    def test_organizational_unit_to_entity(self):
        """
        Test mapping of an OrganizationalUnitModel to an OrganizationalUnit entity.
        """
        tenant_id = uuid4()
        model_id = uuid4()
        parent_id = uuid4()
        created_by = uuid4()
        created_at = datetime.now()

        model = OrganizationalUnitModel(
            id=model_id,
            tenant_id=tenant_id,
            code="OU002",
            description="Test Organizational Unit Model",
            parent_id=parent_id,
            created_by=created_by,
            created_at=created_at,
        )

        entity = OrganizationalUnitMapper.to_entity(model)

        assert entity.id == model_id
        assert entity.tenant_id == tenant_id
        assert entity.code == "OU002"
        assert entity.description == "Test Organizational Unit Model"
        assert entity.parent_id == parent_id
        assert entity.created_by == created_by
        assert entity.created_at == created_at
