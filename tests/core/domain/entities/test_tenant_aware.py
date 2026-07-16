from uuid import uuid4

from src.core.domain.entities.tenant_aware import TenantAwareEntity


class TestTenantAwareEntity:
    """
    Test suite for the TenantAwareEntity.
    """

    def test_tenant_aware_entity_initialization(self):
        """
        Test that TenantAwareEntity initializes correctly with valid data.
        """
        tenant_id = uuid4()
        entity_id = uuid4()

        class MyEntity(TenantAwareEntity):
            def validate(self):
                pass

        entity = MyEntity(id=entity_id, tenant_id=tenant_id)

        assert entity.id == entity_id
        assert entity.tenant_id == tenant_id

    def test_tenant_aware_entity_default_tenant_id(self):
        """
        Test that TenantAwareEntity defaults tenant_id to None if not provided.
        """
        entity_id = uuid4()

        class MyEntity(TenantAwareEntity):
            def validate(self):
                pass

        entity = MyEntity(id=entity_id)

        assert entity.tenant_id is None
