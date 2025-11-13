from fastapi import status
from fastapi.testclient import TestClient

from src.identity_access_management.infrastructure.models import UserModel


class TestUserRouter:
    """
    Integration tests for the UserRouter (IAM).
    """

    def test_list_users_as_admin(self, client: TestClient, admin_token: str):
        """
        Admin should be able to list all users in their tenant.
        """

        response = client.get(
            "/users/", headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Expecting at least 'admin' and 'guest' from seeding
        assert data["meta"]["total_items"] >= 2

    def test_guest_cannot_list_users(self, client: TestClient, guest_token: str):
        """
        Guest user should not be allowed to list users (403).
        """

        response = client.get(
            "/users/", headers={"Authorization": f"Bearer {guest_token}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_get_guest_details(
        self, client: TestClient, admin_token: str, guest_user_model: UserModel
    ):
        """
        Admin should be able to see details of another user (guest) in the same tenant.
        """

        response = client.get(
            f"/users/{guest_user_model.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == "guest"

    def test_create_user_as_admin(self, client: TestClient, admin_token: str):
        """
        Admin should be able to create a new user (e.g., a coworker).
        """

        new_user_data = {
            "username": "new_colleague",
            "password": "secure_password_123",
            "roles": ["guest"],
        }

        response = client.post(
            "/users/",
            json=new_user_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["username"] == "new_colleague"

    def test_update_user_profile_as_admin(self, client: TestClient, admin_token: str):
        """
        Admin updates their own profile.
        """

        # 1. Get admin ID via /me endpoint to ensure we have the right ID
        me_resp = client.get(
            "/users/me", headers={"Authorization": f"Bearer {admin_token}"}
        )
        user_id = me_resp.json()["id"]

        # 2. Update profile
        patch_data = {"first_name": "Super Admin"}
        response = client.patch(
            f"/users/{user_id}/profile",
            json=patch_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # 3. Verify update
        check_resp = client.get(
            f"/users/{user_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert check_resp.json()["first_name"] == "Super Admin"

    def test_delete_user_as_admin(
        self, client: TestClient, admin_token: str, guest_user_model: UserModel
    ):
        """
        Admin should be able to delete (soft delete) the guest user.
        """

        response = client.delete(
            f"/users/{guest_user_model.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify user is no longer retrievable (or is marked inactive)
        # Assuming default repository filters out inactive users:
        check_response = client.get(
            f"/users/{guest_user_model.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert check_response.status_code == status.HTTP_404_NOT_FOUND
