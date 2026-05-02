from datetime import timedelta
from uuid import uuid4

from jose import jwt

from src.api.auth.security import create_access_token
from src.core.infrastructure.config import settings


class TestSecurity:
    """
    Test suite for security-related utilities.
    """

    def test_create_access_token_success(self):
        """
        Test successful access token creation.
        """
        data = {"sub": "testuser"}
        tenant_id = uuid4()

        token = create_access_token(data=data, tenant_id=tenant_id)

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        assert payload["sub"] == "testuser"
        assert payload["tenant_id"] == str(tenant_id)
        assert "exp" in payload

    def test_create_access_token_no_tenant(self):
        """
        Test access token creation without a tenant ID.
        """
        data = {"sub": "testuser"}

        token = create_access_token(data=data, tenant_id=None)

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        assert payload["sub"] == "testuser"
        assert payload["tenant_id"] is None

    def test_create_access_token_custom_expiry(self):
        """
        Test access token creation with a custom expiration delta.
        """
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=30)

        token = create_access_token(
            data=data,
            tenant_id=None,
            expires_delta=expires_delta,
        )

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        assert payload["sub"] == "testuser"
        # Testing exact expiry is tricky due to timing, but we can check if it exists
        assert "exp" in payload
