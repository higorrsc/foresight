from uuid import uuid4

import pytest

from src.identity_access_management.application.use_cases.permission import (
    InsufficientPermissionError,
    PermissionNotFoundError,
)
from src.identity_access_management.application.use_cases.role import RoleNotFoundError
from src.identity_access_management.application.use_cases.role.commands import (
    SetRolePermissionsInputDTO,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities import Permission, Role


class TestSetRolePermissionsUseCase:
    """
    Test suite for SetRolePermissionsUseCase.
    """

    def test_set_permissions_success(
        self,
        set_role_permissions_use_case,
        role_in_memory_repo,
        permission_in_memory_repo,
        admin_actor,
    ):
        """
        Test setting permissions for a role successfully.
        """
        permission_in_memory_repo.save(
            Permission(codename="perm1", description="Description")
        )
        permission_in_memory_repo.save(
            Permission(codename="perm2", description="Description")
        )

        admin_actor.permissions.add(AppPermission.ROLE_SET_PERMISSIONS)
        role = Role(
            name="Test Role",
            description="Desc",
            tenant_id=admin_actor.tenant_id,
        )
        role_in_memory_repo.save(role)

        input_dto = SetRolePermissionsInputDTO(
            actor=admin_actor,
            role_id_to_update=role.id,
            permissions_codes=["perm1", "perm2"],
        )

        set_role_permissions_use_case.execute(input_dto)

        updated_role = role_in_memory_repo.get_by_id(role.id, admin_actor.tenant_id)
        assert "perm1" in updated_role.permissions
        assert "perm2" in updated_role.permissions
        assert len(updated_role.permissions) == 2
        assert updated_role.updated_by == admin_actor.id

    def test_insufficient_permission(
        self, set_role_permissions_use_case, role_in_memory_repo, admin_actor
    ):
        """
        Test that a user without permission cannot set role permissions.
        """
        if AppPermission.ROLE_SET_PERMISSIONS in admin_actor.permissions:
            admin_actor.permissions.remove(AppPermission.ROLE_SET_PERMISSIONS)

        role = Role(
            name="Test Role",
            description="Desc",
            tenant_id=admin_actor.tenant_id,
        )
        role_in_memory_repo.save(role)

        input_dto = SetRolePermissionsInputDTO(
            actor=admin_actor,
            role_id_to_update=role.id,
            permissions_codes=["perm1"],
        )

        with pytest.raises(InsufficientPermissionError):
            set_role_permissions_use_case.execute(input_dto)

    def test_role_not_found(self, set_role_permissions_use_case, admin_actor):
        """
        Test that trying to update a non-existent role raises RoleNotFoundError.
        """
        admin_actor.permissions.add(AppPermission.ROLE_SET_PERMISSIONS)

        input_dto = SetRolePermissionsInputDTO(
            actor=admin_actor,
            role_id_to_update=uuid4(),
            permissions_codes=["perm1"],
        )

        with pytest.raises(RoleNotFoundError):
            set_role_permissions_use_case.execute(input_dto)

    def test_permission_not_found(
        self,
        set_role_permissions_use_case,
        role_in_memory_repo,
        permission_in_memory_repo,
        admin_actor,
    ):
        """
        Test that providing an invalid permission code raises PermissionNotFoundError.
        """
        permission_in_memory_repo.save(
            Permission(codename="perm1", description="Description")
        )

        admin_actor.permissions.add(AppPermission.ROLE_SET_PERMISSIONS)
        role = Role(
            name="Test Role", description="Desc", tenant_id=admin_actor.tenant_id
        )
        role_in_memory_repo.save(role)

        input_dto = SetRolePermissionsInputDTO(
            actor=admin_actor,
            role_id_to_update=role.id,
            permissions_codes=["perm1", "invalid_perm"],
        )

        with pytest.raises(
            PermissionNotFoundError,
            match="Permission 'invalid_perm' not found.",
        ):
            set_role_permissions_use_case.execute(input_dto)
