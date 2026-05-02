from datetime import datetime
from uuid import uuid4

from src.shared_kernel.domain.entities import FinancialScenario, ScenarioType
from src.shared_kernel.infrastructure.mappers import FinancialScenarioMapper
from src.shared_kernel.infrastructure.models import FinancialScenarioModel


def test_to_model():
    tenant_id = uuid4()
    entity_id = uuid4()
    entity = FinancialScenario(
        id=entity_id,
        tenant_id=tenant_id,
        description="Test Scenario",
        scenario_type=ScenarioType.ACTUAL,
        is_locked=True,
        assumptions="Some assumptions",
    )
    # Add auditing fields
    entity.created_at = datetime.now()
    entity.created_by = uuid4()

    model = FinancialScenarioMapper.to_model(entity)

    assert model.id == entity_id
    assert model.tenant_id == tenant_id
    assert model.description == "Test Scenario"
    assert model.scenario_type == ScenarioType.ACTUAL
    assert model.is_locked is True
    assert model.assumptions == "Some assumptions"
    assert model.created_at == entity.created_at
    assert model.created_by == entity.created_by


def test_to_entity():
    tenant_id = uuid4()
    model_id = uuid4()
    created_by = uuid4()
    created_at = datetime.now()
    model = FinancialScenarioModel(
        id=model_id,
        tenant_id=tenant_id,
        description="Test Scenario Model",
        scenario_type=ScenarioType.FORECAST,
        is_locked=False,
        assumptions="Model assumptions",
        created_by=created_by,
        created_at=created_at,
    )

    entity = FinancialScenarioMapper.to_entity(model)

    assert entity.id == model_id
    assert entity.tenant_id == tenant_id
    assert entity.description == "Test Scenario Model"
    assert entity.scenario_type == ScenarioType.FORECAST
    assert entity.is_locked is False
    assert entity.assumptions == "Model assumptions"
    assert entity.created_by == created_by
    assert entity.created_at == created_at
