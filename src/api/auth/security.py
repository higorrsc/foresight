from datetime import datetime, timedelta, timezone
from typing import Dict, Optional
from uuid import UUID

from jose import jwt

from src.core.infrastructure.config import settings


def create_access_token(
    data: Dict,
    tenant_id: Optional[UUID],
    expires_delta: Optional[timedelta] = None,
):
    """
    Create an access token.
    """

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=15)
    )

    to_encode.update(
        {
            "exp": expire,
            "tenant_id": str(tenant_id) if tenant_id else None,
        }
    )
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt
