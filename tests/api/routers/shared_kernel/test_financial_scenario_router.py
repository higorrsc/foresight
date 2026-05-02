from typing import Any

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.shared_kernel.domain.entities import ScenarioType
from src.shared_kernel.infrastructure.models import FinancialScenarioModel


def test_create_financial_scenario_api(
    client: TestClient,
    admin_token: str,
):
    response = client.post(
        "/financial-scenarios/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "description": "API Scenario",
            "scenario_type": "ACTUAL",
            "is_locked": False,
            "assumptions": "API assumptions",
        },
    )

    assert response.status_code == 201
    assert "id" in response.json()


def test_list_financial_scenarios_api(
    client: TestClient,
    admin_token: str,
    db_session_for_test: Session,
    default_tenant: Any,
    admin_actor: Any,
):
    # Seed a scenario directly in DB
    scenario = FinancialScenarioModel(
        description="List Scenario",
        scenario_type=ScenarioType.ACTUAL,
        tenant_id=default_tenant.id,
        created_by=admin_actor.id,
        updated_by=admin_actor.id,
    )
    db_session_for_test.add(scenario)
    db_session_for_test.commit()

    response = client.get(
        "/financial-scenarios/", headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    res_json = response.json()
    assert "data" in res_json
    assert "meta" in res_json
    assert res_json["meta"]["total_items"] >= 1
    assert any(item["description"] == "List Scenario" for item in res_json["data"])


def test_get_financial_scenario_by_id_api(
    client: TestClient,
    admin_token: str,
    db_session_for_test: Session,
    default_tenant: Any,
    admin_actor: Any,
):
    scenario = FinancialScenarioModel(
        description="Get Scenario",
        scenario_type=ScenarioType.ACTUAL,
        tenant_id=default_tenant.id,
        created_by=admin_actor.id,
        updated_by=admin_actor.id,
    )
    db_session_for_test.add(scenario)
    db_session_for_test.commit()

    response = client.get(
        f"/financial-scenarios/{scenario.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert response.json()["description"] == "Get Scenario"


def test_update_financial_scenario_api(
    client: TestClient,
    admin_token: str,
    db_session_for_test: Session,
    default_tenant: Any,
    admin_actor: Any,
):
    scenario = FinancialScenarioModel(
        description="Old API Scenario",
        scenario_type=ScenarioType.ACTUAL,
        tenant_id=default_tenant.id,
        created_by=admin_actor.id,
        updated_by=admin_actor.id,
    )
    db_session_for_test.add(scenario)
    db_session_for_test.commit()

    response = client.put(
        f"/financial-scenarios/{scenario.id}",
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


def test_delete_financial_scenario_api(
    client: TestClient,
    admin_token: str,
    db_session_for_test: Session,
    default_tenant: Any,
    admin_actor: Any,
):
    scenario = FinancialScenarioModel(
        description="Delete API Scenario",
        scenario_type=ScenarioType.ACTUAL,
        tenant_id=default_tenant.id,
        created_by=admin_actor.id,
        updated_by=admin_actor.id,
    )
    db_session_for_test.add(scenario)
    db_session_for_test.commit()

    response = client.delete(
        f"/financial-scenarios/{scenario.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 204

    # Verify it is soft deleted
    db_session_for_test.refresh(scenario)
    assert scenario.is_active is False


def test_lock_financial_scenario_api(
    client: TestClient,
    admin_token: str,
    db_session_for_test: Session,
    default_tenant: Any,
    admin_actor: Any,
):
    scenario = FinancialScenarioModel(
        description="Lock API Scenario",
        scenario_type=ScenarioType.ACTUAL,
        tenant_id=default_tenant.id,
        created_by=admin_actor.id,
        updated_by=admin_actor.id,
        is_locked=False,
    )
    db_session_for_test.add(scenario)
    db_session_for_test.commit()

    response = client.patch(
        f"/financial-scenarios/{scenario.id}/lock",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 204
    db_session_for_test.refresh(scenario)
    assert scenario.is_locked is True


def test_unlock_financial_scenario_api(
    client: TestClient,
    admin_token: str,
    db_session_for_test: Session,
    default_tenant: Any,
    admin_actor: Any,
):
    scenario = FinancialScenarioModel(
        description="Unlock API Scenario",
        scenario_type=ScenarioType.ACTUAL,
        tenant_id=default_tenant.id,
        created_by=admin_actor.id,
        updated_by=admin_actor.id,
        is_locked=True,
    )
    db_session_for_test.add(scenario)
    db_session_for_test.commit()

    response = client.patch(
        f"/financial-scenarios/{scenario.id}/unlock",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 204
    db_session_for_test.refresh(scenario)
    assert scenario.is_locked is False


def test_restore_financial_scenario_api(
    client: TestClient,
    admin_token: str,
    db_session_for_test: Session,
    default_tenant: Any,
    admin_actor: Any,
):
    scenario = FinancialScenarioModel(
        description="Restore API Scenario",
        scenario_type=ScenarioType.ACTUAL,
        tenant_id=default_tenant.id,
        created_by=admin_actor.id,
        updated_by=admin_actor.id,
        is_active=False,
    )
    db_session_for_test.add(scenario)
    db_session_for_test.commit()

    response = client.patch(
        f"/financial-scenarios/{scenario.id}/restore",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 204
    db_session_for_test.refresh(scenario)
    assert scenario.is_active is True
