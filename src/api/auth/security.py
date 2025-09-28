from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from jose import jwt

from src.core.infrastructure.config.settings import settings


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None):
    """
    Create an access token.
    """

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=15)
    )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt
