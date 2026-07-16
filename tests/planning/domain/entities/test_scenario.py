from uuid import uuid4

import pytest

from src.core.domain import EntityValidationError
from src.planning.domain.entities import Scenario, ScenarioType


class TestScenarioEntity:
    """
    Test suite for the Scenario entity.
    """

    def test_scenario_creation(self):
        """
        Test that Scenario initializes correctly with valid data.
        """
        tenant_id = uuid4()
        scenario = Scenario(
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

    def test_scenario_lock_unlock(self):
        """
        Test the lock and unlock methods of Scenario.
        """
        scenario = Scenario(
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

    def test_scenario_validation_empty_description(self):
        """
        Test that creating a Scenario with an
        empty description raises an EntityValidationError.
        """
        with pytest.raises(EntityValidationError) as excinfo:
            scenario = Scenario(
                id=uuid4(),
                tenant_id=uuid4(),
                description="",
                scenario_type=ScenarioType.BUDGET,
                assumptions=None,
            )
            scenario.validate()
        assert "Description must be a non-empty string." in str(excinfo.value)

    def test_scenario_validation_long_description(self):
        """
        Test that creating a Scenario with a
        too-long description raises an EntityValidationError.
        """
        with pytest.raises(EntityValidationError) as excinfo:
            scenario = Scenario(
                id=uuid4(),
                tenant_id=uuid4(),
                description="a" * 101,
                scenario_type=ScenarioType.BUDGET,
                assumptions=None,
            )
            scenario.validate()
        assert "Description must be at most 100 characters long." in str(excinfo.value)

    def test_scenario_update_description(self):
        """
        Test that update_description correctly updates the description.
        """
        scenario = Scenario(
            id=uuid4(),
            tenant_id=uuid4(),
            description="Initial Description",
            scenario_type=ScenarioType.BUDGET,
            assumptions=None,
        )

        scenario.update_description("New Description")
        assert scenario.description == "New Description"

    def test_scenario_update_description_invalid(self):
        """
        Test that update_description raises EntityValidationError when provided with invalid data.
        """
        scenario = Scenario(
            id=uuid4(),
            tenant_id=uuid4(),
            description="Initial Description",
            scenario_type=ScenarioType.BUDGET,
            assumptions=None,
        )

        with pytest.raises(EntityValidationError):
            scenario.update_description("")
