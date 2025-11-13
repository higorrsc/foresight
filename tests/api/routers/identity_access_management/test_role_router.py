from fastapi import status
from fastapi.testclient import TestClient


class TestRolesRouter:
    """
    Integration tests for the RoleRouter.
    Verifies that role management respects permissions and tenant isolation via the actor.
    """

    def test_list_roles_with_valid_token(self, client: TestClient, admin_token: str):
        """
        Admin should be able to list roles.
        The list should contain the roles created by the seeding process for this tenant.
        """
        response = client.get(
            "/roles/",
            headers={
                "Authorization": f"Bearer {admin_token}"
            },  # Passing the actor via token
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # Seeding creates 'admin' and 'guest' roles
        assert data["meta"]["total_items"] >= 2

        role_names = [r["name"] for r in data["data"]]
        assert "admin" in role_names
        assert "guest" in role_names

    def test_create_role_as_admin(self, client: TestClient, admin_token: str):
        """
        Admin (who has role:create permission) should be able to create a new role.
        """
        new_role_data = {"name": "editor", "description": "Can edit content"}

        response = client.post(
            "/roles/",
            json=new_role_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.json()

    def test_create_role_without_token_fails(self, client: TestClient):
        """
        Requests without an actor (token) should be rejected (401).
        """
        response = client.post("/roles/", json={"name": "hacker_role"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_guest_cannot_create_role(self, client: TestClient, guest_token: str):
        """
        A guest user (valid actor but insufficient permissions) cannot create roles (403).
        """
        response = client.post(
            "/roles/",
            json={"name": "guest_role"},
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_role_by_id(self, client: TestClient, admin_token: str):
        """
        Admin should be able to retrieve a role by its ID.
        """
        # 1. List roles to find a valid ID (e.g., the 'admin' role itself)
        list_response = client.get(
            "/roles/", headers={"Authorization": f"Bearer {admin_token}"}
        )
        role_id = list_response.json()["data"][0]["id"]

        # 2. Get the specific role
        response = client.get(
            f"/roles/{role_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == role_id

    def test_delete_role_as_admin(
        self,
        client: TestClient,
        admin_token: str,
        default_tenant_id: str,
    ):
        """
        Admin should be able to delete a role.
        """
        # 1. Create a temporary role to delete
        create_resp = client.post(
            "/roles/",
            json={
                "name": "to_delete",
                "description": "Temp",
                "tenant_id": default_tenant_id,
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        role_id = create_resp.json()["id"]

        # 2. Delete it
        response = client.delete(
            f"/roles/{role_id}", headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # 3. Verify it's gone
        get_response = client.get(
            f"/roles/{role_id}", headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
