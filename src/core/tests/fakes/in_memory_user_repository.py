from typing import Optional

from src.core.domain.entities import User
from src.core.infrastructure.repositories._shared import InMemoryRepository


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
