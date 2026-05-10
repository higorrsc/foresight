from uuid import uuid4

from fastapi import status
from httpx import AsyncClient


class TestAreaRouter:
    """
    Test Area Router.
    """

    async def test_create_area_unauthorized(self, client: AsyncClient):
        """
        Test create area without authentication.
        """

        response = await client.post("/areas/", json={"description": "Test Area"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_create_and_list_areas(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test create and list areas.
        """

        headers = {"Authorization": f"Bearer {admin_token}"}

        area_data = {"description": "My Test Area"}
        response = await client.post(
            "/areas/",
            json=area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        created_area = response.json()
        assert "id" in created_area

        response = await client.get("/areas/", headers=headers)
        assert response.status_code == status.HTTP_200_OK

        list_response = response.json()
        assert list_response["meta"]["total_items"] == 1
        assert list_response["data"][0]["description"] == "My Test Area"
        assert list_response["data"][0]["id"] == created_area["id"]

    async def test_create_area_with_invalid_data(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test create area with invalid data.
        """

        headers = {"Authorization": f"Bearer {admin_token}"}

        response = await client.post(
            "/areas/",
            json={},
            headers=headers,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

        area_data = {"description": "a" * 101}
        response = await client.post(
            "/areas/",
            json=area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    async def test_create_and_get_area_by_id(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test create and get area by id.
        """

        headers = {"Authorization": f"Bearer {admin_token}"}

        area_data = {"description": "My Test Area"}
        response = await client.post(
            "/areas/",
            json=area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        created_area = response.json()
        assert "id" in created_area

        area_id = created_area["id"]

        response = await client.get(f"/areas/{area_id}", headers=headers)
        assert response.status_code == status.HTTP_200_OK

    async def test_create_and_get_area_by_id_with_invalid_id(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test create and get area by id.
        """

        headers = {"Authorization": f"Bearer {admin_token}"}

        response = await client.get(f"/areas/{uuid4()}", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = await client.get("/areas/123}", headers=headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    async def test_create_and_get_area_by_id_with_invalid_id_format(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test create and get area by id.
        """

        headers = {"Authorization": f"Bearer {admin_token}"}

        response = await client.get("/areas/132", headers=headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    async def test_update_area_by_id(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test update area by id.
        """

        headers = {"Authorization": f"Bearer {admin_token}"}

        area_data = {"description": "My Test Area"}
        response = await client.post(
            "/areas/",
            json=area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        area_id = response.json()["id"]

        new_area_data = {"description": "Updated Test Area"}
        response = await client.put(
            f"/areas/{area_id}",
            json=new_area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_200_OK

    async def test_update_area_by_id_with_invalid_id(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test update area by id.
        """

        headers = {"Authorization": f"Bearer {admin_token}"}

        new_area_data = {"description": "Updated Test Area"}
        response = await client.put(
            f"/areas/{uuid4()}",
            json=new_area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_update_area_by_id_with_invalid_description(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test update area by id.
        """

        headers = {"Authorization": f"Bearer {admin_token}"}

        area_data = {"description": "My Test Area"}
        response = await client.post(
            "/areas/",
            json=area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        area_id = response.json()["id"]

        new_area_data = {"description": "a" * 101}
        response = await client.put(
            f"/areas/{area_id}",
            json=new_area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    async def test_delete_area_by_id(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test delete area by id.
        """

        headers = {"Authorization": f"Bearer {admin_token}"}

        area_data = {"description": "My Test Area"}
        response = await client.post(
            "/areas/",
            json=area_data,
            headers=headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        area_id = response.json()["id"]

        response = await client.delete(
            f"/areas/{area_id}",
            headers=headers,
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_delete_area_by_id_with_invalid_id(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test delete area by id.
        """

        headers = {"Authorization": f"Bearer {admin_token}"}

        response = await client.delete(
            f"/areas/{uuid4()}",
            headers=headers,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_delete_and_restore_area(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test the soft delete and restore flow.
        """
        # 1. Create
        create_resp = await client.post(
            "/areas/",
            json={"description": "To be deleted"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        area_id = create_resp.json()["id"]

        # 2. Delete
        del_resp = await client.delete(
            f"/areas/{area_id}",
            headers={
                "Authorization": f"Bearer {admin_token}",
            },
        )
        assert del_resp.status_code == status.HTTP_204_NO_CONTENT

        # 3. Verify it's gone (Get should return 404 or inactive)
        # Assuming repository filters active only by default or throws 404
        get_resp = await client.get(
            f"/areas/{area_id}",
            headers={
                "Authorization": f"Bearer {admin_token}",
            },
        )
        assert get_resp.status_code == status.HTTP_200_OK
        assert get_resp.json()["is_active"] is False

        # 4. Restore
        restore_resp = await client.patch(
            f"/areas/{area_id}/restore",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert restore_resp.status_code == status.HTTP_204_NO_CONTENT

        # 5. Verify it's back
        get_resp_2 = await client.get(
            f"/areas/{area_id}",
            headers={
                "Authorization": f"Bearer {admin_token}",
            },
        )
        assert get_resp_2.status_code == status.HTTP_200_OK
        assert get_resp_2.json()["is_active"] is True
