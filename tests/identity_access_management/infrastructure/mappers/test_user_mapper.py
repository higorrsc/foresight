from datetime import UTC, datetime
from uuid import uuid4

from src.identity_access_management.domain.entities import User
from src.identity_access_management.infrastructure.mappers.user_mapper import UserMapper
from src.identity_access_management.infrastructure.models import (
    PermissionModel,
    RoleModel,
    UserModel,
)


def test_user_mapper_to_model():
    user_id = uuid4()
    tenant_id = uuid4()
    entity = User(
        id=user_id,
        tenant_id=tenant_id,
        username="testuser",
        hashed_password="hashed_password",
        first_name="Test",
        last_name="User",
        email="test@test.com",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        created_by=uuid4(),
        updated_by=uuid4(),
    )

    model = UserMapper.to_model(entity)

    assert model.id == user_id
    assert model.username == "testuser"
    assert model.email == "test@test.com"
    assert model.created_at == entity.created_at


def test_user_mapper_to_entity():
    user_id = uuid4()
    tenant_id = uuid4()

    role_model = RoleModel(id=uuid4(), name="admin", tenant_id=tenant_id)
    perm1 = PermissionModel(id=uuid4(), codename="perm1")
    perm2 = PermissionModel(id=uuid4(), codename="perm2")

    role_model.permissions_rel = [perm1]

    model = UserModel(
        id=user_id,
        tenant_id=tenant_id,
        username="testuser",
        hashed_password="hashed_password",
        first_name="Test",
        last_name="User",
        email="test@test.com",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        created_by=uuid4(),
        updated_by=uuid4(),
    )
    model.roles_rel = [role_model]
    model.permissions_rel = [perm2]

    entity = UserMapper.to_entity(model)

    assert entity.id == user_id
    assert entity.username == "testuser"
    assert "admin" in entity.roles
    assert "perm1" in entity.permissions  # From role
    assert "perm2" in entity.permissions  # Direct
    assert entity.created_at == model.created_at
