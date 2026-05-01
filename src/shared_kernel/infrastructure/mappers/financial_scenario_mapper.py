from src.core.infrastructure.mappers.base_mapper import BaseMapper
from src.core.infrastructure.mappers.mapper import AbstractMapper
from src.shared_kernel.domain.entities import FinancialScenario
from src.shared_kernel.infrastructure.models import FinancialScenarioModel


class FinancialScenarioMapper(
    AbstractMapper[FinancialScenario, FinancialScenarioModel]
):
    """
    Mapper class to convert between FinancialScenario entity and FinancialScenarioModel.
    """

    @staticmethod
    def to_model(entity: FinancialScenario) -> FinancialScenarioModel:
        """
        Converts a FinancialScenario entity to a FinancialScenarioModel instance.
        """

        model = FinancialScenarioModel(
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
    def to_entity(model: FinancialScenarioModel) -> FinancialScenario:
        """
        Converts a FinancialScenarioModel instance to a FinancialScenario entity.
        """

        entity = FinancialScenario(
            id=model.id,  # type: ignore
            tenant_id=model.tenant_id,  # type: ignore
            description=model.description,  # type: ignore
            scenario_type=model.scenario_type,  # type: ignore
            is_locked=model.is_locked,  # type: ignore
            assumptions=model.assumptions,  # type: ignore
        )

        BaseMapper.map_auditing_fields_to_entity(model, entity)
        return entity
