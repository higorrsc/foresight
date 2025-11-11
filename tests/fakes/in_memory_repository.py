from typing import Optional
from uuid import UUID

from src.identity_access_management.domain.entities import Role, User
from src.shared_kernel.infrastructure.repositories._shared import InMemoryRepository


class UserInMemoryRepository(InMemoryRepository[User]):
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


class RoleInMemoryRepository(InMemoryRepository[Role]):
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
