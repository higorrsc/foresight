from fastapi import status
from httpx import AsyncClient


class TestPermissionRouter:
    """
    Tests for the Permission Router.
    """

    async def test_list_permissions_authenticated(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Authenticated user (admin) should be able to list permissions.
        """
        response = await client.get(
            "/permissions/",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_200_OK

        json_response = response.json()
        assert "data" in json_response
        assert "meta" in json_response

        data = json_response["data"]
        assert isinstance(data, list)

    async def test_list_permissions_unauthorized(self, client: AsyncClient):
        """
        Unauthenticated request should fail.
        """
        response = await client.get("/permissions/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
