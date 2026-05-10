from typing import Any

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.planning.domain.entities import ScenarioType
from src.planning.infrastructure.models import ExchangeRateModel, ScenarioModel


class TestScenarioRouter:
    """
    Integration tests for the  Scenario Router.
    """

    async def test_create_scenario_api(
        self,
        client: AsyncClient,
        admin_token: str,
    ):
        """
        Test the creation of a financial scenario via API.
        """
        response = await client.post(
            "/scenarios/",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "description": "API Scenario",
                "scenario_type": "ACTUAL",
                "is_locked": False,
                "assumptions": "API assumptions",
            },
        )

        assert response.status_code == 201, response.json()
        assert "id" in response.json()

    async def test_list_scenarios_api(
        self,
        client: AsyncClient,
        admin_token: str,
        db_session_for_test: AsyncSession,
        default_tenant: Any,
        guest_actor: Any,
    ):
        """
        Test listing financial scenarios via API.
        """
        # Seed a scenario directly in DB
        scenario = ScenarioModel(
            description="List Scenario",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=default_tenant.id,
            created_by=guest_actor.id,
            updated_by=guest_actor.id,
        )
        db_session_for_test.add(scenario)
        await db_session_for_test.commit()

        response = await client.get(
            "/scenarios/",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200
        res_json = response.json()
        assert "data" in res_json
        assert "meta" in res_json
        assert res_json["meta"]["total_items"] >= 1
        assert any(item["description"] == "List Scenario" for item in res_json["data"])

    async def test_get_scenario_by_id_api(
        self,
        client: AsyncClient,
        admin_token: str,
        db_session_for_test: AsyncSession,
        default_tenant: Any,
        guest_actor: Any,
    ):
        """
        Test retrieving a financial scenario by its ID via API.
        """
        scenario = ScenarioModel(
            description="Get Scenario",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=default_tenant.id,
            created_by=guest_actor.id,
            updated_by=guest_actor.id,
        )
        db_session_for_test.add(scenario)
        await db_session_for_test.commit()

        response = await client.get(
            f"/scenarios/{scenario.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200
        assert response.json()["description"] == "Get Scenario"

    async def test_get_scenario_details_api(
        self,
        client: AsyncClient,
        admin_token: str,
        db_session_for_test: AsyncSession,
        default_tenant: Any,
        guest_actor: Any,
    ):
        """
        Test retrieving detailed financial scenario via API.
        """
        scenario = ScenarioModel(
            description="Detailed Scenario",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=default_tenant.id,
            created_by=guest_actor.id,
            updated_by=guest_actor.id,
        )
        db_session_for_test.add(scenario)
        await db_session_for_test.commit()

        response = await client.get(
            f"/scenarios/{scenario.id}/details",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200
        assert response.json()["description"] == "Detailed Scenario"
        assert "exchange_rates" in response.json()

    async def test_update_scenario_api(
        self,
        client: AsyncClient,
        admin_token: str,
        db_session_for_test: AsyncSession,
        default_tenant: Any,
        guest_actor: Any,
    ):
        """
        Test updating a financial scenario via API.
        """
        scenario = ScenarioModel(
            description="Old API Scenario",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=default_tenant.id,
            created_by=guest_actor.id,
            updated_by=guest_actor.id,
        )
        db_session_for_test.add(scenario)
        await db_session_for_test.commit()

        response = await client.put(
            f"/scenarios/{scenario.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "description": "New API Scenario",
                "scenario_type": "FORECAST",
                "is_locked": False,
                "assumptions": "New API assumptions",
            },
        )

        assert response.status_code == 200
        assert response.json()["description"] == "New API Scenario"

    async def test_delete_scenario_api(
        self,
        client: AsyncClient,
        admin_token: str,
        db_session_for_test: AsyncSession,
        default_tenant: Any,
        guest_actor: Any,
    ):
        """
        Test deleting (soft delete) a financial scenario via API.
        """
        scenario = ScenarioModel(
            description="Delete API Scenario",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=default_tenant.id,
            created_by=guest_actor.id,
            updated_by=guest_actor.id,
        )
        db_session_for_test.add(scenario)
        await db_session_for_test.commit()

        response = await client.delete(
            f"/scenarios/{scenario.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 204

        # Verify it is soft deleted
        await db_session_for_test.refresh(scenario)
        assert scenario.is_active is False

    async def test_lock_scenario_api(
        self,
        client: AsyncClient,
        admin_token: str,
        db_session_for_test: AsyncSession,
        default_tenant: Any,
        guest_actor: Any,
    ):
        """
        Test locking a financial scenario via API.
        """
        scenario = ScenarioModel(
            description="Lock API Scenario",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=default_tenant.id,
            created_by=guest_actor.id,
            updated_by=guest_actor.id,
            is_locked=False,
        )
        db_session_for_test.add(scenario)
        await db_session_for_test.commit()

        response = await client.patch(
            f"/scenarios/{scenario.id}/lock",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 204
        await db_session_for_test.refresh(scenario)
        assert scenario.is_locked is True

    async def test_unlock_scenario_api(
        self,
        client: AsyncClient,
        admin_token: str,
        db_session_for_test: AsyncSession,
        default_tenant: Any,
        guest_actor: Any,
    ):
        """
        Test unlocking a financial scenario via API.
        """
        scenario = ScenarioModel(
            description="Unlock API Scenario",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=default_tenant.id,
            created_by=guest_actor.id,
            updated_by=guest_actor.id,
            is_locked=True,
        )
        db_session_for_test.add(scenario)
        await db_session_for_test.commit()

        response = await client.patch(
            f"/scenarios/{scenario.id}/unlock",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 204
        await db_session_for_test.refresh(scenario)
        assert scenario.is_locked is False

    async def test_restore_scenario_api(
        self,
        client: AsyncClient,
        admin_token: str,
        db_session_for_test: AsyncSession,
        default_tenant: Any,
        guest_actor: Any,
    ):
        """
        Test restoring a financial scenario via API.
        """
        scenario = ScenarioModel(
            description="Restore API Scenario",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=default_tenant.id,
            created_by=guest_actor.id,
            updated_by=guest_actor.id,
            is_active=False,
        )
        db_session_for_test.add(scenario)
        await db_session_for_test.commit()

        response = await client.patch(
            f"/scenarios/{scenario.id}/restore",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 204
        await db_session_for_test.refresh(scenario)
        assert scenario.is_active is True

    async def test_add_exchange_rate_to_scenario_api(
        self,
        client: AsyncClient,
        admin_token: str,
        db_session_for_test: AsyncSession,
        default_tenant: Any,
        guest_actor: Any,
    ):
        """
        Test adding an exchange rate to a scenario via API.
        """
        scenario = ScenarioModel(
            description="Scenario for Rate",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=default_tenant.id,
            created_by=guest_actor.id,
            updated_by=guest_actor.id,
        )
        db_session_for_test.add(scenario)
        await db_session_for_test.commit()

        response = await client.post(
            f"/scenarios/{scenario.id}/exchange-rates",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "from_currency": "USD",
                "to_currency": "BRL",
                "rate": 5.25,
            },
        )

        assert response.status_code == 201
        assert "id" in response.json()

    async def test_update_exchange_rate_api(
        self,
        client: AsyncClient,
        admin_token: str,
        db_session_for_test: AsyncSession,
        default_tenant: Any,
        guest_actor: Any,
    ):
        """
        Test updating an exchange rate via API.
        """
        scenario = ScenarioModel(
            description="Scenario for Rate Update",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=default_tenant.id,
            created_by=guest_actor.id,
            updated_by=guest_actor.id,
        )
        db_session_for_test.add(scenario)
        await db_session_for_test.commit()

        rate = ExchangeRateModel(
            scenario_id=scenario.id,
            from_currency="USD",
            to_currency="BRL",
            rate=5.0,
        )
        db_session_for_test.add(rate)
        await db_session_for_test.commit()

        response = await client.put(
            f"/scenarios/exchange-rates/{rate.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "rate": 5.5,
            },
        )

        assert response.status_code == 200
        assert response.json()["message"] == "Exchange rate updated successfully"

    async def test_remove_exchange_rate_api(
        self,
        client: AsyncClient,
        admin_token: str,
        db_session_for_test: AsyncSession,
        default_tenant: Any,
        guest_actor: Any,
    ):
        """
        Test removing an exchange rate via API.
        """
        scenario = ScenarioModel(
            description="Scenario for Rate Removal",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=default_tenant.id,
            created_by=guest_actor.id,
            updated_by=guest_actor.id,
        )
        db_session_for_test.add(scenario)
        await db_session_for_test.commit()

        rate = ExchangeRateModel(
            scenario_id=scenario.id,
            from_currency="USD",
            to_currency="BRL",
            rate=5.0,
        )
        db_session_for_test.add(rate)
        await db_session_for_test.commit()

        response = await client.delete(
            f"/scenarios/exchange-rates/{rate.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 204
