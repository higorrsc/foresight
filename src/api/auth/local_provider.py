from typing import Optional

from jose import JWTError, jwt

from src.api.auth._shared import AbstractAuthenticationProvider
from src.identity_access_management.domain.entities import User
from src.identity_access_management.infrastructure.repositories import UserRepository
from src.shared_kernel.infrastructure.config import settings


class LocalAuthenticationProvider(AbstractAuthenticationProvider):
    """
    Local authentication provider.
    """

    def __init__(self, repository: UserRepository):
        """
        Initialize the local authentication provider.
        """

        self._repository = repository

    async def get_user_from_token(self, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
            username: Optional[str] = payload.get("sub")
            if username is None:
                return None
        except JWTError:
            return None

        user = self._repository.get_by_username(username)
        return user
