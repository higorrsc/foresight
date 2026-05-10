from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4

from src.finance.domain.value_objects import CurrencyCode
from src.planning.domain.entities import ExchangeRate, Scenario, ScenarioType
from src.planning.infrastructure.mappers import ScenarioMapper
from src.planning.infrastructure.models import ExchangeRateModel, ScenarioModel


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

        mapper = ScenarioMapper()
        model = mapper.to_model(entity)

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

        mapper = ScenarioMapper()
        entity = mapper.to_entity(model)

        assert entity.id == model_id
        assert entity.tenant_id == tenant_id
        assert entity.description == "Test Scenario Model"
        assert entity.scenario_type == ScenarioType.FORECAST
        assert entity.is_locked is False
        assert entity.assumptions == "Model assumptions"
        assert entity.created_by == created_by
        assert entity.created_at == created_at

    def test_to_model_with_exchange_rates(self):
        """
        Test mapping of a Scenario entity with exchange rates to a ScenarioModel.
        """
        entity_id = uuid4()
        entity = Scenario(
            id=entity_id,
            tenant_id=uuid4(),
            description="Test Scenario",
            scenario_type=ScenarioType.ACTUAL,
            assumptions=None,
        )
        rate = ExchangeRate(
            scenario_id=entity_id,
            from_currency=CurrencyCode(value="USD"),
            to_currency=CurrencyCode(value="BRL"),
            rate=Decimal("5.0"),
            effective_date=date.today(),
        )
        entity.exchange_rates = [rate]

        mapper = ScenarioMapper()
        model = mapper.to_model(entity)

        assert len(model.exchange_rates) == 1
        assert model.exchange_rates[0].from_currency == "USD"
        assert model.exchange_rates[0].rate == Decimal("5.0")
        assert model.exchange_rates[0].scenario_id == entity_id

    def test_to_entity_with_exchange_rates(self):
        """
        Test mapping of a ScenarioModel with exchange rates to a Scenario entity.
        """
        model_id = uuid4()
        model = ScenarioModel(
            id=model_id,
            tenant_id=uuid4(),
            description="Test Scenario Model",
            scenario_type=ScenarioType.BUDGET,
            is_locked=False,
            assumptions=None,
        )
        rate_model = ExchangeRateModel(
            id=uuid4(),
            scenario_id=model_id,
            from_currency="EUR",
            to_currency="USD",
            rate=Decimal("1.1"),
        )
        model.exchange_rates = [rate_model]

        mapper = ScenarioMapper()
        entity = mapper.to_entity(model)

        assert entity.exchange_rates is not None
        assert len(entity.exchange_rates) == 1
        assert str(entity.exchange_rates[0].from_currency) == "EUR"
        assert entity.exchange_rates[0].rate == Decimal("1.1")
        assert entity.exchange_rates[0].scenario_id == model_id
