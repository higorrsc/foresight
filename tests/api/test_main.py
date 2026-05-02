from fastapi import status
from fastapi.testclient import TestClient


class TestMainRouter:
    """
    Test suite for the main API entry points.
    """

    def test_read_root(self, client: TestClient):
        """
        Test the root endpoint.
        """
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Bem-vindo à Foresight API!"}
