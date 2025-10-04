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
        assert response.status_code == 200, response.json()
        return response.json()["access_token"]

    def test_create_area_unauthorized(self, client: TestClient):
        """
        Test create area without authentication.
        """

        response = client.post("/areas/", json={"description": "Test Area"})
        assert response.status_code == 401

    def test_create_and_list_areas(self, client: TestClient):
        """
        Test create and list areas.
        """

        token = self.get_admin_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        area_data = {"description": "My Test Area"}
        response = client.post(
            "/areas/",
            json=area_data,
            headers=headers,
        )

        assert response.status_code == 201
        created_area = response.json()
        assert "id" in created_area

        response = client.get("/areas/", headers=headers)
        assert response.status_code == 200

        list_response = response.json()
        assert list_response["meta"]["total_items"] == 1
        assert list_response["data"][0]["description"] == "My Test Area"
        assert list_response["data"][0]["id"] == created_area["id"]
