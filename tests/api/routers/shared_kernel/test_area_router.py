from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient


class TestAreaRouter:
    """
    Test Area Router.
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
        assert response.status_code == status.HTTP_200_OK, response.json()
        return response.json()["access_token"]

    def test_create_area_unauthorized(self, client: TestClient):
        """
        Test create area without authentication.
        """

        response = client.post("/areas/", json={"description": "Test Area"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_and_list_areas(self, client: TestClient, admin_token: str):
        """
        Test create and list areas.
        """

        headers = {"Authorization": f"Bearer {admin_token}"}

        area_data = {"description": "My Test Area"}
        response = client.post(
            "/areas/",
            json=area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        created_area = response.json()
        assert "id" in created_area

        response = client.get("/areas/", headers=headers)
        assert response.status_code == status.HTTP_200_OK

        list_response = response.json()
        assert list_response["meta"]["total_items"] == 1
        assert list_response["data"][0]["description"] == "My Test Area"
        assert list_response["data"][0]["id"] == created_area["id"]

    def test_create_area_with_invalid_data(self, client: TestClient):
        """
        Test create area with invalid data.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post(
            "/areas/",
            json={},
            headers=headers,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

        area_data = {"description": "a" * 101}
        response = client.post(
            "/areas/",
            json=area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_and_get_area_by_id(self, client: TestClient):
        """
        Test create and get area by id.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        area_data = {"description": "My Test Area"}
        response = client.post(
            "/areas/",
            json=area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        created_area = response.json()
        assert "id" in created_area

        area_id = created_area["id"]

        response = client.get(f"/areas/{area_id}", headers=headers)
        assert response.status_code == status.HTTP_200_OK

    def test_create_and_get_area_by_id_with_invalid_id(self, client: TestClient):
        """
        Test create and get area by id.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(f"/areas/{uuid4()}", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = client.get("/areas/123}", headers=headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_and_get_area_by_id_with_invalid_id_format(self, client: TestClient):
        """
        Test create and get area by id.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/areas/132", headers=headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_update_area_by_id(self, client: TestClient):
        """
        Test update area by id.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        area_data = {"description": "My Test Area"}
        response = client.post(
            "/areas/",
            json=area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        area_id = response.json()["id"]

        new_area_data = {"description": "Updated Test Area"}
        response = client.put(
            f"/areas/{area_id}",
            json=new_area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_200_OK

    def test_update_area_by_id_with_invalid_id(self, client: TestClient):
        """
        Test update area by id.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        new_area_data = {"description": "Updated Test Area"}
        response = client.put(
            f"/areas/{uuid4()}",
            json=new_area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_area_by_id_with_invalid_description(self, client: TestClient):
        """
        Test update area by id.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        area_data = {"description": "My Test Area"}
        response = client.post(
            "/areas/",
            json=area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        area_id = response.json()["id"]

        new_area_data = {"description": "a" * 101}
        response = client.put(
            f"/areas/{area_id}",
            json=new_area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_delete_area_by_id(self, client: TestClient):
        """
        Test delete area by id.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        area_data = {"description": "My Test Area"}
        response = client.post(
            "/areas/",
            json=area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        area_id = response.json()["id"]

        response = client.delete(
            f"/areas/{area_id}",
            headers=headers,
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_area_by_id_with_invalid_id(self, client: TestClient):
        """
        Test delete area by id.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        response = client.delete(
            f"/areas/{uuid4()}",
            headers=headers,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_and_restore_area(self, client: TestClient, admin_token: str):
        """
        Test the soft delete and restore flow.
        """
        # 1. Create
        create_resp = client.post(
            "/areas/",
            json={"description": "To be deleted"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        area_id = create_resp.json()["id"]

        # 2. Delete
        del_resp = client.delete(
            f"/areas/{area_id}",
            headers={
                "Authorization": f"Bearer {admin_token}",
            },
        )
        assert del_resp.status_code == status.HTTP_204_NO_CONTENT

        # 3. Verify it's gone (Get should return 404 or inactive)
        # Assuming repository filters active only by default or throws 404
        get_resp = client.get(
            f"/areas/{area_id}",
            headers={
                "Authorization": f"Bearer {admin_token}",
            },
        )
        assert get_resp.status_code == status.HTTP_200_OK
        assert get_resp.json()["is_active"] is False

        # 4. Restore
        restore_resp = client.patch(
            f"/areas/{area_id}/restore",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert restore_resp.status_code == status.HTTP_204_NO_CONTENT

        # 5. Verify it's back
        get_resp_2 = client.get(
            f"/areas/{area_id}",
            headers={
                "Authorization": f"Bearer {admin_token}",
            },
        )
        assert get_resp_2.status_code == status.HTTP_200_OK
        assert get_resp_2.json()["is_active"] is True
