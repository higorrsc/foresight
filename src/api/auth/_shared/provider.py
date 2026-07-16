from abc import ABC, abstractmethod

from src.identity_access_management.domain.entities import User


class AbstractAuthenticationProvider(ABC):
    """
    Abstract class for authentication providers.
    """

    @abstractmethod
    async def get_user_from_token(self, token: str) -> User | None:
        """
        Get a user from a token.
        """

        raise NotImplementedError  # pragma: no cover
