from fastapi import status
from fastapi.testclient import TestClient


class TestPermissionRouter:
    """
    Tests for the Permission Router.
    """

    def test_list_permissions_authenticated(self, client: TestClient, admin_token: str):
        """
        Authenticated user (admin) should be able to list permissions.
        """
        response = client.get(
            "/permissions/",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        # Seeding creates many permissions, verify at least one known
        assert any(p["codename"] == "user:read" for p in data)

    def test_list_permissions_unauthorized(self, client: TestClient):
        """
        Unauthenticated request should fail.
        """
        response = client.get("/permissions/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
