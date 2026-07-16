from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from src.api.auth.local_provider import LocalAuthenticationProvider
from src.identity_access_management.domain.entities import User


class TestLocalAuthenticationProvider:
    """Test suite for the LocalAuthenticationProvider."""

    @pytest.mark.anyio
    async def test_get_user_from_token_success(
        self,
        local_auth_provider: LocalAuthenticationProvider,
        local_auth_provider_mock_repo: Mock,
    ):
        """Test successful user retrieval from a valid token."""

        token = "valid_token"
        username = "testuser"
        tenant_id = uuid4()
        payload = {"sub": username, "tenant_id": str(tenant_id)}

        # 1. O utilizador devolvido é um Mock normal
        user = Mock(spec=User)

        # 2. O método de busca do repositório é que é um AsyncMock
        local_auth_provider_mock_repo.get_by_username = AsyncMock(return_value=user)

        # 3. Patch apontando para a biblioteca jose, exatamente como você tinha feito!
        with patch("jose.jwt.decode", return_value=payload):
            result = await local_auth_provider.get_user_from_token(token)

        assert result == user
        local_auth_provider_mock_repo.get_by_username.assert_called_once_with(
            username=username, tenant_id=tenant_id
        )

    @pytest.mark.anyio
    async def test_get_user_from_token_no_tenant_id(
        self,
        local_auth_provider: LocalAuthenticationProvider,
        local_auth_provider_mock_repo: Mock,
    ):
        """Test user retrieval when tenant_id is missing from token payload."""

        token = "valid_token"
        username = "testuser"
        payload = {"sub": username}  # No tenant_id

        # 1. Utilizador normal
        user = Mock(spec=User)

        # 2. O método global de busca é AsyncMock
        local_auth_provider_mock_repo.get_by_username = AsyncMock(return_value=user)

        # 3. Patch apontando para a biblioteca jose
        with patch("jose.jwt.decode", return_value=payload):
            result = await local_auth_provider.get_user_from_token(token)

        assert result == user
        local_auth_provider_mock_repo.get_by_username.assert_called_once_with(
            username="testuser", tenant_id=None
        )
