from src.core.infrastructure.mappers.base_mapper import BaseMapper
from src.core.infrastructure.mappers.mapper import AbstractMapper
from src.planning.domain.entities import Scenario
from src.planning.infrastructure.models import ScenarioModel


class ScenarioMapper(AbstractMapper[Scenario, ScenarioModel]):
    """
    Mapper class to convert between Scenario entity and ScenarioModel.
    """

    @staticmethod
    def to_model(entity: Scenario) -> ScenarioModel:
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

        BaseMapper.map_auditing_fields_to_model(entity, model)
        return model

    @staticmethod
    def to_entity(model: ScenarioModel) -> Scenario:
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

        BaseMapper.map_auditing_fields_to_entity(model, entity)
        return entity
