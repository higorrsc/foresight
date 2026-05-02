from unittest.mock import Mock, patch
from uuid import uuid4

import pytest
from jose import JWTError

from src.identity_access_management.domain.entities import User


class TestLocalAuthenticationProvider:
    """
    Test suite for the LocalAuthenticationProvider.
    """

    @pytest.mark.anyio
    async def test_get_user_from_token_success(
        self, local_auth_provider, local_auth_provider_mock_repo
    ):
        """
        Test successful user retrieval from a valid token.
        """
        token = "valid_token"
        username = "testuser"
        tenant_id = uuid4()
        payload = {"sub": username, "tenant_id": str(tenant_id)}

        user = Mock(spec=User)
        local_auth_provider_mock_repo.get_by_username.return_value = user

        with patch("jose.jwt.decode", return_value=payload):
            result = await local_auth_provider.get_user_from_token(token)

        assert result == user
        local_auth_provider_mock_repo.get_by_username.assert_called_once_with(
            username=username, tenant_id=tenant_id
        )

    @pytest.mark.anyio
    async def test_get_user_from_token_invalid_jwt(self, local_auth_provider):
        """
        Test user retrieval failure due to invalid JWT.
        """
        token = "invalid_token"

        with patch("jose.jwt.decode", side_effect=JWTError):
            result = await local_auth_provider.get_user_from_token(token)

        assert result is None

    @pytest.mark.anyio
    async def test_get_user_from_token_missing_sub(self, local_auth_provider):
        """
        Test user retrieval failure due to missing 'sub' in payload.
        """
        token = "valid_token"
        payload = {"tenant_id": str(uuid4())}

        with patch("jose.jwt.decode", return_value=payload):
            result = await local_auth_provider.get_user_from_token(token)

        assert result is None

    @pytest.mark.anyio
    async def test_get_user_from_token_no_tenant_id(
        self, local_auth_provider, local_auth_provider_mock_repo
    ):
        """
        Test successful user retrieval when tenant_id is missing from token.
        """
        token = "valid_token"
        username = "testuser"
        payload = {"sub": username}

        user = Mock(spec=User)
        local_auth_provider_mock_repo.get_by_username.return_value = user

        with patch("jose.jwt.decode", return_value=payload):
            result = await local_auth_provider.get_user_from_token(token)

        assert result == user
        local_auth_provider_mock_repo.get_by_username.assert_called_once_with(
            username=username, tenant_id=None
        )
