from fastapi import status
from httpx import AsyncClient


class TestPlanRouter:
    """
    Test suite for the PlanRouter.
    """

    async def test_create_plan_as_admin(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """Admin (Super Admin permissions) should be able to create plans."""

        response = await client.post(
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

    async def test_guest_cannot_create_plan(
        self,
        client: AsyncClient,
        guest_token: str,
    ):
        """Guest user should not be able to create plans."""

        response = await client.post(
            "/plans/",
            json={
                "name": "Hacker Plan",
                "price": 0,
            },
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_list_plans_authenticated(
        self,
        client: AsyncClient,
        guest_token: str,
    ):
        """Any authenticated user (even guest) should be able to list plans."""

        # First create a plan as admin to ensure list is not empty
        # (Or rely on seeding if you seeded a plan)

        # Legacy route
        response_legacy = await client.get(
            "/plans/",
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response_legacy.status_code == status.HTTP_200_OK

        data_legacy = response_legacy.json()
        assert "data" in data_legacy
        assert "meta" in data_legacy

        # V1 route
        response_v1 = await client.get(
            "/api/v1/plans/",
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response_v1.status_code == status.HTTP_200_OK

        data_v1 = response_v1.json()

        # Assert both return same data list
        assert data_legacy["data"] == data_v1["data"]

        plans_list = data_legacy["data"]
        assert isinstance(plans_list, list)
        assert any(p["name"] == "Standard" for p in plans_list)
