from fastapi import status
from fastapi.testclient import TestClient

from src.identity_access_management.infrastructure.models import UserModel


class TestUserRouter:
    """
    Integration tests for the UserRouter (IAM).
    These tests verify the behavior of user management endpoints, including
    permissions, tenant isolation, and CRUD operations.
    """

    def test_list_users_as_admin(self, client: TestClient, admin_token: str):
        """
        Admin should be able to list all users in their tenant.
        """

        response = client.get(
            "/users/",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_200_OK

        data = response.json()

        assert data["meta"]["total_items"] >= 2

        assert len(data["data"]) > 0
        assert "id" in data["data"][0]
        assert "username" in data["data"][0]

    def test_guest_cannot_list_users(self, client: TestClient, guest_token: str):
        """
        Guest (without user:read permission) should not be able to list users.
        """

        response = client.get(
            "/users/",
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Operation not permitted" in response.json()["detail"]

    def test_get_me_endpoint(self, client: TestClient, admin_token: str):
        """
        Test the /me endpoint returns the current user's details.
        """

        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["username"] == "admin"
        assert "roles" in data
        assert "permissions" in data
        assert "is_active" in data

    def test_admin_can_get_guest_by_id(
        self,
        client: TestClient,
        admin_token: str,
        guest_user_model: UserModel,
    ):
        """
        Admin fetches details of the guest user by ID.
        """
        response = client.get(
            f"/users/{guest_user_model.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == "guest"

    def test_guest_cannot_get_admin_by_id(
        self,
        client: TestClient,
        guest_token: str,
        admin_user_model: UserModel,
    ):
        """
        Guest (without user:read permission) cannot fetch other users' details.
        """

        response = client.get(
            f"/users/{admin_user_model.id}",
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_user_as_admin(self, client: TestClient, admin_token: str):
        """
        Admin should be able to create a new user in the tenant.
        """

        new_user_data = {
            "username": "new_colleague",
            "password": "secure_password_123",
            "roles": ["guest"],  # Assign existing role
        }

        response = client.post(
            "/users/",
            json=new_user_data,
            headers={"Authorization": f"Bearer {admin_token}"},  # Actor (Admin)
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "new_colleague"
        assert "id" in data

    def test_create_user_without_token_fails(self, client: TestClient):
        """
        Trying to create user without being logged in should fail.
        """

        new_user_data = {"username": "hacker", "password": "pw"}
        response = client.post("/users/", json=new_user_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_guest_cannot_create_user(self, client: TestClient, guest_token: str):
        """
        Guest should not be able to create users.
        """

        new_user_data = {"username": "guest_created_user", "password": "pw"}
        response = client.post(
            "/users/",
            json=new_user_data,
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_user_profile_as_admin(
        self,
        client: TestClient,
        admin_token: str,
        admin_user_model: UserModel,
    ):
        """
        Admin updates their own profile.
        """

        user_id = admin_user_model.id

        patch_data = {"first_name": "Super Admin"}
        response = client.patch(
            f"/users/{user_id}/profile",
            json=patch_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        check_resp = client.get(
            f"/users/{user_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert check_resp.json()["first_name"] == "Super Admin"

    def test_guest_can_update_own_profile(
        self,
        client: TestClient,
        guest_token: str,
        guest_user_model: UserModel,
    ):
        """
        Guest updates their own profile (allowed for self).
        """

        user_id = guest_user_model.id
        patch_data = {"last_name": "Guest User"}

        response = client.patch(
            f"/users/{user_id}/profile",
            json=patch_data,
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_guest_cannot_update_admin_profile(
        self,
        client: TestClient,
        guest_token: str,
        admin_user_model: UserModel,
    ):
        """
        Guest tries to update admin's profile (should fail).
        """

        patch_data = {"first_name": "Hacked Admin"}
        response = client.patch(
            f"/users/{admin_user_model.id}/profile",
            json=patch_data,
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_change_password_as_admin(
        self,
        client: TestClient,
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

        response = client.patch(
            f"/users/{user_id}/password",
            json=payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_admin_can_set_user_roles(
        self,
        client: TestClient,
        admin_token: str,
        guest_user_model: UserModel,
    ):
        """
        Admin changes the roles of the guest user.
        """

        payload = {"role_names": ["admin"]}

        response = client.patch(
            f"/users/{guest_user_model.id}/roles",
            json=payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_guest_cannot_set_roles(
        self,
        client: TestClient,
        guest_token: str,
        guest_user_model: UserModel,
    ):
        """
        Guest tries to change their own roles (should fail).
        """

        payload = {"role_names": ["admin"]}  # Try to self-promote
        response = client.patch(
            f"/users/{guest_user_model.id}/roles",
            json=payload,
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_user_by_admin(
        self,
        client: TestClient,
        admin_token: str,
        guest_user_model: UserModel,
    ):
        """
        Admin deletes (soft delete) the guest user.
        """

        guest_id = guest_user_model.id

        response = client.delete(
            f"/users/{guest_id}", headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        check_response = client.get(
            f"/users/{guest_id}", headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert check_response.status_code == status.HTTP_404_NOT_FOUND
