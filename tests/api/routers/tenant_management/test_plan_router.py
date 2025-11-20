from fastapi import status
from fastapi.testclient import TestClient


class TestPlanRouter:
    """
    Test suite for the PlanRouter.
    """

    def test_create_plan_as_admin(
        self,
        client: TestClient,
        admin_token: str,
    ):
        """Admin (Super Admin permissions) should be able to create plans."""

        response = client.post(
            "/plans/",
            json={
                "name": "Premium",
                "description": "Best plan",
                "price": 199.90,
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.json()

    def test_guest_cannot_create_plan(
        self,
        client: TestClient,
        guest_token: str,
    ):
        """Guest user should not be able to create plans."""

        response = client.post(
            "/plans/",
            json={
                "name": "Hacker Plan",
                "price": 0,
            },
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_plans_authenticated(
        self,
        client: TestClient,
        guest_token: str,
    ):
        """Any authenticated user (even guest) should be able to list plans."""

        # First create a plan as admin to ensure list is not empty
        # (Or rely on seeding if you seeded a plan)

        response = client.get(
            "/plans/",
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert "data" in data
        assert "meta" in data

        plans_list = data["data"]
        assert isinstance(plans_list, list)
        assert any(p["name"] == "Standard" for p in plans_list)
