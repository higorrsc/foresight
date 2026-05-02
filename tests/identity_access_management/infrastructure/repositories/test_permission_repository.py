from src.identity_access_management.domain.entities import Permission


class TestPermissionRepository:
    """
    Test suite for PermissionRepository.
    """

    def test_save_and_get_by_codename(
        self,
        permission_sqlalchemy_repo,
    ):
        """
        Test saving a permission and retrieving it by codename.
        """

        permission = Permission(
            codename="test.permission",
            description="A test permission",
        )
        permission_sqlalchemy_repo.save(permission)

        found_permission = permission_sqlalchemy_repo.get_by_codename(
            codename="test.permission"
        )
        assert found_permission is not None
        assert found_permission.codename == "test.permission"

    def test_list_all(
        self,
        permission_sqlalchemy_repo,
    ):
        """
        Test listing all permissions, including seeded and newly added ones.
        """

        # 1. Get the initial count of seeded permissions
        initial_permissions = permission_sqlalchemy_repo.list_all()
        initial_count = len(initial_permissions)
        assert initial_count > 0, "Permissions should have been seeded"

        perm1 = Permission(codename="perm.one", description="Permission One")
        perm2 = Permission(codename="perm.two", description="Permission Two")
        permission_sqlalchemy_repo.save(perm1)
        permission_sqlalchemy_repo.save(perm2)

        # 2. List all and check if the count has increased by 2
        all_permissions = permission_sqlalchemy_repo.list_all()
        assert len(all_permissions) == initial_count + 2

        # 3. Verify that the new permissions are in the list
        codenames = {p.codename for p in all_permissions}
        assert "perm.one" in codenames
        assert "perm.two" in codenames

    def test_get_by_codename_not_found(self, permission_sqlalchemy_repo):
        """Test that get_by_codename returns None for a non-existent permission."""
        found_permission = permission_sqlalchemy_repo.get_by_codename(
            "non.existent.perm"
        )
        assert found_permission is None
