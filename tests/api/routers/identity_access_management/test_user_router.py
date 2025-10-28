from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient
from jose import jwt

from src.shared_kernel.infrastructure.config import settings


class TestUserRouter:
    """
    Test User Router.
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

    def test_create_user_without_role(self, client: TestClient):
        """
        Test create user.
        """

        response = client.post(
            "/users/",
            json={
                "username": "test_user",
                "password": "test_password",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.json()

    def test_create_user_with_role(self, client: TestClient):
        """
        Test create user with role.
        """

        response = client.post(
            "/users/",
            json={
                "username": "test_user",
                "password": "test_password",
                "roles": ["admin"],
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.json()
        assert "roles" not in response.json()

    def test_create_user_with_invalid_role(self, client: TestClient):
        """
        Test create user with invalid role.
        """

        response = client.post(
            "/users/",
            json={
                "username": "test_user",
                "password": "test_password",
                "roles": ["invalid_role"],
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "detail" in response.json()
        assert "invalid_role" in response.json()["detail"]

    def test_get_users_without_token_raises_error(self, client: TestClient):
        """
        Test get user by id.
        """

        response = client.get("/users/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_users_with_invalid_token_raises_error(self, client: TestClient):
        """
        Test get user by id.
        """

        response = client.get(
            "/users/",
            headers={"Authorization": "Bearer invalid_token"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_users_with_valid_token(self, client: TestClient):
        """
        Test get user by id.
        """

        token = self.get_admin_auth_token(client)

        response = client.get(
            "/users/",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["meta"]["total_items"] == 2
        assert response.json()["data"][0]["username"] == "admin"

    def test_get_user_by_id_without_token_raises_error(self, client: TestClient):
        """
        Test get user by id.
        """

        response = client.get(
            f"/users/{uuid4()}",
            headers={"Authorization": ""},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_user_by_id_with_valid_token(self, client: TestClient):
        """
        Test get user by id.
        """

        token = self.get_admin_auth_token(client)

        response = client.get(
            "/users/",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_200_OK

        valid_user_id = response.json()["data"][0]["id"]

        response = client.get(
            f"/users/{valid_user_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "id" in response.json()
        assert "username" in response.json()
        assert "first_name" in response.json()
        assert "last_name" in response.json()
        assert "email" in response.json()
        assert "is_active" in response.json()
        assert "roles" in response.json()

    def test_delete_user_by_id_without_token_raises_error(self, client: TestClient):
        """
        Test delete user by id.
        """

        response = client.delete(
            f"/users/{uuid4()}",
            headers={"Authorization": ""},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_user_with_inexistent_id_raises_error(self, client: TestClient):
        """
        Test delete user by id.
        """

        token = self.get_admin_auth_token(client)

        response = client.delete(
            f"/users/{uuid4()}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "detail" in response.json()
        assert "User with given ID not found." in response.json()["detail"]

    def test_delete_user_by_id_without_admin_permission_raises_error(
        self, client: TestClient
    ):
        """
        Test delete user by id.
        """

        token = self.get_guest_auth_token(client)

        response = client.get(
            "/users/",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == status.HTTP_200_OK

        valid_user_id = response.json()["data"][0]["id"]

        response = client.delete(
            f"/users/{valid_user_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "detail" in response.json()
        assert (
            "Operation not permitted: Insufficient permissions"
            in response.json()["detail"]
        )

    def test_delete_user_by_id_with_admin_permission(self, client: TestClient):
        """
        Test delete user by id.
        """

        token = self.get_admin_auth_token(client)

        response = client.post(
            "/users/",
            json={
                "username": "test_user",
                "password": "test_password",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        valid_id = response.json()["id"]

        response = client.delete(
            f"/users/{valid_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_change_user_password_without_token_raises_error(self, client: TestClient):
        """
        Test change user password.
        """

        response = client.patch(
            f"/users/{uuid4()}/password",
            json={
                "old_password": "test_password",
                "new_password": "new_test_password",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_change_password_different_user_without_admin_permission_raises_error(
        self,
        client: TestClient,
    ):
        """
        Test change user password.
        """

        response = client.post(
            "/users/",
            json={
                "username": "test_user",
                "password": "test_password",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        valid_id = response.json()["id"]

        token = self.get_guest_auth_token(client)
        response = client.patch(
            f"/users/{valid_id}/password",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "old_password": "string",
                "new_password": "stringst",
            },
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "detail" in response.json()
        assert (
            "Not allowed to update another user's password" in response.json()["detail"]
        )

    def test_change_password_different_user_with_admin_permission(
        self,
        client: TestClient,
    ):
        """
        Test change user password.
        """

        response = client.post(
            "/users/",
            json={
                "username": "test_user",
                "password": "test_password",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        valid_id = response.json()["id"]

        token = self.get_admin_auth_token(client)
        response = client.patch(
            f"/users/{valid_id}/password",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "old_password": "test_password",
                "new_password": "new_test_password",
            },
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_change_password_with_valid_data(self, client: TestClient):
        """
        Test change user password.
        """

        response = client.post(
            "/users/",
            json={
                "username": "test_user",
                "password": "test_password",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        valid_id = response.json()["id"]

        response = client.post(
            "/auth/token",
            data={
                "username": "test_user",
                "password": "test_password",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        token = response.json()["access_token"]

        response = client.patch(
            f"/users/{valid_id}/password",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "old_password": "test_password",
                "new_password": "new_test_password",
            },
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_change_password_with_invalid_old_password(self, client: TestClient):
        """
        Test change user password.
        """

        response = client.post(
            "/users/",
            json={
                "username": "test_user",
                "password": "test_password",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        valid_id = response.json()["id"]

        response = client.post(
            "/auth/token",
            data={
                "username": "test_user",
                "password": "test_password",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        token = response.json()["access_token"]

        response = client.patch(
            f"/users/{valid_id}/password",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "old_password": "asdf",
                "new_password": "new_test_password",
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "detail" in response.json()
        assert "Invalid old password" in response.json()["detail"]

    def test_change_user_profile_without_token_raises_error(self, client: TestClient):
        """
        Test change user profile.
        """

        response = client.patch(
            f"/users/{uuid4()}/profile",
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "user@example.com",
                "is_active": False,
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_change_profile_different_user_without_admin_permission_raises_error(
        self,
        client: TestClient,
    ):
        """
        Test change user profile.
        """

        response = client.post(
            "/users/",
            json={
                "username": "test_user",
                "password": "test_profile",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        valid_id = response.json()["id"]

        token = self.get_guest_auth_token(client)
        response = client.patch(
            f"/users/{valid_id}/profile",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "user@example.com",
                "is_active": False,
            },
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "detail" in response.json()
        assert (
            "Not allowed to update another user's profile" in response.json()["detail"]
        )

    def test_change_profile_different_user_with_admin_permission(
        self,
        client: TestClient,
    ):
        """
        Test change user profile.
        """

        response = client.post(
            "/users/",
            json={
                "username": "test_user",
                "password": "test_profile",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        valid_id = response.json()["id"]

        token = self.get_admin_auth_token(client)
        response = client.patch(
            f"/users/{valid_id}/profile",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@hotmail.com",
                "is_active": False,
            },
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_change_profile_with_valid_data(self, client: TestClient):
        """
        Test change user profile.
        """

        response = client.post(
            "/users/",
            json={
                "username": "test_user",
                "password": "test_profile",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        valid_id = response.json()["id"]

        response = client.post(
            "/auth/token",
            data={
                "username": "test_user",
                "password": "test_profile",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        token = response.json()["access_token"]

        response = client.patch(
            f"/users/{valid_id}/profile",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "user@hotmail.com",
                "is_active": False,
            },
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_change_profile_with_invalid_email(self, client: TestClient):
        """
        Test change user profile.
        """

        response = client.post(
            "/users/",
            json={
                "username": "test_user",
                "password": "test_profile",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        valid_id = response.json()["id"]

        response = client.post(
            "/auth/token",
            data={
                "username": "test_user",
                "password": "test_profile",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        token = response.json()["access_token"]

        response = client.patch(
            f"/users/{valid_id}/profile",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe",
                "is_active": False,
            },
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert "detail" in response.json()
        assert (
            "value is not a valid email address" in response.json()["detail"][0]["msg"]
        )

    def test_access_protected_route_with_invalid_token(self, client: TestClient):
        """
        Test access protected route with invalid token.
        """

        invalid_token = "this-is-not-a-valid-jwt-token"
        headers = {"Authorization": f"Bearer {invalid_token}"}

        response = client.get(
            "/users/me", headers=headers
        )  # Use um endpoint protegido qualquer

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_access_protected_route_with_valid_token_no_sub(self, client: TestClient):
        """
        Test access protected route with valid token.
        """

        payload_sem_sub = {"exp": datetime.now(timezone.utc) + timedelta(minutes=15)}
        token_sem_sub = jwt.encode(
            payload_sem_sub,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

        headers = {"Authorization": f"Bearer {token_sem_sub}"}
        response = client.get("/users/me", headers=headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid authentication credentials" in response.json()["detail"]
