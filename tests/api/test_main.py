from fastapi import status
from fastapi.testclient import TestClient


def test_read_root(client: TestClient):
    """
    Test the root endpoint.
    """
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Bem-vindo à Foresight API!"}
