from uuid import uuid4

import pytest

from src.core.domain import EntityValidationError
from src.shared_kernel.domain.entities import FinancialScenario, ScenarioType


def test_financial_scenario_creation():
    tenant_id = uuid4()
    scenario = FinancialScenario(
        id=uuid4(),
        tenant_id=tenant_id,
        description="Budget 2024",
        scenario_type=ScenarioType.BUDGET,
        assumptions="Based on 5% growth",
    )

    assert scenario.description == "Budget 2024"
    assert scenario.scenario_type == ScenarioType.BUDGET
    assert scenario.assumptions == "Based on 5% growth"
    assert scenario.is_locked is False
    assert scenario.tenant_id == tenant_id


def test_financial_scenario_lock_unlock():
    scenario = FinancialScenario(
        id=uuid4(),
        tenant_id=uuid4(),
        description="Budget 2024",
        scenario_type=ScenarioType.BUDGET,
        assumptions=None,
    )

    scenario.lock()
    assert scenario.is_locked is True

    scenario.unlock()
    assert scenario.is_locked is False


def test_financial_scenario_validation_empty_description():
    with pytest.raises(EntityValidationError) as excinfo:
        scenario = FinancialScenario(
            id=uuid4(),
            tenant_id=uuid4(),
            description="",
            scenario_type=ScenarioType.BUDGET,
            assumptions=None,
        )
        scenario.validate()
    assert "Description must be a non-empty string." in str(excinfo.value)


def test_financial_scenario_validation_long_description():
    with pytest.raises(EntityValidationError) as excinfo:
        scenario = FinancialScenario(
            id=uuid4(),
            tenant_id=uuid4(),
            description="a" * 101,
            scenario_type=ScenarioType.BUDGET,
            assumptions=None,
        )
        scenario.validate()
    assert "Description must be at most 100 characters long." in str(excinfo.value)


def test_financial_scenario_update_description():
    scenario = FinancialScenario(
        id=uuid4(),
        tenant_id=uuid4(),
        description="Initial Description",
        scenario_type=ScenarioType.BUDGET,
        assumptions=None,
    )

    scenario.update_description("New Description")
    assert scenario.description == "New Description"


def test_financial_scenario_update_description_invalid():
    scenario = FinancialScenario(
        id=uuid4(),
        tenant_id=uuid4(),
        description="Initial Description",
        scenario_type=ScenarioType.BUDGET,
        assumptions=None,
    )

    with pytest.raises(EntityValidationError):
        scenario.update_description("")
