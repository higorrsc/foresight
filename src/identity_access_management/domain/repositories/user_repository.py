from abc import abstractmethod
from typing import Optional

from src.identity_access_management.domain.entities.user import User
from src.shared_kernel.domain._shared.repository import AbstractRepository


class IUserRepository(AbstractRepository[User]):
    """
    Interface for the User Repository.
    """

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by its email.
        """

        raise NotImplementedError  # pragma: no cover
