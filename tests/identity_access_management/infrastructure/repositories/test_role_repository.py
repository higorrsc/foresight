import pytest

from src.identity_access_management.domain.entities import Role
from src.identity_access_management.infrastructure.repositories import RoleRepository


@pytest.fixture(scope="function")
def role_repository(db_session_for_test):
    """
    Create a RoleRepository instance for testing.
    """
    return RoleRepository(db_session_for_test)


class TestRoleRepository:
    """
    Test suite for RoleRepository.
    """

    def test_save_and_get_by_id(
        self,
        role_repository,
        default_tenant_id,
    ):
        """
        Test saving a role and retrieving it by ID.
        """

        role = Role(
            name="admin2",
            description="Administrator role",
            tenant_id=default_tenant_id,
        )
        saved_role = role_repository.save(role)

        assert saved_role is not None
        assert saved_role.id == role.id

        found_role = role_repository.get_by_id(
            entity_id=saved_role.id,
            tenant_id=default_tenant_id,
        )
        assert found_role is not None
        assert found_role.name == "admin2"

    def test_get_by_name_found(
        self,
        role_repository,
        default_tenant_id,
    ):
        """
        Test retrieving a role by name when it exists.
        """

        role = Role(
            name="viewer",
            description="Viewer role",
            tenant_id=default_tenant_id,
        )
        role_repository.save(role)

        found_role = role_repository.get_by_name(
            name="viewer",
            tenant_id=default_tenant_id,
        )

        assert found_role is not None
        assert found_role.id == role.id
        assert found_role.name == "viewer"

    def test_get_by_name_not_found(
        self,
        role_repository,
        default_tenant_id,
    ):
        """
        Test retrieving a role by name when it does not exist.
        """

        found_role = role_repository.get_by_name(
            name="non_existent_role",
            tenant_id=default_tenant_id,
        )
        assert found_role is None
