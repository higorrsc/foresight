from abc import abstractmethod
from typing import Optional
from uuid import UUID

from src.identity_access_management.domain.entities.user import User
from src.shared_kernel.domain._shared.repository import AbstractRepository


class IUserRepository(AbstractRepository[User]):
    """
    Interface for the User Repository.
    """

    @abstractmethod
    def get_by_email(
        self,
        email: str,
        tenant_id: Optional[UUID],
    ) -> Optional[User]:
        """
        Get a user by its email.
        """

        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_by_username(
        self,
        username: str,
        tenant_id: Optional[UUID],
    ) -> Optional[User]:
        """
        Get a user by its username and tenant.
        """

        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_by_username_global(self, username: str) -> Optional[User]:
        """
        Get a user by its username at any tenant.
        """

        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def count_users_by_role(self, role_id: UUID) -> int:
        """
        Count the number of users associated with a role.
        """

        raise NotImplementedError  # pragma: no cover
