from fastapi import status
from httpx import AsyncClient


class TestRolesRouter:
    """
    Integration tests for the RoleRouter.
    Verifies that role management respects permissions and tenant isolation
    via the actor.
    """

    async def test_list_roles_with_valid_token(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Admin should be able to list roles.
        The list should contain the roles created by the seeding process
        for this tenant.
        """
        response = await client.get(
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

    async def test_create_role_as_admin(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Admin (who has role:create permission) should be able to create a new role.
        """
        new_role_data = {"name": "editor", "description": "Can edit content"}

        response = await client.post(
            "/roles/",
            json=new_role_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.json()

    async def test_create_role_without_token_fails(self, client: AsyncClient):
        """
        Requests without an actor (token) should be rejected (401).
        """
        response = await client.post("/roles/", json={"name": "hacker_role"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_guest_cannot_create_role(
        self, client: AsyncClient, guest_token: str
    ):
        """
        A guest user (valid actor but insufficient permissions)
        cannot create roles (403).
        """
        response = await client.post(
            "/roles/",
            json={"name": "guest_role"},
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_get_role_by_id(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Admin should be able to retrieve a role by its ID.
        """
        # 1. List roles to find a valid ID (e.g., the 'admin' role itself)
        list_response = await client.get(
            "/roles/", headers={"Authorization": f"Bearer {admin_token}"}
        )
        role_id = list_response.json()["data"][0]["id"]

        # 2. Get the specific role
        response = await client.get(
            f"/roles/{role_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == role_id

    async def test_delete_role_as_admin(
        self,
        client: AsyncClient,
        admin_token: str,
        default_tenant_id: str,
    ):
        """
        Admin should be able to delete a role.
        """
        # 1. Create a temporary role to delete
        post_response = await client.post(
            "/roles/",
            json={
                "name": "to_delete",
                "description": "Temp",
                "tenant_id": default_tenant_id,
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        role_id = post_response.json()["id"]

        # 2. Delete it
        delete_response = await client.delete(
            f"/roles/{role_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # 3. Verify it's gone
        get_response = await client.get(
            f"/roles/{role_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        print(get_response.json())
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["is_active"] is False

    async def test_update_role(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test role update.
        """
        # 1. Create
        create_resp = await client.post(
            "/roles/",
            json={
                "name": "role_to_update",
                "description": "Old Desc",
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        role_id = create_resp.json()["id"]

        # 2. Update
        response = await client.put(
            f"/roles/{role_id}",
            json={
                "name": "updated_role_name",
                "description": "New Desc",
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "updated_role_name"

    async def test_create_role_with_valid_permission(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test role creation with a valid permission.
        """

        response = await client.post(
            "/roles/",
            json={
                "name": "role_with_permission",
                "description": "Role with permission",
                "permissions": ["area:read"],
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.json()

    async def test_create_role_with_invalid_permission(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test role creation with a valid permission.
        """

        response = await client.post(
            "/roles/",
            json={
                "name": "role_with_permission",
                "description": "Role with permission",
                "permissions": ["area:reader"],
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Permission 'area:reader' not found." in response.json()["detail"]

    async def test_set_role_permissions(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test setting role permissions.
        """

        response = await client.get(
            "/roles/",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        role_id = response.json()["data"][1]["id"]

        response = await client.patch(
            f"/roles/{role_id}/permissions",
            json={"permission_codes": ["area:read"]},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_set_role_permissions_invalid_permission(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test setting role permissions with an invalid permission.
        """

        response = await client.get(
            "/roles/",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        role_id = response.json()["data"][1]["id"]

        response = await client.patch(
            f"/roles/{role_id}/permissions",
            json={"permission_codes": ["area:reader"]},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Permission 'area:reader' not found." in response.json()["detail"]

    async def test_restore_role(
        self,
        client: AsyncClient,
        admin_token: str,
        default_tenant_id: str,
    ):
        """
        Test restoring a role.
        """

        # 1. Create a temporary role to delete
        post_response = await client.post(
            "/roles/",
            json={
                "name": "to_delete",
                "description": "Temp",
                "tenant_id": default_tenant_id,
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        role_id = post_response.json()["id"]

        # 2. Delete it
        delete_response = await client.delete(
            f"/roles/{role_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # 3. Verify it's gone
        get_response = await client.get(
            f"/roles/{role_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["is_active"] is False
        assert get_response.json()["deleted_at"] is not None

        # 4. Restore it
        restore_response = await client.patch(
            f"/roles/{role_id}/restore",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert restore_response.status_code == status.HTTP_204_NO_CONTENT

        # 5. Verify it's back
        get_response = await client.get(
            f"/roles/{role_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["is_active"] is True
        assert get_response.json()["deleted_at"] is None
