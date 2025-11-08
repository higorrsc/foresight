from typing import Optional

from src.identity_access_management.domain.entities import Role, User
from src.shared_kernel.infrastructure.repositories._shared import InMemoryRepository


class UserInMemoryRepository(InMemoryRepository[User]):
    """
    In Memory Repository specific to test User entity,
    this implements get_by_username method.
    """

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Method to get a user by its username.
        """

        for user in self._entities:
            if user.username == username:
                return user

        return None


class RoleInMemoryRepository(InMemoryRepository[Role]):
    """
    In Memory Repository specific to test Role entity,
    this implements get_by_name method.
    """

    def get_by_name(self, name: str) -> Optional[Role]:
        """
        Method to get a role by its name.
        """

        for role in self._entities:
            if role.name == name:
                return role

        return None
