from src.identity_access_management.domain.entities import Role


class TestRoleRepository:
    """
    Test suite for RoleRepository.
    """

    async def test_save_and_get_by_id(
        self,
        role_sqlalchemy_repo,
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
        saved_role = await role_sqlalchemy_repo.save(role)

        assert saved_role is not None
        assert saved_role.id == role.id

        found_role = await role_sqlalchemy_repo.get_by_id(
            entity_id=saved_role.id,
            tenant_id=default_tenant_id,
        )
        assert found_role is not None
        assert found_role.name == "admin2"

    async def test_get_by_name_found(
        self,
        role_sqlalchemy_repo,
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
        await role_sqlalchemy_repo.save(role)

        found_role = await role_sqlalchemy_repo.get_by_name(
            name="viewer",
            tenant_id=default_tenant_id,
        )

        assert found_role is not None
        assert found_role.id == role.id
        assert found_role.name == "viewer"

    async def test_get_by_name_not_found(
        self,
        role_sqlalchemy_repo,
        default_tenant_id,
    ):
        """
        Test retrieving a role by name when it does not exist.
        """

        found_role = await role_sqlalchemy_repo.get_by_name(
            name="non_existent_role",
            tenant_id=default_tenant_id,
        )
        assert found_role is None
