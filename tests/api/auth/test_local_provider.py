from unittest.mock import Mock, patch
from uuid import uuid4

import pytest
from jose import JWTError

from src.api.auth.local_provider import LocalAuthenticationProvider
from src.identity_access_management.domain.entities import User


@pytest.fixture
def mock_repo():
    """
    Fixture for a mock repository.
    """
    return Mock()


@pytest.fixture
def provider(mock_repo):
    """
    Fixture for the LocalAuthenticationProvider.
    """
    return LocalAuthenticationProvider(mock_repo)


class TestLocalAuthenticationProvider:
    """
    Test suite for the LocalAuthenticationProvider.
    """

    @pytest.mark.anyio
    async def test_get_user_from_token_success(self, provider, mock_repo):
        """
        Test successful user retrieval from a valid token.
        """
        token = "valid_token"
        username = "testuser"
        tenant_id = uuid4()
        payload = {"sub": username, "tenant_id": str(tenant_id)}

        user = Mock(spec=User)
        mock_repo.get_by_username.return_value = user

        with patch("jose.jwt.decode", return_value=payload):
            result = await provider.get_user_from_token(token)

        assert result == user
        mock_repo.get_by_username.assert_called_once_with(
            username=username, tenant_id=tenant_id
        )

    @pytest.mark.anyio
    async def test_get_user_from_token_invalid_jwt(self, provider):
        """
        Test user retrieval failure due to invalid JWT.
        """
        token = "invalid_token"

        with patch("jose.jwt.decode", side_effect=JWTError):
            result = await provider.get_user_from_token(token)

        assert result is None

    @pytest.mark.anyio
    async def test_get_user_from_token_missing_sub(self, provider):
        """
        Test user retrieval failure due to missing 'sub' in payload.
        """
        token = "valid_token"
        payload = {"tenant_id": str(uuid4())}

        with patch("jose.jwt.decode", return_value=payload):
            result = await provider.get_user_from_token(token)

        assert result is None

    @pytest.mark.anyio
    async def test_get_user_from_token_no_tenant_id(self, provider, mock_repo):
        """
        Test successful user retrieval when tenant_id is missing from token.
        """
        token = "valid_token"
        username = "testuser"
        payload = {"sub": username}

        user = Mock(spec=User)
        mock_repo.get_by_username.return_value = user

        with patch("jose.jwt.decode", return_value=payload):
            result = await provider.get_user_from_token(token)

        assert result == user
        mock_repo.get_by_username.assert_called_once_with(
            username=username, tenant_id=None
        )
