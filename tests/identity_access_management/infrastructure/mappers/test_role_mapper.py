from datetime import UTC, datetime
from uuid import uuid4

from src.identity_access_management.domain.entities import Role
from src.identity_access_management.infrastructure.mappers.role_mapper import RoleMapper
from src.identity_access_management.infrastructure.models import (
    PermissionModel,
    RoleModel,
)


def test_role_mapper_to_model():
    role_id = uuid4()
    tenant_id = uuid4()
    entity = Role(
        id=role_id,
        tenant_id=tenant_id,
        name="admin",
        description="Admin Role",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        created_by=uuid4(),
        updated_by=uuid4(),
    )

    model = RoleMapper.to_model(entity)

    assert model.id == role_id
    assert model.tenant_id == tenant_id
    assert model.name == "admin"
    assert model.description == "Admin Role"
    assert model.created_at == entity.created_at
    assert model.created_by == entity.created_by


def test_role_mapper_to_entity():
    role_id = uuid4()
    tenant_id = uuid4()
    perm_model = PermissionModel(id=uuid4(), codename="perm1")
    model = RoleModel(
        id=role_id,
        tenant_id=tenant_id,
        name="admin",
        description="Admin Role",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        created_by=uuid4(),
        updated_by=uuid4(),
    )
    model.permissions_rel = [perm_model]

    entity = RoleMapper.to_entity(model)

    assert entity.id == role_id
    assert entity.tenant_id == tenant_id
    assert entity.name == "admin"
    assert "perm1" in entity.permissions
    assert entity.created_at == model.created_at
