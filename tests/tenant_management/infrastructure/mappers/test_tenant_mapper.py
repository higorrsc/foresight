from datetime import UTC, datetime
from uuid import uuid4

from src.tenant_management.domain.entities import Tenant
from src.tenant_management.domain.value_objects import TenantStatus
from src.tenant_management.infrastructure.mappers.tenant_mapper import TenantMapper
from src.tenant_management.infrastructure.models import TenantModel


def test_tenant_mapper_to_model():
    tenant_id = uuid4()
    plan_id = uuid4()
    entity = Tenant(
        id=tenant_id,
        name="Test Tenant",
        status=TenantStatus.ACTIVE,
        plan_id=plan_id,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        created_by=uuid4(),
        updated_by=uuid4(),
    )

    model = TenantMapper.to_model(entity)

    assert model.id == tenant_id
    assert model.name == "Test Tenant"
    assert model.status == TenantStatus.ACTIVE
    assert model.plan_id == plan_id
    assert model.created_at == entity.created_at
    assert model.updated_at == entity.updated_at
    assert model.created_by == entity.created_by
    assert model.updated_by == entity.updated_by


def test_tenant_mapper_to_entity():
    tenant_id = uuid4()
    plan_id = uuid4()
    model = TenantModel(
        id=tenant_id,
        name="Mapped Tenant",
        status=TenantStatus.TRIAL,
        plan_id=plan_id,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        created_by=uuid4(),
        updated_by=uuid4(),
    )

    entity = TenantMapper.to_entity(model)

    assert entity.id == tenant_id
    assert entity.name == "Mapped Tenant"
    assert entity.status == TenantStatus.TRIAL
    assert entity.plan_id == plan_id
    assert entity.created_at == model.created_at
    assert entity.updated_at == model.updated_at
    assert entity.created_by == model.created_by
    assert entity.updated_by == model.updated_by
