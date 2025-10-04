from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient


class TestRolesRouter:
    """
    Test Roles Router.
    """

    def get_admin_auth_token(self, client: TestClient) -> str:
        """
        Get admin authentication token for testing.
        """

        response = client.post(
            "/auth/token",
            data={
                "username": "admin",
                "password": "foresight_admin",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        return response.json()["access_token"]

    def get_guest_auth_token(self, client: TestClient) -> str:
        """
        Get guest authentication token for testing.
        """

        response = client.post(
            "/auth/token",
            data={
                "username": "guest",
                "password": "foresight_guest",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        return response.json()["access_token"]

    def test_create_role_without_token_raises_error(self, client: TestClient):
        """
        Test create role.
        """

        response = client.post(
            "/roles/",
            json={
                "description": "Test Role",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_role_with_insufficient_permission_raises_error(
        self,
        client: TestClient,
    ):
        """
        Test create role.
        """

        token = self.get_guest_auth_token(client)
        response = client.post(
            "/roles/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "test_role",
                "description": "Test Role",
            },
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_roles_with_insufficient_permission_raises_error(
        self,
        client: TestClient,
    ):
        """
        Test get roles.
        """

        token = self.get_guest_auth_token(client)
        response = client.get(
            "/roles/",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_roles_with_valid_permission(self, client: TestClient):
        """
        Test create roles.
        """

        token = self.get_admin_auth_token(client)
        response = client.post(
            "/roles/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "test_role",
                "description": "Test Role",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.json()

    def test_get_roles_with_valid_permission(
        self,
        client: TestClient,
    ):
        """
        Test get roles.
        """

        token = self.get_admin_auth_token(client)
        response = client.get(
            "/roles/",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "meta" in response.json()
        assert "data" in response.json()
        assert len(response.json()["data"]) == 2

    def test_get_role_by_id_with_valid_permission(
        self,
        client: TestClient,
    ):
        """
        Test get role by id.
        """

        token = self.get_admin_auth_token(client)
        response = client.get(
            "/roles/",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        valid_id = response.json()["data"][0]["id"]
        response = client.get(
            f"/roles/{valid_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "id" in response.json()

    def test_get_role_by_id_with_invalid_permission_raises_error(
        self,
        client: TestClient,
    ):
        """
        Test get role by id.
        """

        token = self.get_guest_auth_token(client)
        response = client.get(
            f"/roles/{uuid4()}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_role_with_invalid_id_raises_error(
        self,
        client: TestClient,
    ):
        """
        Test get role by id.
        """

        token = self.get_admin_auth_token(client)
        response = client.get(
            f"/roles/{uuid4()}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_role_with_valid_permission(self, client: TestClient):
        """
        Test update role.
        """

        token = self.get_admin_auth_token(client)
        response = client.get(
            "/roles/",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        valid_id = response.json()["data"][0]["id"]

        response = client.patch(
            f"/roles/{valid_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "description": "Updated Test Role",
            },
        )
        assert response.status_code == status.HTTP_200_OK

    def test_update_role_with_invalid_permission_raises_error(
        self,
        client: TestClient,
    ):
        """
        Test update role.
        """

        token = self.get_guest_auth_token(client)
        response = client.patch(
            f"/roles/{uuid4()}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_role_with_valid_permission(self, client: TestClient):
        """
        Test delete role.
        """

        token = self.get_admin_auth_token(client)
        response = client.get(
            "/roles/",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        valid_id = response.json()["data"][1]["id"]

        response = client.delete(
            f"/roles/{valid_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_role_with_invalid_permission_raises_error(
        self,
        client: TestClient,
    ):
        """
        Test delete role.
        """

        token = self.get_guest_auth_token(client)
        response = client.delete(
            f"/roles/{uuid4()}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
