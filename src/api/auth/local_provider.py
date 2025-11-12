from typing import Optional
from uuid import UUID

from jose import JWTError, jwt

from src.api.auth._shared import AbstractAuthenticationProvider
from src.identity_access_management.domain.entities import User
from src.identity_access_management.domain.repositories import IUserRepository
from src.shared_kernel.infrastructure.config import settings


class LocalAuthenticationProvider(AbstractAuthenticationProvider):
    """
    Local authentication provider.
    """

    def __init__(self, repository: IUserRepository):
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
            tenant_id_str: Optional[str] = payload.get("tenant_id")

            if username is None:
                return None

            tenant_id = UUID(tenant_id_str) if tenant_id_str else None
        except JWTError:
            return None

        user = self._repository.get_by_username(
            username=username,
            tenant_id=tenant_id,
        )
        return user
