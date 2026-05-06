from src.core.infrastructure.mappers.base_mapper import BaseMapper
from src.core.infrastructure.mappers.mapper import AbstractMapper
from src.planning.domain.entities import Scenario
from src.planning.infrastructure.models import ScenarioModel

from .exchange_rate_mapper import ExchangeRateMapper


class ScenarioMapper(AbstractMapper[Scenario, ScenarioModel]):
    """
    Mapper class to convert between Scenario entity and ScenarioModel.
    """

    def __init__(self) -> None:
        self._exchange_rate_mapper = ExchangeRateMapper()

    def to_model(self, entity: Scenario) -> ScenarioModel:
        """
        Converts a Scenario entity to a ScenarioModel instance.
        """

        model = ScenarioModel(
            id=entity.id,
            tenant_id=entity.tenant_id,
            description=entity.description,
            scenario_type=entity.scenario_type,
            is_locked=entity.is_locked,
            assumptions=entity.assumptions,
        )

        if entity.exchange_rates:
            model.exchange_rates = [
                self._exchange_rate_mapper.to_model(er) for er in entity.exchange_rates
            ]

        BaseMapper.map_auditing_fields_to_model(entity, model)
        return model

    def to_entity(self, model: ScenarioModel) -> Scenario:
        """
        Converts a ScenarioModel instance to a Scenario entity.
        """

        entity = Scenario(
            id=model.id,  # type: ignore
            tenant_id=model.tenant_id,  # type: ignore
            description=model.description,  # type: ignore
            scenario_type=model.scenario_type,  # type: ignore
            is_locked=model.is_locked,  # type: ignore
            assumptions=model.assumptions,  # type: ignore
        )

        if model.exchange_rates:
            entity.exchange_rates = [
                self._exchange_rate_mapper.to_entity(er_model)
                for er_model in model.exchange_rates
            ]

        BaseMapper.map_auditing_fields_to_entity(model, entity)
        return entity
