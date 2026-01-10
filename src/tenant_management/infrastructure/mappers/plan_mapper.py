from decimal import Decimal

from src.core.infrastructure.mappers import BaseMapper
from src.tenant_management.domain.entities import Plan
from src.tenant_management.infrastructure.models import PlanModel


class PlanMapper:
    """
    Mapper class to convert between Plan entity and PlanModel.
    """

    @staticmethod
    def to_model(entity: Plan) -> PlanModel:
        """
        Converts a Plan entity to a PlanModel instance.
        """

        model = PlanModel(
            id=entity.id,
            name=entity.name,
            price=entity.price,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

        BaseMapper.map_auditing_fields_to_model(entity, model)
        return model

    @staticmethod
    def to_entity(model: PlanModel) -> Plan:
        """
        Converts a PlanModel instance to a Plan entity.
        """

        entity = Plan(
            id=model.id,  # type: ignore
            name=model.name,  # type: ignore
            price=Decimal(model.price),  # type: ignore
            created_at=model.created_at,  # type: ignore
            updated_at=model.updated_at,  # type: ignore
        )

        BaseMapper.map_auditing_fields_to_model(entity, model)
        return entity
