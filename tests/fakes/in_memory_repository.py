from typing import List, Optional
from uuid import UUID

from src.identity_access_management.domain.entities import Permission, Role, User
from src.identity_access_management.domain.repositories import (
    IPermissionRepository,
    IRoleRepository,
    IUserRepository,
)
from src.shared_kernel.domain.entities import Area, OrganizationalUnit
from src.shared_kernel.domain.repositories import (
    IAreaRepository,
    IOrganizationalUnitRepository,
)
from src.shared_kernel.infrastructure.repositories._shared import InMemoryRepository
from src.tenant_management.domain.entities import Plan, Tenant
from src.tenant_management.domain.repositories import IPlanRepository, ITenantRepository


class UserInMemoryRepository(
    InMemoryRepository[User],
    IUserRepository,
):
    """
    In Memory Repository specific to test User entity,
    this implements get_by_username method.
    """

    def get_by_username(
        self,
        username: str,
        tenant_id: Optional[UUID],
    ) -> Optional[User]:
        """
        Method to get a user by its username.
        """

        for user in self._entities:
            if user.username == username and user.tenant_id == tenant_id:
                return user

        return None

    def get_by_username_global(self, username: str) -> Optional[User]:
        """
        Method to get a user by its username globally.
        """

        for entity in self._entities:
            if entity.username == username:
                return entity

        return None

    def get_by_email(self, email: str, tenant_id: UUID | None) -> User | None:
        """
        Method to get a user by its email.
        """

        for user in self._entities:
            if user.email == email and user.tenant_id == tenant_id:
                return user

        return None


class RoleInMemoryRepository(
    InMemoryRepository[Role],
    IRoleRepository,
):
    """
    In Memory Repository specific to test Role entity,
    this implements get_by_name method.
    """

    def get_by_name(
        self,
        name: str,
        tenant_id: Optional[UUID],
    ) -> Optional[Role]:
        """
        Method to get a role by its name.
        """

        for role in self._entities:
            if role.name == name and role.tenant_id == tenant_id:
                return role

        return None


class PermissionInMemoryRepository(
    InMemoryRepository[Permission],
    IPermissionRepository,
):
    """
    In Memory Repository specific to test Permission entity,
    this implements get_by_codename method.
    """

    def list_all(self) -> list[Permission]:
        """
        Method to list all permissions.
        """

        return self._entities

    def get_by_codename(self, codename: str) -> Permission | None:
        """
        Method to get a permission by its codename.
        """

        for permission in self._entities:
            if permission.codename == codename:
                return permission

        return None


class PlanInMemoryRepository(
    InMemoryRepository[Plan],
    IPlanRepository,
):
    """
    In Memory Repository specific to test Plan entity,
    this implements get_by_name method.
    """

    def get_by_name(self, name: str) -> Optional[Plan]:
        """
        Method to get a plan by its name.
        """

        for plan in self._entities:
            if plan.name == name:
                return plan
        return None


class TenantInMemoryRepository(
    InMemoryRepository[Tenant],
    ITenantRepository,
):
    """
    In Memory Repository specific to test Tenant entity,
    this implements get_by_name method.
    """

    def get_by_name(self, name: str) -> Optional[Tenant]:
        """
        Method to get a tenant by its name.
        """

        for tenant in self._entities:
            if tenant.name == name:
                return tenant

        return None

    def get_by_id_global(self, tenant_id: UUID) -> Optional[Tenant]:
        """
        Finds a tenant by its unique id.
        """

        for tenant in self._entities:
            if tenant.id == tenant_id:
                return tenant

        return None


class AreaInMemoryRepository(
    InMemoryRepository[Area],
    IAreaRepository,
):
    """
    In Memory Repository specific to test Area entity
    """


class OrganizationalUnitInMemoryRepository(
    InMemoryRepository[OrganizationalUnit],
    IOrganizationalUnitRepository,
):
    """
    In Memory Repository specific to test OrganizationalUnit entity
    """

    def get_by_parent_id(
        self,
        parent_id: UUID,
        tenant_id: UUID,
    ) -> List[OrganizationalUnit]:
        """
        Get organizational units by parent ID.
        """

        return [
            organizational_unit
            for organizational_unit in self._entities
            if organizational_unit.parent_id == parent_id
            and organizational_unit.tenant_id == tenant_id
        ]
