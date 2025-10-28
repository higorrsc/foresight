from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.api.auth import LocalAuthenticationProvider
from src.api.auth._shared import AbstractAuthenticationProvider
from src.api.dependencies.database import get_db_session
from src.identity_access_management.domain.entities import User
from src.identity_access_management.infrastructure.repositories import UserRepository
from src.shared_kernel.infrastructure.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_auth_provider(
    session: Session = Depends(get_db_session),
) -> AbstractAuthenticationProvider:
    """
    Reads config and return correct instance of authentication provider.
    """

    if settings.AUTH_PROVIDER == "local":
        repo = UserRepository(session)
        return LocalAuthenticationProvider(repo)
    else:
        raise ValueError(
            f"Invalid auth provider: {settings.AUTH_PROVIDER}"
        )  # pragma: no cover


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    provider: AbstractAuthenticationProvider = Depends(get_auth_provider),
) -> User:
    """
    Main security dependency. Uses injected authentication provider to validate token.
    """

    user = await provider.get_user_from_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
