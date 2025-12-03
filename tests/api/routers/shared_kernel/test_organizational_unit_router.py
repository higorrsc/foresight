from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient


class TestOrganizationalUnitRouter:
    """
    Test Organizational Unit Router.
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

    def test_create_organizational_unit_unauthorized(self, client: TestClient):
        """
        Test create organizational unit without authentication.
        """

        response = client.post(
            "/organizational-units/",
            json={
                "code": "TEST",
                "description": "Test Organizational Unit",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_and_list_organizational_units(
        self,
        client: TestClient,
        admin_token: str,
    ):
        """
        Test create and list organizational units.
        """

        headers = {"Authorization": f"Bearer {admin_token}"}

        ou_data = {
            "code": "OU-TEST",
            "description": "My Test OU",
        }
        response = client.post(
            "/organizational-units/",
            json=ou_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        created_ou = response.json()
        assert "id" in created_ou

        response = client.get("/organizational-units/", headers=headers)
        assert response.status_code == status.HTTP_200_OK

        list_response = response.json()
        assert list_response["meta"]["total_items"] == 1
        assert list_response["data"][0]["description"] == "My Test OU"
        assert list_response["data"][0]["id"] == created_ou["id"]

    def test_create_organizational_unit_with_invalid_data(self, client: TestClient):
        """
        Test create organizational unit with invalid data.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        # Missing code and description
        response = client.post(
            "/organizational-units/",
            json={},
            headers=headers,
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

        # Invalid description length
        ou_data = {"code": "VALID", "description": "a" * 101}
        response = client.post(
            "/organizational-units/",
            json=ou_data,
            headers=headers,
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

        # Invalid code length
        ou_data = {"code": "a" * 11, "description": "Valid Description"}
        response = client.post(
            "/organizational-units/",
            json=ou_data,
            headers=headers,
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_and_get_organizational_unit_by_id(self, client: TestClient):
        """
        Test create and get organizational unit by id.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        ou_data = {
            "code": "OU-GET",
            "description": "My Test OU for Get",
        }
        response = client.post(
            "/organizational-units/",
            json=ou_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        created_ou = response.json()
        assert "id" in created_ou

        ou_id = created_ou["id"]

        response = client.get(f"/organizational-units/{ou_id}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        get_response = response.json()
        assert get_response["id"] == ou_id
        assert get_response["code"] == "OU-GET"

    def test_get_organizational_unit_by_id_not_found(self, client: TestClient):
        """
        Test get organizational unit by id with an invalid id.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(
            f"/organizational-units/{uuid4()}",
            headers=headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_organizational_unit_by_id_invalid_format(self, client: TestClient):
        """
        Test get organizational unit by id with an invalid id format.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/organizational-units/123", headers=headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_update_organizational_unit_by_id(self, client: TestClient):
        """
        Test update organizational unit by id.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        ou_data = {
            "code": "OU-OLD",
            "description": "Old Description",
        }
        response = client.post(
            "/organizational-units/",
            json=ou_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        ou_id = response.json()["id"]

        new_ou_data = {
            "code": "OU-NEW",
            "description": "Updated Description",
        }
        response = client.put(
            f"/organizational-units/{ou_id}",
            json=new_ou_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_200_OK
        updated_ou = response.json()
        assert updated_ou["description"] == "Updated Description"

    def test_update_organizational_unit_not_found(self, client: TestClient):
        """
        Test update organizational unit by id with an invalid id.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        new_ou_data = {
            "code": "OU-NEW",
            "description": "Updated Description",
        }
        response = client.put(
            f"/organizational-units/{uuid4()}",
            json=new_ou_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_organizational_unit_by_id(self, client: TestClient):
        """
        Test delete organizational unit by id.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        ou_data = {
            "code": "OU-DEL",
            "description": "To Be Deleted",
        }
        response = client.post(
            "/organizational-units/",
            json=ou_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        ou_id = response.json()["id"]

        response = client.delete(
            f"/organizational-units/{ou_id}",
            headers=headers,
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify it's not found anymore
        response = client.get(
            f"/organizational-units/{ou_id}",
            headers=headers,
        )
        assert response.status_code == status.HTTP_200_OK

        ou_status = response.json()["is_active"]
        assert ou_status is False

    def test_delete_organizational_unit_not_found(self, client: TestClient):
        """
        Test delete organizational unit by id with an invalid id.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        response = client.delete(
            f"/organizational-units/{uuid4()}",
            headers=headers,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_restore_organizational_unit_by_id(self, client: TestClient):
        """
        Test restore organizational unit by id.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        ou_data = {
            "code": "OU-DEL",
            "description": "To Be Restored",
        }
        response = client.post(
            "/organizational-units/",
            json=ou_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        ou_id = response.json()["id"]

        response = client.delete(
            f"/organizational-units/{ou_id}",
            headers=headers,
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify it's not found anymore
        response = client.get(
            f"/organizational-units/{ou_id}",
            headers=headers,
        )
        assert response.status_code == status.HTTP_200_OK

        ou_status = response.json()["is_active"]
        assert ou_status is False

        response = client.patch(
            f"/organizational-units/{ou_id}/restore",
            headers=headers,
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify it's not found anymore
        response = client.get(
            f"/organizational-units/{ou_id}",
            headers=headers,
        )
        assert response.status_code == status.HTTP_200_OK

        ou_status = response.json()["is_active"]
        assert ou_status is True

    def test_restore_organizational_unit_not_found(self, client: TestClient):
        """
        Test restore organizational unit by id with an invalid id.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        response = client.patch(
            f"/organizational-units/{uuid4()}/restore",
            headers=headers,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
