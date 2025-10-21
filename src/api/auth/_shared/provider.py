from abc import ABC, abstractmethod
from typing import Optional

from src.core.domain.entities import User


class AbstractAuthenticationProvider(ABC):
    """
    Abstract class for authentication providers.
    """

    @abstractmethod
    async def get_user_from_token(self, token: str) -> Optional[User]:
        """
        Get a user from a token.
        """

        raise NotImplementedError  # pragma: no cover
