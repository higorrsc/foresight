from datetime import datetime
from uuid import uuid4

from src.planning.domain.entities import Scenario, ScenarioType
from src.planning.infrastructure.mappers import ScenarioMapper
from src.planning.infrastructure.models import ScenarioModel


class TestScenarioMapper:
    """
    Test suite for the ScenarioMapper.
    """

    def test_to_model(self):
        """
        Test mapping of a Scenario entity to a ScenarioModel.
        """
        tenant_id = uuid4()
        entity_id = uuid4()
        entity = Scenario(
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

        model = ScenarioMapper.to_model(entity)

        assert model.id == entity_id
        assert model.tenant_id == tenant_id
        assert model.description == "Test Scenario"
        assert model.scenario_type == ScenarioType.ACTUAL
        assert model.is_locked is True
        assert model.assumptions == "Some assumptions"
        assert model.created_at == entity.created_at
        assert model.created_by == entity.created_by

    def test_to_entity(self):
        """
        Test mapping of a ScenarioModel to a Scenario entity.
        """
        tenant_id = uuid4()
        model_id = uuid4()
        created_by = uuid4()
        created_at = datetime.now()
        model = ScenarioModel(
            id=model_id,
            tenant_id=tenant_id,
            description="Test Scenario Model",
            scenario_type=ScenarioType.FORECAST,
            is_locked=False,
            assumptions="Model assumptions",
            created_by=created_by,
            created_at=created_at,
        )

        entity = ScenarioMapper.to_entity(model)

        assert entity.id == model_id
        assert entity.tenant_id == tenant_id
        assert entity.description == "Test Scenario Model"
        assert entity.scenario_type == ScenarioType.FORECAST
        assert entity.is_locked is False
        assert entity.assumptions == "Model assumptions"
        assert entity.created_by == created_by
        assert entity.created_at == created_at
