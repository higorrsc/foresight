from fastapi import status
from httpx import AsyncClient

from src.identity_access_management.infrastructure.models import UserModel


class TestUserRouter:
    """
    Integration tests for the UserRouter (IAM).
    These tests verify the behavior of user management endpoints, including
    permissions, tenant isolation, and CRUD operations.
    """

    async def test_list_users_as_admin(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Admin should be able to list all users in their tenant.
        """

        response = await client.get(
            "/users/",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_200_OK

        data = response.json()

        assert data["meta"]["total_items"] >= 2

        assert len(data["data"]) > 0
        assert "id" in data["data"][0]
        assert "username" in data["data"][0]

    async def test_guest_cannot_list_users(self, client: AsyncClient, guest_token: str):
        """
        Guest (without user:read permission) should not be able to list users.
        """

        response = await client.get(
            "/users/",
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Operation not permitted" in response.json()["detail"]

    async def test_get_me_endpoint(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test the /me endpoint returns the current user's details.
        """

        response = await client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["username"] == "admin"
        assert "roles" in data
        assert "permissions" in data
        assert "is_active" in data

    async def test_admin_can_get_guest_by_id(
        self,
        client: AsyncClient,
        admin_token: str,
        guest_user_model: UserModel,
    ):
        """
        Admin fetches details of the guest user by ID.
        """
        response = await client.get(
            f"/users/{guest_user_model.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == "guest"

    async def test_guest_cannot_get_admin_by_id(
        self,
        client: AsyncClient,
        guest_token: str,
        admin_user_model: UserModel,
    ):
        """
        Guest (without user:read permission) cannot fetch other users' details.
        """

        response = await client.get(
            f"/users/{admin_user_model.id}",
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_create_user_as_admin(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Admin should be able to create a new user in the tenant.
        """

        new_user_data = {
            "username": "new_colleague",
            "password": "secure_password_123",
            "roles": ["guest"],  # Assign existing role
        }

        response = await client.post(
            "/users/",
            json=new_user_data,
            headers={"Authorization": f"Bearer {admin_token}"},  # Actor (Admin)
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "new_colleague"
        assert "id" in data

    async def test_create_user_without_token_fails(self, client: AsyncClient):
        """
        Trying to create user without being logged in should fail.
        """

        new_user_data = {"username": "hacker", "password": "pw"}
        response = await client.post("/users/", json=new_user_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_guest_cannot_create_user(
        self, client: AsyncClient, guest_token: str
    ):
        """
        Guest should not be able to create users.
        """

        new_user_data = {"username": "guest_created_user", "password": "pw"}
        response = await client.post(
            "/users/",
            json=new_user_data,
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_update_user_profile_as_admin(
        self,
        client: AsyncClient,
        admin_token: str,
        admin_user_model: UserModel,
    ):
        """
        Admin updates their own profile.
        """

        user_id = admin_user_model.id

        patch_data = {"first_name": "Super Admin"}
        response = await client.patch(
            f"/users/{user_id}/profile",
            json=patch_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        check_resp = await client.get(
            f"/users/{user_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert check_resp.json()["first_name"] == "Super Admin"

    async def test_guest_can_update_own_profile(
        self,
        client: AsyncClient,
        guest_token: str,
        guest_user_model: UserModel,
    ):
        """
        Guest updates their own profile (allowed for self).
        """

        user_id = guest_user_model.id
        patch_data = {"last_name": "Guest User"}

        response = await client.patch(
            f"/users/{user_id}/profile",
            json=patch_data,
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_guest_cannot_update_admin_profile(
        self,
        client: AsyncClient,
        guest_token: str,
        admin_user_model: UserModel,
    ):
        """
        Guest tries to update admin's profile (should fail).
        """

        patch_data = {"first_name": "Hacked Admin"}
        response = await client.patch(
            f"/users/{admin_user_model.id}/profile",
            json=patch_data,
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_change_password_as_admin(
        self,
        client: AsyncClient,
        admin_token: str,
        admin_user_model: UserModel,
    ):
        """
        Admin changes their own password.
        """

        user_id = admin_user_model.id

        payload = {
            "old_password": "foresight_admin",
            "new_password": "new_admin_password_123",
        }

        response = await client.patch(
            f"/users/{user_id}/password",
            json=payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_admin_can_set_user_roles(
        self,
        client: AsyncClient,
        admin_token: str,
        guest_user_model: UserModel,
    ):
        """
        Admin changes the roles of the guest user.
        """

        payload = {"role_names": ["admin"]}

        response = await client.patch(
            f"/users/{guest_user_model.id}/roles",
            json=payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_guest_cannot_set_roles(
        self,
        client: AsyncClient,
        guest_token: str,
        guest_user_model: UserModel,
    ):
        """
        Guest tries to change their own roles (should fail).
        """

        payload = {"role_names": ["admin"]}  # Try to self-promote
        response = await client.patch(
            f"/users/{guest_user_model.id}/roles",
            json=payload,
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_delete_user_by_admin(
        self,
        client: AsyncClient,
        admin_token: str,
        guest_user_model: UserModel,
    ):
        """
        Admin deletes (soft delete) the guest user.
        """

        guest_id = guest_user_model.id

        response = await client.delete(
            f"/users/{guest_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        check_response = await client.get(
            f"/users/{guest_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert check_response.status_code == status.HTTP_200_OK
        assert check_response.json()["is_active"] is False

    async def test_restore_user_by_admin(
        self,
        client: AsyncClient,
        admin_token: str,
        guest_user_model: UserModel,
    ):
        """
        Admin restores the guest user.
        """

        guest_id = guest_user_model.id

        response = await client.delete(
            f"/users/{guest_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        check_response = await client.get(
            f"/users/{guest_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert check_response.status_code == status.HTTP_200_OK
        assert check_response.json()["is_active"] is False

        response = await client.patch(
            f"/users/{guest_id}/restore",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        check_response = await client.get(
            f"/users/{guest_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert check_response.status_code == status.HTTP_200_OK
        assert check_response.json()["is_active"] is True
