from fastapi import status
from httpx import AsyncClient

from src.tenant_management.infrastructure.models import TenantModel


class TestTenantRouter:
    """
    Test suite for the TenantRouter.
    """

    async def test_signup_public(self, client: AsyncClient):
        """Public signup should work without token."""
        signup_data = {
            "tenant_name": "New Startup",
            "username": "startup_admin",
            "password": "secure_password",
            "email": "admin@startup.com",
        }
        response = await client.post("/tenants/signup", json=signup_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert "tenant_id" in response.json()

    async def test_list_tenants_as_admin(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """Super Admin should be able to list all tenants."""
        # First create a tenant as admin to ensure list is not empty
        # (Or rely on seeding if you seeded a tenant)

        response = await client.get(
            "/tenants/",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert "data" in data
        assert "meta" in data

        tenants_list = data["data"]
        assert isinstance(tenants_list, list)
        assert any(t["name"] == "System Tenant" for t in tenants_list)

    async def test_guest_cannot_list_tenants(
        self,
        client: AsyncClient,
        guest_token: str,
    ):
        """Regular users cannot list other tenants."""
        response = await client.get(
            "/tenants/",
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_update_tenant_status_as_admin(
        self,
        client: AsyncClient,
        admin_token: str,
        default_tenant: TenantModel,
    ):
        """Admin can suspend a tenant."""
        response = await client.patch(
            f"/tenants/{default_tenant.id}/status",
            json={"status": "suspended"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
