from httpx import AsyncClient


class TestAuthRouter:
    """
    Test Auth Router.
    """

    async def test_get_token(self, client: AsyncClient):
        """
        Test get token.
        """

        response = await client.post(
            "/auth/token",
            data={
                "username": "admin",
                "password": "foresight_admin",
            },
        )

        assert response.status_code == 200, response.json()
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    async def test_get_token_invalid_credentials(self, client: AsyncClient):
        """
        Test get token with invalid credentials.
        """

        response = await client.post(
            "/auth/token",
            data={
                "username": "admin",
                "password": "invalid_password",
            },
        )

        assert response.status_code == 401, response.json()
        assert "detail" in response.json()
        assert response.json()["detail"] == "Incorrect username or password"
