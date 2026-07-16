from uuid import uuid4

from src.identity_access_management.domain.entities import Permission
from src.identity_access_management.infrastructure.mappers.permission_mapper import (
    PermissionMapper,
)
from src.identity_access_management.infrastructure.models import PermissionModel


class TestPermissionMapper:
    """
    Test suite for the PermissionMapper.
    """

    def test_permission_mapper_to_model(self):
        """
        Test mapping a Permission entity to a PermissionModel.
        """
        permission_id = uuid4()
        entity = Permission(
            id=permission_id, codename="test:perm", description="Test Permission"
        )

        model = PermissionMapper.to_model(entity)

        assert model.id == permission_id
        assert model.codename == "test:perm"
        assert model.description == "Test Permission"

    def test_permission_mapper_to_entity(self):
        """
        Test mapping a PermissionModel to a Permission entity.
        """
        permission_id = uuid4()
        model = PermissionModel(
            id=permission_id, codename="test:perm", description="Test Permission"
        )

        entity = PermissionMapper.to_entity(model)

        assert entity.id == permission_id
        assert entity.codename == "test:perm"
        assert entity.description == "Test Permission"
