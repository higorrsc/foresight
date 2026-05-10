from fastapi import status
from httpx import AsyncClient


class TestMainRouter:
    """
    Test suite for the main API entry points.
    """

    async def test_read_root(self, client: AsyncClient):
        """
        Test the root endpoint.
        """
        response = await client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Bem-vindo à Foresight API!"}
