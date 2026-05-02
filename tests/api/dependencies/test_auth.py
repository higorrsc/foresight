from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

from src.api.auth import LocalAuthenticationProvider
from src.api.dependencies.auth import get_auth_provider, get_current_user
from src.identity_access_management.domain.entities import User


class TestAuthDependencies:
    """
    Test suite for authentication dependencies.
    """

    def test_get_auth_provider_local(self, auth_dependency_mock_session):
        """
        Test retrieval of the local authentication provider.
        """
        with patch("src.api.dependencies.auth.settings") as mock_settings:
            mock_settings.AUTH_PROVIDER = "local"
            provider = get_auth_provider(auth_dependency_mock_session)
            assert isinstance(provider, LocalAuthenticationProvider)

    @pytest.mark.anyio
    async def test_get_current_user_success(self, auth_dependency_mock_provider):
        """
        Test successful retrieval of the current user.
        """
        token = "valid_token"
        user = Mock(spec=User)
        auth_dependency_mock_provider.get_user_from_token.return_value = user

        result = await get_current_user(auth_dependency_mock_provider, token)

        assert result == user
        auth_dependency_mock_provider.get_user_from_token.assert_called_once_with(token)

    @pytest.mark.anyio
    async def test_get_current_user_failure(self, auth_dependency_mock_provider):
        """
        Test current user retrieval failure due to invalid credentials.
        """
        token = "invalid_token"
        auth_dependency_mock_provider.get_user_from_token.return_value = None

        with pytest.raises(HTTPException) as excinfo:
            await get_current_user(auth_dependency_mock_provider, token)

        assert excinfo.value.status_code == 401
        assert excinfo.value.detail == "Invalid authentication credentials"
